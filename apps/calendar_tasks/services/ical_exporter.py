from datetime import datetime, time, timedelta
from icalendar import Calendar, Event, Alarm
from django.utils import timezone
from apps.calendar_tasks.models import CalendarTask


def generate_ical_feed(tasks_queryset=None) -> bytes:
    """
    Exports calendar tasks to standard RFC 5545 iCalendar (.ics) format
    for direct sync with Google Calendar, Apple Calendar, and Microsoft Outlook.
    """
    if tasks_queryset is None:
        tasks_queryset = CalendarTask.objects.exclude(status=CalendarTask.Status.CANCELLED)

    cal = Calendar()
    cal.add('prodid', '-//Company Records & Accounting Agent//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'Company Financial & Operational Tasks')
    cal.add('x-wr-timezone', 'UTC')

    priority_map = {
        CalendarTask.Priority.URGENT: 1,
        CalendarTask.Priority.HIGH: 3,
        CalendarTask.Priority.MEDIUM: 5,
        CalendarTask.Priority.LOW: 9,
    }

    for task in tasks_queryset:
        event = Event()
        event.add('uid', f"task-{task.id}@company-accounting-erp")
        event.add('summary', task.title)

        desc_lines = []
        if task.description:
            desc_lines.append(task.description)
        if task.amount:
            desc_lines.append(f"Amount: {task.amount} {task.currency}")
        desc_lines.append(f"Type: {task.get_task_type_display()}")
        desc_lines.append(f"Status: {task.get_status_display()}")
        event.add('description', "\n".join(desc_lines))

        # Dates
        if task.due_time:
            dt_start = datetime.combine(task.due_date, task.due_time)
            dt_end = dt_start + timedelta(hours=1)
        else:
            dt_start = task.due_date
            dt_end = task.due_date + timedelta(days=1)

        event.add('dtstart', dt_start)
        event.add('dtend', dt_end)
        event.add('dtstamp', timezone.now())
        event.add('priority', priority_map.get(task.priority, 5))

        # Add Alarm / Reminder trigger (1 day before)
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('description', f"Reminder: {task.title}")
        alarm.add('trigger', timedelta(days=-1))
        event.add_component(alarm)

        cal.add_component(event)

    return cal.to_ical()
