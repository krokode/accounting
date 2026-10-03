from django.contrib import admin
from apps.calendar_tasks.models import CalendarTask, CalendarFeedToken


@admin.register(CalendarTask)
class CalendarTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_type', 'due_date', 'priority', 'status', 'amount', 'is_automated')
    list_filter = ('task_type', 'priority', 'status', 'due_date', 'is_automated')
    search_fields = ('title', 'description')


@admin.register(CalendarFeedToken)
class CalendarFeedTokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'token', 'is_active', 'created_at')
