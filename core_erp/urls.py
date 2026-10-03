"""
URL configuration for core_erp project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core_erp.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Standard language switch view
    path('', dashboard, name='dashboard'),
    path('documents/', include('apps.documents.urls')),
    path('administration/', include('apps.administration.urls')),
    path('accounting/', include('apps.accounting.urls')),
    path('warehouse/', include('apps.warehouse.urls')),
    path('calendar/', include('apps.calendar_tasks.urls')),
    path('reminders/', include('apps.reminders.urls')),
    path('assistant/', include('apps.ai_assistant.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
