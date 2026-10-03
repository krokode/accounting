from django.core.management.base import BaseCommand
from apps.reminders.services.reminder_service import run_daily_reminders_check


class Command(BaseCommand):
    help = 'Evaluates upcoming obligations (payables, receivables, contracts, consignments) and generates proactive reminders.'

    def handle(self, *args, **options):
        self.stdout.write("Running proactive reminders check...")
        stats = run_daily_reminders_check()
        self.stdout.write(self.style.SUCCESS(
            f"Reminders check complete!\n"
            f"  - Outgoing Payables Reminders: {stats['payables_reminders']}\n"
            f"  - Incoming Receivables Reminders: {stats['receivables_reminders']}\n"
            f"  - Overdue Escalations: {stats['overdue_alerts']}\n"
            f"  - Contract Renewal Notices: {stats['contract_reminders']}\n"
            f"  - Consignment Delivery Alerts: {stats['consignment_reminders']}\n"
            f"  - Low Stock Alerts: {stats['stock_alerts']}"
        ))
