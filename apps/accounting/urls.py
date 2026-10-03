from django.urls import path
from apps.accounting import views

app_name = 'accounting'

urlpatterns = [
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<int:pk>/record-payment/', views.record_payment, name='record_payment'),
    path('receipts/', views.receipt_list, name='receipt_list'),
    path('receipts/create/', views.receipt_create, name='receipt_create'),
]
