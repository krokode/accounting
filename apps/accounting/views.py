from decimal import Decimal
from django.contrib import messages
from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from apps.accounting.models import Invoice, PaymentRecord, Receipt
from apps.calendar_tasks.models import CalendarTask
from apps.administration.models import Counterparty


def invoice_list(request):
    direction = request.GET.get('direction')
    status = request.GET.get('status')
    
    invoices = Invoice.objects.select_related('counterparty').all()
    if direction:
        invoices = invoices.filter(direction=direction)
    if status:
        invoices = invoices.filter(payment_status=status)

    today = timezone.localdate()
    # Auto-update status for overdue items
    for inv in invoices:
        if inv.due_date < today and inv.payment_status not in [Invoice.PaymentStatus.PAID, Invoice.PaymentStatus.DISPUTED]:
            if inv.payment_status != Invoice.PaymentStatus.OVERDUE:
                inv.payment_status = Invoice.PaymentStatus.OVERDUE
                inv.save(update_fields=['payment_status'])

    # Totals
    payables_unpaid = Invoice.objects.filter(
        direction=Invoice.Direction.PAYABLE,
        payment_status__in=[Invoice.PaymentStatus.UNPAID, Invoice.PaymentStatus.PARTIALLY_PAID, Invoice.PaymentStatus.OVERDUE]
    )
    total_payable = sum(i.remaining_amount for i in payables_unpaid)

    receivables_unpaid = Invoice.objects.filter(
        direction=Invoice.Direction.RECEIVABLE,
        payment_status__in=[Invoice.PaymentStatus.UNPAID, Invoice.PaymentStatus.PARTIALLY_PAID, Invoice.PaymentStatus.OVERDUE]
    )
    total_receivable = sum(i.remaining_amount for i in receivables_unpaid)

    context = {
        'invoices': invoices,
        'selected_direction': direction,
        'selected_status': status,
        'total_payable': total_payable,
        'total_receivable': total_receivable,
    }
    return render(request, 'accounting/invoice_list.html', context)


def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('counterparty', 'source_document'), pk=pk)
    context = {
        'invoice': invoice,
        'items': invoice.items.all(),
        'payments': invoice.payments.order_by('-payment_date'),
        'today': timezone.localdate(),
    }
    return render(request, 'accounting/invoice_detail.html', context)


@require_POST
def record_payment(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    amount_str = request.POST.get('amount', '0')
    payment_method = request.POST.get('payment_method', PaymentRecord.Method.BANK_TRANSFER)
    reference = request.POST.get('transaction_reference', '').strip()
    notes = request.POST.get('notes', '').strip()

    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            messages.error(request, _("Payment amount must be greater than zero."))
            return redirect('accounting:invoice_detail', pk=invoice.pk)
    except Exception:
        messages.error(request, _("Invalid payment amount."))
        return redirect('accounting:invoice_detail', pk=invoice.pk)

    PaymentRecord.objects.create(
        invoice=invoice,
        amount=amount,
        payment_method=payment_method,
        transaction_reference=reference,
        notes=notes
    )

    # Check if fully paid and resolve linked calendar task
    invoice.refresh_from_db()
    if invoice.payment_status == Invoice.PaymentStatus.PAID:
        linked_tasks = CalendarTask.objects.filter(linked_invoice=invoice)
        linked_tasks.update(status=CalendarTask.Status.COMPLETED)
        messages.success(
            request,
            _("Full payment of %(amount)s %(currency)s recorded! Invoice #%(number)s is now marked as Paid, and the calendar task is completed.") % {
                'amount': amount,
                'currency': invoice.currency,
                'number': invoice.invoice_number,
            }
        )
    else:
        messages.success(
            request,
            _("Partial payment of %(amount)s %(currency)s recorded. Remaining: %(remaining)s %(currency)s.") % {
                'amount': amount,
                'currency': invoice.currency,
                'remaining': invoice.remaining_amount,
            }
        )

    return redirect('accounting:invoice_detail', pk=invoice.pk)


def receipt_list(request):
    receipts = Receipt.objects.select_related('counterparty', 'source_document').all()
    total_expenses = receipts.aggregate(sum=Sum('total_amount'))['sum'] or Decimal('0.00')

    context = {
        'receipts': receipts,
        'total_expenses': total_expenses,
        'counterparties': Counterparty.objects.all(),
    }
    return render(request, 'accounting/receipt_list.html', context)


@require_POST
def receipt_create(request):
    category = request.POST.get('category', 'Office Supplies')
    total_amount = Decimal(request.POST.get('total_amount', 0))
    tax_amount = Decimal(request.POST.get('tax_amount', 0))
    cp_id = request.POST.get('counterparty_id')
    notes = request.POST.get('notes', '')

    counterparty = None
    if cp_id:
        counterparty = Counterparty.objects.filter(pk=cp_id).first()

    Receipt.objects.create(
        counterparty=counterparty,
        category=category,
        total_amount=total_amount,
        tax_amount=tax_amount,
        notes=notes
    )
    messages.success(request, _("Expense receipt for €%(amount)s recorded.") % {'amount': total_amount})
    return redirect('accounting:receipt_list')
