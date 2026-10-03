from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.calendar_tasks.models import CalendarTask, CalendarFeedToken
from apps.calendar_tasks.services.ical_exporter import generate_ical_feed


def calendar_view(request):
    # Ensure a feed token exists
    feed_token, _ = CalendarFeedToken.objects.get_or_create(name="Company Calendar Sync")
    
    tasks = CalendarTask.objects.all().order_by('due_date')
    pending_tasks = tasks.filter(status=CalendarTask.Status.PENDING)
    
    # Absolute URL for ical subscription
    ical_url = request.build_absolute_uri(f"/calendar/feed.ics?token={feed_token.token}")

    context = {
        'tasks': tasks,
        'pending_tasks': pending_tasks,
        'feed_token': feed_token,
        'ical_url': ical_url,
    }
    return render(request, 'calendar_tasks/calendar.html', context)


def calendar_events_api(request):
    """Feeds events in JSON format to FullCalendar.js."""
    tasks = CalendarTask.objects.exclude(status=CalendarTask.Status.CANCELLED)
    
    event_list = []
    for t in tasks:
        colors = t.color_classes
        amt_str = f" (€{t.amount:,.2f})" if t.amount else ""
        
        # Determine click URL
        click_url = ""
        if t.linked_invoice:
            click_url = f"/accounting/invoices/{t.linked_invoice.pk}/"
        elif t.linked_document:
            click_url = f"/documents/{t.linked_document.pk}/"

        event_list.append({
            'id': t.id,
            'title': f"{t.display_title}{amt_str}",
            'start': str(t.due_date),
            'allDay': True,
            'backgroundColor': colors['bg'],
            'borderColor': colors['border'],
            'textColor': colors['text'],
            'url': click_url,
            'extendedProps': {
                'priority': t.get_priority_display(),
                'type': t.get_task_type_display(),
                'status': t.get_status_display(),
                'description': t.description,
            }
        })

    return JsonResponse(event_list, safe=False)


@require_POST
def task_toggle_status(request, pk):
    task = get_object_or_404(CalendarTask, pk=pk)
    if task.status == CalendarTask.Status.COMPLETED:
        task.status = CalendarTask.Status.PENDING
    else:
        task.status = CalendarTask.Status.COMPLETED
    task.save(update_fields=['status', 'updated_at'])
    return redirect('calendar_tasks:calendar_view')


def ical_feed(request):
    """
    Standard RFC 5545 iCalendar endpoint.
    Compatible with Google Calendar, Microsoft Outlook, Apple Calendar, Thunderbird.
    """
    token = request.GET.get('token')
    # Validate token if token exists in DB
    if token and not CalendarFeedToken.objects.filter(token=token, is_active=True).exists():
        return HttpResponse("Unauthorized: Invalid calendar token", status=401)

    ical_bytes = generate_ical_feed()
    response = HttpResponse(ical_bytes, content_type='text/calendar; charset=utf-8')
    response['Content-Disposition'] = 'inline; filename="company_tasks.ics"'
    return response
