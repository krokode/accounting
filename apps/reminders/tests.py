from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone

from apps.accounting.models import Invoice
from apps.administration.models import Counterparty
from apps.reminders.models import Notification
from apps.reminders.services.reminder_service import run_daily_reminders_check


class RemindersServiceTestCase(TestCase):
    def setUp(self):
        self.today = timezone.localdate()
        self.vendor = Counterparty.objects.create(name="Energy Corp")

        # Invoice due in 3 days (triggers upcoming payment reminder)
        self.upcoming_inv = Invoice.objects.create(
            direction=Invoice.Direction.PAYABLE,
            invoice_number="INV-ENERGY-01",
            counterparty=self.vendor,
            issue_date=self.today - timedelta(days=10),
            due_date=self.today + timedelta(days=3),
            total_amount=Decimal('420.00'),
            payment_status=Invoice.PaymentStatus.UNPAID
        )

        # Invoice past due by 5 days (triggers overdue critical alert)
        self.overdue_inv = Invoice.objects.create(
            direction=Invoice.Direction.PAYABLE,
            invoice_number="INV-ENERGY-OVERDUE",
            counterparty=self.vendor,
            issue_date=self.today - timedelta(days=30),
            due_date=self.today - timedelta(days=5),
            total_amount=Decimal('890.00'),
            payment_status=Invoice.PaymentStatus.UNPAID
        )

    def test_daily_reminders_creates_notifications(self):
        stats = run_daily_reminders_check()

        self.assertEqual(stats['payables_reminders'], 1)
        self.assertEqual(stats['overdue_alerts'], 1)

        # Verify notifications in database
        upcoming_notif = Notification.objects.filter(
            related_invoice=self.upcoming_inv,
            category=Notification.Category.PAYMENT_DUE
        ).first()
        self.assertIsNotNone(upcoming_notif)
        self.assertIn("INV-ENERGY-01", upcoming_notif.title)

        overdue_notif = Notification.objects.filter(
            related_invoice=self.overdue_inv,
            category=Notification.Category.PAYMENT_OVERDUE
        ).first()
        self.assertIsNotNone(overdue_notif)
        self.assertEqual(overdue_notif.level, Notification.Level.CRITICAL)

        # Verify overdue invoice status transitioned
        self.overdue_inv.refresh_from_db()
        self.assertEqual(self.overdue_inv.payment_status, Invoice.PaymentStatus.OVERDUE)

    def test_trigger_check_multilingual_success_message(self):
        Invoice.objects.all().delete()

        # Test Russian
        self.client.cookies.load({'django_language': 'ru'})
        response = self.client.post('/reminders/trigger-check/', follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertIn("Проверка напоминаний завершена", str(messages_list[0]))
        self.assertContains(response, "Проверка напоминаний завершена")

        # Test Spanish
        self.client.cookies.load({'django_language': 'es'})
        response = self.client.post('/reminders/trigger-check/', follow=True)
        messages_list = list(response.context['messages'])
        self.assertIn("¡Comprobación de recordatorios completa!", str(messages_list[0]))
        self.assertContains(response, "¡Comprobación de recordatorios completa!")

        # Test English
        self.client.cookies.load({'django_language': 'en'})
        response = self.client.post('/reminders/trigger-check/', follow=True)
        messages_list = list(response.context['messages'])
        self.assertIn("Reminders check complete", str(messages_list[0]))
        self.assertContains(response, "Reminders check complete")
