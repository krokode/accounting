from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Invoice(models.Model):
    class Direction(models.TextChoices):
        PAYABLE = 'PAYABLE', _('Vendor Bill (Outgoing Payment)')
        RECEIVABLE = 'RECEIVABLE', _('Customer Invoice (Incoming Payment)')

    class PaymentStatus(models.TextChoices):
        UNPAID = 'UNPAID', _('Unpaid')
        PARTIALLY_PAID = 'PARTIALLY_PAID', _('Partially Paid')
        PAID = 'PAID', _('Paid')
        OVERDUE = 'OVERDUE', _('Overdue')
        DISPUTED = 'DISPUTED', _('Disputed')

    direction = models.CharField(
        max_length=16,
        choices=Direction.choices,
        default=Direction.PAYABLE
    )
    invoice_number = models.CharField(max_length=128, db_index=True)
    counterparty = models.ForeignKey(
        'administration.Counterparty',
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField(db_index=True)
    tax_point_date = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=8, default='EUR')
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    paid_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
        db_index=True
    )
    source_document = models.ForeignKey(
        'documents.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_invoices'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', '-created_at']

    def __str__(self):
        return f"{self.get_direction_display()} #{self.invoice_number} - {self.counterparty.name} ({self.total_amount} {self.currency})"

    @property
    def remaining_amount(self):
        return max(Decimal('0.00'), self.total_amount - self.paid_amount)

    @property
    def is_overdue(self):
        today = timezone.localdate()
        return self.payment_status not in (self.PaymentStatus.PAID, self.PaymentStatus.DISPUTED) and self.due_date < today

    def update_payment_status(self, save=True):
        today = timezone.localdate()
        if self.paid_amount >= self.total_amount and self.total_amount > 0:
            self.payment_status = self.PaymentStatus.PAID
        elif self.paid_amount > 0:
            self.payment_status = self.PaymentStatus.PARTIALLY_PAID
        elif self.due_date < today and self.payment_status != self.PaymentStatus.DISPUTED:
            self.payment_status = self.PaymentStatus.OVERDUE
        elif self.payment_status not in (self.PaymentStatus.DISPUTED,):
            self.payment_status = self.PaymentStatus.UNPAID
        if save:
            self.save(update_fields=['payment_status', 'paid_amount', 'updated_at'])


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    line_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        if not self.line_total:
            self.line_total = (self.quantity * self.unit_price).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} ({self.quantity} @ {self.unit_price})"


class PaymentRecord(models.Model):
    class Method(models.TextChoices):
        BANK_TRANSFER = 'BANK_TRANSFER', _('Bank Transfer / Wire')
        CREDIT_CARD = 'CREDIT_CARD', _('Credit / Debit Card')
        CASH = 'CASH', _('Cash')
        DIRECT_DEBIT = 'DIRECT_DEBIT', _('Direct Debit')
        OTHER = 'OTHER', _('Other')

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_method = models.CharField(max_length=24, choices=Method.choices, default=Method.BANK_TRANSFER)
    transaction_reference = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Recalculate invoice total paid
        total_paid = sum(p.amount for p in self.invoice.payments.all())
        self.invoice.paid_amount = total_paid
        self.invoice.update_payment_status()

    def __str__(self):
        return f"Payment of {self.amount} for #{self.invoice.invoice_number} on {self.payment_date}"


class Receipt(models.Model):
    receipt_number = models.CharField(max_length=128, blank=True)
    counterparty = models.ForeignKey(
        'administration.Counterparty',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='receipts'
    )
    receipt_date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=100, default='Office Supplies', help_text="e.g. Travel, Utilities, Meals")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=8, default='EUR')
    source_document = models.ForeignKey(
        'documents.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_receipts'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-receipt_date', '-created_at']

    def __str__(self):
        vendor_name = self.counterparty.name if self.counterparty else "General Receipt"
        return f"{vendor_name} ({self.total_amount} {self.currency}) on {self.receipt_date}"
