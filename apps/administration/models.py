from django.db import models
from django.utils.translation import gettext_lazy as _


class Counterparty(models.Model):
    class TypeChoices(models.TextChoices):
        VENDOR = 'VENDOR', _('Vendor / Supplier')
        CUSTOMER = 'CUSTOMER', _('Customer / Client')
        PARTNER = 'PARTNER', _('Business Partner')
        CARRIER = 'CARRIER', _('Logistics / Carrier')
        FINANCIAL = 'FINANCIAL', _('Bank / Financial Institution')

    name = models.CharField(max_length=255, db_index=True)
    counterparty_type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
        default=TypeChoices.VENDOR
    )
    tax_id = models.CharField(max_length=64, blank=True, help_text="Tax / VAT / EIN Number")
    registration_number = models.CharField(max_length=64, blank=True, help_text="Company Registry No.")
    iban = models.CharField(max_length=64, blank=True, help_text="Bank Account IBAN")
    bank_name = models.CharField(max_length=128, blank=True)
    swift_bic = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=64, blank=True)
    address = models.TextField(blank=True)
    default_payment_terms_days = models.PositiveIntegerField(
        default=14,
        help_text="Standard payment terms in days (e.g. 14, 30)"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Counterparty'
        verbose_name_plural = 'Counterparties'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_counterparty_type_display()})"


class Contract(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        ACTIVE = 'ACTIVE', _('Active')
        PENDING_RENEWAL = 'PENDING_RENEWAL', _('Pending Renewal')
        EXPIRED = 'EXPIRED', _('Expired')
        TERMINATED = 'TERMINATED', _('Terminated')

    title = models.CharField(max_length=255)
    contract_number = models.CharField(max_length=128, blank=True, db_index=True)
    counterparty = models.ForeignKey(
        Counterparty,
        on_delete=models.CASCADE,
        related_name='contracts'
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True, help_text="Expiration or renewal deadline")
    auto_renew = models.BooleanField(default=False)
    renewal_notice_period_days = models.PositiveIntegerField(
        default=30,
        help_text="Days before expiration to take renewal decision"
    )
    total_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=8, default='EUR')
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )
    key_terms_summary = models.TextField(blank=True, help_text="AI or user summarized terms and clauses")
    source_document = models.ForeignKey(
        'documents.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_contracts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-end_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.counterparty.name} ({self.status})"


class CompanyProfile(models.Model):
    legal_name = models.CharField(
        max_length=255,
        default="Sole Enterprise Group Ltd",
        verbose_name=_("Legal Entity Name"),
        help_text=_("Official registered corporate name")
    )
    trade_name = models.CharField(
        max_length=255,
        blank=True,
        default="Sole Enterprise",
        verbose_name=_("Trade / Commercial Name"),
        help_text=_("Public-facing business name if different from legal name")
    )
    tax_id = models.CharField(
        max_length=64,
        blank=True,
        default="DE982341902",
        verbose_name=_("Tax / VAT ID"),
        help_text=_("VAT number, EIN, or national tax identifier")
    )
    registration_number = models.CharField(
        max_length=64,
        blank=True,
        default="HRB 88392 B",
        verbose_name=_("Company Registry No."),
        help_text=_("Commercial register number / CRN")
    )
    iban = models.CharField(
        max_length=64,
        blank=True,
        default="DE44500105178823901234",
        verbose_name=_("Primary Bank IBAN"),
        help_text=_("Default bank account for receiving customer payments")
    )
    bank_name = models.CharField(
        max_length=128,
        blank=True,
        default="Commerzbank AG",
        verbose_name=_("Bank Name")
    )
    swift_bic = models.CharField(
        max_length=32,
        blank=True,
        default="COBADEFFXXX",
        verbose_name=_("SWIFT / BIC Code")
    )
    email = models.EmailField(
        blank=True,
        default="accounting@sole-enterprise.io",
        verbose_name=_("Accounting / Finance Email")
    )
    phone = models.CharField(
        max_length=64,
        blank=True,
        default="+49 30 987654",
        verbose_name=_("Phone Number")
    )
    address = models.TextField(
        blank=True,
        default="Potsdamer Platz 1, 10785 Berlin, Germany",
        verbose_name=_("Registered Address")
    )
    currency = models.CharField(
        max_length=8,
        default="EUR",
        verbose_name=_("Functional Currency"),
        help_text=_("Base currency code (e.g. EUR, USD, GBP)")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Company Profile')
        verbose_name_plural = _('Company Profile')

    def __str__(self):
        return self.trade_name or self.legal_name

    @classmethod
    def get_solo(cls):
        profile = cls.objects.first()
        if not profile:
            profile = cls.objects.create(
                legal_name="Sole Enterprise Group Ltd",
                trade_name="Sole Enterprise",
                tax_id="DE982341902",
                registration_number="HRB 88392 B",
                iban="DE44500105178823901234",
                bank_name="Commerzbank AG",
                swift_bic="COBADEFFXXX",
                email="accounting@sole-enterprise.io",
                phone="+49 30 987654",
                address="Potsdamer Platz 1, 10785 Berlin, Germany",
                currency="EUR"
            )
        return profile

