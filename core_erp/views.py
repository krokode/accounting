from datetime import timedelta
from decimal import Decimal
from django.db.models import F
from django.shortcuts import render
from django.utils import timezone

from apps.accounting.models import Invoice
from apps.administration.models import Contract, Counterparty
from apps.calendar_tasks.models import CalendarTask
from apps.documents.models import Document
from apps.warehouse.models import Product


def dashboard(request):
    today = timezone.localdate()

    # Invoices AP / AR
    unpaid_payables = Invoice.objects.filter(
        direction=Invoice.Direction.PAYABLE,
        payment_status__in=[Invoice.PaymentStatus.UNPAID, Invoice.PaymentStatus.PARTIALLY_PAID, Invoice.PaymentStatus.OVERDUE]
    )
    total_payable = sum(i.remaining_amount for i in unpaid_payables)

    unpaid_receivables = Invoice.objects.filter(
        direction=Invoice.Direction.RECEIVABLE,
        payment_status__in=[Invoice.PaymentStatus.UNPAID, Invoice.PaymentStatus.PARTIALLY_PAID, Invoice.PaymentStatus.OVERDUE]
    )
    total_receivable = sum(i.remaining_amount for i in unpaid_receivables)

    overdue_invoices = Invoice.objects.filter(payment_status=Invoice.PaymentStatus.OVERDUE)

    # Documents
    pending_docs = Document.objects.filter(
        status__in=[Document.Status.UPLOADED, Document.Status.READY_FOR_REVIEW]
    ).order_by('-created_at')[:5]

    # Upcoming Calendar Tasks (next 7 days)
    upcoming_tasks = CalendarTask.objects.filter(
        due_date__gte=today,
        due_date__lte=today + timedelta(days=7),
        status__in=[CalendarTask.Status.PENDING, CalendarTask.Status.IN_PROGRESS]
    ).order_by('due_date')[:6]

    # Warehouse & Contracts
    low_stock_products = Product.objects.filter(quantity_on_hand__lte=F('reorder_threshold'))
    active_contracts = Contract.objects.filter(status=Contract.StatusChoices.ACTIVE)

    context = {
        'total_payable': total_payable,
        'total_receivable': total_receivable,
        'net_position': total_receivable - total_payable,
        'overdue_count': overdue_invoices.count(),
        'overdue_invoices': overdue_invoices[:4],
        'pending_docs': pending_docs,
        'upcoming_tasks': upcoming_tasks,
        'low_stock_count': low_stock_products.count(),
        'active_contracts_count': active_contracts.count(),
        'today': today,
    }
    return render(request, 'dashboard.html', context)
