import logging
import os
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
from django.db.models import Sum, F
from django.utils import timezone

from apps.accounting.models import Invoice, Receipt
from apps.administration.models import Contract, Counterparty
from apps.calendar_tasks.models import CalendarTask
from apps.warehouse.models import Product, Consignment

logger = logging.getLogger(__name__)


def get_system_context() -> dict:
    """Gathers real-time operational context across the database."""
    today = timezone.localdate()

    # Invoices
    unpaid_payables = Invoice.objects.filter(
        direction=Invoice.Direction.PAYABLE,
        payment_status__in=[Invoice.PaymentStatus.UNPAID, Invoice.PaymentStatus.PARTIALLY_PAID, Invoice.PaymentStatus.OVERDUE]
    )
    total_payable = sum(inv.remaining_amount for inv in unpaid_payables)

    unpaid_receivables = Invoice.objects.filter(
        direction=Invoice.Direction.RECEIVABLE,
        payment_status__in=[Invoice.PaymentStatus.UNPAID, Invoice.PaymentStatus.PARTIALLY_PAID, Invoice.PaymentStatus.OVERDUE]
    )
    total_receivable = sum(inv.remaining_amount for inv in unpaid_receivables)

    overdue_invoices = Invoice.objects.filter(
        payment_status=Invoice.PaymentStatus.OVERDUE
    )

    # Next 14 days tasks
    upcoming_tasks = CalendarTask.objects.filter(
        due_date__gte=today,
        due_date__lte=today + timedelta(days=14),
        status__in=[CalendarTask.Status.PENDING, CalendarTask.Status.IN_PROGRESS]
    )

    # Low stock
    low_stock = Product.objects.filter(quantity_on_hand__lte=F('reorder_threshold'))

    # Expiring contracts
    expiring_contracts = Contract.objects.filter(
        end_date__gte=today,
        end_date__lte=today + timedelta(days=60),
        status__in=[Contract.StatusChoices.ACTIVE, Contract.StatusChoices.PENDING_RENEWAL]
    )

    # Receipts & Expense Vouchers
    recent_receipts = Receipt.objects.select_related('counterparty').all()[:5]
    total_receipts_amount = Receipt.objects.aggregate(sum=Sum('total_amount'))['sum'] or Decimal('0.00')

    from apps.administration.models import CompanyProfile
    profile = CompanyProfile.get_solo()

    return {
        'company_name': profile.trade_name or profile.legal_name,
        'company_legal_name': profile.legal_name,
        'company_tax_id': profile.tax_id,
        'currency': profile.currency,
        'today': str(today),
        'total_payable': float(total_payable),
        'total_receivable': float(total_receivable),
        'total_receipts_expense': float(total_receipts_amount),
        'recent_receipts_list': [
            {'category': r.category, 'party': r.counterparty.name if r.counterparty else 'General', 'date': str(r.receipt_date), 'amount': float(r.total_amount), 'currency': r.currency}
            for r in recent_receipts
        ],
        'overdue_count': overdue_invoices.count(),
        'overdue_list': [
            {'num': i.invoice_number, 'party': i.counterparty.name, 'due': str(i.due_date), 'amount': float(i.remaining_amount), 'currency': i.currency}
            for i in overdue_invoices[:5]
        ],
        'upcoming_tasks_count': upcoming_tasks.count(),
        'upcoming_tasks_list': [
            {'title': t.title, 'type': t.get_task_type_display(), 'due': str(t.due_date), 'amount': float(t.amount or 0)}
            for t in upcoming_tasks[:5]
        ],
        'low_stock_count': low_stock.count(),
        'low_stock_list': [
            {'name': p.name, 'sku': p.sku, 'stock': float(p.quantity_on_hand), 'min': float(p.reorder_threshold)}
            for p in low_stock[:5]
        ],
        'expiring_contracts_list': [
            {'title': c.title, 'party': c.counterparty.name, 'end': str(c.end_date)}
            for c in expiring_contracts[:5]
        ]
    }


from apps.ai_assistant.providers.registry import get_active_provider
from apps.ai_assistant.providers.exceptions import (
    AIConfigurationError,
    AIRateLimitError,
    AIOfflineError,
    AIAuthenticationError,
    AIError,
)
from django.utils.translation import gettext as _


def query_copilot(user_prompt: str) -> str:
    """Answers user natural language questions using the active LLM provider with strict error reporting."""
    provider = get_active_provider()
    context = get_system_context()

    try:
        provider.validate_configuration()
    except AIConfigurationError as ce:
        return f"⚠️ **{_('AI Configuration Required')}**\n\n{ce.message}\n\n👉 [{_('Open AI Settings')}](/assistant/settings/) | `python setup_llm.py`"

    from django.utils.translation import get_language
    lang = get_language() or 'en'

    system_instruction = f"""You are the senior financial and operational AI Copilot for {context['company_name']} (Legal Name: {context['company_legal_name']}, Tax ID: {context['company_tax_id']}).
The user's active application language code is: '{lang}'.
Please respond accurately and professionally in the user's language ({lang}).
You have real-time live access to the company's records database:
- Operating Currency: {context['currency']}
- Current Date: {context['today']}
- Total Outstanding Payables (Bills We Owe to Suppliers): {context['currency']} {context['total_payable']:,.2f}
- Total Expected Receivables (Customer Invoices Owed to Us): {context['currency']} {context['total_receivable']:,.2f}
- Total Recorded Receipts & Direct Expenses: {context['currency']} {context['total_receipts_expense']:,.2f}
- Overdue Invoices: {context['overdue_count']} ({context['overdue_list']})
- Upcoming Tasks (Next 14 days): {context['upcoming_tasks_count']} ({context['upcoming_tasks_list']})
- Low Stock Items: {context['low_stock_count']} ({context['low_stock_list']})
- Contracts Expiring within 60 days: {context['expiring_contracts_list']}

Answer the user's questions clearly, concisely, and accurately. Use Markdown tables, bold text, and bullet points where helpful.
"""
    try:
        return provider.generate_text(user_prompt, system_instruction)
    except AIRateLimitError as rle:
        return f"⏳ **{_('Rate Limit Exceeded')}**\n\n{rle.message}\n\n👉 [{_('Switch Provider in AI Settings')}](/assistant/settings/)"
    except AIOfflineError as oe:
        return f"🔌 **{_('AI Provider Offline / Unreachable')}**\n\n{oe.message}\n\n👉 [{_('Check Endpoint in AI Settings')}](/assistant/settings/)"
    except AIAuthenticationError as ae:
        return f"🔑 **{_('Authentication Failed')}**\n\n{ae.message}\n\n👉 [{_('Update API Key in AI Settings')}](/assistant/settings/)"
    except AIError as aie:
        return f"❌ **{_('AI Error')}**\n\n{aie.message}"
    except Exception as e:
        logger.error(f"Unexpected AI Copilot error: {e}")
        return f"❌ **{_('AI Execution Failed')}**: {e}"



def _rule_based_copilot(prompt: str, ctx: dict) -> str:
    """Rule-based intelligent responder supporting all 8 languages."""
    from django.utils.translation import get_language
    raw_lang = (get_language() or 'en').lower()
    lang = 'zh_Hans' if 'zh' in raw_lang else raw_lang.split('-')[0]
    p = prompt.lower()

    # Intent 1: Payables / Bills
    if any(k in p for k in ["pay", "owe", "bill", "payable", "счет", "оплат", "долг", "factura", "pagar", "facture", "betaal", "fatura", "账单", "应付", "支払", "請求"]):
        if lang == 'ru':
            text = f"### 💳 Обзор кредиторской задолженности (Счета к оплате)\n\nСумма неоплаченных счетов поставщиков: **€{ctx['total_payable']:,.2f}**.\n\n"
            if ctx['overdue_list']:
                text += f"⚠️ **Внимание: {ctx['overdue_count']} просроченных счетов**:\n"
                for o in ctx['overdue_list']:
                    text += f"- **Счет #{o['num']}** ({o['party']}): **€{o['amount']:,.2f}** (срок: {o['due']})\n"
            else:
                text += "✅ Просроченных счетов к оплате нет.\n"
            return text
        elif lang == 'es':
            text = f"### 💳 Resumen de Cuentas por Pagar (Facturas)\n\nTotal de facturas pendientes a proveedores: **€{ctx['total_payable']:,.2f}**.\n\n"
            if ctx['overdue_list']:
                text += f"⚠️ **Atención: {ctx['overdue_count']} factura(s) vencida(s)**:\n"
                for o in ctx['overdue_list']:
                    text += f"- **Factura #{o['num']}** ({o['party']}): **€{o['amount']:,.2f}** (venció el {o['due']})\n"
            else:
                text += "✅ No hay facturas vencidas pendientes.\n"
            return text
        elif lang == 'nl':
            text = f"### 💳 Overzicht Te Betalen Facturen (Crediteuren)\n\nOpenstaande leveranciersfacturen: **€{ctx['total_payable']:,.2f}**.\n\n"
            if ctx['overdue_list']:
                text += f"⚠️ **Let op: {ctx['overdue_count']} vervallen factu(u)r(en)**:\n"
                for o in ctx['overdue_list']:
                    text += f"- **Factuur #{o['num']}** ({o['party']}): **€{o['amount']:,.2f}** (vervaldatum was {o['due']})\n"
            else:
                text += "✅ Er zijn momenteel geen vervallen facturen.\n"
            return text
        elif lang == 'fr':
            text = f"### 💳 Aperçu des Factures à Payer (Fournisseurs)\n\nFactures fournisseurs en attente : **€{ctx['total_payable']:,.2f}**.\n\n"
            if ctx['overdue_list']:
                text += f"⚠️ **Attention : {ctx['overdue_count']} facture(s) en retard** :\n"
                for o in ctx['overdue_list']:
                    text += f"- **Facture #{o['num']}** ({o['party']}) : **€{o['amount']:,.2f}** (échéance : {o['due']})\n"
            else:
                text += "✅ Aucune facture en retard.\n"
            return text
        elif lang == 'pt':
            text = f"### 💳 Visão Geral de Contas a Pagar\n\nTotal de faturas pendentes de fornecedores: **€{ctx['total_payable']:,.2f}**.\n\n"
            if ctx['overdue_list']:
                text += f"⚠️ **Atenção: {ctx['overdue_count']} fatura(s) vencida(s)**:\n"
                for o in ctx['overdue_list']:
                    text += f"- **Fatura #{o['num']}** ({o['party']}): **€{o['amount']:,.2f}** (venceu a {o['due']})\n"
            else:
                text += "✅ Não existem faturas em atraso no momento.\n"
            return text
        elif lang == 'zh_Hans':
            text = f"### 💳 应付账款概览 (待付账单)\n\n当前待付供应商账单总额为 **€{ctx['total_payable']:,.2f}**。\n\n"
            if ctx['overdue_list']:
                text += f"⚠️ **紧急提醒: 共有 {ctx['overdue_count']} 张逾期账单**:\n"
                for o in ctx['overdue_list']:
                    text += f"- **账单 #{o['num']}** ({o['party']}): **€{o['amount']:,.2f}** (到期日: {o['due']})\n"
            else:
                text += "✅ 当前没有任何逾期待付账单。\n"
            return text
        elif lang == 'ja':
            text = f"### 💳 買掛金・未払請求書の概要\n\n未払いの仕入先請求書合計: **€{ctx['total_payable']:,.2f}**。\n\n"
            if ctx['overdue_list']:
                text += f"⚠️ **注意: {ctx['overdue_count']}件の支払期日超過請求書があります**:\n"
                for o in ctx['overdue_list']:
                    text += f"- **請求書 #{o['num']}** ({o['party']}): **€{o['amount']:,.2f}** (期日: {o['due']})\n"
            else:
                text += "✅ 期日を超過した未払請求書はありません。\n"
            return text
        else:
            text = f"### 💳 Outstanding Payables Overview\n\nWe currently have **€{ctx['total_payable']:,.2f}** in unpaid vendor bills.\n\n"
            if ctx['overdue_list']:
                text += f"⚠️ **Attention: {ctx['overdue_count']} Overdue Invoice(s)**:\n"
                for o in ctx['overdue_list']:
                    text += f"- **Invoice #{o['num']}** to *{o['party']}*: **€{o['amount']:,.2f}** (was due on {o['due']})\n"
            else:
                text += "✅ There are currently no overdue payables.\n"
            return text

    # Intent 2: Receivables
    if any(k in p for k in ["receivable", "incoming", "customer", "дебитор", "поступлен", "клиент", "cobrar", "receb", "ontvang", "client", "应收", "入金"]):
        labels = {
            'ru': f"### 📥 Ожидаемые поступления (Дебиторка)\n\nСумма ожидаемых платежей от клиентов: **€{ctx['total_receivable']:,.2f}**.\n\n",
            'es': f"### 📥 Cuentas por Cobrar Previstas\n\nTotal de cobros previstos de clientes: **€{ctx['total_receivable']:,.2f}**.\n\n",
            'nl': f"### 📥 Verwachte Ontvangsten (Debiteuren)\n\nVerwachte betalingen van klanten: **€{ctx['total_receivable']:,.2f}**.\n\n",
            'fr': f"### 📥 Créances Clients Attendues\n\nTotal des encaissements prévus : **€{ctx['total_receivable']:,.2f}**.\n\n",
            'pt': f"### 📥 Contas a Receber Previstas\n\nTotal de recebimentos de clientes previstos: **€{ctx['total_receivable']:,.2f}**.\n\n",
            'zh_Hans': f"### 📥 预期应收账款 (客户款项)\n\n预计收到的客户销售账款总额为 **€{ctx['total_receivable']:,.2f}**。\n\n",
            'ja': f"### 📥 売掛金・入金予定\n\n顧客からの入金予定総額は **€{ctx['total_receivable']:,.2f}** です。\n\n",
            'en': f"### 📥 Expected Incoming Receivables\n\nTotal expected incoming payments from customers: **€{ctx['total_receivable']:,.2f}**.\n\n"
        }
        return labels.get(lang, labels['en'])

    # Intent 3: Stock / Warehouse
    if any(k in p for k in ["stock", "warehouse", "inventor", "склад", "остатк", "inventario", "voorraad", "inventaire", "estoque", "库存", "在库", "在庫"]):
        headers = {
            'ru': ("### 📦 Склад и остатки товаров\n\n", "| Товар | Артикул | На складе | Порог дозаказа |\n|---|---|---|---|\n", "✅ Все товары на складе выше порога дозаказа.\n"),
            'es': ("### 📦 Estado del Inventario de Almacén\n\n", "| Producto | SKU | En Stock | Punto Reorden |\n|---|---|---|---|\n", "✅ Todo el inventario se encuentra por encima del umbral de reorden.\n"),
            'nl': ("### 📦 Voorraad- en Magazijnstatus\n\n", "| Product | SKU | Op Voorraad | Bestelpunt |\n|---|---|---|---|\n", "✅ Alle magazijnartikelen bevinden zich boven het bestelpunt.\n"),
            'fr': ("### 📦 État des Stocks de l'Entrepôt\n\n", "| Produit | SKU | En Stock | Seuil Réappro |\n|---|---|---|---|\n", "✅ Tous les articles en stock sont au-dessus de leur seuil de réapprovisionnement.\n"),
            'pt': ("### 📦 Estado do Stock e Armazém\n\n", "| Produto | SKU | Em Stock | Ponto de Reencomenda |\n|---|---|---|---|\n", "✅ Todos os artigos em armazém estão acima do limiar de reposição.\n"),
            'zh_Hans': ("### 📦 仓库与库存状态\n\n", "| 商品名称 | SKU编号 | 当前库存 | 补货预警线 |\n|---|---|---|---|\n", "✅ 当前所有商品的库存量均高于补货警戒线。\n"),
            'ja': ("### 📦 倉庫在庫ステータス\n\n", "| 商品名 | SKUコード | 現在庫 | 発注点 |\n|---|---|---|---|\n", "✅ すべての在庫品目は安全発注点以上の水準を維持しています。\n"),
            'en': ("### 📦 Warehouse & Stock Status\n\n", "| Product Name | SKU | On Hand | Reorder Point |\n|---|---|---|---|\n", "✅ All warehouse inventory items are currently above their reorder thresholds.\n")
        }
        h_title, h_table, h_ok = headers.get(lang, headers['en'])
        if ctx['low_stock_list']:
            text = f"{h_title}⚠️ **{ctx['low_stock_count']} SKU(s)**:\n\n{h_table}"
            for item in ctx['low_stock_list']:
                text += f"| {item['name']} | `{item['sku']}` | **{item['stock']}** | {item['min']} |\n"
            return text
        return f"{h_title}{h_ok}"

    # Intent 4: Contracts
    if any(k in p for k in ["contract", "renewal", "договор", "контракт", "contrat", "acuerdo", "overeenkomst", "合同", "契約"]):
        c_headers = {
            'ru': ("### 📜 Реестр договоров и сроки действия\n\n", "Следующие договоры требуют внимания или уведомления о продлении:\n\n", "✅ Нет активных договоров, истекающих в ближайшие 60 дней.\n"),
            'es': ("### 📜 Registro de Contratos y Vencimientos\n\n", "Los siguientes contratos requieren revisión o aviso de renovación pronto:\n\n", "✅ No hay contratos activos que venzan en los próximos 60 días.\n"),
            'nl': ("### 📜 Contracten & Verlengingen\n\n", "De volgende contracten vereisen binnenkort herziening of opzegging:\n\n", "✅ Geen actieve contracten die binnen 60 dagen aflopen.\n"),
            'fr': ("### 📜 Contrats & Échéances\n\n", "Les contrats suivants nécessitent une révision ou un préavis prochainement :\n\n", "✅ Aucun contrat actif n'expire dans les 60 prochains jours.\n"),
            'pt': ("### 📜 Registo de Contratos e Renovações\n\n", "Os seguintes contratos necessitam de revisão ou aviso prévio em breve:\n\n", "✅ Nenhum contrato ativo expira nos próximos 60 dias.\n"),
            'zh_Hans': ("### 📜 合同台账与续签管理\n\n", "以下合同近期需进行审核或发出续约/终止通知:\n\n", "✅ 未来60天内无即将到期的商业合同。\n"),
            'ja': ("### 📜 契約管理・更新通知\n\n", "以下の契約は間もなく見直しまたは更新通知の期限を迎えます:\n\n", "✅ 今後60日以内に満了する有効な契約はありません。\n"),
            'en': ("### 📜 Contracts & Expirations\n\n", "The following contracts require review or renewal notice soon:\n\n", "✅ No active contracts are expiring within the next 60 days.\n")
        }
        ct, cm, co = c_headers.get(lang, c_headers['en'])
        if ctx['expiring_contracts_list']:
            text = f"{ct}{cm}"
            for c in ctx['expiring_contracts_list']:
                text += f"- **{c['title']}** (*{c['party']}*) — `{c['end']}`\n"
            return text
        return f"{ct}{co}"

    # Intent 5: Tasks / Calendar
    if any(k in p for k in ["task", "calendar", "today", "week", "задач", "календар", "tarea", "calendario", "taak", "agenda", "tâche", "tarefa", "日程", "任务", "タスク", "予定"]):
        t_headers = {
            'ru': ("### 📅 Задачи и сроки в календаре (следующие 14 дней)\n\n", "Нет запланированных задач на ближайшие 14 дней.\n"),
            'es': ("### 📅 Tareas y Vencimientos en Calendario (Próximos 14 días)\n\n", "No hay tareas pendientes en el calendario para los próximos 14 días.\n"),
            'nl': ("### 📅 Taken & Deadlines in Agenda (Komende 14 dagen)\n\n", "Geen openstaande agendataken gevonden voor de komende 14 dagen.\n"),
            'fr': ("### 📅 Tâches & Échéances au Calendrier (14 prochains jours)\n\n", "Aucune tâche en attente dans le calendrier pour les 14 prochains jours.\n"),
            'pt': ("### 📅 Tarefas e Prazos no Calendário (Próximos 14 dias)\n\n", "Nenhuma tarefa pendente encontrada no calendário para os próximos 14 dias.\n"),
            'zh_Hans': ("### 📅 日程任务与待办事项 (未来14天)\n\n", "未来14天内无待处理的日程任务。\n"),
            'ja': ("### 📅 カレンダータスク＆期日 (今後14日間)\n\n", "今後14日間に予定されている保留中のタスクはありません。\n"),
            'en': ("### 📅 Upcoming Tasks & Deadlines (Next 14 Days)\n\n", "No pending calendar tasks found for the next 14 days.\n")
        }
        tt, te = t_headers.get(lang, t_headers['en'])
        if ctx['upcoming_tasks_list']:
            text = tt
            for t in ctx['upcoming_tasks_list']:
                amt_str = f" (€{t['amount']:,.2f})" if t['amount'] else ""
                text += f"- **{t['due']}** — [{t['type']}] **{t['title']}**{amt_str}\n"
            return text
        return f"{tt}{te}"

    # General Financial & Operational Summary
    net_position = ctx['total_receivable'] - ctx['total_payable']
    if lang == 'ru':
        return (
            f"### 📊 Финансовая и операционная сводка компании\n\n"
            f"- **Кредиторская задолженность (Мы должны)**: €{ctx['total_payable']:,.2f}\n"
            f"- **Ожидаемая дебиторка (Нам должны)**: €{ctx['total_receivable']:,.2f}\n"
            f"- **Прогнозируемый чистый баланс**: €{net_position:,.2f}\n"
            f"- **Просроченных счетов**: {ctx['overdue_count']}\n"
            f"- **Задач на ближайшие 14 дней**: {ctx['upcoming_tasks_count']}\n"
            f"- **Позиций с низким остатком на складе**: {ctx['low_stock_count']}\n\n"
            f"*Задайте любой вопрос, например: 'Какие счета подлежат оплате на этой неделе?', 'Покажи товары с низким остатком' или 'Сводка по договорам'.*"
        )
    elif lang == 'es':
        return (
            f"### 📊 Resumen Financiero y Operativo de la Empresa\n\n"
            f"- **Cuentas por Pagar (Debemos)**: €{ctx['total_payable']:,.2f}\n"
            f"- **Cuentas por Cobrar (Entrantes)**: €{ctx['total_receivable']:,.2f}\n"
            f"- **Posición Financiera Neta**: €{net_position:,.2f}\n"
            f"- **Facturas Vencidas**: {ctx['overdue_count']}\n"
            f"- **Tareas Próximas (14 Días)**: {ctx['upcoming_tasks_count']}\n"
            f"- **Artículos con Stock Bajo**: {ctx['low_stock_count']}\n\n"
            f"*Consúlteme cualquier detalle, por ejemplo: '¿Qué facturas vencen esta semana?', 'Mostrar productos con stock bajo' o 'Resumen de contratos'.*"
        )
    elif lang == 'nl':
        return (
            f"### 📊 Financieel & Operationeel Overzicht\n\n"
            f"- **Te Betalen Crediteuren (Schulden)**: €{ctx['total_payable']:,.2f}\n"
            f"- **Verwachte Debiteuren (Vorderingen)**: €{ctx['total_receivable']:,.2f}\n"
            f"- **Netto Kasstroompositie**: €{net_position:,.2f}\n"
            f"- **Vervallen Facturen**: {ctx['overdue_count']}\n"
            f"- **Komende Taken (14 Dagen)**: {ctx['upcoming_tasks_count']}\n"
            f"- **Artikelen met Lage Voorraad**: {ctx['low_stock_count']}\n\n"
            f"*Stel een vraag, zoals: 'Welke facturen vervallen deze week?', 'Toon voorraadwaarschuwingen' of 'Vat contracten samen'.*"
        )
    elif lang == 'fr':
        return (
            f"### 📊 Synthèse Financière & Opérationnelle\n\n"
            f"- **Dettes Fournisseurs (À Payer)** : €{ctx['total_payable']:,.2f}\n"
            f"- **Créances Clients (À Recevoir)** : €{ctx['total_receivable']:,.2f}\n"
            f"- **Position de Trésorerie Nette** : €{net_position:,.2f}\n"
            f"- **Factures en Retard** : {ctx['overdue_count']}\n"
            f"- **Tâches à Venir (14 Jours)** : {ctx['upcoming_tasks_count']}\n"
            f"- **Articles en Rupture Proche** : {ctx['low_stock_count']}\n\n"
            f"*Posez-moi une question telle que : 'Quelles factures arrivent à échéance ?', 'Afficher les stocks bas' ou 'Résumé des contrats'.*"
        )
    elif lang == 'pt':
        return (
            f"### 📊 Resumo Financeiro e Operacional\n\n"
            f"- **Contas a Pagar (Fornecedores)**: €{ctx['total_payable']:,.2f}\n"
            f"- **Contas a Receber (Clientes)**: €{ctx['total_receivable']:,.2f}\n"
            f"- **Posição Líquida de Caixa**: €{net_position:,.2f}\n"
            f"- **Faturas Vencidas**: {ctx['overdue_count']}\n"
            f"- **Tarefas Próximas (14 Dias)**: {ctx['upcoming_tasks_count']}\n"
            f"- **Artigos com Stock Baixo**: {ctx['low_stock_count']}\n\n"
            f"*Pergunte-me qualquer questão, como: 'Quais faturas vencem esta semana?', 'Mostrar produtos com pouco stock' ou 'Resumo de contratos'.*"
        )
    elif lang == 'zh_Hans':
        return (
            f"### 📊 企业财务与综合运营摘要\n\n"
            f"- **待付应付账款 (应付)**: €{ctx['total_payable']:,.2f}\n"
            f"- **预期应收账款 (应收)**: €{ctx['total_receivable']:,.2f}\n"
            f"- **预计净头寸**: €{net_position:,.2f}\n"
            f"- **逾期账单数量**: {ctx['overdue_count']}\n"
            f"- **近期日程任务 (14天)**: {ctx['upcoming_tasks_count']}\n"
            f"- **低库存预警品类数**: {ctx['low_stock_count']}\n\n"
            f"*您可以随时提问，例如: '本周有哪些账单到期？'、'展示低库存商品' 或 '概括当前商务合同'。*"
        )
    elif lang == 'ja':
        return (
            f"### 📊 企業財務・業務運用サマリー\n\n"
            f"- **買掛金・未払債務 (支払)**: €{ctx['total_payable']:,.2f}\n"
            f"- **売掛金・回収予定 (入金)**: €{ctx['total_receivable']:,.2f}\n"
            f"- **予測純キャッシュポジション**: €{net_position:,.2f}\n"
            f"- **期日超過請求書数**: {ctx['overdue_count']}\n"
            f"- **直近14日間のタスク数**: {ctx['upcoming_tasks_count']}\n"
            f"- **在庫僅少品目数**: {ctx['low_stock_count']}\n\n"
            f"*「今週期限の支払いは？」「在庫僅少の品目を表示して」「契約サマリーを見せて」など、自然言語でお尋ねください。*"
        )
    else:
        net_label = "positive surplus" if net_position >= 0 else "payable deficit"
        return (
            f"### 📊 Company Financial & Operational Summary\n\n"
            f"- **Outstanding Payables (We Owe)**: €{ctx['total_payable']:,.2f}\n"
            f"- **Expected Receivables (Incoming)**: €{ctx['total_receivable']:,.2f}\n"
            f"- **Net Cashflow Position**: €{net_position:,.2f} ({net_label})\n"
            f"- **Overdue Invoices**: {ctx['overdue_count']}\n"
            f"- **Upcoming Tasks (14 Days)**: {ctx['upcoming_tasks_count']}\n"
            f"- **Low Stock Inventory Items**: {ctx['low_stock_count']}\n\n"
            f"*Ask me anything specific, such as 'What bills are due this week?', 'Show low stock products', or 'Summarize our contracts'.*"
        )
