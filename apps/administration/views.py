from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from apps.administration.models import Counterparty, Contract, CompanyProfile


def counterparty_list(request):
    counterparties = Counterparty.objects.all().order_by('name')
    context = {
        'counterparties': counterparties,
    }
    return render(request, 'administration/counterparty_list.html', context)


@require_POST
def counterparty_create(request):
    name = request.POST.get('name', '').strip()
    cp_type = request.POST.get('counterparty_type', Counterparty.TypeChoices.VENDOR)
    tax_id = request.POST.get('tax_id', '').strip()
    iban = request.POST.get('iban', '').strip()
    bank_name = request.POST.get('bank_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    address = request.POST.get('address', '').strip()

    Counterparty.objects.create(
        name=name,
        counterparty_type=cp_type,
        tax_id=tax_id,
        iban=iban,
        bank_name=bank_name,
        email=email,
        phone=phone,
        address=address
    )
    messages.success(request, _("Counterparty '%(name)s' created successfully.") % {'name': name})
    return redirect('administration:counterparty_list')


def counterparty_update(request, pk):
    counterparty = get_object_or_404(Counterparty, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            counterparty.name = name
        counterparty.counterparty_type = request.POST.get('counterparty_type', counterparty.counterparty_type)
        counterparty.tax_id = request.POST.get('tax_id', '').strip()
        counterparty.registration_number = request.POST.get('registration_number', '').strip()
        counterparty.iban = request.POST.get('iban', '').strip()
        counterparty.bank_name = request.POST.get('bank_name', '').strip()
        counterparty.swift_bic = request.POST.get('swift_bic', '').strip()
        counterparty.email = request.POST.get('email', '').strip()
        counterparty.phone = request.POST.get('phone', '').strip()
        counterparty.address = request.POST.get('address', '').strip()
        terms = request.POST.get('default_payment_terms_days')
        if terms and terms.isdigit():
            counterparty.default_payment_terms_days = int(terms)
        counterparty.notes = request.POST.get('notes', '').strip()
        counterparty.save()

        messages.success(request, _("Counterparty '%(name)s' updated successfully.") % {'name': counterparty.name})
    return redirect('administration:counterparty_list')


def contract_list(request):
    contracts = Contract.objects.select_related('counterparty').all()
    context = {
        'contracts': contracts,
        'counterparties': Counterparty.objects.all(),
    }
    return render(request, 'administration/contract_list.html', context)


@require_POST
def contract_create(request):
    title = request.POST.get('title', '').strip()
    cp_id = request.POST.get('counterparty_id')
    start_date = request.POST.get('start_date') or None
    end_date = request.POST.get('end_date') or None
    notice_days = int(request.POST.get('renewal_notice_period_days') or 30)
    auto_renew = request.POST.get('auto_renew') == 'on'

    counterparty = get_object_or_404(Counterparty, pk=cp_id)

    Contract.objects.create(
        title=title,
        counterparty=counterparty,
        start_date=start_date,
        end_date=end_date,
        renewal_notice_period_days=notice_days,
        auto_renew=auto_renew
    )
    messages.success(request, _("Contract '%(title)s' registered.") % {'title': title})
    return redirect('administration:contract_list')


def company_profile_view(request):
    profile = CompanyProfile.get_solo()

    if request.method == 'POST':
        legal_name = request.POST.get('legal_name', '').strip()
        if legal_name:
            profile.legal_name = legal_name
        profile.trade_name = request.POST.get('trade_name', '').strip()
        profile.tax_id = request.POST.get('tax_id', '').strip()
        profile.registration_number = request.POST.get('registration_number', '').strip()
        profile.iban = request.POST.get('iban', '').strip()
        profile.bank_name = request.POST.get('bank_name', '').strip()
        profile.swift_bic = request.POST.get('swift_bic', '').strip()
        profile.email = request.POST.get('email', '').strip()
        profile.phone = request.POST.get('phone', '').strip()
        profile.address = request.POST.get('address', '').strip()
        curr = request.POST.get('currency', '').strip().upper()
        if curr:
            profile.currency = curr
        profile.save()

        messages.success(
            request,
            _("Company profile updated successfully. AI document classification and ledger rules will now use these entity details.")
        )
        return redirect('administration:company_profile')

    context = {
        'profile': profile,
    }
    return render(request, 'administration/company_profile.html', context)

