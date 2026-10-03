from decimal import Decimal
from django.contrib import messages
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from apps.warehouse.models import Product, Consignment, ConsignmentItem, StockMovement
from apps.administration.models import Counterparty


def product_list(request):
    products = Product.objects.all().order_by('name')
    low_stock_count = Product.objects.filter(quantity_on_hand__lte=F('reorder_threshold')).count()
    
    context = {
        'products': products,
        'low_stock_count': low_stock_count,
    }
    return render(request, 'warehouse/product_list.html', context)


@require_POST
def product_create(request):
    sku = request.POST.get('sku', '').strip()
    name = request.POST.get('name', '').strip()
    category = request.POST.get('category', '').strip()
    unit = request.POST.get('unit_of_measure', 'pcs').strip()
    cost_price = Decimal(request.POST.get('cost_price', 0))
    sale_price = Decimal(request.POST.get('sale_price', 0))
    reorder_threshold = Decimal(request.POST.get('reorder_threshold', 5))
    initial_stock = Decimal(request.POST.get('quantity_on_hand', 0))

    if Product.objects.filter(sku=sku).exists():
        messages.error(request, _("Product with SKU '%(sku)s' already exists.") % {'sku': sku})
        return redirect('warehouse:product_list')

    prod = Product.objects.create(
        sku=sku,
        name=name,
        category=category,
        unit_of_measure=unit,
        cost_price=cost_price,
        sale_price=sale_price,
        reorder_threshold=reorder_threshold,
        quantity_on_hand=initial_stock
    )
    if initial_stock > 0:
        StockMovement.objects.create(
            product=prod,
            movement_type=StockMovement.MovementType.INVENTORY_ADJUSTMENT,
            quantity=initial_stock,
            balance_after=initial_stock,
            reference="Initial stock on product creation"
        )
    messages.success(request, _("Product '%(name)s' [%(sku)s] created successfully.") % {'name': name, 'sku': sku})
    return redirect('warehouse:product_list')


def consignment_list(request):
    consignments = Consignment.objects.select_related('counterparty').all()
    context = {
        'consignments': consignments,
        'counterparties': Counterparty.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'warehouse/consignment_list.html', context)


def consignment_detail(request, pk):
    consignment = get_object_or_404(Consignment.objects.select_related('counterparty', 'source_document'), pk=pk)
    context = {
        'consignment': consignment,
        'items': consignment.items.select_related('product').all(),
        'movements': consignment.stock_movements.all(),
    }
    return render(request, 'warehouse/consignment_detail.html', context)


@require_POST
def consignment_confirm(request, pk):
    consignment = get_object_or_404(Consignment, pk=pk)
    if consignment.status == Consignment.Status.RECEIVED_CONFIRMED:
        messages.warning(request, _("This consignment has already been received and stocked."))
        return redirect('warehouse:consignment_detail', pk=consignment.pk)

    consignment.confirm_and_update_stock()
    messages.success(
        request,
        _("Consignment #%(number)s received! Warehouse stock levels automatically updated.") % {
            'number': consignment.consignment_number
        }
    )
    return redirect('warehouse:consignment_detail', pk=consignment.pk)
