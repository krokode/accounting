from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from apps.ai_assistant.models import AISetting
from apps.ai_assistant.providers.registry import get_provider, list_providers
from apps.ai_assistant.services.copilot_engine import query_copilot
from apps.ai_assistant.utils_env import update_env_variables


def ai_settings_view(request):
    """Configuration view for managing multi-LLM providers and credentials."""
    setting = AISetting.get_settings()

    if request.method == 'POST':
        provider = request.POST.get('active_provider', 'gemini').lower()
        setting.active_provider = provider

        # Map form fields
        setting.gemini_api_key = request.POST.get('gemini_api_key', '').strip() or setting.gemini_api_key
        setting.gemini_model = request.POST.get('gemini_model', '').strip() or 'gemini-2.5-flash'

        setting.openai_api_key = request.POST.get('openai_api_key', '').strip() or setting.openai_api_key
        setting.openai_model = request.POST.get('openai_model', '').strip() or 'gpt-4o'
        setting.openai_base_url = request.POST.get('openai_base_url', '').strip() or 'https://api.openai.com/v1'

        setting.claude_api_key = request.POST.get('claude_api_key', '').strip() or setting.claude_api_key
        setting.claude_model = request.POST.get('claude_model', '').strip() or 'claude-3-7-sonnet-20250219'
        setting.claude_base_url = request.POST.get('claude_base_url', '').strip() or 'https://api.anthropic.com'

        setting.deepseek_api_key = request.POST.get('deepseek_api_key', '').strip() or setting.deepseek_api_key
        setting.deepseek_model = request.POST.get('deepseek_model', '').strip() or 'deepseek-chat'
        setting.deepseek_base_url = request.POST.get('deepseek_base_url', '').strip() or 'https://api.deepseek.com'

        setting.qwen_api_key = request.POST.get('qwen_api_key', '').strip() or setting.qwen_api_key
        setting.qwen_model = request.POST.get('qwen_model', '').strip() or 'qwen-plus'
        setting.qwen_base_url = request.POST.get('qwen_base_url', '').strip() or 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'

        setting.custom_api_key = request.POST.get('custom_api_key', '').strip()
        setting.custom_model = request.POST.get('custom_model', '').strip() or 'llama3.3'
        setting.custom_base_url = request.POST.get('custom_base_url', '').strip() or 'http://localhost:11434/v1'

        setting.save()

        # Sync to .env
        env_updates = {
            'LLM_PROVIDER': setting.active_provider,
            'GEMINI_API_KEY': setting.gemini_api_key,
            'GEMINI_MODEL': setting.gemini_model,
            'OPENAI_API_KEY': setting.openai_api_key,
            'OPENAI_MODEL': setting.openai_model,
            'OPENAI_BASE_URL': setting.openai_base_url,
            'ANTHROPIC_API_KEY': setting.claude_api_key,
            'ANTHROPIC_MODEL': setting.claude_model,
            'ANTHROPIC_BASE_URL': setting.claude_base_url,
            'DEEPSEEK_API_KEY': setting.deepseek_api_key,
            'DEEPSEEK_MODEL': setting.deepseek_model,
            'DEEPSEEK_BASE_URL': setting.deepseek_base_url,
            'QWEN_API_KEY': setting.qwen_api_key,
            'QWEN_MODEL': setting.qwen_model,
            'QWEN_BASE_URL': setting.qwen_base_url,
            'CUSTOM_API_KEY': setting.custom_api_key,
            'CUSTOM_MODEL': setting.custom_model,
            'CUSTOM_BASE_URL': setting.custom_base_url,
        }
        update_env_variables(env_updates)

        messages.success(request, _("AI configuration and active provider updated successfully!"))
        return redirect('ai_assistant:settings')

    providers = list_providers()
    context = {
        'setting': setting,
        'providers': providers,
    }
    return render(request, 'ai_assistant/settings.html', context)


@require_POST
def test_connection_api(request):
    """Tests connectivity to a specific provider."""
    provider_name = request.POST.get('provider', '').lower().strip()
    api_key = request.POST.get('api_key', '').strip()
    model = request.POST.get('model', '').strip()
    base_url = request.POST.get('base_url', '').strip()

    setting = AISetting.get_settings()

    # If field is blank in test, fall back to current saved setting
    if not api_key:
        if provider_name == 'gemini':
            api_key = setting.gemini_api_key
        elif provider_name == 'openai':
            api_key = setting.openai_api_key
        elif provider_name == 'claude':
            api_key = setting.claude_api_key
        elif provider_name == 'deepseek':
            api_key = setting.deepseek_api_key
        elif provider_name == 'qwen':
            api_key = setting.qwen_api_key
        elif provider_name == 'custom':
            api_key = setting.custom_api_key

    try:
        provider_instance = get_provider(
            provider_name=provider_name,
            api_key=api_key,
            model=model or None,
            base_url=base_url or None
        )
        success, message = provider_instance.test_connection()
    except Exception as e:
        success = False
        message = str(e)

    # Return HTMX badge fragment
    if success:
        html = f"""
        <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold">
            <i class="fa-solid fa-circle-check text-emerald-600"></i>
            <span>{_('Success')}: {message}</span>
        </div>
        """
    else:
        html = f"""
        <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-red-50 border border-red-200 text-red-800 text-xs font-medium">
            <i class="fa-solid fa-circle-xmark text-red-600"></i>
            <span>{_('Error')}: {message}</span>
        </div>
        """
    return HttpResponse(html)


@require_POST
def chat_api(request):
    prompt = request.POST.get('prompt', '').strip()
    if not prompt:
        return HttpResponse("")

    response_text = query_copilot(prompt)

    context = {
        'prompt': prompt,
        'response_text': response_text,
    }
    return render(request, 'ai_assistant/chat_message_fragment.html', context)
