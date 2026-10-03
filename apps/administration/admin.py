from django.contrib import admin
from apps.administration.models import Counterparty, Contract


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'counterparty_type', 'tax_id', 'iban', 'email', 'phone')
    list_filter = ('counterparty_type', 'created_at')
    search_fields = ('name', 'tax_id', 'iban', 'email')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('title', 'counterparty', 'start_date', 'end_date', 'auto_renew', 'status', 'total_value')
    list_filter = ('status', 'auto_renew', 'end_date')
    search_fields = ('title', 'contract_number', 'counterparty__name')
