"""
Interactive & Scripted Multi-LLM Provider Configuration Command.
Supports 8 languages (EN, RU, ES, NL, FR, PT, ZH, JA), live connectivity testing,
and automatic synchronization with .env and database.
"""
import sys
from django.core.management.base import BaseCommand
from apps.ai_assistant.models import AISetting
from apps.ai_assistant.providers.registry import (
    PROVIDER_CLASSES,
    get_provider,
    get_active_provider,
    list_providers,
    mask_key,
)
from apps.ai_assistant.utils_env import update_env_variables

# Multilingual strings for CLI setup wizard across 8 languages
CLI_TRANSLATIONS = {
    'en': {
        'title': "Sole Enterprise Orchestrator - AI Model Setup Wizard",
        'subtitle': "Configure LLM Provider for Document Extraction & Copilot",
        'lang_selected': "Language: English",
        'current_active': "Current Active Provider",
        'select_provider': "Select an AI Provider to Configure & Activate:",
        'provider_options': [
            ("[1] Google Gemini", "gemini", "Multimodal PDF/image extraction (gemini-2.5-flash)"),
            ("[2] OpenAI / ChatGPT", "openai", "GPT-4o, GPT-4o-mini structured analysis"),
            ("[3] Anthropic Claude", "claude", "Claude 3.7 Sonnet, Claude 3.5 Haiku"),
            ("[4] DeepSeek", "deepseek", "Cost-effective deep reasoning (deepseek-chat)"),
            ("[5] Alibaba Qwen", "qwen", "Enterprise DashScope models (qwen-plus, qwen-vl)"),
            ("[6] Custom / Local", "custom", "100% private on-premise Ollama / vLLM / OpenRouter"),
        ],
        'cancel': "[0] Cancel / Keep Current Settings",
        'prompt_choice': "Enter your choice (0-6): ",
        'prompt_api_key': "Enter API Key",
        'press_enter_keep': "Press Enter to keep current",
        'optional_ollama': "Optional for local Ollama",
        'prompt_model': "Model name",
        'prompt_base_url': "Endpoint Base URL",
        'test_connection_prompt': "Would you like to test connection now? [Y/n]: ",
        'testing': "Testing connection to {provider} ({model})...",
        'test_success': "SUCCESS: Connection verified! Latency: {latency}",
        'test_failed': "FAILED: {error}",
        'save_prompt': "Save this configuration as active provider? [Y/n]: ",
        'saved_success': "SUCCESS: Provider '{provider}' activated and saved to .env & database!",
        'cancelled': "Operation cancelled. Settings were not modified.",
        'list_header': "Registered AI Providers Status:",
    },
    'ru': {
        'title': "Sole Enterprise Orchestrator - Мастер настройки AI-моделей",
        'subtitle': "Настройка провайдера LLM для анализа документов и Copilot",
        'lang_selected': "Язык: Русский",
        'current_active': "Текущий активный провайдер",
        'select_provider': "Выберите провайдера ИИ для настройки и активации:",
        'provider_options': [
            ("[1] Google Gemini", "gemini", "Мультимодальный анализ PDF и фото (gemini-2.5-flash)"),
            ("[2] OpenAI / ChatGPT", "openai", "Структурированный анализ GPT-4o, GPT-4o-mini"),
            ("[3] Anthropic Claude", "claude", "Claude 3.7 Sonnet, Claude 3.5 Haiku"),
            ("[4] DeepSeek", "deepseek", "Мощная и доступная логика (deepseek-chat)"),
            ("[5] Alibaba Qwen", "qwen", "Модели платформы DashScope (qwen-plus, qwen-vl)"),
            ("[6] Custom / Local", "custom", "100% локальный Ollama / vLLM / OpenRouter"),
        ],
        'cancel': "[0] Отмена / Оставить без изменений",
        'prompt_choice': "Введите ваш выбор (0-6): ",
        'prompt_api_key': "Введите API-ключ",
        'press_enter_keep': "Нажмите Enter, чтобы оставить текущий",
        'optional_ollama': "Необязательно для локального Ollama",
        'prompt_model': "Название модели",
        'prompt_base_url': "Базовый URL эндпоинта",
        'test_connection_prompt': "Проверить подключение прямо сейчас? [Y/n]: ",
        'testing': "Проверка подключения к {provider} ({model})...",
        'test_success': "УСПЕШНО: Соединение установлено! Задержка: {latency}",
        'test_failed': "ОШИБКА: {error}",
        'save_prompt': "Сохранить конфигурацию и активировать провайдера? [Y/n]: ",
        'saved_success': "УСПЕШНО: Провайдер '{provider}' активирован и сохранен в .env и БД!",
        'cancelled': "Операция отменена. Настройки не изменены.",
        'list_header': "Статус зарегистрированных провайдеров ИИ:",
    },
    'es': {
        'title': "Sole Enterprise Orchestrator - Asistente de Configuración de IA",
        'subtitle': "Configure el proveedor LLM para análisis de documentos y Copilot",
        'lang_selected': "Idioma: Español",
        'current_active': "Proveedor Activo Actual",
        'select_provider': "Seleccione un proveedor de IA para configurar y activar:",
        'provider_options': [
            ("[1] Google Gemini", "gemini", "Extracción multimodal PDF/imágenes (gemini-2.5-flash)"),
            ("[2] OpenAI / ChatGPT", "openai", "Análisis estructurado con GPT-4o y GPT-4o-mini"),
            ("[3] Anthropic Claude", "claude", "Claude 3.7 Sonnet, Claude 3.5 Haiku"),
            ("[4] DeepSeek", "deepseek", "Razonamiento eficiente y económico (deepseek-chat)"),
            ("[5] Alibaba Qwen", "qwen", "Modelos empresariales DashScope (qwen-plus, qwen-vl)"),
            ("[6] Custom / Local", "custom", "100% privado en hardware local (Ollama, vLLM)"),
        ],
        'cancel': "[0] Cancelar / Mantener configuración actual",
        'prompt_choice': "Ingrese su opción (0-6): ",
        'prompt_api_key': "Ingrese la Clave API",
        'press_enter_keep': "Presione Enter para mantener la actual",
        'optional_ollama': "Opcional para Ollama local",
        'prompt_model': "Nombre del modelo",
        'prompt_base_url': "URL base del endpoint",
        'test_connection_prompt': "¿Desea probar la conexión ahora? [Y/n]: ",
        'testing': "Probando conexión con {provider} ({model})...",
        'test_success': "ÉXITO: Conexión verificada! Latencia: {latency}",
        'test_failed': "ERROR: {error}",
        'save_prompt': "¿Guardar esta configuración y activarla? [Y/n]: ",
        'saved_success': "ÉXITO: ¡Proveedor '{provider}' activado y guardado en .env y BD!",
        'cancelled': "Operación cancelada. No se modificaron ajustes.",
        'list_header': "Estado de proveedores de IA registrados:",
    },
    'nl': {
        'title': "Sole Enterprise Orchestrator - AI Model Setup Wizard",
        'subtitle': "Configureer LLM-provider voor documentextractie en Copilot",
        'lang_selected': "Taal: Nederlands",
        'current_active': "Huidige Actieve Provider",
        'select_provider': "Selecteer een AI-provider om te configureren en activeren:",
        'provider_options': [
            ("[1] Google Gemini", "gemini", "Multimodale PDF/foto extractie (gemini-2.5-flash)"),
            ("[2] OpenAI / ChatGPT", "openai", "Gestructureerde analyse met GPT-4o / mini"),
            ("[3] Anthropic Claude", "claude", "Claude 3.7 Sonnet, Claude 3.5 Haiku"),
            ("[4] DeepSeek", "deepseek", "Kosteneffectieve logica (deepseek-chat)"),
            ("[5] Alibaba Qwen", "qwen", "Enterprise DashScope-modellen (qwen-plus)"),
            ("[6] Custom / Local", "custom", "100% privé on-premise Ollama / vLLM"),
        ],
        'cancel': "[0] Annuleren / Huidige instellingen behouden",
        'prompt_choice': "Voer uw keuze in (0-6): ",
        'prompt_api_key': "Voer API-sleutel in",
        'press_enter_keep': "Druk op Enter om huidige te behouden",
        'optional_ollama': "Optioneel voor lokale Ollama",
        'prompt_model': "Modelnaam",
        'prompt_base_url': "Endpoint Base URL",
        'test_connection_prompt': "Wilt u de verbinding nu testen? [Y/n]: ",
        'testing': "Verbinding testen met {provider} ({model})...",
        'test_success': "SUCCES: Verbinding geverifieerd! Latentie: {latency}",
        'test_failed': "FOUT: {error}",
        'save_prompt': "Deze configuratie opslaan en activeren? [Y/n]: ",
        'saved_success': "SUCCES: Provider '{provider}' geactiveerd en opgeslagen!",
        'cancelled': "Geannuleerd. Geen wijzigingen opgeslagen.",
        'list_header': "Status van geregistreerde AI-providers:",
    },
    'fr': {
        'title': "Sole Enterprise Orchestrator - Assistant de Configuration IA",
        'subtitle': "Configurer le fournisseur LLM pour l'extraction de documents et Copilot",
        'lang_selected': "Langue : Français",
        'current_active': "Fournisseur Actuel",
        'select_provider': "Sélectionnez un fournisseur IA à configurer et activer :",
        'provider_options': [
            ("[1] Google Gemini", "gemini", "Extraction multimodale PDF/photos (gemini-2.5-flash)"),
            ("[2] OpenAI / ChatGPT", "openai", "Analyse structurée GPT-4o et GPT-4o-mini"),
            ("[3] Anthropic Claude", "claude", "Claude 3.7 Sonnet, Claude 3.5 Haiku"),
            ("[4] DeepSeek", "deepseek", "Raisonnement avancé et économique (deepseek-chat)"),
            ("[5] Alibaba Qwen", "qwen", "Modèles d'entreprise DashScope (qwen-plus)"),
            ("[6] Custom / Local", "custom", "100% privé en local via Ollama / vLLM"),
        ],
        'cancel': "[0] Annuler / Conserver les paramètres actuels",
        'prompt_choice': "Entrez votre choix (0-6) : ",
        'prompt_api_key': "Entrez la clé API",
        'press_enter_keep': "Appuyez sur Entrée pour conserver l'actuelle",
        'optional_ollama': "Optionnel pour Ollama local",
        'prompt_model': "Nom du modèle",
        'prompt_base_url': "URL de base de l'endpoint",
        'test_connection_prompt': "Tester la connexion maintenant ? [Y/n] : ",
        'testing': "Test de connexion à {provider} ({model})...",
        'test_success': "SUCCÈS : Connexion établie ! Latence : {latency}",
        'test_failed': "ÉCHEC : {error}",
        'save_prompt': "Enregistrer et activer cette configuration ? [Y/n] : ",
        'saved_success': "SUCCÈS : Fournisseur '{provider}' activé et enregistré !",
        'cancelled': "Opération annulée. Aucun paramètre modifié.",
        'list_header': "État des fournisseurs IA enregistrés :",
    },
    'pt': {
        'title': "Sole Enterprise Orchestrator - Assistente de Configuração de IA",
        'subtitle': "Configurar provedor LLM para extração de documentos e Copilot",
        'lang_selected': "Idioma: Português",
        'current_active': "Provedor Ativo Atual",
        'select_provider': "Selecione um provedor de IA para configurar e ativar:",
        'provider_options': [
            ("[1] Google Gemini", "gemini", "Extração multimodal de PDF/imagens (gemini-2.5-flash)"),
            ("[2] OpenAI / ChatGPT", "openai", "Análise estruturada com GPT-4o e GPT-4o-mini"),
            ("[3] Anthropic Claude", "claude", "Claude 3.7 Sonnet, Claude 3.5 Haiku"),
            ("[4] DeepSeek", "deepseek", "Raciocínio avançado de baixo custo (deepseek-chat)"),
            ("[5] Alibaba Qwen", "qwen", "Modelos empresariais DashScope (qwen-plus)"),
            ("[6] Custom / Local", "custom", "100% privado no hardware local (Ollama / vLLM)"),
        ],
        'cancel': "[0] Cancelar / Manter configurações atuais",
        'prompt_choice': "Digite sua opção (0-6): ",
        'prompt_api_key': "Digite a chave de API",
        'press_enter_keep': "Pressione Enter para manter a atual",
        'optional_ollama': "Opcional para Ollama local",
        'prompt_model': "Nome do modelo",
        'prompt_base_url': "URL base do endpoint",
        'test_connection_prompt': "Deseja testar a conexão agora? [Y/n]: ",
        'testing': "Testando conexão com {provider} ({model})...",
        'test_success': "SUCESSO: Conexão verificada! Latência: {latency}",
        'test_failed': "FALHA: {error}",
        'save_prompt': "Salvar esta configuração e ativá-la? [Y/n]: ",
        'saved_success': "SUCESSO: Provedor '{provider}' ativado e salvo!",
        'cancelled': "Operação cancelada. Nenhuma alteração salva.",
        'list_header': "Status dos provedores de IA registrados:",
    },
    'zh_Hans': {
        'title': "Sole Enterprise Orchestrator - AI 多模型配置向导",
        'subtitle': "配置单据提取与 Copilot 智能助手的 LLM 模型提供商",
        'lang_selected': "当前语言: 简体中文",
        'current_active': "当前激活的提供商",
        'select_provider': "请选择要配置并激活的 AI 模型提供商:",
        'provider_options': [
            ("[1] Google Gemini", "gemini", "多模态 PDF 与图像解析 (gemini-2.5-flash)"),
            ("[2] OpenAI / ChatGPT", "openai", "GPT-4o、GPT-4o-mini 结构化提取"),
            ("[3] Anthropic Claude", "claude", "Claude 3.7 Sonnet、Claude 3.5 Haiku"),
            ("[4] DeepSeek", "deepseek", "超高性价比深度推理 (deepseek-chat / V3 / R1)"),
            ("[5] 阿里通义千问 (Qwen)", "qwen", "阿里云百炼 DashScope 平台 (qwen-plus, qwen-vl)"),
            ("[6] 自定义 / 本地模型", "custom", "100% 局域网私有化部署 (Ollama / vLLM / OpenRouter)"),
        ],
        'cancel': "[0] 取消 / 保持当前配置",
        'prompt_choice': "请输入选项编号 (0-6): ",
        'prompt_api_key': "请输入 API 密钥 (API Key)",
        'press_enter_keep': "直接按回车保留当前密钥",
        'optional_ollama': "本地 Ollama 无需填写密钥",
        'prompt_model': "模型名称 (Model)",
        'prompt_base_url': "服务地址 (Base URL)",
        'test_connection_prompt': "是否立即测试接口连接？ [Y/n]: ",
        'testing': "正在测试连接到 {provider} ({model})...",
        'test_success': "成功: 接口连接畅通！响应延迟: {latency}",
        'test_failed': "失败: {error}",
        'save_prompt': "是否将此配置保存并激活为默认提供商？ [Y/n]: ",
        'saved_success': "成功: 模型提供商 '{provider}' 已激活并同步保存至 .env 与数据库！",
        'cancelled': "操作已取消，未做任何修改。",
        'list_header': "已注册的 AI 模型提供商状态清单:",
    },
    'ja': {
        'title': "Sole Enterprise Orchestrator - AIモデルセットアップウィザード",
        'subtitle': "書類解析・ERP Copilot 用の LLM プロバイダー設定",
        'lang_selected': "言語: 日本語",
        'current_active': "現在のアクティブプロバイダー",
        'select_provider': "設定およびアクティブ化する AI プロバイダーを選択してください:",
        'provider_options': [
            ("[1] Google Gemini", "gemini", "マルチモーダル PDF/画像高精度抽出 (gemini-2.5-flash)"),
            ("[2] OpenAI / ChatGPT", "openai", "GPT-4o, GPT-4o-mini 構造化データ抽出"),
            ("[3] Anthropic Claude", "claude", "Claude 3.7 Sonnet, Claude 3.5 Haiku"),
            ("[4] DeepSeek", "deepseek", "高コスパ高推論モデル (deepseek-chat)"),
            ("[5] Alibaba Qwen (通義千問)", "qwen", "Alibaba DashScope プラットフォーム (qwen-plus)"),
            ("[6] カスタム / ローカルLLM", "custom", "100% 社内オンプレミス運用 (Ollama / vLLM)"),
        ],
        'cancel': "[0] キャンセル / 現在の設定を維持",
        'prompt_choice': "選択番号を入力してください (0-6): ",
        'prompt_api_key': "API キーを入力",
        'press_enter_keep': "Enterキーを押すと現在値を保持",
        'optional_ollama': "ローカル Ollama の場合は省略可能",
        'prompt_model': "モデル名",
        'prompt_base_url': "エンドポイント Base URL",
        'test_connection_prompt': "今すぐ接続テストを実行しますか？ [Y/n]: ",
        'testing': "{provider} ({model}) への接続テストを実行中...",
        'test_success': "成功: 接続を確認しました！レイテンシ: {latency}",
        'test_failed': "失敗: {error}",
        'save_prompt': "この設定を保存してアクティブ化しますか？ [Y/n]: ",
        'saved_success': "成功: プロバイダー '{provider}' をアクティブ化し、.env と DB に保存しました！",
        'cancelled': "操作をキャンセルしました。設定は変更されていません。",
        'list_header': "登録済み AI プロバイダーのステータス一覧:",
    },
}


class Command(BaseCommand):
    help = "Interactive or scripted CLI setup wizard to select and configure AI/LLM providers."

    def add_arguments(self, parser):
        parser.add_argument('--lang', type=str, choices=['en', 'ru', 'es', 'nl', 'fr', 'pt', 'zh-hans', 'ja'], help="Language for wizard (en, ru, es, nl, fr, pt, zh-hans, ja)")
        parser.add_argument('--provider', type=str, choices=['gemini', 'openai', 'claude', 'deepseek', 'qwen', 'custom'], help="Target provider ID")
        parser.add_argument('--api-key', type=str, help="API key")
        parser.add_argument('--model', type=str, help="Model name")
        parser.add_argument('--base-url', type=str, help="Base URL endpoint")
        parser.add_argument('--test', action='store_true', help="Perform connection test")
        parser.add_argument('--list', action='store_true', help="List all available providers and their status")
        parser.add_argument('--non-interactive', action='store_true', help="Save changes without interactive prompts")

    def handle(self, *args, **options):
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, 'reconfigure'):
                try:
                    stream.reconfigure(encoding='utf-8', errors='replace')
                except Exception:
                    pass

        # 1. Handle --list flag
        if options['list']:
            self.print_provider_list(options.get('lang') or 'en')
            return

        # 2. Handle non-interactive mode
        if options.get('provider') and (options.get('non_interactive') or options.get('non-interactive')):
            self.handle_scripted(options)
            return

        # 3. Interactive Mode
        lang_code = self.resolve_language(options.get('lang'))
        t = CLI_TRANSLATIONS.get(lang_code, CLI_TRANSLATIONS['en'])
        self.run_interactive_wizard(t, options)

    def resolve_language(self, lang_arg: str) -> str:
        if lang_arg:
            clean = lang_arg.lower().replace('-', '_')
            if 'zh' in clean:
                return 'zh_Hans'
            if clean in CLI_TRANSLATIONS:
                return clean

        # Prompt for language selection
        self.stdout.write("\n" + "=" * 65)
        self.stdout.write(" Select Language / Выберите язык / Seleccione idioma / 语言选择:")
        self.stdout.write(" [1] English      [2] Русский     [3] Español     [4] Nederlands")
        self.stdout.write(" [5] Français     [6] Português   [7] 简体中文    [8] 日本語")
        self.stdout.write("=" * 65)

        choice = input(" Choice [1-8, Default: 1]: ").strip()
        mapping = {
            '1': 'en', '2': 'ru', '3': 'es', '4': 'nl',
            '5': 'fr', '6': 'pt', '7': 'zh_Hans', '8': 'ja'
        }
        return mapping.get(choice, 'en')

    def print_provider_list(self, lang_code: str):
        lang = 'zh_Hans' if 'zh' in lang_code else lang_code.split('-')[0]
        t = CLI_TRANSLATIONS.get(lang, CLI_TRANSLATIONS['en'])
        providers = list_providers()

        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(f" {t['list_header']}")
        self.stdout.write("=" * 70)
        for p in providers:
            active_marker = " [ACTIVE]" if p['is_active'] else ""
            status_text = "Configured" if p['is_configured'] else "Key Missing"
            key_display = f" (Key: {p['api_key_masked']})" if p['api_key_masked'] else ""
            self.stdout.write(f" * {p['name']:<25} ID: {p['id']:<10} Model: {p['current_model']:<20}{active_marker}")
            self.stdout.write(f"   Status: {status_text}{key_display} | Endpoint: {p['current_base_url']}")
        self.stdout.write("=" * 70 + "\n")

    def run_interactive_wizard(self, t: dict, options: dict):
        active_provider = get_active_provider()
        setting = AISetting.get_settings()

        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(f"  {t['title']}")
        self.stdout.write(f"  {t['subtitle']}")
        self.stdout.write("=" * 70)
        self.stdout.write(f" {t['current_active']}: {active_provider.display_name} ({active_provider.model})")
        self.stdout.write("-" * 70)
        self.stdout.write(f" {t['select_provider']}\n")

        options_map = {}
        for idx, (label, pid, desc) in enumerate(t['provider_options'], start=1):
            options_map[str(idx)] = pid
            self.stdout.write(f"  {label:<26} - {desc}")
        self.stdout.write(f"  {t['cancel']}\n")

        choice = input(f" {t['prompt_choice']}").strip()
        if choice in ['0', '', 'q', 'exit']:
            self.stdout.write(f"\n {t['cancelled']}\n")
            return

        target_provider_id = options_map.get(choice)
        if not target_provider_id:
            self.stdout.write("\n Invalid selection. Exiting.\n")
            return

        # Fetch default class to get default model/url
        prov_cls = PROVIDER_CLASSES.get(target_provider_id)
        current_inst = get_provider(target_provider_id)

        self.stdout.write("\n" + "-" * 70)
        self.stdout.write(f" Configuring {prov_cls.display_name}")
        self.stdout.write("-" * 70)

        # 1. API Key
        existing_key = current_inst.api_key
        key_hint = f" [{t['press_enter_keep']}: {mask_key(existing_key)}]" if existing_key else f" ({t['optional_ollama'] if target_provider_id == 'custom' else 'Required'})"
        new_key = input(f" {t['prompt_api_key']}{key_hint}: ").strip()
        final_key = new_key if new_key else existing_key

        # 2. Model
        default_model = current_inst.model or prov_cls.default_model
        model_input = input(f" {t['prompt_model']} [Default: {default_model}]: ").strip()
        final_model = model_input if model_input else default_model

        # 3. Base URL
        default_url = current_inst.base_url or prov_cls.default_base_url
        url_input = input(f" {t['prompt_base_url']} [Default: {default_url}]: ").strip()
        final_url = url_input if url_input else default_url

        # 4. Connection Test
        test_choice = input(f"\n {t['test_connection_prompt']}").strip().lower()
        if test_choice in ['', 'y', 'yes']:
            self.stdout.write(f" {t['testing'].format(provider=prov_cls.display_name, model=final_model)}")
            try:
                test_prov = prov_cls(api_key=final_key, model=final_model, base_url=final_url)
                success, msg = test_prov.test_connection()
                if success:
                    self.stdout.write(self.style.SUCCESS(f" {t['test_success'].format(latency=msg)}"))
                else:
                    self.stdout.write(self.style.ERROR(f" {t['test_failed'].format(error=msg)}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f" {t['test_failed'].format(error=e)}"))

        # 5. Save confirmation
        save_choice = input(f"\n {t['save_prompt']}").strip().lower()
        if save_choice in ['', 'y', 'yes']:
            self.save_configuration(target_provider_id, final_key, final_model, final_url)
            self.stdout.write(self.style.SUCCESS(f"\n {t['saved_success'].format(provider=prov_cls.display_name)}\n"))
        else:
            self.stdout.write(f"\n {t['cancelled']}\n")

    def save_configuration(self, provider_id: str, api_key: str, model: str, base_url: str):
        setting = AISetting.get_settings()
        setting.active_provider = provider_id

        env_updates = {'LLM_PROVIDER': provider_id}

        if provider_id == 'gemini':
            setting.gemini_api_key = api_key
            setting.gemini_model = model
            env_updates['GEMINI_API_KEY'] = api_key
            env_updates['GEMINI_MODEL'] = model
        elif provider_id == 'openai':
            setting.openai_api_key = api_key
            setting.openai_model = model
            setting.openai_base_url = base_url
            env_updates['OPENAI_API_KEY'] = api_key
            env_updates['OPENAI_MODEL'] = model
            env_updates['OPENAI_BASE_URL'] = base_url
        elif provider_id == 'claude':
            setting.claude_api_key = api_key
            setting.claude_model = model
            setting.claude_base_url = base_url
            env_updates['ANTHROPIC_API_KEY'] = api_key
            env_updates['ANTHROPIC_MODEL'] = model
            env_updates['ANTHROPIC_BASE_URL'] = base_url
        elif provider_id == 'deepseek':
            setting.deepseek_api_key = api_key
            setting.deepseek_model = model
            setting.deepseek_base_url = base_url
            env_updates['DEEPSEEK_API_KEY'] = api_key
            env_updates['DEEPSEEK_MODEL'] = model
            env_updates['DEEPSEEK_BASE_URL'] = base_url
        elif provider_id == 'qwen':
            setting.qwen_api_key = api_key
            setting.qwen_model = model
            setting.qwen_base_url = base_url
            env_updates['QWEN_API_KEY'] = api_key
            env_updates['QWEN_MODEL'] = model
            env_updates['QWEN_BASE_URL'] = base_url
        elif provider_id == 'custom':
            setting.custom_api_key = api_key
            setting.custom_model = model
            setting.custom_base_url = base_url
            env_updates['CUSTOM_API_KEY'] = api_key
            env_updates['CUSTOM_MODEL'] = model
            env_updates['CUSTOM_BASE_URL'] = base_url

        setting.save()
        update_env_variables(env_updates)

    def handle_scripted(self, options: dict):
        provider_id = options['provider'].lower()
        api_key = options.get('api_key') or ""
        model = options.get('model') or ""
        base_url = options.get('base_url') or ""

        prov_cls = PROVIDER_CLASSES.get(provider_id)
        if not model:
            model = prov_cls.default_model
        if not base_url:
            base_url = prov_cls.default_base_url

        if options['test']:
            test_prov = prov_cls(api_key=api_key, model=model, base_url=base_url)
            success, msg = test_prov.test_connection()
            if success:
                self.stdout.write(self.style.SUCCESS(f"Test Success: {msg}"))
            else:
                self.stdout.write(self.style.ERROR(f"Test Failed: {msg}"))
                if not options.get('api_key'):
                    sys.exit(1)

        self.save_configuration(provider_id, api_key, model, base_url)
        self.stdout.write(self.style.SUCCESS(f"Successfully configured active provider: {provider_id}"))
