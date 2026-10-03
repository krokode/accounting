from django.urls import path
from apps.ai_assistant import views

app_name = 'ai_assistant'

urlpatterns = [
    path('chat-api/', views.chat_api, name='chat_api'),
    path('settings/', views.ai_settings_view, name='settings'),
    path('settings/test/', views.test_connection_api, name='test_connection'),
]
