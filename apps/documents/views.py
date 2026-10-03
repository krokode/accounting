import json
from decimal import Decimal
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from apps.documents.models import Document
from apps.documents.services.ai_extractor import extract_document_with_ai
from apps.documents.services.sync_service import sync_verified_document_to_ledgers


def document_list(request):
    doc_type = request.GET.get('type')
    status = request.GET.get('status')
    
    docs = Document.objects.all()
    if doc_type:
        docs = docs.filter(document_type=doc_type)
    if status:
        docs = docs.filter(status=status)
        
    context = {
        'documents': docs,
        'selected_type': doc_type,
        'selected_status': status,
        'total_count': Document.objects.count(),
        'pending_count': Document.objects.filter(status__in=[Document.Status.UPLOADED, Document.Status.READY_FOR_REVIEW]).count(),
        'receipts_count': Document.objects.filter(document_type=Document.DocumentType.RECEIPT).count(),
        'invoices_count': Document.objects.filter(document_type=Document.DocumentType.INVOICE_PAYABLE).count(),
        'contracts_count': Document.objects.filter(document_type=Document.DocumentType.CONTRACT).count(),
        'consignments_count': Document.objects.filter(document_type=Document.DocumentType.CONSIGNMENT).count(),
    }
    return render(request, 'documents/document_list.html', context)


def document_upload(request):
    initial_type = request.GET.get('type', '').strip()
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document_file')
        if not uploaded_file:
            messages.error(request, _("Please select a scanned PDF or image document."))
            return redirect('documents:upload')

        mime = uploaded_file.content_type or 'application/pdf'
        doc = Document(
            file=uploaded_file,
            original_filename=uploaded_file.name,
            mime_type=mime,
            status=Document.Status.PROCESSING
        )
        if initial_type in Document.DocumentType.values:
            doc.document_type = initial_type
        doc.save()

        # Run AI extraction
        try:
            extraction_result = extract_document_with_ai(doc)
            doc.raw_ai_response = extraction_result
            extracted_type = extraction_result.get('document_type')
            if extracted_type in Document.DocumentType.values:
                doc.document_type = extracted_type
            elif initial_type in Document.DocumentType.values:
                doc.document_type = initial_type
            else:
                doc.document_type = Document.DocumentType.UNKNOWN
            doc.status = Document.Status.READY_FOR_REVIEW
            doc.save()
            messages.success(
                request,
                _("Scanned file '%(name)s' successfully processed by AI! Please review extracted data.") % {
                    'name': doc.original_filename
                }
            )
            return redirect('documents:detail', pk=doc.pk)
        except Exception as e:
            doc.status = Document.Status.FAILED
            doc.extraction_error = str(e)
            doc.save()
            messages.error(request, _("Extraction failed: %(error)s") % {'error': str(e)})
            return redirect('documents:detail', pk=doc.pk)

    return render(request, 'documents/document_upload.html', {'initial_type': initial_type})


def document_detail(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    extraction = doc.verified_data or doc.raw_ai_response or {}

    context = {
        'document': doc,
        'data': extraction,
        'raw_json': json.dumps(extraction, indent=2),
    }
    return render(request, 'documents/document_detail.html', context)


@require_POST
def document_confirm(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    
    # Collect form fields
    doc_type = request.POST.get('document_type', doc.document_type)
    doc_number = request.POST.get('document_number', '')
    category = request.POST.get('receipt_category', '').strip() or request.POST.get('category', '').strip()
    summary = request.POST.get('summary', '')

    counterparty = {
        'name': request.POST.get('cp_name', '').strip() or 'Unknown Counterparty',
        'type': request.POST.get('cp_type', 'VENDOR'),
        'tax_id': request.POST.get('cp_tax_id', ''),
        'iban': request.POST.get('cp_iban', ''),
        'bank_name': request.POST.get('cp_bank_name', ''),
        'swift_bic': request.POST.get('cp_swift_bic', ''),
        'email': request.POST.get('cp_email', ''),
        'phone': request.POST.get('cp_phone', ''),
        'address': request.POST.get('cp_address', ''),
    }

    dates = {
        'issue_date': request.POST.get('issue_date') or None,
        'due_date': request.POST.get('due_date') or None,
        'delivery_date': request.POST.get('delivery_date') or None,
        'contract_start': request.POST.get('contract_start') or None,
        'contract_end': request.POST.get('contract_end') or None,
        'renewal_notice_days': request.POST.get('renewal_notice_days') or 30,
    }

    financials = {
        'currency': request.POST.get('currency', 'EUR'),
        'subtotal': request.POST.get('subtotal', 0),
        'tax_amount': request.POST.get('tax_amount', 0),
        'total_amount': request.POST.get('total_amount', 0),
    }

    # Line Items
    line_items = []
    descriptions = request.POST.getlist('item_description')
    skus = request.POST.getlist('item_sku')
    quantities = request.POST.getlist('item_quantity')
    unit_prices = request.POST.getlist('item_unit_price')
    line_totals = request.POST.getlist('item_line_total')

    for i in range(len(descriptions)):
        if descriptions[i].strip():
            line_items.append({
                'description': descriptions[i].strip(),
                'sku': skus[i] if i < len(skus) else '',
                'quantity': quantities[i] if i < len(quantities) else 1,
                'unit_price': unit_prices[i] if i < len(unit_prices) else 0,
                'line_total': line_totals[i] if i < len(line_totals) else 0,
            })

    # Calendar Action
    cal_action_date = request.POST.get('action_date') or dates.get('due_date') or dates.get('delivery_date')
    cal_action_title = request.POST.get('action_title') or f"Action for #{doc_number}"
    cal_action_type = request.POST.get('action_type', 'OUTGOING_PAYMENT_DUE')
    cal_priority = request.POST.get('action_priority', 'HIGH')

    calendar_actions = []
    if cal_action_date:
        calendar_actions.append({
            'title': cal_action_title,
            'date': cal_action_date,
            'action_type': cal_action_type,
            'priority': cal_priority,
            'amount': financials.get('total_amount', 0),
            'description': f"Automated ledger action for {doc.original_filename}"
        })

    verified_payload = {
        'document_type': doc_type,
        'document_number': doc_number,
        'category': category,
        'summary': summary,
        'counterparty': counterparty,
        'dates': dates,
        'financials': financials,
        'line_items': line_items,
        'calendar_actions': calendar_actions,
    }

    try:
        sync_verified_document_to_ledgers(doc, verified_payload)
        messages.success(
            request,
            _("Document #%(number)s confirmed! Created ledger records & scheduled calendar tasks.") % {
                'number': doc_number
            }
        )
        return redirect('documents:detail', pk=doc.pk)
    except Exception as e:
        messages.error(request, _("Error saving records: %(error)s") % {'error': str(e)})
        return redirect('documents:detail', pk=doc.pk)


@require_POST
def document_reextract(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    try:
        extraction_result = extract_document_with_ai(doc)
        doc.raw_ai_response = extraction_result
        doc.document_type = extraction_result.get('document_type', Document.DocumentType.UNKNOWN)
        doc.status = Document.Status.READY_FOR_REVIEW
        doc.save()
        messages.success(request, _("AI extraction re-run complete!"))
    except Exception as e:
        messages.error(request, _("Re-extraction failed: %(error)s") % {'error': str(e)})
    return redirect('documents:detail', pk=doc.pk)
