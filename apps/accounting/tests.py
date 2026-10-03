from decimal import Decimal
from django.test import TestCase
from django.utils import timezone

from apps.accounting.models import Invoice, PaymentRecord
from apps.administration.models import Counterparty
from apps.calendar_tasks.models import CalendarTask


class AccountingWorkflowTestCase(TestCase):
    def setUp(self):
        self.vendor = Counterparty.objects.create(
            name="Alpha Supplier",
            counterparty_type=Counterparty.TypeChoices.VENDOR
        )
        self.invoice = Invoice.objects.create(
            direction=Invoice.Direction.PAYABLE,
            invoice_number="INV-ALPHA-101",
            counterparty=self.vendor,
            issue_date=timezone.localdate(),
            due_date=timezone.localdate() + timezone.timedelta(days=7),
            total_amount=Decimal('500.00'),
            payment_status=Invoice.PaymentStatus.UNPAID
        )
        self.task = CalendarTask.objects.create(
            title="Pay Invoice #INV-ALPHA-101",
            task_type=CalendarTask.TaskType.OUTGOING_PAYMENT_DUE,
            due_date=self.invoice.due_date,
            linked_invoice=self.invoice,
            status=CalendarTask.Status.PENDING
        )

    def test_partial_and_full_payment_workflow(self):
        # 1. Record partial payment of 200
        PaymentRecord.objects.create(
            invoice=self.invoice,
            amount=Decimal('200.00'),
            payment_method=PaymentRecord.Method.BANK_TRANSFER
        )
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.payment_status, Invoice.PaymentStatus.PARTIALLY_PAID)
        self.assertEqual(self.invoice.remaining_amount, Decimal('300.00'))

        # 2. Record full settlement via endpoint
        response = self.client.post(f"/accounting/invoices/{self.invoice.pk}/record-payment/", {
            'amount': '300.00',
            'payment_method': 'BANK_TRANSFER',
            'transaction_reference': 'TXN-SETTLE-001'
        })
        self.assertEqual(response.status_code, 302)

        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.payment_status, Invoice.PaymentStatus.PAID)
        self.assertEqual(self.invoice.remaining_amount, Decimal('0.00'))

        # Check linked task was automatically marked COMPLETED
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, CalendarTask.Status.COMPLETED)
