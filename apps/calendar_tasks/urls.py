from django.urls import path
from apps.calendar_tasks import views

app_name = 'calendar_tasks'

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('api/events/', views.calendar_events_api, name='events_api'),
    path('tasks/<int:pk>/toggle/', views.task_toggle_status, name='task_toggle'),
    path('feed.ics', views.ical_feed, name='ical_feed'),
]
