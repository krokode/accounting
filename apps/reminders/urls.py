from django.urls import path
from apps.reminders import views

app_name = 'reminders'

urlpatterns = [
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/mark-read/', views.mark_all_read, name='mark_all_read'),
    path('trigger-check/', views.trigger_check, name='trigger_check'),
]
