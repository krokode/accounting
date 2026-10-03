from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from apps.reminders.models import Notification
from apps.reminders.services.reminder_service import run_daily_reminders_check


def notification_list(request):
    notifications = Notification.objects.all().order_by('-created_at')
    context = {
        'notifications': notifications,
    }
    return render(request, 'reminders/notification_list.html', context)


@require_POST
def mark_all_read(request):
    Notification.objects.filter(is_read=False).update(is_read=True)
    messages.success(request, _("All notifications marked as read."))
    return redirect('reminders:notification_list')


@require_POST
def trigger_check(request):
    stats = run_daily_reminders_check()
    total_actions = sum(stats.values())
    if total_actions > 0:
        messages.warning(
            request,
            _(
                "Reminders check triggered! Generated %(total)s active alert(s) "
                "(Payables: %(payables)s, Receivables: %(receivables)s, "
                "Overdue: %(overdue)s, Contracts: %(contracts)s, Stock: %(stock)s)."
            ) % {
                'total': total_actions,
                'payables': stats['payables_reminders'],
                'receivables': stats['receivables_reminders'],
                'overdue': stats['overdue_alerts'],
                'contracts': stats['contract_reminders'],
                'stock': stats['stock_alerts'],
            }
        )
    else:
        messages.success(request, _("Reminders check complete. All payments, contracts, and inventory are in order!"))
    
    # Redirect to referer or dashboard
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
