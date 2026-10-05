import json
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from apps.documents.models import Document
from apps.documents.services.sync_service import sync_verified_document_to_ledgers
from apps.accounting.models import Invoice
from apps.calendar_tasks.models import CalendarTask


class DocumentWorkflowTestCase(TestCase):
    def setUp(self):
        self.sample_file = SimpleUploadedFile(
            "sample_invoice.pdf",
            b"%PDF-1.4 sample test content for invoice",
            content_type="application/pdf"
        )

    def test_document_creation_and_hashing(self):
        doc = Document.objects.create(
            file=self.sample_file,
            original_filename="sample_invoice.pdf",
            mime_type="application/pdf",
        )
        self.assertTrue(len(doc.file_hash) > 0)
        self.assertEqual(doc.status, Document.Status.UPLOADED)

    def test_sync_verified_document_creates_invoice_and_calendar_task(self):
        doc = Document.objects.create(
            file=self.sample_file,
            original_filename="vendor_bill.pdf",
            mime_type="application/pdf",
            document_type=Document.DocumentType.INVOICE_PAYABLE
        )
        today = timezone.localdate()
        due_date = today + timezone.timedelta(days=14)

        payload = {
            'document_type': 'INVOICE_PAYABLE',
            'document_number': 'TEST-INV-999',
            'summary': 'Test bill for software licenses',
            'counterparty': {
                'name': 'Cloud Global Ltd',
                'type': 'VENDOR',
                'tax_id': 'VAT999888',
                'iban': 'DE89370400440532019999',
                'email': 'billing@cloudglobal.com'
            },
            'dates': {
                'issue_date': str(today),
                'due_date': str(due_date),
            },
            'financials': {
                'currency': 'EUR',
                'subtotal': 1000.00,
                'tax_amount': 200.00,
                'total_amount': 1200.00,
            },
            'line_items': [
                {
                    'description': 'DevOps Subscription',
                    'quantity': 1,
                    'unit_price': 1000.00,
                    'line_total': 1000.00
                }
            ],
            'calendar_actions': [
                {
                    'title': 'Pay Bill TEST-INV-999 to Cloud Global Ltd',
                    'date': str(due_date),
                    'action_type': 'OUTGOING_PAYMENT_DUE',
                    'priority': 'HIGH',
                    'amount': 1200.00
                }
            ]
        }

        sync_verified_document_to_ledgers(doc, payload)

        doc.refresh_from_db()
        self.assertEqual(doc.status, Document.Status.CONFIRMED)

        # Check invoice was created
        invoice = Invoice.objects.filter(invoice_number='TEST-INV-999').first()
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.counterparty.name, 'Cloud Global Ltd')
        self.assertEqual(invoice.total_amount, Decimal('1200.00'))

        # Check calendar task was created
        task = CalendarTask.objects.filter(linked_invoice=invoice).first()
        self.assertIsNotNone(task)
        self.assertEqual(task.task_type, CalendarTask.TaskType.OUTGOING_PAYMENT_DUE)
        self.assertEqual(task.due_date, due_date)

    def test_extract_document_with_ai_raises_configuration_error_when_no_key(self):
        from apps.documents.services.ai_extractor import extract_document_with_ai
        from apps.ai_assistant.providers.exceptions import AIConfigurationError
        from apps.ai_assistant.models import AISetting

        setting = AISetting.get_settings()
        setting.active_provider = 'openai'
        setting.openai_api_key = ''
        setting.save()

        doc = Document.objects.create(
            file=self.sample_file,
            original_filename="sample_invoice.pdf",
            mime_type="application/pdf",
        )
        with self.assertRaises(AIConfigurationError):
            extract_document_with_ai(doc)

    def test_sync_verified_receipt_creates_accounting_receipt(self):
        from apps.accounting.models import Receipt

        doc = Document.objects.create(
            file=self.sample_file,
            original_filename="taxi_receipt.jpg",
            mime_type="image/jpeg",
            document_type=Document.DocumentType.RECEIPT
        )
        today = timezone.localdate()

        payload = {
            'document_type': 'RECEIPT',
            'document_number': 'RCP-TAXI-001',
            'category': 'Travel & Transportation',
            'summary': 'Airport taxi transfer',
            'counterparty': {
                'name': 'City Taxi Cab',
                'type': 'VENDOR',
            },
            'dates': {
                'issue_date': str(today),
            },
            'financials': {
                'currency': 'EUR',
                'subtotal': 45.00,
                'tax_amount': 5.00,
                'total_amount': 50.00,
            },
            'line_items': [],
            'calendar_actions': []
        }

        sync_verified_document_to_ledgers(doc, payload)

        doc.refresh_from_db()
        self.assertEqual(doc.status, Document.Status.CONFIRMED)

        receipt = Receipt.objects.filter(receipt_number='RCP-TAXI-001').first()
        self.assertIsNotNone(receipt)
        self.assertEqual(receipt.category, 'Travel & Transportation')
        self.assertEqual(receipt.total_amount, Decimal('50.00'))
        self.assertEqual(receipt.tax_amount, Decimal('5.00'))
        self.assertEqual(receipt.counterparty.name, 'City Taxi Cab')
        self.assertEqual(receipt.source_document, doc)

    def test_documents_list_receipts_filter(self):
        doc = Document.objects.create(
            file=self.sample_file,
            original_filename="fuel_slip.pdf",
            mime_type="application/pdf",
            document_type=Document.DocumentType.RECEIPT
        )
        response = self.client.get('/documents/?type=RECEIPT')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fuel_slip.pdf")
        self.assertEqual(response.context['selected_type'], 'RECEIPT')
        self.assertGreaterEqual(response.context['receipts_count'], 1)

    def test_accounting_receipt_list_shows_ai_scan_link(self):
        from apps.accounting.models import Receipt
        from apps.administration.models import Counterparty

        vendor = Counterparty.objects.create(name="Office Depot")
        doc = Document.objects.create(
            file=self.sample_file,
            original_filename="office_supplies.pdf",
            mime_type="application/pdf",
            document_type=Document.DocumentType.RECEIPT,
            status=Document.Status.CONFIRMED
        )
        Receipt.objects.create(
            receipt_number="RCP-101",
            counterparty=vendor,
            category="Office Supplies",
            total_amount=Decimal('89.50'),
            source_document=doc
        )

        response = self.client.get('/accounting/receipts/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RCP-101")
        self.assertContains(response, f"/documents/{doc.pk}/")
        self.assertContains(response, "Scan Receipt with AI")

    def test_build_extraction_prompt_includes_company_profile(self):
        from apps.documents.services.ai_extractor import build_extraction_system_prompt
        from apps.administration.models import CompanyProfile

        profile = CompanyProfile.get_solo()
        profile.legal_name = "Global Logistics Enterprise Ltd"
        profile.tax_id = "DE99887766"
        profile.save()

        prompt = build_extraction_system_prompt()
        self.assertIn("Global Logistics Enterprise Ltd", prompt)
        self.assertIn("DE99887766", prompt)
        self.assertIn("INVOICE_RECEIVABLE", prompt)
        self.assertIn("INVOICE_PAYABLE", prompt)


