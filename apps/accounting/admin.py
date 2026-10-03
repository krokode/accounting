from django.contrib import admin
from apps.accounting.models import Invoice, InvoiceItem, PaymentRecord, Receipt


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


class PaymentRecordInline(admin.TabularInline):
    model = PaymentRecord
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'direction', 'counterparty', 'due_date', 'total_amount', 'paid_amount', 'payment_status')
    list_filter = ('direction', 'payment_status', 'due_date', 'currency')
    search_fields = ('invoice_number', 'counterparty__name')
    inlines = [InvoiceItemInline, PaymentRecordInline]


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'counterparty', 'category', 'receipt_date', 'total_amount', 'currency')
    list_filter = ('category', 'receipt_date')
    search_fields = ('receipt_number', 'counterparty__name', 'notes')
