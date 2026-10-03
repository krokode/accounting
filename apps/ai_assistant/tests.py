from io import StringIO
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import translation

from apps.ai_assistant.models import AISetting
from apps.ai_assistant.providers.registry import get_provider, get_active_provider, list_providers
from apps.ai_assistant.providers.exceptions import (
    AIConfigurationError,
    AIRateLimitError,
    AIOfflineError,
    AIAuthenticationError,
)
from apps.ai_assistant.services.copilot_engine import query_copilot


class MultiLLMProviderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Reset settings
        setting = AISetting.get_settings()
        setting.active_provider = 'gemini'
        setting.gemini_api_key = ''
        setting.openai_api_key = ''
        setting.save()

    def test_provider_registry_listing(self):
        providers = list_providers()
        self.assertEqual(len(providers), 6)
        provider_ids = [p['id'] for p in providers]
        self.assertIn('gemini', provider_ids)
        self.assertIn('openai', provider_ids)
        self.assertIn('claude', provider_ids)
        self.assertIn('deepseek', provider_ids)
        self.assertIn('qwen', provider_ids)
        self.assertIn('custom', provider_ids)

    def test_ai_setting_singleton(self):
        s1 = AISetting.get_settings()
        s2 = AISetting.get_settings()
        self.assertEqual(s1.pk, s2.pk)
        self.assertEqual(AISetting.objects.count(), 1)

    def test_missing_api_key_raises_configuration_error(self):
        prov = get_provider('openai', api_key='', model='gpt-4o')
        with self.assertRaises(AIConfigurationError) as ctx:
            prov.validate_configuration()
        self.assertIn("OpenAI / ChatGPT", str(ctx.exception))

    def test_custom_provider_does_not_require_api_key(self):
        prov = get_provider('custom', api_key='', model='llama3.3', base_url='http://localhost:11434/v1')
        # Custom provider should validate successfully without API key
        prov.validate_configuration()
        self.assertEqual(prov.model, 'llama3.3')

    def test_multilingual_exception_messages(self):
        # Russian
        with translation.override('ru'):
            err_ru = AIConfigurationError(provider='DeepSeek')
            self.assertIn("API-ключ для DeepSeek не настроен", str(err_ru))

            rate_ru = AIRateLimitError(provider='OpenAI')
            self.assertIn("Превышен лимит запросов", str(rate_ru))

            offline_ru = AIOfflineError(provider='Claude', endpoint='https://api.anthropic.com')
            self.assertIn("Не удалось подключиться к Claude", str(offline_ru))

        # Chinese
        with translation.override('zh-hans'):
            err_zh = AIConfigurationError(provider='DeepSeek')
            self.assertIn("DeepSeek 的 API 密钥尚未配置", str(err_zh))

            rate_zh = AIRateLimitError(provider='OpenAI')
            self.assertIn("请求频率超限或配额已耗尽", str(rate_zh))

        # Spanish
        with translation.override('es'):
            err_es = AIConfigurationError(provider='DeepSeek')
            self.assertIn("La clave API para DeepSeek no está configurada", str(err_es))

        # Japanese
        with translation.override('ja'):
            err_ja = AIConfigurationError(provider='DeepSeek')
            self.assertIn("DeepSeek の API キーが設定されていません", str(err_ja))

    def test_ai_settings_web_views(self):
        url = reverse('ai_assistant:settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Google Gemini")
        self.assertContains(response, "DeepSeek")
        self.assertContains(response, "Alibaba Qwen")

        # Test POST
        post_response = self.client.post(url, {
            'active_provider': 'deepseek',
            'deepseek_api_key': 'test-post-key',
            'deepseek_model': 'deepseek-chat',
            'deepseek_base_url': 'https://api.deepseek.com'
        })
        self.assertEqual(post_response.status_code, 302)
        setting = AISetting.get_settings()
        self.assertEqual(setting.active_provider, 'deepseek')
        self.assertEqual(setting.deepseek_api_key, 'test-post-key')

    def test_test_connection_api_missing_key(self):
        url = reverse('ai_assistant:test_connection')
        response = self.client.post(url, {
            'provider': 'openai',
            'api_key': '',
            'model': 'gpt-4o'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error")

    def test_copilot_engine_missing_key_callout(self):
        setting = AISetting.get_settings()
        setting.active_provider = 'openai'
        setting.openai_api_key = ''
        setting.save()

        # Copilot must return diagnostic callout informing user to configure key, NOT silent rule fallback
        answer = query_copilot("What bills are due this week?")
        self.assertIn("AI Configuration Required", answer)
        self.assertIn("/assistant/settings/", answer)

    def test_configure_llm_command_list(self):
        out = StringIO()
        call_command('configure_llm', '--list', stdout=out)
        output = out.getvalue()
        self.assertIn("Google Gemini", output)
        self.assertIn("DeepSeek", output)
        self.assertIn("OpenAI / ChatGPT", output)

    def test_configure_llm_command_scripted(self):
        out = StringIO()
        call_command(
            'configure_llm',
            '--provider', 'claude',
            '--api-key', 'sk-ant-test-key-999',
            '--model', 'claude-3-7-sonnet-20250219',
            '--non-interactive',
            stdout=out
        )
        self.assertIn("Successfully configured active provider: claude", out.getvalue())
        setting = AISetting.get_settings()
        self.assertEqual(setting.active_provider, 'claude')
        self.assertEqual(setting.claude_api_key, 'sk-ant-test-key-999')
