def unread_reminders_processor(request):
    try:
        from apps.reminders.models import Notification
        unread_notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:10]
        unread_count = Notification.objects.filter(is_read=False).count()
        return {
            'unread_notifications': unread_notifications,
            'unread_notifications_count': unread_count,
        }
    except Exception:
        return {
            'unread_notifications': [],
            'unread_notifications_count': 0,
        }
