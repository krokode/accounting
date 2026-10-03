import re
from django.db import models
from django.utils.translation import gettext as _, gettext_lazy as _lazy


class Notification(models.Model):
    class Level(models.TextChoices):
        INFO = 'INFO', _lazy('Info')
        WARNING = 'WARNING', _lazy('Warning')
        CRITICAL = 'CRITICAL', _lazy('Critical / Urgent')
        SUCCESS = 'SUCCESS', _lazy('Success')

    class Category(models.TextChoices):
        PAYMENT_DUE = 'PAYMENT_DUE', _lazy('Upcoming Payment Due')
        PAYMENT_OVERDUE = 'PAYMENT_OVERDUE', _lazy('Overdue Payment')
        CONTRACT_RENEWAL = 'CONTRACT_RENEWAL', _lazy('Contract Renewal')
        CONSIGNMENT_DELIVERY = 'CONSIGNMENT_DELIVERY', _lazy('Consignment Delivery')
        STOCK_ALERT = 'STOCK_ALERT', _lazy('Low Stock Alert')
        DOCUMENT_PROCESSED = 'DOCUMENT_PROCESSED', _lazy('Document Analyzed')
        GENERAL = 'GENERAL', _lazy('General Alert')

    title = models.CharField(max_length=255)
    message = models.TextField()
    level = models.CharField(max_length=16, choices=Level.choices, default=Level.INFO)
    category = models.CharField(max_length=32, choices=Category.choices, default=Category.GENERAL)
    action_url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)

    related_invoice = models.ForeignKey(
        'accounting.Invoice',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    related_contract = models.ForeignKey(
        'administration.Contract',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    related_task = models.ForeignKey(
        'calendar_tasks.CalendarTask',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.level}] {self.display_title} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def display_title(self) -> str:
        if not self.title:
            return ""

        translated = _(self.title)
        if translated != self.title:
            return str(translated)

        # Pattern 1: New <doc_type> Processed
        m = re.match(r"^New\s+(.*?)\s+Processed$", self.title)
        if m:
            doc_type_raw = m.group(1).strip()
            doc_type_trans = _(doc_type_raw)
            return str(_("New %(doc_type)s Processed") % {'doc_type': doc_type_trans})

        # Pattern 2: Low Stock Alert: <product>
        m = re.match(r"^Low Stock Alert:\s*(.*)$", self.title)
        if m:
            prod = m.group(1).strip()
            return str(_("Low Stock Alert: %(product)s") % {'product': prod})

        # Pattern 3: OVERDUE: <kind> #<num>
        m = re.match(r"^OVERDUE:\s*(Outgoing Bill|Incoming Payment|Vendor Bill)?\s*#?\s*([A-Za-z0-9\-_]+)$", self.title)
        if m:
            kind = m.group(1) or "Outgoing Bill"
            num = m.group(2)
            kind_trans = _(kind)
            return str(_("OVERDUE: %(kind)s #%(number)s") % {'kind': kind_trans, 'number': num})

        # Pattern 4: Payment Due in <N> day(s): #<num>
        m = re.match(r"^Payment Due in\s+(\d+)\s+day\(s\):\s*#?\s*([A-Za-z0-9\-_]+)$", self.title)
        if m:
            days = m.group(1)
            num = m.group(2)
            return str(_("Payment Due in %(days)s day(s): #%(number)s") % {'days': days, 'number': num})

        # Pattern 5: Payment Due TODAY: #<num>
        m = re.match(r"^Payment Due TODAY:\s*#?\s*([A-Za-z0-9\-_]+)$", self.title)
        if m:
            num = m.group(1)
            return str(_("Payment Due TODAY: #%(number)s") % {'number': num})

        # Pattern 6: Contract Renewal Decision: <counterparty>
        m = re.match(r"^Contract Renewal Decision:\s*(.*)$", self.title)
        if m:
            cp = m.group(1).strip()
            return str(_("Contract Renewal Decision: %(counterparty)s") % {'counterparty': cp})

        # Pattern 7: Consignment Delivery Expected: #<num>
        m = re.match(r"^Consignment Delivery Expected:\s*#?\s*([A-Za-z0-9\-_]+)$", self.title)
        if m:
            num = m.group(1)
            return str(_("Consignment Delivery Expected: #%(number)s") % {'number': num})

        return self.title

    @property
    def display_message(self) -> str:
        if not self.message:
            return ""

        translated = _(self.message)
        if translated != self.message:
            return str(translated)

        # Message Pattern 1: confirmed and scheduled into calendar
        m = re.match(r"^(.*?)\s*-\s*#?(.*?)\s+confirmed and scheduled into calendar\.$", self.message)
        if m:
            return str(_("%(counterparty)s - #%(number)s confirmed and scheduled into calendar.") % {
                'counterparty': m.group(1).strip(),
                'number': m.group(2).strip()
            })

        # Message Pattern 2: We owe ... Due date was ... (N days ago)
        m = re.match(r"^We owe\s+(.*?)\s+([\d\.,]+)\s+([A-Za-z]{3})\.\s+Due date was\s+([\d\-]+)\s+\((\d+)\s+days ago\)\.$", self.message)
        if m:
            return str(_("We owe %(counterparty)s %(amount)s %(currency)s. Due date was %(date)s (%(days)s days ago).") % {
                'counterparty': m.group(1).strip(),
                'amount': m.group(2).strip(),
                'currency': m.group(3).strip(),
                'date': m.group(4).strip(),
                'days': m.group(5).strip()
            })

        # Message Pattern 3: Expected from ... Due date was ... (N days ago)
        m = re.match(r"^Expected from\s+(.*?)\s+([\d\.,]+)\s+([A-Za-z]{3})\.\s+Due date was\s+([\d\-]+)\s+\((\d+)\s+days ago\)\.$", self.message)
        if m:
            return str(_("Expected from %(counterparty)s %(amount)s %(currency)s. Due date was %(date)s (%(days)s days ago).") % {
                'counterparty': m.group(1).strip(),
                'amount': m.group(2).strip(),
                'currency': m.group(3).strip(),
                'date': m.group(4).strip(),
                'days': m.group(5).strip()
            })

        # Message Pattern 4: Scheduled payment to ... for ... on ...
        m = re.match(r"^Scheduled payment to\s+(.*?)\s+for\s+([\d\.,]+)\s+([A-Za-z]{3})\s+on\s+([\d\-]+)\.$", self.message)
        if m:
            return str(_("Scheduled payment to %(counterparty)s for %(amount)s %(currency)s on %(date)s.") % {
                'counterparty': m.group(1).strip(),
                'amount': m.group(2).strip(),
                'currency': m.group(3).strip(),
                'date': m.group(4).strip()
            })

        # Message Pattern 5: Expected incoming payment from ... for ... on ...
        m = re.match(r"^Expected incoming payment from\s+(.*?)\s+for\s+([\d\.,]+)\s+([A-Za-z]{3})\s+on\s+([\d\-]+)\.$", self.message)
        if m:
            return str(_("Expected incoming payment from %(counterparty)s for %(amount)s %(currency)s on %(date)s.") % {
                'counterparty': m.group(1).strip(),
                'amount': m.group(2).strip(),
                'currency': m.group(3).strip(),
                'date': m.group(4).strip()
            })

        # Message Pattern 6: Stock for '...' [...] is down to ...
        m = re.match(r"^Stock for\s+'(.*?)'\s+\[(.*?)\]\s+is down to\s+([\d\.,]+)\s+(.*?)\s+\(Reorder threshold:\s+([\d\.,]+)\)\.$", self.message)
        if m:
            return str(_("Stock for '%(name)s' [%(sku)s] is down to %(qty)s %(uom)s (Reorder threshold: %(threshold)s).") % {
                'name': m.group(1).strip(),
                'sku': m.group(2).strip(),
                'qty': m.group(3).strip(),
                'uom': _(m.group(4).strip()),
                'threshold': m.group(5).strip()
            })

        # Message Pattern 7: Contract '...' expires on ... Notice deadline is ... (... days left)
        m = re.match(r"^Contract\s+'(.*?)'\s+expires on\s+([\d\-]+)\.\s+Notice deadline is\s+([\d\-]+)\s+\((\d+)\s+days left\)\.$", self.message)
        if m:
            return str(_("Contract '%(title)s' expires on %(end_date)s. Notice deadline is %(notice_date)s (%(days)s days left).") % {
                'title': m.group(1).strip(),
                'end_date': m.group(2).strip(),
                'notice_date': m.group(3).strip(),
                'days': m.group(4).strip()
            })

        # Message Pattern 8: Expected delivery from ... scheduled for ...
        m = re.match(r"^Expected delivery from\s+(.*?)\s+scheduled for\s+([\d\-]+)\.$", self.message)
        if m:
            return str(_("Expected delivery from %(counterparty)s scheduled for %(date)s.") % {
                'counterparty': m.group(1).strip(),
                'date': m.group(2).strip()
            })

        return self.message
