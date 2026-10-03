import hashlib
from django.db import models
from django.utils.translation import gettext_lazy as _


def document_upload_path(instance, filename):
    return f"documents/{filename}"


class Document(models.Model):
    class DocumentType(models.TextChoices):
        INVOICE_PAYABLE = 'INVOICE_PAYABLE', _('Vendor Invoice (Payable)')
        INVOICE_RECEIVABLE = 'INVOICE_RECEIVABLE', _('Customer Invoice (Receivable)')
        CONTRACT = 'CONTRACT', _('Contract / Agreement')
        CONSIGNMENT = 'CONSIGNMENT', _('Consignment / Delivery Note')
        RECEIPT = 'RECEIPT', _('Receipt / Expense Voucher')
        UNKNOWN = 'UNKNOWN', _('General / Unclassified')

    class Status(models.TextChoices):
        UPLOADED = 'UPLOADED', _('Uploaded')
        PROCESSING = 'PROCESSING', _('Processing with AI')
        READY_FOR_REVIEW = 'READY_FOR_REVIEW', _('Ready for Review')
        CONFIRMED = 'CONFIRMED', _('Confirmed & Synced')
        FAILED = 'FAILED', _('Processing Failed')

    file = models.FileField(upload_to='documents/%Y/%m/')
    original_filename = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=64, blank=True, db_index=True)
    file_size = models.BigIntegerField(default=0)
    mime_type = models.CharField(max_length=128, default='application/pdf')
    document_type = models.CharField(
        max_length=32,
        choices=DocumentType.choices,
        default=DocumentType.UNKNOWN
    )
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.UPLOADED
    )
    raw_ai_response = models.JSONField(default=dict, blank=True)
    verified_data = models.JSONField(default=dict, blank=True)
    extraction_error = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.original_filename} ({self.get_document_type_display()}) - {self.get_status_display()}"

    def compute_hash(self):
        if not self.file:
            return ""
        hasher = hashlib.sha256()
        for chunk in self.file.chunks():
            hasher.update(chunk)
        return hasher.hexdigest()

    def save(self, *args, **kwargs):
        if not self.file_hash and self.file:
            try:
                self.file_hash = self.compute_hash()
                self.file_size = self.file.size
            except Exception:
                pass
        super().save(*args, **kwargs)


class DocumentPage(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='pages')
    page_number = models.PositiveIntegerField(default=1)
    page_image = models.ImageField(upload_to='documents/pages/%Y/%m/', null=True, blank=True)
    extracted_text = models.TextField(blank=True)

    class Meta:
        ordering = ['document', 'page_number']
        unique_together = ('document', 'page_number')

    def __str__(self):
        return f"{self.document.original_filename} - Page {self.page_number}"
