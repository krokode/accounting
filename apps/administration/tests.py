from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import activate
from apps.administration.models import Counterparty, Contract, CompanyProfile


class CounterpartyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cp = Counterparty.objects.create(
            name="Alpha Corp",
            counterparty_type=Counterparty.TypeChoices.VENDOR,
            tax_id="VAT123456",
            iban="DE89370400440532013000",
            email="contact@alphacorp.com",
            phone="+49 30 111222",
            address="Alexanderplatz 1, Berlin",
            default_payment_terms_days=30
        )

    def test_counterparty_list_renders_table_with_edit_actions(self):
        url = reverse('administration:counterparty_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Corp")
        self.assertContains(response, "Actions")
        self.assertContains(response, "Edit")
        self.assertContains(response, f"openEdit({{")

    def test_counterparty_update_post(self):
        url = reverse('administration:counterparty_update', kwargs={'pk': self.cp.pk})
        payload = {
            'name': 'Alpha Corporation International',
            'counterparty_type': Counterparty.TypeChoices.CUSTOMER,
            'tax_id': 'VAT999888',
            'registration_number': 'HRB 98765',
            'iban': 'FR7630006000011234567890189',
            'bank_name': 'BNP Paribas',
            'swift_bic': 'BNPAFRPP',
            'email': 'billing@alphacorp.com',
            'phone': '+33 1 23456789',
            'address': '10 Rue de la Paix, Paris',
            'default_payment_terms_days': '45',
            'notes': 'Preferred client terms'
        }
        response = self.client.post(url, payload)
        self.assertRedirects(response, reverse('administration:counterparty_list'))

        self.cp.refresh_from_db()
        self.assertEqual(self.cp.name, 'Alpha Corporation International')
        self.assertEqual(self.cp.counterparty_type, Counterparty.TypeChoices.CUSTOMER)
        self.assertEqual(self.cp.tax_id, 'VAT999888')
        self.assertEqual(self.cp.registration_number, 'HRB 98765')
        self.assertEqual(self.cp.iban, 'FR7630006000011234567890189')
        self.assertEqual(self.cp.bank_name, 'BNP Paribas')
        self.assertEqual(self.cp.swift_bic, 'BNPAFRPP')
        self.assertEqual(self.cp.email, 'billing@alphacorp.com')
        self.assertEqual(self.cp.phone, '+33 1 23456789')
        self.assertEqual(self.cp.address, '10 Rue de la Paix, Paris')
        self.assertEqual(self.cp.default_payment_terms_days, 45)
        self.assertEqual(self.cp.notes, 'Preferred client terms')

    def test_counterparty_update_get_redirects(self):
        url = reverse('administration:counterparty_update', kwargs={'pk': self.cp.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('administration:counterparty_list'))

    def test_multilingual_counterparty_list(self):
        url = reverse('administration:counterparty_list')
        langs = [
            ('ru', 'Редактировать'),
            ('es', 'Editar'),
            ('nl', 'Bewerken'),
            ('fr', 'Modifier'),
            ('pt', 'Editar'),
            ('zh-hans', '编辑'),
            ('ja', '編集'),
            ('en', 'Edit'),
        ]
        for lang, expected_btn in langs:
            activate(lang)
            self.client.cookies.load({'django_language': lang})
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE=lang)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, expected_btn)


class CompanyProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = CompanyProfile.get_solo()

    def test_company_profile_singleton(self):
        profile1 = CompanyProfile.get_solo()
        profile2 = CompanyProfile.get_solo()
        self.assertEqual(profile1.pk, profile2.pk)
        self.assertEqual(CompanyProfile.objects.count(), 1)

    def test_company_profile_get_view(self):
        url = reverse('administration:company_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profile.legal_name)
        self.assertContains(response, self.profile.tax_id)

    def test_company_profile_post_update(self):
        url = reverse('administration:company_profile')
        payload = {
            'legal_name': 'Horizon Innovations Inc',
            'trade_name': 'Horizon Tech',
            'tax_id': 'US987654321',
            'registration_number': 'CRN-777888',
            'iban': 'US1234567890123456',
            'bank_name': 'JPMorgan Chase',
            'swift_bic': 'CHASUS33',
            'email': 'finance@horizon.tech',
            'phone': '+1 212 555 0199',
            'address': '350 5th Ave, New York, NY 10118',
            'currency': 'USD',
        }
        response = self.client.post(url, payload)
        self.assertRedirects(response, url)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.legal_name, 'Horizon Innovations Inc')
        self.assertEqual(self.profile.trade_name, 'Horizon Tech')
        self.assertEqual(self.profile.tax_id, 'US987654321')
        self.assertEqual(self.profile.currency, 'USD')

    def test_company_profile_context_processor(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('active_company_profile', response.context)
        self.assertEqual(response.context['active_company_profile'].pk, self.profile.pk)

    def test_multilingual_company_profile(self):
        url = reverse('administration:company_profile')
        langs = [
            ('ru', 'Профиль компании'),
            ('es', 'Perfil de la empresa'),
            ('nl', 'Bedrijfsprofiel'),
            ('fr', "Profil de l'entreprise"),
            ('pt', 'Perfil da empresa'),
            ('zh-hans', '企业资料'),
            ('ja', '会社概要'),
            ('en', 'Company Profile'),
        ]
        for lang, expected_text in langs:
            activate(lang)
            self.client.cookies.load({'django_language': lang})
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE=lang)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, expected_text)


