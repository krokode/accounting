from datetime import datetime
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from apps.administration.models import Counterparty, Contract
from apps.accounting.models import Invoice, InvoiceItem, Receipt
from apps.warehouse.models import Product, Consignment, ConsignmentItem
from apps.calendar_tasks.models import CalendarTask
from apps.reminders.models import Notification


def parse_date_str(date_str, fallback=None):
    if not date_str:
        return fallback or timezone.localdate()
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return fallback or timezone.localdate()


def parse_decimal(value, default=Decimal('0.00')):
    if value is None or value == '':
        return default
    try:
        return Decimal(str(value))
    except Exception:
        return default


@transaction.atomic
def sync_verified_document_to_ledgers(document, data: dict):
    """
    Takes confirmed structured extraction data and creates all corresponding records
    in Administration, Accounting, Warehouse, and Calendar/Tasks.
    """
    document.verified_data = data
    doc_type = data.get('document_type', document.document_type)
    document.document_type = doc_type

    # 1. Sync or Create Counterparty
    cp_info = data.get('counterparty', {})
    cp_name = cp_info.get('name') or "Unknown Counterparty"
    counterparty, _ = Counterparty.objects.get_or_create(
        name=cp_name,
        defaults={
            'counterparty_type': cp_info.get('type', Counterparty.TypeChoices.VENDOR),
            'tax_id': cp_info.get('tax_id', ''),
            'iban': cp_info.get('iban', ''),
            'bank_name': cp_info.get('bank_name', ''),
            'swift_bic': cp_info.get('swift_bic', ''),
            'email': cp_info.get('email', ''),
            'phone': cp_info.get('phone', ''),
            'address': cp_info.get('address', ''),
        }
    )

    dates = data.get('dates', {})
    financials = data.get('financials', {})
    currency = financials.get('currency', 'EUR')
    total_amount = parse_decimal(financials.get('total_amount', 0))
    subtotal = parse_decimal(financials.get('subtotal', 0))
    tax_amount = parse_decimal(financials.get('tax_amount', 0))
    line_items = data.get('line_items', [])

    linked_invoice = None
    linked_contract = None
    linked_consignment = None

    # 2. Sync by Document Type
    if doc_type in ['INVOICE_PAYABLE', 'INVOICE_RECEIVABLE']:
        direction = Invoice.Direction.PAYABLE if doc_type == 'INVOICE_PAYABLE' else Invoice.Direction.RECEIVABLE
        invoice_number = data.get('document_number') or f"INV-{timezone.now().strftime('%Y%m%d%H%M')}"
        issue_date = parse_date_str(dates.get('issue_date'))
        due_date = parse_date_str(dates.get('due_date'))

        linked_invoice = Invoice.objects.create(
            direction=direction,
            invoice_number=invoice_number,
            counterparty=counterparty,
            issue_date=issue_date,
            due_date=due_date,
            currency=currency,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
            source_document=document,
            notes=data.get('summary', '')
        )
        linked_invoice.update_payment_status(save=True)

        for item in line_items:
            qty = parse_decimal(item.get('quantity', 1))
            unit_price = parse_decimal(item.get('unit_price', 0))
            line_tot = parse_decimal(item.get('line_total', qty * unit_price))
            InvoiceItem.objects.create(
                invoice=linked_invoice,
                description=item.get('description', 'Service / Product'),
                quantity=qty,
                unit_price=unit_price,
                line_total=line_tot
            )

    elif doc_type == 'CONTRACT':
        contract_number = data.get('document_number') or f"CTR-{timezone.now().strftime('%Y%m%d')}"
        start_date = parse_date_str(dates.get('contract_start'), fallback=timezone.localdate())
        end_date = parse_date_str(dates.get('contract_end'), fallback=timezone.localdate() + timezone.timedelta(days=365))
        notice_days = int(dates.get('renewal_notice_days') or 30)

        linked_contract = Contract.objects.create(
            title=f"Agreement with {counterparty.name}",
            contract_number=contract_number,
            counterparty=counterparty,
            start_date=start_date,
            end_date=end_date,
            auto_renew=True,
            renewal_notice_period_days=notice_days,
            total_value=total_amount if total_amount > 0 else None,
            currency=currency,
            status=Contract.StatusChoices.ACTIVE,
            key_terms_summary=data.get('summary', ''),
            source_document=document
        )

    elif doc_type == 'CONSIGNMENT':
        waybill_number = data.get('document_number') or f"WAYBILL-{timezone.now().strftime('%Y%m%d%H%M')}"
        delivery_date = parse_date_str(dates.get('delivery_date'))

        linked_consignment = Consignment.objects.create(
            consignment_number=waybill_number,
            direction=Consignment.Direction.INWARD,
            counterparty=counterparty,
            delivery_date=delivery_date,
            carrier=cp_info.get('name', 'Carrier'),
            status=Consignment.Status.EXPECTED,
            source_document=document,
            notes=data.get('summary', '')
        )

        for item in line_items:
            sku = item.get('sku') or f"SKU-{timezone.now().strftime('%M%S%f')[:8]}"
            desc = item.get('description', 'Warehouse Goods')
            product, _ = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': desc,
                    'cost_price': parse_decimal(item.get('unit_price', 0)),
                }
            )
            qty = parse_decimal(item.get('quantity', 1))
            ConsignmentItem.objects.create(
                consignment=linked_consignment,
                product=product,
                quantity_expected=qty,
                quantity_received=0
            )

    elif doc_type == 'RECEIPT':
        category = (data.get('category') or data.get('receipt_category') or '').strip() or 'Office Supplies'
        receipt_num = data.get('document_number', '').strip() or f"RCP-{timezone.now().strftime('%Y%m%d%H%M')}"
        Receipt.objects.create(
            receipt_number=receipt_num,
            counterparty=counterparty,
            receipt_date=parse_date_str(dates.get('issue_date')),
            category=category,
            total_amount=total_amount,
            tax_amount=tax_amount,
            currency=currency,
            source_document=document,
            notes=data.get('summary', '')
        )

    # 3. Calendar & Task Generation
    calendar_actions = data.get('calendar_actions', [])
    for action in calendar_actions:
        act_date = parse_date_str(action.get('date'))
        act_type = action.get('action_type', CalendarTask.TaskType.ADMINISTRATIVE_TASK)
        priority = action.get('priority', CalendarTask.Priority.HIGH)
        act_amount = parse_decimal(action.get('amount'), default=total_amount)

        CalendarTask.objects.create(
            title=action.get('title', f"Action for {document.original_filename}"),
            description=action.get('description', ''),
            task_type=act_type,
            due_date=act_date,
            priority=priority,
            status=CalendarTask.Status.PENDING,
            amount=act_amount if act_amount > 0 else None,
            currency=currency,
            linked_invoice=linked_invoice,
            linked_contract=linked_contract,
            linked_consignment=linked_consignment,
            linked_document=document,
            is_automated=True
        )

    # 4. Create Notification
    Notification.objects.create(
        title=f"New {document.get_document_type_display()} Processed",
        message=f"{counterparty.name} - #{data.get('document_number', '')} confirmed and scheduled into calendar.",
        level=Notification.Level.SUCCESS,
        category=Notification.Category.DOCUMENT_PROCESSED,
        action_url=f"/documents/{document.pk}/",
        related_invoice=linked_invoice,
        related_contract=linked_contract
    )

    document.status = document.Status.CONFIRMED
    document.save(update_fields=['status', 'document_type', 'verified_data', 'updated_at'])
    return document
