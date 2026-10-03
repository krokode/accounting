from django.contrib import admin
from apps.warehouse.models import Product, Consignment, ConsignmentItem, StockMovement


class ConsignmentItemInline(admin.TabularInline):
    model = ConsignmentItem
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'unit_of_measure', 'cost_price', 'sale_price', 'quantity_on_hand', 'reorder_threshold')
    list_filter = ('category',)
    search_fields = ('sku', 'name')


@admin.register(Consignment)
class ConsignmentAdmin(admin.ModelAdmin):
    list_display = ('consignment_number', 'direction', 'counterparty', 'delivery_date', 'status', 'carrier')
    list_filter = ('direction', 'status', 'delivery_date')
    search_fields = ('consignment_number', 'counterparty__name')
    inlines = [ConsignmentItemInline]


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'balance_after', 'reference', 'timestamp')
    list_filter = ('movement_type', 'timestamp')
    search_fields = ('product__name', 'product__sku', 'reference')
