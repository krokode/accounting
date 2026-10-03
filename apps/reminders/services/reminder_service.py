from datetime import timedelta
from django.utils import timezone
from apps.accounting.models import Invoice
from apps.administration.models import Contract
from apps.warehouse.models import Consignment, Product
from apps.reminders.models import Notification


def run_daily_reminders_check() -> dict:
    """
    Evaluates upcoming obligations across Accounting, Contracts, and Warehouse,
    generating proactive in-app notifications and escalating overdue items.
    """
    today = timezone.localdate()
    stats = {
        'payables_reminders': 0,
        'receivables_reminders': 0,
        'overdue_alerts': 0,
        'contract_reminders': 0,
        'consignment_reminders': 0,
        'stock_alerts': 0,
    }

    # 1. Check Unpaid Invoices (Payable & Receivable)
    unpaid_invoices = Invoice.objects.filter(
        payment_status__in=[Invoice.PaymentStatus.UNPAID, Invoice.PaymentStatus.PARTIALLY_PAID, Invoice.PaymentStatus.OVERDUE]
    )

    for invoice in unpaid_invoices:
        days_until_due = (invoice.due_date - today).days

        # Overdue check
        if days_until_due < 0:
            if invoice.payment_status != Invoice.PaymentStatus.OVERDUE:
                invoice.payment_status = Invoice.PaymentStatus.OVERDUE
                invoice.save(update_fields=['payment_status', 'updated_at'])

            # Avoid spamming duplicate overdue notification within the same 3 days
            already_notified = Notification.objects.filter(
                related_invoice=invoice,
                category=Notification.Category.PAYMENT_OVERDUE,
                created_at__date=today
            ).exists()

            if not already_notified:
                is_payable = invoice.direction == Invoice.Direction.PAYABLE
                title = f"OVERDUE: {'Outgoing Bill' if is_payable else 'Incoming Payment'} #{invoice.invoice_number}"
                msg = f"{'We owe' if is_payable else 'Expected from'} {invoice.counterparty.name} {invoice.remaining_amount} {invoice.currency}. Due date was {invoice.due_date} ({abs(days_until_due)} days ago)."
                Notification.objects.create(
                    title=title,
                    message=msg,
                    level=Notification.Level.CRITICAL,
                    category=Notification.Category.PAYMENT_OVERDUE,
                    action_url=f"/accounting/invoices/{invoice.pk}/",
                    related_invoice=invoice
                )
                stats['overdue_alerts'] += 1

        # Upcoming due checks: 7 days, 3 days, 1 day, or due today
        elif days_until_due in [7, 3, 1, 0]:
            already_notified = Notification.objects.filter(
                related_invoice=invoice,
                category=Notification.Category.PAYMENT_DUE,
                created_at__date=today
            ).exists()

            if not already_notified:
                is_payable = invoice.direction == Invoice.Direction.PAYABLE
                urgency = Notification.Level.WARNING if days_until_due <= 1 else Notification.Level.INFO
                due_label = "TODAY" if days_until_due == 0 else f"in {days_until_due} day(s)"
                action_text = "Scheduled payment to" if is_payable else "Expected incoming payment from"

                Notification.objects.create(
                    title=f"Payment Due {due_label}: #{invoice.invoice_number}",
                    message=f"{action_text} {invoice.counterparty.name} for {invoice.remaining_amount} {invoice.currency} on {invoice.due_date}.",
                    level=urgency,
                    category=Notification.Category.PAYMENT_DUE,
                    action_url=f"/accounting/invoices/{invoice.pk}/",
                    related_invoice=invoice
                )
                if is_payable:
                    stats['payables_reminders'] += 1
                else:
                    stats['receivables_reminders'] += 1

    # 2. Check Contract Renewals
    active_contracts = Contract.objects.filter(
        status__in=[Contract.StatusChoices.ACTIVE, Contract.StatusChoices.PENDING_RENEWAL],
        end_date__isnull=False
    )
    for contract in active_contracts:
        notice_days = contract.renewal_notice_period_days or 30
        notice_date = contract.end_date - timedelta(days=notice_days)
        days_until_notice = (notice_date - today).days

        if 0 <= days_until_notice <= 7:
            already_notified = Notification.objects.filter(
                related_contract=contract,
                category=Notification.Category.CONTRACT_RENEWAL,
                created_at__date=today
            ).exists()

            if not already_notified:
                contract.status = Contract.StatusChoices.PENDING_RENEWAL
                contract.save(update_fields=['status', 'updated_at'])

                Notification.objects.create(
                    title=f"Contract Renewal Decision: {contract.counterparty.name}",
                    message=f"Contract '{contract.title}' expires on {contract.end_date}. Notice deadline is {notice_date} ({days_until_notice} days left).",
                    level=Notification.Level.WARNING,
                    category=Notification.Category.CONTRACT_RENEWAL,
                    action_url=f"/administration/contracts/{contract.pk}/",
                    related_contract=contract
                )
                stats['contract_reminders'] += 1

    # 3. Check Consignment Deliveries
    pending_consignments = Consignment.objects.filter(
        status=Consignment.Status.EXPECTED,
        delivery_date__lte=today
    )
    for consignment in pending_consignments:
        already_notified = Notification.objects.filter(
            category=Notification.Category.CONSIGNMENT_DELIVERY,
            message__contains=consignment.consignment_number,
            created_at__date=today
        ).exists()

        if not already_notified:
            Notification.objects.create(
                title=f"Consignment Delivery Expected: #{consignment.consignment_number}",
                message=f"Expected delivery from {consignment.counterparty.name} scheduled for {consignment.delivery_date}.",
                level=Notification.Level.INFO,
                category=Notification.Category.CONSIGNMENT_DELIVERY,
                action_url=f"/warehouse/consignments/{consignment.pk}/"
            )
            stats['consignment_reminders'] += 1

    # 4. Check Warehouse Low Stock
    low_stock_products = Product.objects.filter(quantity_on_hand__lte=models_reorder())
    for product in low_stock_products:
        already_notified = Notification.objects.filter(
            category=Notification.Category.STOCK_ALERT,
            message__contains=product.sku,
            created_at__date=today
        ).exists()

        if not already_notified:
            Notification.objects.create(
                title=f"Low Stock Alert: {product.name}",
                message=f"Stock for '{product.name}' [{product.sku}] is down to {product.quantity_on_hand} {product.unit_of_measure} (Reorder threshold: {product.reorder_threshold}).",
                level=Notification.Level.WARNING,
                category=Notification.Category.STOCK_ALERT,
                action_url=f"/warehouse/products/"
            )
            stats['stock_alerts'] += 1

    return stats


def models_reorder():
    from django.db.models import F
    return F('reorder_threshold')
