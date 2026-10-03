"""
Central LLM Provider Registry and Dynamic Factory.
"""
import logging
import os
from typing import Dict, List, Optional, Type
from django.conf import settings

from apps.ai_assistant.providers.base import BaseLLMProvider
from apps.ai_assistant.providers.gemini_provider import GeminiProvider
from apps.ai_assistant.providers.openai_provider import OpenAIProvider
from apps.ai_assistant.providers.claude_provider import ClaudeProvider
from apps.ai_assistant.providers.deepseek_provider import DeepSeekProvider
from apps.ai_assistant.providers.qwen_provider import QwenProvider
from apps.ai_assistant.providers.custom_provider import CustomProvider
from apps.ai_assistant.providers.exceptions import AIConfigurationError

logger = logging.getLogger(__name__)

PROVIDER_CLASSES: Dict[str, Type[BaseLLMProvider]] = {
    'gemini': GeminiProvider,
    'openai': OpenAIProvider,
    'claude': ClaudeProvider,
    'deepseek': DeepSeekProvider,
    'qwen': QwenProvider,
    'custom': CustomProvider,
}

PROVIDER_ENV_MAPPINGS = {
    'gemini': {
        'api_key': 'GEMINI_API_KEY',
        'model': 'GEMINI_MODEL',
        'base_url': 'GEMINI_BASE_URL',
    },
    'openai': {
        'api_key': 'OPENAI_API_KEY',
        'model': 'OPENAI_MODEL',
        'base_url': 'OPENAI_BASE_URL',
    },
    'claude': {
        'api_key': 'ANTHROPIC_API_KEY',
        'model': 'ANTHROPIC_MODEL',
        'base_url': 'ANTHROPIC_BASE_URL',
    },
    'deepseek': {
        'api_key': 'DEEPSEEK_API_KEY',
        'model': 'DEEPSEEK_MODEL',
        'base_url': 'DEEPSEEK_BASE_URL',
    },
    'qwen': {
        'api_key': 'QWEN_API_KEY',
        'model': 'QWEN_MODEL',
        'base_url': 'QWEN_BASE_URL',
    },
    'custom': {
        'api_key': 'CUSTOM_API_KEY',
        'model': 'CUSTOM_MODEL',
        'base_url': 'CUSTOM_BASE_URL',
    },
}


def get_provider(
    provider_name: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None
) -> BaseLLMProvider:
    """Instantiates a provider instance with explicit or fallback configuration."""
    provider_name = (provider_name or 'gemini').lower().strip()
    cls = PROVIDER_CLASSES.get(provider_name)
    if not cls:
        raise AIConfigurationError(provider=provider_name, details=f"Unknown AI provider '{provider_name}'")

    mapping = PROVIDER_ENV_MAPPINGS.get(provider_name, {})

    resolved_key = api_key if api_key is not None else getattr(settings, mapping.get('api_key', ''), '') or os.getenv(mapping.get('api_key', ''), '')
    resolved_model = model if model is not None else getattr(settings, mapping.get('model', ''), '') or os.getenv(mapping.get('model', ''), '')
    resolved_url = base_url if base_url is not None else getattr(settings, mapping.get('base_url', ''), '') or os.getenv(mapping.get('base_url', ''), '')

    return cls(
        api_key=resolved_key or "",
        model=resolved_model or "",
        base_url=resolved_url or ""
    )


def get_active_provider() -> BaseLLMProvider:
    """
    Retrieves the currently configured active LLM provider.
    Checks the database AISetting singleton first, then falls back to Django settings and .env.
    """
    try:
        from apps.ai_assistant.models import AISetting
        setting = AISetting.get_settings()
        if setting and setting.active_provider:
            return setting.get_provider_instance()
    except Exception as e:
        logger.debug(f"Could not load AISetting from DB (possibly during migration): {e}")

    active_name = getattr(settings, 'LLM_PROVIDER', '') or os.getenv('LLM_PROVIDER', 'gemini')
    return get_provider(active_name)


def mask_key(key: str) -> str:
    """Masks an API key for safe display in UI/CLI."""
    if not key:
        return ""
    if len(key) <= 8:
        return "***"
    return f"{key[:4]}...{key[-4:]}"


def list_providers() -> List[dict]:
    """Returns metadata for all available providers."""
    active_prov = get_active_provider()
    result = []
    for pid, cls in PROVIDER_CLASSES.items():
        prov = get_provider(pid)
        is_active = (prov.name == active_prov.name)
        is_configured = bool(prov.api_key or pid == 'custom')
        result.append({
            'id': pid,
            'name': prov.display_name,
            'default_model': prov.default_model,
            'current_model': prov.model,
            'default_base_url': prov.default_base_url,
            'current_base_url': prov.base_url,
            'is_vision_supported': prov.is_vision_supported,
            'is_active': is_active,
            'is_configured': is_configured,
            'api_key_masked': mask_key(prov.api_key),
        })
    return result
