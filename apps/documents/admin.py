from django.contrib import admin
from apps.documents.models import Document, DocumentPage


class DocumentPageInline(admin.TabularInline):
    model = DocumentPage
    extra = 0


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'document_type', 'status', 'file_size', 'created_at')
    list_filter = ('document_type', 'status', 'created_at')
    search_fields = ('original_filename', 'notes')
    inlines = [DocumentPageInline]
