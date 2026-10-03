from django.contrib import admin
from apps.reminders.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'category', 'is_read', 'created_at')
    list_filter = ('level', 'category', 'is_read', 'created_at')
    search_fields = ('title', 'message')
