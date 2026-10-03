import re
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


class CalendarTask(models.Model):
    class TaskType(models.TextChoices):
        OUTGOING_PAYMENT_DUE = 'OUTGOING_PAYMENT_DUE', _('Outgoing Payment Due (Payable)')
        INCOMING_PAYMENT_EXPECTED = 'INCOMING_PAYMENT_EXPECTED', _('Expected Payment (Receivable)')
        CONTRACT_RENEWAL = 'CONTRACT_RENEWAL', _('Contract Renewal / Notice')
        CONSIGNMENT_DELIVERY = 'CONSIGNMENT_DELIVERY', _('Consignment / Delivery Due')
        ADMINISTRATIVE_TASK = 'ADMINISTRATIVE_TASK', _('Administrative Task')

    class Priority(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
        URGENT = 'URGENT', _('Urgent')

    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    task_type = models.CharField(
        max_length=32,
        choices=TaskType.choices,
        default=TaskType.ADMINISTRATIVE_TASK,
        db_index=True
    )
    due_date = models.DateField(db_index=True)
    due_time = models.TimeField(null=True, blank=True)
    priority = models.CharField(
        max_length=16,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=8, default='EUR')
    is_automated = models.BooleanField(default=True, help_text="Generated automatically by document AI")

    # Links to core entities
    linked_invoice = models.ForeignKey(
        'accounting.Invoice',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='calendar_tasks'
    )
    linked_contract = models.ForeignKey(
        'administration.Contract',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='calendar_tasks'
    )
    linked_consignment = models.ForeignKey(
        'warehouse.Consignment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='calendar_tasks'
    )
    linked_document = models.ForeignKey(
        'documents.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calendar_tasks'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', '-priority', 'title']

    def __str__(self):
        return f"[{self.get_task_type_display()}] {self.display_title} (Due: {self.due_date})"

    @property
    def display_title(self) -> str:
        if not self.title:
            return ""
        t = gettext(self.title)
        if t != self.title:
            return str(t)

        m = re.match(r"^Pay (?:Outgoing Bill|Invoice)\s*#?(.*?)\s+to\s+(.*)$", self.title)
        if m:
            return str(gettext("Pay Bill #%(number)s to %(counterparty)s") % {
                'number': m.group(1).strip(),
                'counterparty': m.group(2).strip()
            })

        m = re.match(r"^OVERDUE:\s*Pay (?:Freight Bill|Bill|Invoice)\s*#?(.*?)\s+to\s+(.*)$", self.title)
        if m:
            return str(gettext("OVERDUE: Pay Bill #%(number)s to %(counterparty)s") % {
                'number': m.group(1).strip(),
                'counterparty': m.group(2).strip()
            })

        m = re.match(r"^Expected Incoming Payment\s*#?(.*?)\s+from\s+(.*)$", self.title)
        if m:
            return str(gettext("Expected Incoming Payment #%(number)s from %(counterparty)s") % {
                'number': m.group(1).strip(),
                'counterparty': m.group(2).strip()
            })

        m = re.match(r"^Inspect Incoming Delivery\s*#?(.*?)\s+at Dock$", self.title)
        if m:
            return str(gettext("Inspect Incoming Delivery #%(number)s at Dock") % {
                'number': m.group(1).strip()
            })

        return self.title

    @property
    def color_classes(self):
        colors = {
            self.TaskType.OUTGOING_PAYMENT_DUE: {'bg': '#fee2e2', 'border': '#ef4444', 'text': '#991b1b', 'badge': 'bg-red-100 text-red-800'},
            self.TaskType.INCOMING_PAYMENT_EXPECTED: {'bg': '#dcfce7', 'border': '#22c55e', 'text': '#166534', 'badge': 'bg-green-100 text-green-800'},
            self.TaskType.CONTRACT_RENEWAL: {'bg': '#f3e8ff', 'border': '#a855f7', 'text': '#6b21a8', 'badge': 'bg-purple-100 text-purple-800'},
            self.TaskType.CONSIGNMENT_DELIVERY: {'bg': '#ffedd5', 'border': '#f97316', 'text': '#9a3412', 'badge': 'bg-orange-100 text-orange-800'},
            self.TaskType.ADMINISTRATIVE_TASK: {'bg': '#e0f2fe', 'border': '#3b82f6', 'text': '#1e40af', 'badge': 'bg-blue-100 text-blue-800'},
        }
        return colors.get(self.task_type, {'bg': '#f3f4f6', 'border': '#9ca3af', 'text': '#374151', 'badge': 'bg-gray-100 text-gray-800'})


class CalendarFeedToken(models.Model):
    name = models.CharField(max_length=128, default="Default Calendar Sync")
    token = models.CharField(max_length=64, unique=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.token[:8]}...)"
