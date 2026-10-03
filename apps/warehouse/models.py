from decimal import Decimal
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    category = models.CharField(max_length=100, blank=True)
    unit_of_measure = models.CharField(max_length=32, default='pcs')
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    quantity_on_hand = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    reorder_threshold = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('5.00'))
    location = models.CharField(max_length=128, blank=True, help_text="Warehouse shelf/bin location")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} [{self.sku}] ({self.quantity_on_hand} {self.unit_of_measure})"

    @property
    def is_low_stock(self):
        return self.quantity_on_hand <= self.reorder_threshold


class Consignment(models.Model):
    class Direction(models.TextChoices):
        INWARD = 'INWARD', _('Inward Receipt (Supplier Delivery)')
        OUTWARD = 'OUTWARD', _('Outward Dispatch (Customer Delivery)')

    class Status(models.TextChoices):
        EXPECTED = 'EXPECTED', _('Expected / In Transit')
        RECEIVED_CONFIRMED = 'RECEIVED_CONFIRMED', _('Received & Stocked')
        DISCREPANCY = 'DISCREPANCY', _('Discrepancy Noted')
        REJECTED = 'REJECTED', _('Rejected')

    consignment_number = models.CharField(max_length=128, db_index=True, help_text="Waybill or Consignment Note No.")
    direction = models.CharField(max_length=16, choices=Direction.choices, default=Direction.INWARD)
    counterparty = models.ForeignKey(
        'administration.Counterparty',
        on_delete=models.CASCADE,
        related_name='consignments'
    )
    delivery_date = models.DateField(default=timezone.now, db_index=True)
    carrier = models.CharField(max_length=128, blank=True)
    tracking_number = models.CharField(max_length=128, blank=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.EXPECTED)
    source_document = models.ForeignKey(
        'documents.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_consignments'
    )
    linked_invoice = models.ForeignKey(
        'accounting.Invoice',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consignments'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-delivery_date', '-created_at']

    def __str__(self):
        return f"{self.get_direction_display()} #{self.consignment_number} - {self.counterparty.name} ({self.get_status_display()})"

    def confirm_and_update_stock(self):
        """Processes stock movements for all items in the consignment."""
        with transaction.atomic():
            for item in self.items.all():
                qty = item.quantity_received if item.quantity_received > 0 else item.quantity_expected
                if self.direction == self.Direction.INWARD:
                    movement_type = StockMovement.MovementType.PURCHASE_RECEIPT
                    item.product.quantity_on_hand += qty
                else:
                    movement_type = StockMovement.MovementType.SALES_SHIPMENT
                    item.product.quantity_on_hand -= qty

                item.product.save(update_fields=['quantity_on_hand', 'updated_at'])

                StockMovement.objects.create(
                    product=item.product,
                    consignment=self,
                    movement_type=movement_type,
                    quantity=qty if self.direction == self.Direction.INWARD else -qty,
                    balance_after=item.product.quantity_on_hand,
                    reference=f"Consignment #{self.consignment_number}"
                )
            self.status = self.Status.RECEIVED_CONFIRMED
            self.save(update_fields=['status', 'updated_at'])


class ConsignmentItem(models.Model):
    consignment = models.ForeignKey(Consignment, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='consignment_items')
    quantity_expected = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.product.name}: Expected {self.quantity_expected}, Received {self.quantity_received}"


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        PURCHASE_RECEIPT = 'PURCHASE_RECEIPT', _('Purchase Receipt / Inward')
        SALES_SHIPMENT = 'SALES_SHIPMENT', _('Sales Shipment / Outward')
        INVENTORY_ADJUSTMENT = 'INVENTORY_ADJUSTMENT', _('Stock Count / Adjustment')
        RETURN = 'RETURN', _('Return to Supplier / Customer Return')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    consignment = models.ForeignKey(Consignment, on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_movements')
    movement_type = models.CharField(max_length=32, choices=MovementType.choices)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, help_text="Positive for additions, negative for reductions")
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=128, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.product.name} ({self.quantity:+}) on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
