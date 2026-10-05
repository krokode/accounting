from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounting.models import Invoice, InvoiceItem, PaymentRecord, Receipt
from apps.administration.models import Counterparty, Contract, CompanyProfile
from apps.calendar_tasks.models import CalendarTask
from apps.reminders.services.reminder_service import run_daily_reminders_check
from apps.warehouse.models import Product, Consignment, ConsignmentItem, StockMovement


class Command(BaseCommand):
    help = 'Seeds realistic enterprise demonstration records (invoices, contracts, warehouse items, calendar tasks).'

    def handle(self, *args, **options):
        self.stdout.write("Populating demo business data...")
        today = timezone.localdate()

        # 0. Ensure Company Profile is established
        CompanyProfile.get_solo()

        # 1. Counterparties
        apex, _ = Counterparty.objects.get_or_create(
            name="Apex Cloud Services GmbH",
            defaults={
                'counterparty_type': Counterparty.TypeChoices.VENDOR,
                'tax_id': 'DE318492019',
                'iban': 'DE89370400440532013000',
                'bank_name': 'Deutsche Bank AG',
                'email': 'invoicing@apex-cloud.de',
                'phone': '+49 30 554321',
                'address': 'Friedrichstrasse 120, 10117 Berlin, Germany',
                'default_payment_terms_days': 14
            }
        )

        nordic, _ = Counterparty.objects.get_or_create(
            name="Nordic Logix Freight AB",
            defaults={
                'counterparty_type': Counterparty.TypeChoices.CARRIER,
                'tax_id': 'SE556123456701',
                'iban': 'SE45500000000583920184',
                'bank_name': 'SEB Bank',
                'email': 'dispatch@nordiclogix.se',
                'phone': '+46 8 1234567',
                'address': 'Hamnvägen 14, 115 41 Stockholm, Sweden',
                'default_payment_terms_days': 30
            }
        )

        quantum, _ = Counterparty.objects.get_or_create(
            name="Quantum Systems International",
            defaults={
                'counterparty_type': Counterparty.TypeChoices.CUSTOMER,
                'tax_id': 'NL883920184B01',
                'iban': 'NL91ABNA0417164300',
                'bank_name': 'ABN AMRO',
                'email': 'finance@quantumsys.io',
                'phone': '+31 20 890123',
                'address': 'Keizersgracht 421, 1016 EK Amsterdam, Netherlands',
                'default_payment_terms_days': 30
            }
        )

        # 2. Contracts
        contract1, _ = Contract.objects.get_or_create(
            contract_number="CTR-APEX-2026",
            defaults={
                'title': "Enterprise Dedicated Cloud Infrastructure SLA",
                'counterparty': apex,
                'start_date': today - timedelta(days=320),
                'end_date': today + timedelta(days=45),
                'auto_renew': True,
                'renewal_notice_period_days': 30,
                'total_value': Decimal('29400.00'),
                'currency': 'EUR',
                'status': Contract.StatusChoices.ACTIVE,
                'key_terms_summary': "Dedicated rack servers with 99.99% uptime guarantee. Auto-renews unless terminated 30 days prior to expiry."
            }
        )

        # 3. Invoices
        # Upcoming Payable (Due in 3 days)
        inv_payable, _ = Invoice.objects.get_or_create(
            invoice_number="APEX-2026-881",
            defaults={
                'direction': Invoice.Direction.PAYABLE,
                'counterparty': apex,
                'issue_date': today - timedelta(days=11),
                'due_date': today + timedelta(days=3),
                'currency': 'EUR',
                'subtotal': Decimal('2041.67'),
                'tax_amount': Decimal('408.33'),
                'total_amount': Decimal('2450.00'),
                'payment_status': Invoice.PaymentStatus.UNPAID,
                'notes': "Monthly dedicated cloud hosting & bandwidth"
            }
        )
        if not inv_payable.items.exists():
            InvoiceItem.objects.create(
                invoice=inv_payable,
                description="Cluster Node Hosting & Backup Storage",
                quantity=Decimal('1.00'),
                unit_price=Decimal('2041.67'),
                line_total=Decimal('2041.67')
            )

        # Overdue Payable (Was due 4 days ago)
        inv_overdue, _ = Invoice.objects.get_or_create(
            invoice_number="LOGIX-7712",
            defaults={
                'direction': Invoice.Direction.PAYABLE,
                'counterparty': nordic,
                'issue_date': today - timedelta(days=34),
                'due_date': today - timedelta(days=4),
                'currency': 'EUR',
                'subtotal': Decimal('983.33'),
                'tax_amount': Decimal('196.67'),
                'total_amount': Decimal('1180.00'),
                'payment_status': Invoice.PaymentStatus.OVERDUE,
                'notes': "Pallet freight shipment from Hamburg depot"
            }
        )

        # Incoming Receivable (Expected from Quantum in 10 days)
        inv_receivable, _ = Invoice.objects.get_or_create(
            invoice_number="INV-QUANTUM-04",
            defaults={
                'direction': Invoice.Direction.RECEIVABLE,
                'counterparty': quantum,
                'issue_date': today - timedelta(days=5),
                'due_date': today + timedelta(days=10),
                'currency': 'EUR',
                'subtotal': Decimal('7083.33'),
                'tax_amount': Decimal('1416.67'),
                'total_amount': Decimal('8500.00'),
                'payment_status': Invoice.PaymentStatus.UNPAID,
                'notes': "Enterprise software integration milestone 2"
            }
        )

        # 4. Products & Inventory
        p1, _ = Product.objects.get_or_create(
            sku="SRV-2U-MOD",
            defaults={
                'name': "Server Rack Chassis 2U",
                'category': "Hardware",
                'unit_of_measure': 'pcs',
                'cost_price': Decimal('320.00'),
                'sale_price': Decimal('499.00'),
                'quantity_on_hand': Decimal('2.00'),
                'reorder_threshold': Decimal('5.00')  # Low stock!
            }
        )

        p2, _ = Product.objects.get_or_create(
            sku="NET-SW-24P",
            defaults={
                'name': "Managed Gigabit Switch 24-Port PoE+",
                'category': "Networking",
                'unit_of_measure': 'pcs',
                'cost_price': Decimal('210.00'),
                'sale_price': Decimal('349.00'),
                'quantity_on_hand': Decimal('14.00'),
                'reorder_threshold': Decimal('4.00')
            }
        )

        # Consignment
        consignment, _ = Consignment.objects.get_or_create(
            consignment_number="WAYBILL-ND-4919",
            defaults={
                'direction': Consignment.Direction.INWARD,
                'counterparty': nordic,
                'delivery_date': today + timedelta(days=2),
                'carrier': "Nordic Logix Cargo",
                'status': Consignment.Status.EXPECTED,
                'notes': "Incoming stock replenishment batch"
            }
        )
        if not consignment.items.exists():
            ConsignmentItem.objects.create(
                consignment=consignment,
                product=p1,
                quantity_expected=Decimal('10.00'),
                quantity_received=Decimal('0.00')
            )

        # 5. Calendar Tasks
        CalendarTask.objects.get_or_create(
            title=f"Pay Outgoing Bill #{inv_payable.invoice_number} to {apex.name}",
            defaults={
                'task_type': CalendarTask.TaskType.OUTGOING_PAYMENT_DUE,
                'due_date': inv_payable.due_date,
                'priority': CalendarTask.Priority.URGENT,
                'amount': inv_payable.total_amount,
                'linked_invoice': inv_payable,
                'status': CalendarTask.Status.PENDING,
                'is_automated': True
            }
        )

        CalendarTask.objects.get_or_create(
            title=f"OVERDUE: Pay Freight Bill #{inv_overdue.invoice_number} to {nordic.name}",
            defaults={
                'task_type': CalendarTask.TaskType.OUTGOING_PAYMENT_DUE,
                'due_date': inv_overdue.due_date,
                'priority': CalendarTask.Priority.URGENT,
                'amount': inv_overdue.total_amount,
                'linked_invoice': inv_overdue,
                'status': CalendarTask.Status.PENDING,
                'is_automated': True
            }
        )

        CalendarTask.objects.get_or_create(
            title=f"Expected Incoming Payment #{inv_receivable.invoice_number} from {quantum.name}",
            defaults={
                'task_type': CalendarTask.TaskType.INCOMING_PAYMENT_EXPECTED,
                'due_date': inv_receivable.due_date,
                'priority': CalendarTask.Priority.HIGH,
                'amount': inv_receivable.total_amount,
                'linked_invoice': inv_receivable,
                'status': CalendarTask.Status.PENDING,
                'is_automated': True
            }
        )

        CalendarTask.objects.get_or_create(
            title=f"Inspect Incoming Delivery #{consignment.consignment_number} at Dock",
            defaults={
                'task_type': CalendarTask.TaskType.CONSIGNMENT_DELIVERY,
                'due_date': consignment.delivery_date,
                'priority': CalendarTask.Priority.MEDIUM,
                'linked_consignment': consignment,
                'status': CalendarTask.Status.PENDING,
                'is_automated': True
            }
        )

        # 6. Run Reminders Check
        run_daily_reminders_check()

        self.stdout.write(self.style.SUCCESS("Demo data successfully created! Run the development server to explore."))
