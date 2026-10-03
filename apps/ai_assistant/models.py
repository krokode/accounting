from django.db import models
from django.utils.translation import gettext_lazy as _


class Conversation(models.Model):
    session_id = models.CharField(max_length=64, unique=True, db_index=True)
    title = models.CharField(max_length=255, default="New Consultation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class ChatMessage(models.Model):
    class Role(models.TextChoices):
        USER = 'user', _('User')
        ASSISTANT = 'assistant', _('Assistant')
        SYSTEM = 'system', _('System')

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=16, choices=Role.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.role}] {self.content[:40]}..."


class AISetting(models.Model):
    class Provider(models.TextChoices):
        GEMINI = 'gemini', _('Google Gemini')
        OPENAI = 'openai', _('OpenAI / ChatGPT')
        CLAUDE = 'claude', _('Anthropic Claude')
        DEEPSEEK = 'deepseek', _('DeepSeek')
        QWEN = 'qwen', _('Alibaba Qwen (通义千问)')
        CUSTOM = 'custom', _('Custom / Local (Ollama)')

    active_provider = models.CharField(
        max_length=32,
        choices=Provider.choices,
        default=Provider.GEMINI,
        help_text=_("Currently active AI model provider.")
    )

    # Provider specific credentials & overrides
    gemini_api_key = models.CharField(max_length=255, blank=True)
    gemini_model = models.CharField(max_length=64, blank=True, default='gemini-2.5-flash')

    openai_api_key = models.CharField(max_length=255, blank=True)
    openai_model = models.CharField(max_length=64, blank=True, default='gpt-4o')
    openai_base_url = models.CharField(max_length=255, blank=True, default='https://api.openai.com/v1')

    claude_api_key = models.CharField(max_length=255, blank=True)
    claude_model = models.CharField(max_length=64, blank=True, default='claude-3-7-sonnet-20250219')
    claude_base_url = models.CharField(max_length=255, blank=True, default='https://api.anthropic.com')

    deepseek_api_key = models.CharField(max_length=255, blank=True)
    deepseek_model = models.CharField(max_length=64, blank=True, default='deepseek-chat')
    deepseek_base_url = models.CharField(max_length=255, blank=True, default='https://api.deepseek.com')

    qwen_api_key = models.CharField(max_length=255, blank=True)
    qwen_model = models.CharField(max_length=64, blank=True, default='qwen-plus')
    qwen_base_url = models.CharField(max_length=255, blank=True, default='https://dashscope-intl.aliyuncs.com/compatible-mode/v1')

    custom_api_key = models.CharField(max_length=255, blank=True)
    custom_model = models.CharField(max_length=64, blank=True, default='llama3.3')
    custom_base_url = models.CharField(max_length=255, blank=True, default='http://localhost:11434/v1')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("AI Configuration")
        verbose_name_plural = _("AI Configurations")

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    def get_provider_instance(self):
        from apps.ai_assistant.providers.registry import get_provider
        p = (self.active_provider or 'gemini').lower()
        if p == 'gemini':
            return get_provider('gemini', api_key=self.gemini_api_key, model=self.gemini_model)
        elif p == 'openai':
            return get_provider('openai', api_key=self.openai_api_key, model=self.openai_model, base_url=self.openai_base_url)
        elif p == 'claude':
            return get_provider('claude', api_key=self.claude_api_key, model=self.claude_model, base_url=self.claude_base_url)
        elif p == 'deepseek':
            return get_provider('deepseek', api_key=self.deepseek_api_key, model=self.deepseek_model, base_url=self.deepseek_base_url)
        elif p == 'qwen':
            return get_provider('qwen', api_key=self.qwen_api_key, model=self.qwen_model, base_url=self.qwen_base_url)
        elif p == 'custom':
            return get_provider('custom', api_key=self.custom_api_key, model=self.custom_model, base_url=self.custom_base_url)
        return get_provider('gemini')
