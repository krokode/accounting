"""
Standard exception hierarchy for AI/LLM providers in Sole Enterprise Orchestrator.
Provides localized, actionable error messages across all 8 supported languages.
"""
from django.utils.translation import get_language


def get_active_lang_code() -> str:
    """Returns normalized active language code (en, ru, es, nl, fr, pt, zh_Hans, ja)."""
    raw = (get_language() or 'en').lower()
    if 'zh' in raw:
        return 'zh_Hans'
    code = raw.split('-')[0].split('_')[0]
    if code in ['ru', 'es', 'nl', 'fr', 'pt', 'ja']:
        return code
    return 'en'


class AIError(Exception):
    """Base exception for all AI provider errors."""
    def __init__(self, message: str, provider: str = "", details: str = ""):
        self.message = message
        self.provider = provider
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        return self.message


class AIConfigurationError(AIError):
    """Raised when an API key or critical configuration is missing."""
    MESSAGES = {
        'en': "API key for {provider} is not configured. Please add your API key in AI Settings (/assistant/settings/) or run 'python setup_llm.py'.",
        'ru': "API-ключ для {provider} не настроен. Пожалуйста, укажите ваш API-ключ в настройках ИИ (/assistant/settings/) или запустите 'python setup_llm.py'.",
        'es': "La clave API para {provider} no está configurada. Agregue su clave API en Configuración de IA (/assistant/settings/) o ejecute 'python setup_llm.py'.",
        'nl': "API-sleutel voor {provider} is niet geconfigureerd. Voeg uw API-sleutel toe in AI-instellingen (/assistant/settings/) of voer 'python setup_llm.py' uit.",
        'fr': "La clé API pour {provider} n'est pas configurée. Veuillez ajouter votre clé API dans Paramètres IA (/assistant/settings/) ou exécuter 'python setup_llm.py'.",
        'pt': "A chave de API para {provider} não está configurada. Adicione sua chave de API nas Configurações de IA (/assistant/settings/) ou execute 'python setup_llm.py'.",
        'zh_Hans': "{provider} 的 API 密钥尚未配置。请在 AI 设置 (/assistant/settings/) 中添加您的 API 密钥，或运行 'python setup_llm.py'。",
        'ja': "{provider} の API キーが設定されていません。AI設定 (/assistant/settings/) で API キーを追加するか、'python setup_llm.py' を実行してください。",
    }

    def __init__(self, provider: str, details: str = ""):
        lang = get_active_lang_code()
        template = self.MESSAGES.get(lang, self.MESSAGES['en'])
        formatted_message = template.format(provider=provider)
        super().__init__(formatted_message, provider=provider, details=details)


class AIRateLimitError(AIError):
    """Raised on HTTP 429, quota exhaustion, or rate limit exceeded."""
    MESSAGES = {
        'en': "Rate limit or quota exceeded for {provider}. Please wait a moment, extend your API quotas/billing limits with the provider, or switch providers in AI Settings.",
        'ru': "Превышен лимит запросов или квота для {provider}. Пожалуйста, подождите, увеличьте лимиты/квоту у провайдера или выберите другого провайдера в настройках ИИ.",
        'es': "Límite de solicitudes o cuota excedida para {provider}. Espere un momento, amplíe sus cuotas/límites de facturación con el proveedor o cambie de proveedor en Configuración de IA.",
        'nl': "Verzoeklimiet of quotum overschreden voor {provider}. Wacht even, verhoog uw API-quota/facturatielimieten bij de provider, of wissel van provider in AI-instellingen.",
        'fr': "Limite de requêtes ou quota dépassé pour {provider}. Veuillez patienter un instant, étendre vos quotas/limites de facturation auprès du fournisseur ou changer de fournisseur dans les Paramètres IA.",
        'pt': "Limite de taxa ou quota excedida para {provider}. Aguarde um momento, aumente seus limites/quotas de faturação com o fornecedor ou mude de fornecedor nas Configurações de IA.",
        'zh_Hans': "{provider} 请求频率超限或配额已耗尽。请稍候重试、向提供商扩展配额/账单上限，或在 AI 设置中切换其他模型提供商。",
        'ja': "{provider} の利用制限またはクォータを超過しました。しばらく待つか、プロバイダーのクォータ／利用枠を拡張するか、AI設定で別のプロバイダーに切り替えてください。",
    }

    def __init__(self, provider: str, details: str = ""):
        lang = get_active_lang_code()
        template = self.MESSAGES.get(lang, self.MESSAGES['en'])
        formatted_message = template.format(provider=provider)
        super().__init__(formatted_message, provider=provider, details=details)


class AIOfflineError(AIError):
    """Raised when the AI provider endpoint is unreachable or offline."""
    MESSAGES = {
        'en': "Could not connect to {provider} at {endpoint}. The service is currently offline or unreachable. Please check your network connection, verify the endpoint URL, or try again later.",
        'ru': "Не удалось подключиться к {provider} по адресу {endpoint}. Сервис в данный момент недоступен или отключен. Проверьте сетевое подключение, адрес эндпоинта или повторите попытку позже.",
        'es': "No se pudo conectar a {provider} en {endpoint}. El servicio está actualmente desconectado o no disponible. Verifique su conexión de red, la URL del endpoint o intente nuevamente más tarde.",
        'nl': "Kan geen verbinding maken met {provider} op {endpoint}. De service is momenteel offline of onbereikbaar. Controleer uw netwerkverbinding, controleer de endpoint-URL of probeer het later opnieuw.",
        'fr': "Impossible de se connecter à {provider} sur {endpoint}. Le service est actuellement hors ligne ou inaccessible. Veuillez vérifier votre connexion réseau, l'URL du point de terminaison ou réessayer plus tard.",
        'pt': "Não foi possível ligar a {provider} em {endpoint}. O serviço está atualmente offline ou inacessível. Verifique a sua ligação de rede, confirme o URL do endpoint ou tente novamente mais tarde.",
        'zh_Hans': "无法连接到 {provider} ({endpoint})。该服务当前处于离线状态或不可达。请检查网络连接、确认端点地址，或稍后重试。",
        'ja': "{provider} ({endpoint}) に接続できませんでした。サービスがオフラインまたは到達不能です。ネットワーク接続やエンドポイントURLを確認するか、後ほど再試行してください。",
    }

    def __init__(self, provider: str, endpoint: str = "", details: str = ""):
        lang = get_active_lang_code()
        template = self.MESSAGES.get(lang, self.MESSAGES['en'])
        formatted_message = template.format(provider=provider, endpoint=endpoint or "API endpoint")
        super().__init__(formatted_message, provider=provider, details=details)


class AIAuthenticationError(AIError):
    """Raised on HTTP 401/403 or invalid credentials."""
    MESSAGES = {
        'en': "Authentication failed for {provider}. Invalid API key or unauthorized access. Please verify and update your API key in AI Settings (/assistant/settings/).",
        'ru': "Ошибка аутентификации для {provider}. Неверный API-ключ или нет доступа. Проверьте и обновите ваш API-ключ в настройках ИИ (/assistant/settings/).",
        'es': "Error de autenticación para {provider}. Clave API no válida o acceso no autorizado. Verifique y actualice su clave API en Configuración de IA (/assistant/settings/).",
        'nl': "Authenticatie mislukt voor {provider}. Ongeldige API-sleutel of ongeautoriseerde toegang. Controleer en werk uw API-sleutel bij in AI-instellingen (/assistant/settings/).",
        'fr': "Échec de l'authentification pour {provider}. Clé API non valide ou accès non autorisé. Veuillez vérifier et mettre à jour votre clé API dans les Paramètres IA (/assistant/settings/).",
        'pt': "Falha na autenticação para {provider}. Chave de API inválida ou acesso não autorizado. Verifique e atualize sua chave de API nas Configurações de IA (/assistant/settings/).",
        'zh_Hans': "{provider} 身份验证失败。API 密钥无效或未授权。请在 AI 设置 (/assistant/settings/) 中检查并更新您的密钥。",
        'ja': "{provider} の認証に失敗しました。無効な API キーまたはアクセス権限がありません。AI設定 (/assistant/settings/) でキーを確認・更新してください。",
    }

    def __init__(self, provider: str, details: str = ""):
        lang = get_active_lang_code()
        template = self.MESSAGES.get(lang, self.MESSAGES['en'])
        formatted_message = template.format(provider=provider)
        super().__init__(formatted_message, provider=provider, details=details)
