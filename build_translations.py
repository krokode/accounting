import os
import polib
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Comprehensive multilingual translation database for all 8 supported languages
COMMON_STRINGS = {
    # Company Profile & AI Debit/Credit Matching
    "Company Profile": {
        "ru": "Профиль компании", "es": "Perfil de la empresa", "nl": "Bedrijfsprofiel",
        "fr": "Profil de l'entreprise", "pt": "Perfil da empresa", "zh_Hans": "企业资料", "ja": "会社概要"
    },
    "Company & Organization Profile": {
        "ru": "Профиль компании и реквизиты", "es": "Perfil de la empresa y organización", "nl": "Bedrijfs- & Organisatieprofiel",
        "fr": "Profil de l'entreprise & de l'organisation", "pt": "Perfil da empresa e organização", "zh_Hans": "公司与组织基本资料", "ja": "会社・組織プロファイル"
    },
    "Master identity details used by AI agents to automatically determine Debit vs. Credit, invoice directions, and ledger accounts.": {
        "ru": "Основные реквизиты организации, используемые ИИ для определения дебета/кредита, направления счетов и бухгалтерских проводок.",
        "es": "Datos maestros de identidad utilizados por los agentes de IA para determinar automáticamente Débito vs. Crédito, dirección de facturas y cuentas contables.",
        "nl": "Basisidentiteitsgegevens die door AI-agents worden gebruikt om automatisch Debet vs. Credit, factuurrichtingen en grootboekrekeningen te bepalen.",
        "fr": "Coordonnées principales de l'entité utilisées par les agents IA pour déterminer automatiquement le Débit et le Crédit, le sens des factures et les écritures comptables.",
        "pt": "Dados de identificação utilizados pelos agentes de IA para determinar automaticamente Débito vs. Crédito, direção de faturas e contas de razão.",
        "zh_Hans": "用于让 AI 智能助理自动判定借贷方向、发票收付类型及记账科目的主体基础信息。",
        "ja": "AIエージェントが借方・貸方の判定、請求書の方向、勘定科目を自動決定するために使用する組織の基本情報。"
    },
    "How AI Determines Debit vs. Credit Using Your Profile": {
        "ru": "Как ИИ определяет дебет и кредит на основе профиля компании",
        "es": "Cómo determina la IA Débito vs. Crédito usando el perfil de su empresa",
        "nl": "Hoe AI Debet vs. Credit bepaalt aan de hand van uw bedrijfsprofiel",
        "fr": "Comment l'IA détermine le Débit et le Crédit grâce au profil de votre entreprise",
        "pt": "Como a IA determina Débito vs. Crédito usando o perfil da sua empresa",
        "zh_Hans": "AI 如何根据企业信息判定借贷方向与发票归属",
        "ja": "AIが企業情報に基づいて借方・貸方を判定する仕組み"
    },
    "When processing scanned paperwork or receipts, the AI agent compares the document against your company's name and tax identifiers to eliminate accounting ambiguity:": {
        "ru": "При обработке отсканированных документов и чеков ИИ сопоставляет реквизиты документа с названием и ИНН вашей компании, исключая двусмысленность:",
        "es": "Al procesar documentos escaneados o recibos, el agente de IA compara el documento con el nombre e identificación fiscal de su empresa para eliminar ambigüedades:",
        "nl": "Bij het verwerken van gescande documenten of bonnen vergelijkt de AI-agent het document met uw bedrijfsnaam en belastingnummers om boekhoudkundige onzekerheid weg te nemen:",
        "fr": "Lors du traitement des documents numérisés ou des reçus, l'agent IA compare le document au nom et aux identifiants fiscaux de votre entreprise pour éliminer toute ambiguïté comptable :",
        "pt": "Ao processar documentos digitalizados ou recibos, o agente de IA compara o documento com o nome e NIF da sua empresa para eliminar ambiguidades contabilísticas:",
        "zh_Hans": "在处理扫描单据或收据时，AI 助理会将单据信息与您公司的名称及税号进行比对，消除会计核算歧义：",
        "ja": "スキャンされた書類や領収書を処理する際、AIエージェントは書類と貴社の名称・納税者番号を照合し、仕訳の曖昧さを解消します："
    },
    "Our Company is the Buyer (Billed To)": {
        "ru": "Наша компания является покупателем (Счет выставлен нам)",
        "es": "Nuestra empresa es el comprador (Facturado a)",
        "nl": "Ons bedrijf is de koper (Gefactureerd aan)",
        "fr": "Notre entreprise est l'acheteur (Facturé à)",
        "pt": "A nossa empresa é o comprador (Faturado a)",
        "zh_Hans": "我司为购买方 / 客户（抬头为我司）",
        "ja": "貴社が買い手（宛先が貴社）"
    },
    "Classified as <strong>Vendor Bill (Payable)</strong>. Ledger effect: <strong>Debit</strong> = Expense/Inventory, <strong>Credit</strong> = Accounts Payable.": {
        "ru": "Классифицируется как <strong>Счет поставщика (К оплате)</strong>. Проводка: <strong>Дебет</strong> = Расходы/Склад, <strong>Кредит</strong> = Кредиторская задолженность.",
        "es": "Clasificado como <strong>Factura de proveedor (Por pagar)</strong>. Efecto contable: <strong>Débito</strong> = Gasto/Inventario, <strong>Crédito</strong> = Cuentas por pagar.",
        "nl": "Geclassificeerd als <strong>Inkoopfactuur (Crediteuren)</strong>. Boeking: <strong>Debet</strong> = Kosten/Voorraad, <strong>Credit</strong> = Crediteuren.",
        "fr": "Classé comme <strong>Facture fournisseur (À payer)</strong>. Écriture : <strong>Débit</strong> = Charges/Stock, <strong>Crédit</strong> = Dettes fournisseurs.",
        "pt": "Classificado como <strong>Fatura de fornecedor (A pagar)</strong>. Efeito: <strong>Débito</strong> = Despesa/Inventário, <strong>Crédito</strong> = Contas a pagar.",
        "zh_Hans": "归类为 <strong>供应商账单（应付款项）</strong>。记账影响：<strong>借方</strong> = 费用/库存存货，<strong>贷方</strong> = 应付账款。",
        "ja": "<strong>仕入先請求書（買掛金）</strong> として分類。仕訳効果：<strong>借方</strong> = 経費／在庫、<strong>貸方</strong> = 買掛金。"
    },
    "Our Company is the Seller (Billed From)": {
        "ru": "Наша компания является продавцом (Счет выставлен нами)",
        "es": "Nuestra empresa es el vendedor (Facturado por)",
        "nl": "Ons bedrijf is de verkoper (Gefactureerd door)",
        "fr": "Notre entreprise est le vendeur (Facturé par)",
        "pt": "A nossa empresa é o vendedor (Faturado por)",
        "zh_Hans": "我司为销售方 / 供应商（开票方为我司）",
        "ja": "貴社が売り手（発行者が貴社）"
    },
    "Classified as <strong>Customer Invoice (Receivable)</strong>. Ledger effect: <strong>Debit</strong> = Accounts Receivable, <strong>Credit</strong> = Sales Revenue.": {
        "ru": "Классифицируется как <strong>Счет клиенту (К получению)</strong>. Проводка: <strong>Дебет</strong> = Дебиторская задолженность, <strong>Кредит</strong> = Выручка от продаж.",
        "es": "Clasificado como <strong>Factura de cliente (Por cobrar)</strong>. Efecto contable: <strong>Débito</strong> = Cuentas por cobrar, <strong>Crédito</strong> = Ingresos por ventas.",
        "nl": "Geclassificeerd als <strong>Verkoopfactuur (Debiteuren)</strong>. Boeking: <strong>Debet</strong> = Debiteuren, <strong>Credit</strong> = Omzet.",
        "fr": "Classé comme <strong>Facture client (À recevoir)</strong>. Écriture : <strong>Débit</strong> = Créances clients, <strong>Crédit</strong> = Produits des ventes.",
        "pt": "Classificado como <strong>Fatura de cliente (A receber)</strong>. Efeito: <strong>Débito</strong> = Contas a receber, <strong>Crédito</strong> = Receita de vendas.",
        "zh_Hans": "归类为 <strong>客户销售发票（应收款项）</strong>。记账影响：<strong>借方</strong> = 应收账款，<strong>贷方</strong> = 营业收入。",
        "ja": "<strong>得意先請求書（売掛金）</strong> として分類。仕訳効果：<strong>借方</strong> = 売掛金、<strong>貸方</strong> = 売上高。"
    },
    "Corporate Identity": {
        "ru": "Реквизиты юридического лица", "es": "Identidad corporativa", "nl": "Bedrijfsidentiteit",
        "fr": "Identité juridique", "pt": "Identidade corporativa", "zh_Hans": "企业主体身份", "ja": "法人基本情報"
    },
    "Legal Entity Name": {
        "ru": "Юридическое наименование", "es": "Razón social", "nl": "Statutaire naam",
        "fr": "Raison sociale", "pt": "Denominação social", "zh_Hans": "法定全称", "ja": "法人正式名称"
    },
    "Official registered corporate name appearing on legal contracts and invoices.": {
        "ru": "Официальное зарегистрированное наименование компании в договорах и счетах.",
        "es": "Nombre corporativo registrado oficialmente que figura en contratos y facturas.",
        "nl": "Officieel geregistreerde bedrijfsnaam zoals vermeld op contracten en facturen.",
        "fr": "Dénomination sociale officielle figurant sur les contrats et factures.",
        "pt": "Nome oficial registado da empresa constante em contratos e faturas.",
        "zh_Hans": "出现在法律合同及发票上的工商注册企业法定名称。",
        "ja": "契約書や請求書に記載される正式な登記法人名。"
    },
    "Official registered corporate name": {
        "ru": "Официальное зарегистрированное наименование", "es": "Razón social oficial registrada", "nl": "Officieel geregistreerde bedrijfsnaam",
        "fr": "Dénomination sociale officielle", "pt": "Denominação social oficial", "zh_Hans": "工商注册官方企业法定名称", "ja": "登記上の正式法人名"
    },
    "Trade / Commercial Name": {
        "ru": "Торговое / коммерческое название", "es": "Nombre comercial", "nl": "Handelsnaam",
        "fr": "Nom commercial", "pt": "Nome comercial", "zh_Hans": "品牌 / 商业简称", "ja": "商号・ブランド名"
    },
    "Trade / Brand Name": {
        "ru": "Бренд / Торговое наименование", "es": "Nombre comercial / Marca", "nl": "Handels- / Merknaam",
        "fr": "Nom commercial / Marque", "pt": "Nome comercial / Marca", "zh_Hans": "商业名称 / 品牌", "ja": "屋号・ブランド名"
    },
    "Brand name or commercial trade name displayed in system headers.": {
        "ru": "Бренд или торговое название, отображаемое в шапке системы.",
        "es": "Nombre de marca o denominación comercial que se muestra en los encabezados del sistema.",
        "nl": "Merknaam of handelsnaam weergegeven in de systeemkopteksten.",
        "fr": "Marque ou nom commercial affiché dans les en-têtes du système.",
        "pt": "Nome da marca ou denominação comercial apresentada nos cabeçalhos do sistema.",
        "zh_Hans": "显示在系统顶部及界面的品牌或商业简称。",
        "ja": "システムヘッダー等に表示されるブランド名または通称。"
    },
    "Public-facing business name if different from legal name": {
        "ru": "Публичное название компании, если отличается от юридического",
        "es": "Nombre comercial si es diferente de la razón social",
        "nl": "Commerciële naam indien afwijkend van de statutaire naam",
        "fr": "Nom commercial s'il diffère de la raison sociale",
        "pt": "Nome comercial caso difira da denominação social",
        "zh_Hans": "对外经营名称（若与法定全称不同）",
        "ja": "登記名と異なる場合の対外的な事業所名・商号"
    },
    "Tax / VAT ID": {
        "ru": "ИНН / Номер плательщика НДС", "es": "NIF / CIF / IVA", "nl": "Btw-identificatienummer",
        "fr": "N° de TVA / SIRET", "pt": "NIF / Número de IVA", "zh_Hans": "纳税人识别号 / 统一社会信用代码", "ja": "法人番号 / インボイス登録番号"
    },
    "Crucial for AI to match issuer vs recipient on official tax documents.": {
        "ru": "Необходимо для ИИ для точного определения продавца и покупателя в налоговых документах.",
        "es": "Fundamental para que la IA identifique emisor vs. receptor en documentos fiscales.",
        "nl": "Cruciaal voor AI om verzender vs. ontvanger te identificeren op officiële belastingdocumenten.",
        "fr": "Indispensable pour que l'IA identifie l'émetteur et le destinataire sur les documents fiscaux.",
        "pt": "Fundamental para a IA identificar emitente vs. destinatário em documentos fiscais.",
        "zh_Hans": "AI 识别税务单据开票方与受票方的核心依据。",
        "ja": "AIが税務書類の発行元と受取人を正確に照合するために不可欠です。"
    },
    "VAT number, EIN, or national tax identifier": {
        "ru": "Номер НДС, ИНН или государственный налоговый номер",
        "es": "Número de IVA, NIF o identificación fiscal nacional",
        "nl": "Btw-nummer of nationaal fiscaal identificatienummer",
        "fr": "Numéro de TVA, SIREN ou identifiant fiscal national",
        "pt": "Número de IVA, NIF ou identificador fiscal nacional",
        "zh_Hans": "增值税号、税号或国家税务登记号",
        "ja": "消費税インボイス番号または国税識別番号"
    },
    "Company Registry No.": {
        "ru": "ОГРН / Регистрационный номер", "es": "Número de registro mercantil", "nl": "Handelsregisternummer",
        "fr": "Numéro RCS / Immatriculation", "pt": "Número de registo comercial", "zh_Hans": "公司登记号", "ja": "会社登記番号"
    },
    "Company Registry No. (CRN)": {
        "ru": "ОГРН / Регистрационный номер (CRN)", "es": "Número de registro mercantil (CRN)", "nl": "KVK-nummer / Handelsregisternummer",
        "fr": "Numéro RCS / Immatriculation (CRN)", "pt": "Número de registo comercial (CRN)", "zh_Hans": "工商注册号 / 公司登记代码 (CRN)", "ja": "法人登記番号 (CRN)"
    },
    "Commercial register number / CRN": {
        "ru": "Номер в торговом реестре / ОГРН", "es": "Número de registro mercantil / CRN", "nl": "Handelsregisternummer (KVK)",
        "fr": "Numéro d'immatriculation au RCS", "pt": "Número de registo comercial / CRN", "zh_Hans": "商业登记号 / 工商注册编号", "ja": "商業登記番号"
    },
    "Commercial registry number in state or national records.": {
        "ru": "Номер записи в едином государственном торговом реестре.",
        "es": "Número de inscripción en el registro mercantil estatal o nacional.",
        "nl": "Inschrijfnummer in het handelsregister (bijv. KVK).",
        "fr": "Numéro d'immatriculation au registre du commerce et des sociétés.",
        "pt": "Número de inscrição no registo comercial.",
        "zh_Hans": "在国家市场监管部门登记的工商营业执照注册编号。",
        "ja": "法務局等に登録された商業登記番号。"
    },
    "Accounting Functional Currency": {
        "ru": "Функциональная валюта учета", "es": "Moneda funcional de contabilidad", "nl": "Functionele boekhoudvaluta",
        "fr": "Devise fonctionnelle de comptabilité", "pt": "Moeda funcional de contabilidade", "zh_Hans": "会计本位币", "ja": "会計機能通貨"
    },
    "Functional Currency": {
        "ru": "Функциональная валюта", "es": "Moneda funcional", "nl": "Functionele valuta",
        "fr": "Devise fonctionnelle", "pt": "Moeda funcional", "zh_Hans": "记账本位币", "ja": "機能通貨"
    },
    "Accounting Currency": {
        "ru": "Валюта учета", "es": "Moneda contable", "nl": "Boekhoudvaluta",
        "fr": "Devise comptable", "pt": "Moeda contabilística", "zh_Hans": "记账币种", "ja": "会計通貨"
    },
    "Base currency code (e.g. EUR, USD, GBP)": {
        "ru": "Код базовой валюты (напр., EUR, USD, GBP, RUB)", "es": "Código de moneda base (ej. EUR, USD, GBP)", "nl": "Basisvalutacode (bijv. EUR, USD, GBP)",
        "fr": "Code de la devise de base (ex. EUR, USD, GBP)", "pt": "Código da moeda base (ex. EUR, USD, GBP)", "zh_Hans": "基础币种代码（如 EUR, USD, CNY）", "ja": "基本通貨コード（例：EUR, USD, JPY）"
    },
    "Default currency for ledger balance sheets and summaries.": {
        "ru": "Валюта по умолчанию для балансовых отчетов и финансовой сводки.",
        "es": "Moneda predeterminada para balances y resúmenes contables.",
        "nl": "Standaardvaluta voor balansoverzichten en financiële samenvattingen.",
        "fr": "Devise par défaut pour les bilans et les synthèses comptables.",
        "pt": "Moeda padrão para balancetes e resumos contabilísticos.",
        "zh_Hans": "资产负债表与财务汇总报告使用的默认核算币种。",
        "ja": "貸借対照表や財務サマリーで使用するデフォルト通貨。"
    },
    "Banking & Settlement Accounts": {
        "ru": "Банковские и расчетные счета", "es": "Cuentas bancarias y de liquidación", "nl": "Bank- & Betalingsrekeningen",
        "fr": "Comptes bancaires et de règlement", "pt": "Contas bancárias e de liquidação", "zh_Hans": "银行及结算账户", "ja": "銀行決済口座"
    },
    "Primary Bank IBAN": {
        "ru": "Основной расчетный счет / IBAN", "es": "IBAN bancario principal", "nl": "Primaire bank-IBAN",
        "fr": "IBAN bancaire principal", "pt": "IBAN bancário principal", "zh_Hans": "主银行结算账号 (IBAN)", "ja": "主要銀行口座番号 (IBAN)"
    },
    "Default bank account for receiving customer payments": {
        "ru": "Основной банковский счет для приема платежей от клиентов",
        "es": "Cuenta bancaria predeterminada para recibir pagos de clientes",
        "nl": "Standaard bankrekening voor het ontvangen van klantbetalingen",
        "fr": "Compte bancaire par défaut pour recevoir les paiements des clients",
        "pt": "Conta bancária padrão para receber pagamentos de clientes",
        "zh_Hans": "用于接收客户付款的默认银行账户",
        "ja": "顧客からの入金を受け取る主要口座"
    },
    "SWIFT / BIC Code": {
        "ru": "Код SWIFT / БИК", "es": "Código SWIFT / BIC", "nl": "SWIFT / BIC-code",
        "fr": "Code SWIFT / BIC", "pt": "Código SWIFT / BIC", "zh_Hans": "SWIFT / BIC 代码", "ja": "SWIFT / BIC コード"
    },
    "Contact & Headquarters Address": {
        "ru": "Контакты и юридический адрес", "es": "Contacto y dirección de la sede", "nl": "Contact & Hoofdkantooradres",
        "fr": "Contact et adresse du siège social", "pt": "Contacto e endereço da sede", "zh_Hans": "联系方式与注册地址", "ja": "連絡先および本社所在地"
    },
    "Accounting / Finance Email": {
        "ru": "Email бухгалтерии / финансового отдела", "es": "Correo de contabilidad / finanzas", "nl": "E-mailadres boekhouding / financiën",
        "fr": "Email comptabilité / finances", "pt": "Email de contabilidade / finanças", "zh_Hans": "财务部门官方邮箱", "ja": "経理・財務担当メールアドレス"
    },
    "Official Email": {
        "ru": "Официальный email", "es": "Correo oficial", "nl": "Officieel e-mailadres",
        "fr": "Email officiel", "pt": "Email oficial", "zh_Hans": "官方联系邮箱", "ja": "公式メールアドレス"
    },
    "Registered Address": {
        "ru": "Юридический адрес", "es": "Dirección registrada", "nl": "Statutair adres",
        "fr": "Adresse du siège social", "pt": "Endereço registado", "zh_Hans": "注册营业地址", "ja": "登記上所在地"
    },
    "Save Company Profile": {
        "ru": "Сохранить профиль компании", "es": "Guardar perfil de la empresa", "nl": "Bedrijfsprofiel opslaan",
        "fr": "Enregistrer le profil de l'entreprise", "pt": "Guardar perfil da empresa", "zh_Hans": "保存企业资料", "ja": "会社概要を保存"
    },
    "Company profile updated successfully. AI document classification and ledger rules will now use these entity details.": {
        "ru": "Профиль компании успешно обновлен. Классификация документов ИИ и правила проводок теперь используют эти реквизиты.",
        "es": "Perfil de la empresa actualizado correctamente. La clasificación de documentos por IA y las reglas contables utilizarán estos datos.",
        "nl": "Bedrijfsprofiel succesvol bijgewerkt. AI-documentclassificatie en grootboekregels gebruiken nu deze entiteitsgegevens.",
        "fr": "Profil de l'entreprise mis à jour avec succès. La classification des documents par l'IA et les règles comptables utiliseront désormais ces informations.",
        "pt": "Perfil da empresa atualizado com sucesso. A classificação de documentos por IA e as regras de razão utilizarão agora estes dados.",
        "zh_Hans": "企业资料已成功更新。AI 单据分类与借贷记账规则现已同步采用该主体信息。",
        "ja": "会社概要が正常に更新されました。AIの書類分類と仕訳ルールにこの組織情報が適用されます。"
    },

    # Core Navigation & Header
    "Accounting & Agent": {
        "ru": "Бухгалтерия и AI-агент", "es": "Contabilidad y Agente IA", "nl": "Boekhouding & AI-Agent",
        "fr": "Comptabilité & Agent IA", "pt": "Contabilidade e Agente IA", "zh_Hans": "财务与智能助理", "ja": "会計＆AIエージェント"
    },
    "Collapse Sidebar": {
        "ru": "Свернуть боковую панель", "es": "Contraer barra lateral", "nl": "Zijbalk inklappen",
        "fr": "Réduire la barre latérale", "pt": "Recolher barra lateral", "zh_Hans": "折叠侧边栏", "ja": "サイドバーを折りたたむ"
    },
    "Expand Sidebar": {
        "ru": "Развернуть боковую панель", "es": "Expandir barra lateral", "nl": "Zijbalk uitklappen",
        "fr": "Développer la barre latérale", "pt": "Expandir barra lateral", "zh_Hans": "展开侧边栏", "ja": "サイドバーを展開する"
    },
    "Close Sidebar": {
        "ru": "Закрыть боковую панель", "es": "Cerrar barra lateral", "nl": "Zijbalk sluiten",
        "fr": "Fermer la barre latérale", "pt": "Fechar barra lateral", "zh_Hans": "关闭侧边栏", "ja": "サイドバーを閉じる"
    },
    "Scan Receipt with AI": {
        "ru": "Сканировать чек с помощью ИИ", "es": "Escanear recibo con IA", "nl": "Bon scannen met AI",
        "fr": "Scanner le reçu avec l'IA", "pt": "Digitalizar recibo com IA", "zh_Hans": "使用 AI 扫描单据", "ja": "AIで領収書をスキャン"
    },
    "View Scanned Receipts": {
        "ru": "Смотреть отсканированные чеки", "es": "Ver recibos escaneados", "nl": "Gescande bonnen bekijken",
        "fr": "Voir les reçus numérisés", "pt": "Ver recibos digitalizados", "zh_Hans": "查看已扫描收据", "ja": "スキャン済み領収書を表示"
    },
    "View all scanned receipts in Scanned Records": {
        "ru": "Смотреть все отсканированные чеки в журнале документов", "es": "Ver todos los recibos escaneados en Registros Escaneados", "nl": "Bekijk alle gescande bonnen in Gescande Documenten",
        "fr": "Voir tous les reçus numérisés dans les Documents Numérisés", "pt": "Ver todos os recibos digitalizados nos Registos Digitalizados", "zh_Hans": "在扫描记录中查看所有已扫描收据", "ja": "スキャン済み書類で領収書一覧を表示"
    },
    "Scan Source": {
        "ru": "Источник скана", "es": "Origen del escaneo", "nl": "Scanbron",
        "fr": "Source de numérisation", "pt": "Origem da digitalização", "zh_Hans": "扫描来源", "ja": "スキャンソース"
    },
    "AI Verified Scan": {
        "ru": "Проверено ИИ", "es": "Escaneo verificado por IA", "nl": "AI-geverifieerde scan",
        "fr": "Scan vérifié par l'IA", "pt": "Digitalização verificada por IA", "zh_Hans": "AI 验证扫描件", "ja": "AI検証済みスキャン"
    },
    "Manual Entry": {
        "ru": "Ручной ввод", "es": "Entrada manual", "nl": "Handmatige invoer",
        "fr": "Saisie manuelle", "pt": "Entrada manual", "zh_Hans": "手动录入", "ja": "手動入力"
    },
    "View original scan and AI extracted details": {
        "ru": "Просмотреть исходный скан и данные, извлеченные ИИ", "es": "Ver escaneo original y datos extraídos por IA", "nl": "Bekijk originele scan en door AI geëxtraheerde gegevens",
        "fr": "Voir le scan original et les détails extraits par l'IA", "pt": "Ver digitalização original e detalhes extraídos por IA", "zh_Hans": "查看原始扫描件与 AI 提取详情", "ja": "元のスキャンとAI抽出詳細を表示"
    },
    "Receipt & Expense Voucher Mode": {
        "ru": "Режим чеков и расходных ордеров", "es": "Modo Recibos y Vales de Gasto", "nl": "Modus Bonnen & Onkostennota's",
        "fr": "Mode Reçus & Justificatifs de Dépenses", "pt": "Modo de Recibos e Comprovativos de Despesa", "zh_Hans": "收据与支出凭证模式", "ja": "領収書・出金伝票モード"
    },
    "AI will extract merchant name, receipt date, expense category, VAT/tax, and totals directly into your accounting ledgers.": {
        "ru": "ИИ автоматически извлечет название поставщика, дату, категорию расходов, НДС и итоговую сумму в бухгалтерский журнал.",
        "es": "La IA extraerá el nombre del comercio, fecha, categoría de gasto, IVA y totales directamente en su contabilidad.",
        "nl": "AI extraheert de naam van de handelaar, ontvangstdatum, onkostencategorie, btw en totalen direct in uw grootboek.",
        "fr": "L'IA extraira le commerçant, la date, la catégorie de dépenses, la TVA et les totaux directement dans votre comptabilité.",
        "pt": "A IA extrairá o comerciante, a data, a categoria de despesas, o IVA e os totais diretamente para a sua contabilidade.",
        "zh_Hans": "AI 将自动提取商户名称、单据日期、费用类别、税额及总金额并同步至账簿。",
        "ja": "AIが店舗名、領収日、経費項目、消費税、合計金額を自動抽出し帳簿に記帳します。"
    },
    "Expense Category *": {
        "ru": "Категория расходов *", "es": "Categoría de gasto *", "nl": "Onkostencategorie *",
        "fr": "Catégorie de dépenses *", "pt": "Categoria de despesa *", "zh_Hans": "费用类别 *", "ja": "経費区分 *"
    },
    "e.g. Office Supplies, Fuel, Travel": {
        "ru": "напр., канцтовары, топливо, командировочные", "es": "ej. material de oficina, combustible, viajes", "nl": "bijv. kantoorartikelen, brandstof, reizen",
        "fr": "ex. fournitures de bureau, carburant, déplacements", "pt": "ex. material de escritório, combustível, viagens", "zh_Hans": "例如：办公用品、燃油、差旅", "ja": "例：事務用品、ガソリン代、出張旅費"
    },
    "Travel & Transportation": {
        "ru": "Командировки и транспорт", "es": "Viajes y transporte", "nl": "Reizen en vervoer",
        "fr": "Déplacements & transports", "pt": "Viagens e transporte", "zh_Hans": "差旅与交通", "ja": "旅費交通費"
    },
    "Meals & Entertainment": {
        "ru": "Питание и представительские", "es": "Comidas y representación", "nl": "Maaltijden en representatie",
        "fr": "Repas & réception", "pt": "Refeições e representação", "zh_Hans": "餐饮与招待", "ja": "飲食接待費"
    },
    "Fuel & Vehicle": {
        "ru": "ГСМ и автотранспорт", "es": "Combustible y vehículos", "nl": "Brandstof en voertuigen",
        "fr": "Carburant & véhicules", "pt": "Combustível e veículos", "zh_Hans": "燃油与车辆", "ja": "燃料・車両費"
    },
    "Utilities & Telecom": {
        "ru": "Коммунальные и связь", "es": "Suministros y telecomunicaciones", "nl": "Nutsvoorzieningen en telecom",
        "fr": "Services publics & télécom", "pt": "Serviços públicos e telecomunicações", "zh_Hans": "水电气与通信", "ja": "水道光熱・通信費"
    },
    "Software & IT": {
        "ru": "ПО и IT-услуги", "es": "Software e informática", "nl": "Software en IT",
        "fr": "Logiciels & informatique", "pt": "Software e TI", "zh_Hans": "软件与 IT 服务", "ja": "ソフトウェア・IT費"
    },
    "Repairs & Maintenance": {
        "ru": "Ремонт и обслуживание", "es": "Reparaciones y mantenimiento", "nl": "Reparaties en onderhoud",
        "fr": "Réparations & entretien", "pt": "Reparações e manutenção", "zh_Hans": "维修与保养", "ja": "修繕維持費"
    },
    "General / Other": {
        "ru": "Прочие расходы", "es": "General / Otros", "nl": "Algemeen / Overig",
        "fr": "Général / Autre", "pt": "Geral / Outros", "zh_Hans": "其他通用支出", "ja": "雑費・その他"
    },
    "View in Receipts Ledger": {
        "ru": "Перейти в журнал чеков", "es": "Ver en el libro de recibos", "nl": "Bekijken in het bonnenoverzicht",
        "fr": "Voir dans le registre des reçus", "pt": "Ver no livro de recibos", "zh_Hans": "在收据账本中查看", "ja": "領収書台帳で確認"
    },
    "View Invoices": {
        "ru": "Смотреть счета", "es": "Ver facturas", "nl": "Facturen bekijken",
        "fr": "Voir les factures", "pt": "Ver faturas", "zh_Hans": "查看发票", "ja": "請求書を表示"
    },
    "Reminders check triggered! Generated %(total)s active alert(s) (Payables: %(payables)s, Receivables: %(receivables)s, Overdue: %(overdue)s, Contracts: %(contracts)s, Stock: %(stock)s).": {
        "ru": "Проверка напоминаний выполнена! Создано %(total)s активных оповещений (Кредиторы: %(payables)s, Дебиторы: %(receivables)s, Просрочено: %(overdue)s, Договоры: %(contracts)s, Склад: %(stock)s).",
        "es": "¡Comprobación de recordatorios ejecutada! %(total)s alertas activas generadas (Cuentas por pagar: %(payables)s, Cuentas por cobrar: %(receivables)s, Vencidas: %(overdue)s, Contratos: %(contracts)s, Stock: %(stock)s).",
        "nl": "Herinneringencontrole uitgevoerd! %(total)s actieve meldingen gegenereerd (Crediteuren: %(payables)s, Debiteuren: %(receivables)s, Achterstallig: %(overdue)s, Contracten: %(contracts)s, Voorraad: %(stock)s).",
        "fr": "Vérification des rappels effectuée ! %(total)s alertes actives générées (Dettes fournisseurs: %(payables)s, Créances clients: %(receivables)s, En retard: %(overdue)s, Contrats: %(contracts)s, Stock: %(stock)s).",
        "pt": "Verificação de lembretes executada! %(total)s alertas ativos gerados (Contas a pagar: %(payables)s, Contas a receber: %(receivables)s, Vencidas: %(overdue)s, Contratos: %(contracts)s, Stock: %(stock)s).",
        "zh_Hans": "提醒检查已执行！已生成 %(total)s 条活跃提醒（应付账款: %(payables)s，应收账款: %(receivables)s，逾期: %(overdue)s，合同: %(contracts)s，库存: %(stock)s）。",
        "ja": "リマインダー確認を実行しました！ %(total)s 件のアクティブアラートが生成されました（買掛金: %(payables)s、売掛金: %(receivables)s、期日超過: %(overdue)s、契約: %(contracts)s、在庫: %(stock)s）。"
    },
    "Full payment of %(amount)s %(currency)s recorded! Invoice #%(number)s is now marked as Paid, and the calendar task is completed.": {
        "ru": "Полная оплата %(amount)s %(currency)s зарегистрирована! Счет №%(number)s отмечен как оплаченный, задача в календаре завершена.",
        "es": "¡Pago total de %(amount)s %(currency)s registrado! La factura #%(number)s se ha marcado como pagada y la tarea del calendario se ha completado.",
        "nl": "Volledige betaling van %(amount)s %(currency)s geregistreerd! Factuur #%(number)s is gemarkeerd als betaald en de kalendertaak is voltooid.",
        "fr": "Paiement intégral de %(amount)s %(currency)s enregistré ! La facture n°%(number)s est marquée comme payée et la tâche de calendrier est terminée.",
        "pt": "Pagamento total de %(amount)s %(currency)s registado! A fatura #%(number)s foi marcada como paga e a tarefa do calendário foi concluída.",
        "zh_Hans": "全额付款 %(amount)s %(currency)s 已登记！发票 #%(number)s 已标记为已付款，关联日程任务已完成。",
        "ja": "満額支払 %(amount)s %(currency)s を記録しました！請求書 #%(number)s は支払済となり、カレンダータスクも完了しました。"
    },
    "Partial payment of %(amount)s %(currency)s recorded. Remaining: %(remaining)s %(currency)s.": {
        "ru": "Частичная оплата %(amount)s %(currency)s зарегистрирована. Остаток: %(remaining)s %(currency)s.",
        "es": "Pago parcial de %(amount)s %(currency)s registrado. Restante: %(remaining)s %(currency)s.",
        "nl": "Gedeeltelijke betaling van %(amount)s %(currency)s geregistreerd. Resterend: %(remaining)s %(currency)s.",
        "fr": "Paiement partiel de %(amount)s %(currency)s enregistré. Reste à payer : %(remaining)s %(currency)s.",
        "pt": "Pagamento parcial de %(amount)s %(currency)s registado. Restante: %(remaining)s %(currency)s.",
        "zh_Hans": "部分付款 %(amount)s %(currency)s 已登记。剩余待付: %(remaining)s %(currency)s。",
        "ja": "一部支払 %(amount)s %(currency)s を記録しました。残額: %(remaining)s %(currency)s。"
    },
    "Expense receipt for €%(amount)s recorded.": {
        "ru": "Расходный чек на сумму €%(amount)s зарегистрирован.",
        "es": "Recibo de gasto por €%(amount)s registrado.",
        "nl": "Onkostenbon voor €%(amount)s geregistreerd.",
        "fr": "Reçu de dépenses de €%(amount)s enregistré.",
        "pt": "Recibo de despesa de €%(amount)s registado.",
        "zh_Hans": "支出收据 €%(amount)s 已登记。",
        "ja": "経費領収書（€%(amount)s）が記録されました。"
    },
    "Contract '%(title)s' registered.": {
        "ru": "Договор '%(title)s' успешно зарегистрирован.",
        "es": "Contrato '%(title)s' registrado.",
        "nl": "Contract '%(title)s' geregistreerd.",
        "fr": "Contrat '%(title)s' enregistré.",
        "pt": "Contrato '%(title)s' registado.",
        "zh_Hans": "合同 '%(title)s' 已登记。",
        "ja": "契約 '%(title)s' を登録しました。"
    },
    "Scanned file '%(name)s' successfully processed by AI! Please review extracted data.": {
        "ru": "Файл '%(name)s' успешно обработан ИИ! Проверьте извлеченные данные.",
        "es": "¡El archivo escaneado '%(name)s' fue procesado con éxito por la IA! Revise los datos extraídos.",
        "nl": "Gescand bestand '%(name)s' succesvol verwerkt door AI! Controleer de geëxtraheerde gegevens.",
        "fr": "Fichier numérisé '%(name)s' traité avec succès par l'IA ! Veuillez vérifier les données extraites.",
        "pt": "Ficheiro digitalizado '%(name)s' processado com sucesso pela IA! Por favor, reveja os dados extraídos.",
        "zh_Hans": "扫描文件 '%(name)s' 已通过 AI 成功解析！请核对提取数据。",
        "ja": "スキャンファイル '%(name)s' のAI解析が完了しました！抽出データをご確認ください。"
    },
    "Extraction failed: %(error)s": {
        "ru": "Ошибка извлечения: %(error)s",
        "es": "Extracción fallida: %(error)s",
        "nl": "Extractie mislukt: %(error)s",
        "fr": "Échec de l'extraction : %(error)s",
        "pt": "Falha na extração: %(error)s",
        "zh_Hans": "提取失败: %(error)s",
        "ja": "抽出に失敗しました: %(error)s"
    },
    "Document #%(number)s confirmed! Created ledger records & scheduled calendar tasks.": {
        "ru": "Документ №%(number)s подтвержден! Созданы бухгалтерские записи и задачи в календаре.",
        "es": "¡Documento #%(number)s confirmado! Registros contables y tareas de calendario creados.",
        "nl": "Document #%(number)s bevestigd! Grootboekrecords en kalendertaken aangemaakt.",
        "fr": "Document n°%(number)s confirmé ! Écritures comptables et tâches de calendrier créées.",
        "pt": "Documento #%(number)s confirmado! Registos contabilísticos e tarefas de calendário criados.",
        "zh_Hans": "单据 #%(number)s 已确认！已生成账簿记录并排入日程任务。",
        "ja": "書類 #%(number)s を確認・確定しました！台帳レコードの記帳とカレンダータスクを生成しました。"
    },
    "Error saving records: %(error)s": {
        "ru": "Ошибка сохранения записей: %(error)s",
        "es": "Error al guardar registros: %(error)s",
        "nl": "Fout bij opslaan van records: %(error)s",
        "fr": "Erreur lors de l'enregistrement : %(error)s",
        "pt": "Erro ao guardar registos: %(error)s",
        "zh_Hans": "保存记录出错: %(error)s",
        "ja": "レコード保存エラー: %(error)s"
    },
    "Re-extraction failed: %(error)s": {
        "ru": "Повторное извлечение не удалось: %(error)s",
        "es": "Error en la reextracción: %(error)s",
        "nl": "Opnieuw extraheren mislukt: %(error)s",
        "fr": "Échec de la ré-extraction : %(error)s",
        "pt": "Falha na nova extração: %(error)s",
        "zh_Hans": "重新提取失败: %(error)s",
        "ja": "再抽出に失敗しました: %(error)s"
    },
    "Product with SKU '%(sku)s' already exists.": {
        "ru": "Товар с артикулом '%(sku)s' уже существует.",
        "es": "El producto con SKU '%(sku)s' ya existe.",
        "nl": "Product met SKU '%(sku)s' bestaat al.",
        "fr": "Le produit avec le SKU '%(sku)s' existe déjà.",
        "pt": "O produto com o SKU '%(sku)s' já existe.",
        "zh_Hans": "SKU 为 '%(sku)s' 的商品已存在。",
        "ja": "SKU '%(sku)s' の商品は既に存在します。"
    },
    "Product '%(name)s' [%(sku)s] created successfully.": {
        "ru": "Товар '%(name)s' [%(sku)s] успешно создан.",
        "es": "Producto '%(name)s' [%(sku)s] creado con éxito.",
        "nl": "Product '%(name)s' [%(sku)s] succesvol aangemaakt.",
        "fr": "Produit '%(name)s' [%(sku)s] créé avec succès.",
        "pt": "Produto '%(name)s' [%(sku)s] criado com sucesso.",
        "zh_Hans": "商品 '%(name)s' [%(sku)s] 创建成功。",
        "ja": "商品 '%(name)s' [%(sku)s] を作成しました。"
    },
    "Consignment #%(number)s received! Warehouse stock levels automatically updated.": {
        "ru": "Партия №%(number)s принята! Складские остатки автоматически обновлены.",
        "es": "¡Envío #%(number)s recibido! Los niveles de inventario del almacén se actualizaron automáticamente.",
        "nl": "Zending #%(number)s ontvangen! Magazijnvoorraad automatisch bijgewerkt.",
        "fr": "Envoi n°%(number)s reçu ! Niveaux de stock automatiquement mis à jour.",
        "pt": "Remessa #%(number)s recebida! Níveis de stock do armazém atualizados automaticamente.",
        "zh_Hans": "发货单 #%(number)s 已收货！仓库库存数量已自动更新。",
        "ja": "委託貨物 #%(number)s を検収しました！倉庫在庫数が自動更新されました。"
    },
    "Dashboard": {
        "ru": "Панель управления", "es": "Panel de Control", "nl": "Dashboard",
        "fr": "Tableau de Bord", "pt": "Painel de Controlo", "zh_Hans": "仪表板", "ja": "ダッシュボード"
    },
    "Documents & AI": {
        "ru": "Документы и ИИ", "es": "Documentos e IA", "nl": "Documenten & AI",
        "fr": "Documents & IA", "pt": "Documentos e IA", "zh_Hans": "文档与人工智能", "ja": "書類＆AI解析"
    },
    "AI Provider Settings": {
        "ru": "Настройки AI-провайдеров", "es": "Configuración de Proveedores IA", "nl": "AI-providerinstellingen",
        "fr": "Paramètres des Fournisseurs IA", "pt": "Configurações de Provedores de IA", "zh_Hans": "AI 模型提供商设置", "ja": "AIプロバイダー設定"
    },
    "AI & LLM Configuration": {
        "ru": "Конфигурация AI и LLM", "es": "Configuración de IA y LLM", "nl": "AI & LLM-configuratie",
        "fr": "Configuration IA et LLM", "pt": "Configuração de IA e LLM", "zh_Hans": "AI 与大模型配置", "ja": "AI・LLM設定"
    },
    "AI & LLM Provider Configuration": {
        "ru": "Настройка провайдеров AI и LLM", "es": "Configuración de Proveedores de IA y LLM", "nl": "Configuratie van AI & LLM-providers",
        "fr": "Configuration des Fournisseurs d'IA et LLM", "pt": "Configuração de Provedores de IA e LLM", "zh_Hans": "AI 与大模型提供商配置", "ja": "AI・LLMプロバイダー詳細設定"
    },
    "Select and configure your preferred multimodal AI engine for document extraction and Copilot intelligence.": {
        "ru": "Выберите и настройте мультимодальный AI-движок для анализа документов и работы Copilot.",
        "es": "Seleccione y configure su motor de IA multimodal preferido para la extracción de documentos y Copilot.",
        "nl": "Selecteer en configureer uw gewenste multimodale AI-engine voor documentextractie en Copilot.",
        "fr": "Sélectionnez et configurez votre moteur IA multimodal pour l'extraction de documents et Copilot.",
        "pt": "Selecione e configure seu motor de IA multimodal preferido para extração de documentos e Copilot.",
        "zh_Hans": "选择并配置用于单据解析与 Copilot 智能助手的首选多模态 AI 引擎。",
        "ja": "書類の解析および Copilot 支援に使用するマルチモーダル AI エンジンを選択・設定します。"
    },
    "Active": {
        "ru": "Активен", "es": "Activo", "nl": "Actief",
        "fr": "Actif", "pt": "Ativo", "zh_Hans": "已激活", "ja": "アクティブ"
    },
    "High-speed multimodal AI by Google. Supports native PDF and photo scans with precision extraction.": {
        "ru": "Высокоскоростной мультимодальный ИИ от Google. Прямой анализ PDF и фото с высокой точностью.",
        "es": "IA multimodal de alta velocidad de Google. Admite PDF y fotos con extracción precisa.",
        "nl": "Snelle multimodale AI van Google. Ondersteunt native PDF en scans met nauwkeurige extractie.",
        "fr": "IA multimodale haute vitesse par Google. Prend en charge les PDF et photos avec une grande précision.",
        "pt": "IA multimodal de alta velocidade da Google. Suporta PDF e fotos com extração de alta precisão.",
        "zh_Hans": "谷歌高速多模态 AI，支持原生 PDF 与图片单据的高精度识别提取。",
        "ja": "Googleの高速マルチモーダルAI。ネイティブPDFおよび画像書類の高精度抽出に対応。"
    },
    "Gemini API Key": {
        "ru": "API-ключ Gemini", "es": "Clave API de Gemini", "nl": "Gemini API-sleutel",
        "fr": "Clé API Gemini", "pt": "Chave de API Gemini", "zh_Hans": "Gemini API 密钥", "ja": "Gemini APIキー"
    },
    "Industry standard GPT-4o models with multimodal document inspection and structured JSON schemas.": {
        "ru": "Модели GPT-4o с мультимодальным анализом документов и строгими схемами JSON.",
        "es": "Modelos GPT-4o estándar con inspección multimodal de documentos y esquemas JSON estructurados.",
        "nl": "Standaard GPT-4o modellen met multimodale documentinspectie en gestructureerde JSON-schema's.",
        "fr": "Modèles GPT-4o avec inspection multimodale des documents et schémas JSON structurés.",
        "pt": "Modelos GPT-4o com inspeção multimodal de documentos e esquemas JSON estruturados.",
        "zh_Hans": "业界主流的 GPT-4o 系列模型，具备多模态单据检查与严谨的结构化 JSON 输出能力。",
        "ja": "マルチモーダル文書検査と構造化JSONスキーマを備えた業界標準のGPT-4oモデル。"
    },
    "OpenAI API Key": {
        "ru": "API-ключ OpenAI", "es": "Clave API de OpenAI", "nl": "OpenAI API-sleutel",
        "fr": "Clé API OpenAI", "pt": "Chave de API OpenAI", "zh_Hans": "OpenAI API 密钥", "ja": "OpenAI APIキー"
    },
    "Deep reasoning and native PDF contract analysis with state-of-the-art accuracy and nuanced understanding.": {
        "ru": "Глубокая логика и нативный анализ PDF-договоров с высочайшей точностью и пониманием нюансов.",
        "es": "Razonamiento profundo y análisis nativo de contratos en PDF con máxima precisión.",
        "nl": "Geavanceerde logica en native PDF-contractanalyse met ongeëvenaarde precisie.",
        "fr": "Raisonnement approfondi et analyse native des contrats PDF avec une précision exemplaire.",
        "pt": "Raciocínio profundo e análise nativa de contratos em PDF com máxima precisão.",
        "zh_Hans": "领先的深度逻辑推理与原生 PDF 合同解析能力，具备极高精度与细致理解力。",
        "ja": "高度な推論とネイティブPDF契約書解析により、最高水準の精度と文脈理解を実現。"
    },
    "Anthropic API Key": {
        "ru": "API-ключ Anthropic", "es": "Clave API de Anthropic", "nl": "Anthropic API-sleutel",
        "fr": "Clé API Anthropic", "pt": "Chave de API Anthropic", "zh_Hans": "Anthropic API 密钥", "ja": "Anthropic APIキー"
    },
    "Cost-effective, powerful reasoning model (DeepSeek-V3 / R1) for intelligent ledger automation.": {
        "ru": "Экономичная и мощная модель рассуждений (DeepSeek-V3 / R1) для автоматизации учета.",
        "es": "Modelo de razonamiento potente y económico (DeepSeek-V3 / R1) para la gestión contable.",
        "nl": "Kosteneffectief en krachtig redeneermodel (DeepSeek-V3 / R1) voor slimme boekhouding.",
        "fr": "Modèle de raisonnement puissant et économique (DeepSeek-V3 / R1) pour la comptabilité automatisée.",
        "pt": "Modelo de raciocínio avançado e de baixo custo (DeepSeek-V3 / R1) para automatização de livros fiscais.",
        "zh_Hans": "超高性价比的高性能推理大模型 (DeepSeek-V3 / R1)，智能驱动财务账本自动化。",
        "ja": "スマートな台帳自動化を実現する高コスパ・強力な推論モデル (DeepSeek-V3 / R1)。"
    },
    "DeepSeek API Key": {
        "ru": "API-ключ DeepSeek", "es": "Clave API de DeepSeek", "nl": "DeepSeek API-sleutel",
        "fr": "Clé API DeepSeek", "pt": "Chave de API DeepSeek", "zh_Hans": "DeepSeek API 密钥", "ja": "DeepSeek APIキー"
    },
    "Enterprise Alibaba Cloud DashScope platform with excellent multilingual and vision capabilities.": {
        "ru": "Корпоративная платформа Alibaba Cloud DashScope с отличными возможностями мультиязычности и распознавания.",
        "es": "Plataforma empresarial Alibaba Cloud DashScope con excelentes capacidades multilingües y visuales.",
        "nl": "Enterprise Alibaba Cloud DashScope-platform met uitstekende meertalige en visuele mogelijkheden.",
        "fr": "Plateforme d'entreprise Alibaba Cloud DashScope avec d'excellentes capacités multilingues et visuelles.",
        "pt": "Plataforma corporativa Alibaba Cloud DashScope com excelentes capacidades multilíngues e visuais.",
        "zh_Hans": "阿里云百炼企业级 DashScope 平台，具备出色的多语言理解与视觉解析能力。",
        "ja": "優れた多言語処理と視覚認識能力を備えた Alibaba Cloud DashScope エンタープライズ基盤。"
    },
    "DashScope API Key": {
        "ru": "API-ключ DashScope", "es": "Clave API de DashScope", "nl": "DashScope API-sleutel",
        "fr": "Clé API DashScope", "pt": "Chave de API DashScope", "zh_Hans": "DashScope API 密钥", "ja": "DashScope APIキー"
    },
    "100% private, on-premise AI via Ollama, LM Studio, vLLM, or OpenRouter. Keeps financial data on local hardware.": {
        "ru": "100% приватный локальный ИИ через Ollama, LM Studio, vLLM или OpenRouter. Финансовые данные остаются на вашем сервере.",
        "es": "IA 100% privada y local mediante Ollama, LM Studio, vLLM u OpenRouter. Mantiene los datos en su infraestructura.",
        "nl": "100% privé, lokale AI via Ollama, LM Studio, vLLM of OpenRouter. Houdt financiële gegevens op eigen hardware.",
        "fr": "IA 100% privée en local via Ollama, LM Studio, vLLM ou OpenRouter. Garde les données financières en interne.",
        "pt": "IA 100% privada e local via Ollama, LM Studio, vLLM ou OpenRouter. Mantém os dados no seu próprio hardware.",
        "zh_Hans": "100% 私有化本地 AI 部署 (Ollama, LM Studio, vLLM, OpenRouter)，财务敏感数据全程不出内网。",
        "ja": "Ollama、LM Studio、vLLM、OpenRouter による完全プライベートなローカルAI。社内ハードウェア上で安全に処理。"
    },
    "API Key (Optional for Ollama)": {
        "ru": "API-ключ (необязательно для Ollama)", "es": "Clave API (opcional para Ollama)", "nl": "API-sleutel (optioneel voor Ollama)",
        "fr": "Clé API (optionnel pour Ollama)", "pt": "Chave de API (opcional para Ollama)", "zh_Hans": "API 密钥 (Ollama 可留空)", "ja": "APIキー (Ollamaの場合は省略可)"
    },
    "Model Name": {
        "ru": "Название модели", "es": "Nombre del Modelo", "nl": "Modelnaam",
        "fr": "Nom du Modèle", "pt": "Nome do Modelo", "zh_Hans": "模型名称", "ja": "モデル名"
    },
    "Endpoint Base URL": {
        "ru": "Базовый URL эндпоинта", "es": "URL Base del Endpoint", "nl": "Endpoint Base URL",
        "fr": "URL de Base du Point de Terminaison", "pt": "URL Base do Endpoint", "zh_Hans": "服务端点 Base URL", "ja": "エンドポイント Base URL"
    },
    "Test Ping": {
        "ru": "Тест связи", "es": "Probar Ping", "nl": "Test Ping",
        "fr": "Tester Ping", "pt": "Testar Ping", "zh_Hans": "测试连通性", "ja": "接続テスト"
    },
    "Settings are saved to both database and .env configuration file.": {
        "ru": "Настройки сохраняются в базу данных и в конфигурационный файл .env.",
        "es": "La configuración se guarda tanto en la base de datos como en el archivo .env.",
        "nl": "Instellingen worden opgeslagen in zowel de database als het .env-configuratiebestand.",
        "fr": "Les paramètres sont enregistrés à la fois dans la base de données et dans le fichier .env.",
        "pt": "As configurações são guardadas na base de dados e no ficheiro .env.",
        "zh_Hans": "设置将同步保存至数据库与 .env 环境变量配置文件中。",
        "ja": "設定はデータベースおよび .env 構成ファイルの両方に同期保存されます。"
    },
    "Save & Apply AI Settings": {
        "ru": "Сохранить и применить настройки ИИ", "es": "Guardar y Aplicar Configuración de IA", "nl": "AI-instellingen Opslaan & Toepassen",
        "fr": "Enregistrer et Appliquer les Paramètres IA", "pt": "Guardar e Aplicar Configurações de IA", "zh_Hans": "保存并应用 AI 设置", "ja": "AI設定を保存して適用"
    },
    "AI Configuration successfully updated!": {
        "ru": "Конфигурация ИИ успешно обновлена!", "es": "¡Configuración de IA actualizada con éxito!", "nl": "AI-configuratie succesvol bijgewerkt!",
        "fr": "Configuration IA mise à jour avec succès !", "pt": "Configuração de IA atualizada com sucesso!", "zh_Hans": "AI 配置更新成功！", "ja": "AI設定が正常に更新されました！"
    },
    "AI configuration and active provider updated successfully!": {
        "ru": "Конфигурация ИИ и активный провайдер успешно обновлены!", "es": "¡Configuración de IA y proveedor activo actualizados con éxito!", "nl": "AI-configuratie en actieve provider succesvol bijgewerkt!",
        "fr": "Configuration IA et fournisseur actif mis à jour avec succès !", "pt": "Configuração de IA e provedor ativo atualizados com sucesso!", "zh_Hans": "AI 配置与当前激活提供商已成功更新！", "ja": "AI構成およびアクティブプロバイダーが正常に更新されました！"
    },
    "AI Configuration Required": {
        "ru": "Требуется настройка ИИ", "es": "Se requiere configuración de IA", "nl": "AI-configuratie Vereist",
        "fr": "Configuration IA Requise", "pt": "Configuração de IA Necessária", "zh_Hans": "需要配置 AI 模型", "ja": "AIプロバイダー設定が必要です"
    },
    "Open AI Settings": {
        "ru": "Открыть настройки ИИ", "es": "Abrir Configuración de IA", "nl": "Open AI-instellingen",
        "fr": "Ouvrir les Paramètres IA", "pt": "Abrir Configurações de IA", "zh_Hans": "打开 AI 设置", "ja": "AI設定を開く"
    },
    "Rate Limit Exceeded": {
        "ru": "Превышен лимит запросов", "es": "Límite de Solicitudes Excedido", "nl": "Aanvraaglimiet Overschreden",
        "fr": "Limite de Requêtes Dépassée", "pt": "Limite de Taxa Excedido", "zh_Hans": "模型请求频率超限或配额耗尽", "ja": "利用制限・クォータを超過しました"
    },
    "Switch Provider in AI Settings": {
        "ru": "Сменить провайдера в настройках ИИ", "es": "Cambiar Proveedor en Configuración de IA", "nl": "Wissel van Provider in AI-instellingen",
        "fr": "Changer de Fournisseur dans les Paramètres IA", "pt": "Mudar de Provedor nas Configurações de IA", "zh_Hans": "在 AI 设置中切换模型提供商", "ja": "AI設定でプロバイダーを切り替える"
    },
    "AI Provider Offline / Unreachable": {
        "ru": "AI-сервис отключен или недоступен", "es": "Proveedor de IA Desconectado o Inaccesible", "nl": "AI-provider Offline / Onbereikbaar",
        "fr": "Fournisseur IA Hors Ligne ou Inaccessible", "pt": "Provedor de IA Offline / Inacessível", "zh_Hans": "AI 服务离线或连接不可达", "ja": "AIプロバイダーがオフラインまたは接続不能です"
    },
    "Check Endpoint in AI Settings": {
        "ru": "Проверить эндпоинт в настройках ИИ", "es": "Verificar Endpoint en Configuración de IA", "nl": "Controleer Endpoint in AI-instellingen",
        "fr": "Vérifier le Point de Terminaison dans les Paramètres IA", "pt": "Verificar Endpoint nas Configurações de IA", "zh_Hans": "在 AI 设置中检查服务端点", "ja": "AI設定でエンドポイントを確認する"
    },
    "Authentication Failed": {
        "ru": "Ошибка аутентификации", "es": "Error de Autenticación", "nl": "Authenticatie Mislukt",
        "fr": "Échec de l'Authentification", "pt": "Falha na Autenticação", "zh_Hans": "身份验证失败", "ja": "認証に失敗しました"
    },
    "Update API Key in AI Settings": {
        "ru": "Обновить API-ключ в настройках ИИ", "es": "Actualizar Clave API en Configuración de IA", "nl": "Werk API-sleutel bij in AI-instellingen",
        "fr": "Mettre à Jour la Clé API dans les Paramètres IA", "pt": "Atualizar Chave de API nas Configurações de IA", "zh_Hans": "在 AI 设置中更新 API 密钥", "ja": "AI設定で API キーを更新する"
    },
    "AI Execution Failed": {
        "ru": "Ошибка выполнения ИИ", "es": "Error en la Ejecución de IA", "nl": "AI-uitvoering Mislukt",
        "fr": "Échec de l'Exécution de l'IA", "pt": "Falha na Execução da IA", "zh_Hans": "AI 处理执行失败", "ja": "AI処理の実行に失敗しました"
    },
    "AI Document Extraction Alert": {
        "ru": "Оповещение об извлечении документа через ИИ", "es": "Alerta de Extracción de Documento por IA", "nl": "Melding AI-documentextractie",
        "fr": "Alerte d'Extraction de Document par IA", "pt": "Alerta de Extração de Documento por IA", "zh_Hans": "AI 单据解析提示", "ja": "AI書類抽出アラート"
    },
    "Configure AI Settings": {
        "ru": "Настроить параметры ИИ", "es": "Configurar Ajustes de IA", "nl": "AI-instellingen Configureren",
        "fr": "Configurer les Paramètres IA", "pt": "Configurar Definições de IA", "zh_Hans": "配置 AI 设置", "ja": "AI環境を設定する"
    },
    "Or run in terminal:": {
        "ru": "Или выполните в терминале:", "es": "O ejecute en la terminal:", "nl": "Of voer uit in de terminal:",
        "fr": "Ou exécutez dans le terminal :", "pt": "Ou execute no terminal:", "zh_Hans": "或在终端中运行：", "ja": "またはターミナルで実行："
    },
    "Documents": {
        "ru": "Документы", "es": "Documentos", "nl": "Documenten",
        "fr": "Documents", "pt": "Documentos", "zh_Hans": "单据中心", "ja": "書類管理"
    },
    "Scanned Records": {
        "ru": "Скан-копии документов", "es": "Documentos Escaneados", "nl": "Gescande Documenten",
        "fr": "Documents Numérisés", "pt": "Documentos Digitalizados", "zh_Hans": "扫描单据记录", "ja": "スキャン書類一覧"
    },
    "Scanned Records Management": {
        "ru": "Управление отсканированными документами", "es": "Gestión de Documentos Escaneados", "nl": "Beheer van Gescande Documenten",
        "fr": "Gestion des Documents Numérisés", "pt": "Gestão de Documentos Digitalizados", "zh_Hans": "扫描单据管理", "ja": "スキャン書類管理"
    },
    "Upload & Ingest": {
        "ru": "Загрузка и обработка", "es": "Subir y Procesar", "nl": "Uploaden & Verwerken",
        "fr": "Téléverser & Traiter", "pt": "Carregar e Processar", "zh_Hans": "上传与智能解析", "ja": "アップロード＆解析"
    },
    "Upload": {
        "ru": "Загрузить", "es": "Subir", "nl": "Uploaden",
        "fr": "Téléverser", "pt": "Carregar", "zh_Hans": "上传", "ja": "登録"
    },
    "Accounting": {
        "ru": "Бухгалтерия", "es": "Contabilidad", "nl": "Boekhouding",
        "fr": "Comptabilité", "pt": "Contabilidade", "zh_Hans": "财务核算", "ja": "会計・財務"
    },
    "Invoices (AP/AR)": {
        "ru": "Счета (Кредиторка/Дебиторка)", "es": "Facturas (Pagar/Cobrar)", "nl": "Facturen (Crediteuren/Debiteuren)",
        "fr": "Factures (Fournisseurs/Clients)", "pt": "Faturas (Pagar/Receber)", "zh_Hans": "发票管理 (应付/应收)", "ja": "請求書 (買掛金/売掛金)"
    },
    "Invoices": {
        "ru": "Счета", "es": "Facturas", "nl": "Facturen",
        "fr": "Factures", "pt": "Faturas", "zh_Hans": "发票", "ja": "請求書"
    },
    "Invoice": {
        "ru": "Счет", "es": "Factura", "nl": "Factuur",
        "fr": "Facture", "pt": "Fatura", "zh_Hans": "发票", "ja": "請求書"
    },
    "Invoices & Payments": {
        "ru": "Счета и платежи", "es": "Facturas y Pagos", "nl": "Facturen & Betalingen",
        "fr": "Factures & Paiements", "pt": "Faturas e Pagamentos", "zh_Hans": "发票与收支款项", "ja": "請求書＆支払管理"
    },
    "Invoices & Payments (AP/AR)": {
        "ru": "Счета и платежи (Кредиторка/Дебиторка)", "es": "Facturas y Pagos (Pagar/Cobrar)", "nl": "Facturen & Betalingen (Crediteuren/Debiteuren)",
        "fr": "Factures & Paiements (Fournisseurs/Clients)", "pt": "Faturas e Pagamentos (Pagar/Receber)", "zh_Hans": "发票与收支管理 (应付/应收)", "ja": "請求書＆支払管理 (買掛金/売掛金)"
    },
    "Accounts Payable & Receivable": {
        "ru": "Кредиторская и дебиторская задолженность", "es": "Cuentas por Pagar y Cobrar", "nl": "Crediteuren en Debiteuren",
        "fr": "Comptabilité Fournisseurs et Clients", "pt": "Contas a Pagar e a Receber", "zh_Hans": "应付账款与应收账款", "ja": "買掛金・売掛金管理"
    },
    "Receipts & Expenses": {
        "ru": "Чеки и расходы", "es": "Recibos y Gastos", "nl": "Bonnetjes & Uitgaven",
        "fr": "Reçus & Dépenses", "pt": "Recibos e Despesas", "zh_Hans": "收据与费用报销", "ja": "領収書＆経費精算"
    },
    "Receipts & Petty Cash": {
        "ru": "Чеки и мелкие расходы", "es": "Recibos y Caja Chica", "nl": "Bonnetjes & Kleine Kas",
        "fr": "Reçus & Petite Caisse", "pt": "Recibos e Caixa Pequena", "zh_Hans": "收据与零用现金", "ja": "領収書＆小口現金"
    },
    "Operations & Admin": {
        "ru": "Операции и управление", "es": "Operaciones y Administración", "nl": "Operaties & Beheer",
        "fr": "Opérations & Administration", "pt": "Operações e Administração", "zh_Hans": "综合运营与管理", "ja": "業務・総務管理"
    },
    "Operations": {
        "ru": "Операции", "es": "Operaciones", "nl": "Operaties",
        "fr": "Opérations", "pt": "Operações", "zh_Hans": "业务运营", "ja": "業務管理"
    },
    "Administration": {
        "ru": "Управление", "es": "Administración", "nl": "Beheer",
        "fr": "Administration", "pt": "Administração", "zh_Hans": "企业管理", "ja": "総務・管理"
    },
    "Calendar & Tasks": {
        "ru": "Календарь и задачи", "es": "Calendario y Tareas", "nl": "Agenda & Taken",
        "fr": "Calendrier & Tâches", "pt": "Calendário e Tarefas", "zh_Hans": "日历日程与任务", "ja": "カレンダー＆タスク"
    },
    "Company Calendar & Tasks": {
        "ru": "Календарь компании и задачи", "es": "Calendario de la Empresa y Tareas", "nl": "Bedrijfsagenda & Taken",
        "fr": "Calendrier d'Entreprise & Tâches", "pt": "Calendário da Empresa e Tarefas", "zh_Hans": "企业日历与任务中心", "ja": "全社カレンダー＆タスク管理"
    },
    "Operational & Financial Calendar": {
        "ru": "Операционный и финансовый календарь", "es": "Calendario Operativo y Financiero", "nl": "Operationele & Financiële Agenda",
        "fr": "Calendrier Opérationnel et Financier", "pt": "Calendário Operacional e Financeiro", "zh_Hans": "运营与财务日历", "ja": "業務・財務カレンダー"
    },
    "Warehouse & Stock": {
        "ru": "Склад и запасы", "es": "Almacén e Inventario", "nl": "Magazijn & Voorraad",
        "fr": "Entrepôt & Stocks", "pt": "Armazém e Inventário", "zh_Hans": "仓储与库存", "ja": "倉庫＆在庫管理"
    },
    "Warehouse & Inventory": {
        "ru": "Склад и инвентарь", "es": "Almacén e Inventario", "nl": "Magazijn & Voorraad",
        "fr": "Entrepôt & Stocks", "pt": "Armazém e Inventário", "zh_Hans": "仓库与库存", "ja": "倉庫＆在庫"
    },
    "Warehouse Inventory": {
        "ru": "Складские запасы", "es": "Inventario de Almacén", "nl": "Magazijnvoorraad",
        "fr": "Inventaire d'Entrepôt", "pt": "Inventário de Armazém", "zh_Hans": "仓库库存明细", "ja": "倉庫在庫一覧"
    },
    "Warehouse & Inventory Management": {
        "ru": "Управление складом и запасами", "es": "Gestión de Almacén e Inventario", "nl": "Magazijn- & Voorraadbeheer",
        "fr": "Gestion d'Entrepôt et des Stocks", "pt": "Gestão de Armazém e Inventário", "zh_Hans": "仓库与库存管理", "ja": "倉庫・在庫総合管理"
    },
    "Consignments": {
        "ru": "Накладные", "es": "Albaranes / Envíos", "nl": "Leveringen & Vrachtbrieven",
        "fr": "Bordereaux de Livraison", "pt": "Guias de Remessa / Entregas", "zh_Hans": "发货与送货单", "ja": "納品書・受領証"
    },
    "Consignment": {
        "ru": "Накладная", "es": "Albarán", "nl": "Levering",
        "fr": "Bordereau", "pt": "Guia de Remessa", "zh_Hans": "送货单", "ja": "納品書"
    },
    "Consignments & Waybills": {
        "ru": "Накладные и транспортные листы", "es": "Albaranes y Guías de Transporte", "nl": "Leveringen en Vrachtbrieven",
        "fr": "Bordereaux et Lettres de Voiture", "pt": "Guias de Remessa e Transporte", "zh_Hans": "送货单与物流运单", "ja": "納品書・運送状管理"
    },
    "Consignments & Delivery Slips": {
        "ru": "Накладные и квитанции о доставке", "es": "Albaranes y Guías de Entrega", "nl": "Leveringen en Afleverbonnen",
        "fr": "Bordereaux et Bons de Livraison", "pt": "Guias de Remessa e Recibos de Entrega", "zh_Hans": "发货运单与交付清单", "ja": "納品伝票・受領書"
    },
    "Counterparties": {
        "ru": "Контрагенты", "es": "Contrapartes", "nl": "Relaties / Tegenpartijen",
        "fr": "Tiers & Partenaires", "pt": "Entidades / Fornecedores", "zh_Hans": "往来企业 (供应商/客户)", "ja": "取引先一覧"
    },
    "Counterparties Directory": {
        "ru": "Справочник контрагентов", "es": "Directorio de Contrapartes", "nl": "Relatieoverzicht",
        "fr": "Répertoire des Tiers", "pt": "Diretório de Entidades", "zh_Hans": "往来单位名录", "ja": "取引先台帳"
    },
    "Counterparties & Vendors Directory": {
        "ru": "Справочник поставщиков и клиентов", "es": "Directorio de Contrapartes y Proveedores", "nl": "Overzicht van Relaties & Leveranciers",
        "fr": "Répertoire des Tiers et Fournisseurs", "pt": "Diretório de Entidades e Fornecedores", "zh_Hans": "供应商与客户档案目录", "ja": "取引先・仕入先台帳"
    },
    "Contracts": {
        "ru": "Договоры", "es": "Contratos", "nl": "Contracten",
        "fr": "Contrats", "pt": "Contratos", "zh_Hans": "商业合同", "ja": "契約書管理"
    },
    "Contracts Registry": {
        "ru": "Реестр договоров", "es": "Registro de Contratos", "nl": "Contractenregister",
        "fr": "Registre des Contrats", "pt": "Registo de Contratos", "zh_Hans": "合同管理档案", "ja": "契約台帳"
    },
    "Contracts & Agreements Registry": {
        "ru": "Реестр договоров и соглашений", "es": "Registro de Contratos y Acuerdos", "nl": "Register van Contracten & Overeenkomsten",
        "fr": "Registre des Contrats et Accords", "pt": "Registo de Contratos e Acordos", "zh_Hans": "商业合同与合作协议名录", "ja": "契約・協定台帳"
    },
    "Alerts": {
        "ru": "Уведомления", "es": "Alertas", "nl": "Meldingen",
        "fr": "Alertes", "pt": "Alertas", "zh_Hans": "预警提醒", "ja": "アラート"
    },
    "Notifications": {
        "ru": "Уведомления", "es": "Notificaciones", "nl": "Notificaties",
        "fr": "Notifications", "pt": "Notificações", "zh_Hans": "通知消息", "ja": "通知一覧"
    },
    "Proactive Reminders & Notifications": {
        "ru": "Упреждающие напоминания и уведомления", "es": "Recordatorios Proactivos y Notificaciones", "nl": "Proactieve Herinneringen & Notificaties",
        "fr": "Rappels Proactifs & Notifications", "pt": "Lembretes Proativos e Notificações", "zh_Hans": "主动提醒与预警通知", "ja": "事前リマインダー＆通知"
    },
    "Proactive Reminders & Alerts": {
        "ru": "Упреждающие напоминания и оповещения", "es": "Recordatorios Proactivos y Alertas", "nl": "Proactieve Herinneringen & Meldingen",
        "fr": "Rappels Proactifs & Alertes", "pt": "Lembretes Proativos e Alertas", "zh_Hans": "主动到期提醒与事件预警", "ja": "事前リマインダー＆アラート"
    },
    "AI Copilot Assistant": {
        "ru": "AI-ассистент Copilot", "es": "Asistente Copilot IA", "nl": "AI Copilot Assistent",
        "fr": "Assistant Copilot IA", "pt": "Assistente Copilot IA", "zh_Hans": "AI 智能副驾驶助理", "ja": "AI コパイロット"
    },
    "ERP AI Copilot": {
        "ru": "ERP AI Copilot", "es": "Copilot IA del ERP", "nl": "ERP AI Copilot",
        "fr": "Copilot IA ERP", "pt": "Copilot IA do ERP", "zh_Hans": "ERP AI 智能副驾驶", "ja": "ERP AI コパイロット"
    },
    "Real-time ledger & calendar intelligence": {
        "ru": "Интеллектуальный анализ учета и календаря в реальном времени", "es": "Inteligencia en tiempo real para libros y calendario", "nl": "Realtime inzicht in grootboek en agenda",
        "fr": "Intelligence en temps réel pour le grand livre et l'agenda", "pt": "Inteligência em tempo real para contabilidade e calendário", "zh_Hans": "实时账本与日历智能分析", "ja": "元帳とカレンダーのリアルタイムインテリジェンス"
    },
    "Check Reminders": {
        "ru": "Проверить напоминания", "es": "Comprobar Recordatorios", "nl": "Herinneringen Controleren",
        "fr": "Vérifier les Rappels", "pt": "Verificar Lembretes", "zh_Hans": "检查到期提醒", "ja": "リマインダー確認"
    },
    "Proactive Alerts": {
        "ru": "Упреждающие уведомления", "es": "Alertas Proactivas", "nl": "Proactieve Meldingen",
        "fr": "Alertes Proactives", "pt": "Alertas Proativos", "zh_Hans": "主动预警提醒", "ja": "事前通知アラート"
    },
    "View All": {
        "ru": "Смотреть все", "es": "Ver Todo", "nl": "Alles Bekijken",
        "fr": "Voir Tout", "pt": "Ver Tudo", "zh_Hans": "查看全部", "ja": "すべて表示"
    },
    "Take Action": {
        "ru": "Принять меры", "es": "Tomar Medidas", "nl": "Actie Ondernemen",
        "fr": "Agir", "pt": "Agir", "zh_Hans": "立即处理", "ja": "対応する"
    },
    "ago": {
        "ru": "назад", "es": "hace", "nl": "geleden",
        "fr": "il y a", "pt": "atrás", "zh_Hans": "前", "ja": "前"
    },
    "Upload Scan": {
        "ru": "Загрузить скан", "es": "Subir Escaneo", "nl": "Scan Uploaden",
        "fr": "Téléverser Scan", "pt": "Carregar Digitalização", "zh_Hans": "上传扫描件", "ja": "スキャン読込"
    },
    "Upload New Scan": {
        "ru": "Загрузить новый скан", "es": "Subir Nuevo Escaneo", "nl": "Nieuwe Scan Uploaden",
        "fr": "Téléverser un Nouveau Scan", "pt": "Carregar Nova Digitalização", "zh_Hans": "上传新扫描件", "ja": "新規スキャン登録"
    },
    "Upload Scanned Record": {
        "ru": "Загрузить скан документа", "es": "Subir Documento Escaneado", "nl": "Gescand Document Uploaden",
        "fr": "Téléverser un Document Numérisé", "pt": "Carregar Documento Digitalizado", "zh_Hans": "上传扫描单据", "ja": "スキャン書類の登録"
    },
    "Upload Scanned Document": {
        "ru": "Загрузка отсканированного документа", "es": "Subir Documento Escaneado", "nl": "Gescand Document Uploaden",
        "fr": "Téléverser un Document Numérisé", "pt": "Carregar Documento Digitalizado", "zh_Hans": "上传扫描业务单据", "ja": "スキャン書類のアップロード"
    },
    "Company Operational Dashboard": {
        "ru": "Операционная панель управления компании", "es": "Panel Operativo de la Empresa", "nl": "Operationeel Bedrijfsdashboard",
        "fr": "Tableau de Bord Opérationnel de l'Entreprise", "pt": "Painel Operacional da Empresa", "zh_Hans": "企业综合运营工作台", "ja": "全社業務ダッシュボード"
    },
    "Autonomous records management, invoice tracking, warehouse stock, and calendar automation.": {
        "ru": "Автономное управление документами, отслеживание счетов, складских остатков и автоматизация задач.",
        "es": "Gestión autónoma de documentos, seguimiento de facturas, stock de almacén y automatización de calendario.",
        "nl": "Autonoom documentbeheer, factuuropvolging, magazijnvoorraad en agenda-automatisering.",
        "fr": "Gestion autonome des documents, suivi des factures, stocks d'entrepôt et automatisation du calendrier.",
        "pt": "Gestão autónoma de documentos, acompanhamento de faturas, stocks de armazém e automatização de calendário.",
        "zh_Hans": "自动化单据归档、发票跟踪、仓储库存与日程任务协同管理。",
        "ja": "書類の自動管理、請求書追跡、在庫管理、カレンダー連携の自動化システム。"
    },
    "Consult AI Copilot": {
        "ru": "Консультация с AI Copilot", "es": "Consultar Copilot IA", "nl": "Raadpleeg AI Copilot",
        "fr": "Consulter le Copilot IA", "pt": "Consultar Copilot IA", "zh_Hans": "咨询 AI 副驾驶", "ja": "AIコパイロットに相談"
    },
    "Urgent: Invoice(s) Overdue": {
        "ru": "Срочно: Просрочены счета", "es": "Urgente: Factura(s) Vencida(s)", "nl": "Urgent: Vervallen Factu(u)r(en)",
        "fr": "Urgent: Facture(s) en Retard", "pt": "Urgente: Fatura(s) Vencida(s)", "zh_Hans": "紧急提醒：发票已逾期", "ja": "至急：支払期限超過の請求書"
    },
    "There are overdue obligations requiring immediate payment or collection action.": {
        "ru": "Есть просроченные обязательства, требующие немедленной оплаты или взыскания.",
        "es": "Existen obligaciones vencidas que requieren pago o cobro inmediato.",
        "nl": "Er zijn achterstallige verplichtingen die onmiddellijke betaling of incasso vereisen.",
        "fr": "Il existe des obligations en retard nécessitant un paiement ou recouvrement immédiat.",
        "pt": "Existem obrigações vencidas que exigem pagamento ou cobrança imediata.",
        "zh_Hans": "存在已逾期的款项，需要立即安排付款或发起催收。",
        "ja": "支払期限が超過している案件があります。速やかに支払または回収を行ってください。"
    },
    "View All Overdue": {
        "ru": "Все просроченные", "es": "Ver Vencidas", "nl": "Bekijk Alle Achterstallige",
        "fr": "Voir Toutes les Factures en Retard", "pt": "Ver Faturas Vencidas", "zh_Hans": "查看全部逾期账单", "ja": "超過案件をすべて確認"
    },
    "Outgoing Payables": {
        "ru": "К оплате поставщикам", "es": "Pagos Pendientes (Acreedores)", "nl": "Te Betalen Facturen (Crediteuren)",
        "fr": "Dettes Fournisseurs (À Payer)", "pt": "Pagamentos Pendentes (Fornecedores)", "zh_Hans": "待付账款 (应付款)", "ja": "買掛金 (支払予定)"
    },
    "Outgoing Payables (We Owe)": {
        "ru": "Исходящие платежи (наш долг)", "es": "Pagos Pendientes (Acreedores)", "nl": "Te Betalen (Uitgaand)",
        "fr": "Dettes Fournisseurs (Nous Devons)", "pt": "Pagamentos Pendentes (Nós Devemos)", "zh_Hans": "待付款项 (公司应付)", "ja": "買掛金 (当社支払分)"
    },
    "Track vendor bills": {
        "ru": "Счета поставщиков", "es": "Facturas de proveedores", "nl": "Leveranciersfacturen opvolgen",
        "fr": "Suivi des factures fournisseurs", "pt": "Faturas de fornecedores", "zh_Hans": "跟踪供应商发票", "ja": "仕入先請求書を確認"
    },
    "Expected Receivables": {
        "ru": "Ожидаемые поступления", "es": "Cobros Esperados (Deudores)", "nl": "Verwachte Ontvangsten (Debiteuren)",
        "fr": "Créances Clients (À Recevoir)", "pt": "Recebimentos Esperados (Clientes)", "zh_Hans": "待收账款 (应收款)", "ja": "売掛金 (入金予定)"
    },
    "Expected Receivables (Incoming)": {
        "ru": "Ожидаемая дебиторка (входящие)", "es": "Cobros Esperados (Ingresos)", "nl": "Verwachte Ontvangsten (Inkomend)",
        "fr": "Créances Clients (Entrantes)", "pt": "Recebimentos Esperados (Entradas)", "zh_Hans": "待收款项 (预期收入)", "ja": "売掛金 (回収見込分)"
    },
    "Customer payments": {
        "ru": "Платежи клиентов", "es": "Pagos de clientes", "nl": "Klantbetalingen",
        "fr": "Paiements clients", "pt": "Pagamentos de clientes", "zh_Hans": "客户回款", "ja": "顧客からの入金"
    },
    "Customer payments expected": {
        "ru": "Ожидаемые платежи клиентов", "es": "Pagos de clientes esperados", "nl": "Verwachte klantbetalingen",
        "fr": "Paiements clients attendus", "pt": "Pagamentos de clientes esperados", "zh_Hans": "预期客户应收款", "ja": "回収見込の顧客入金"
    },
    "Net Position": {
        "ru": "Чистая позиция", "es": "Posición Neta", "nl": "Netto Positie",
        "fr": "Position Nette", "pt": "Posição Líquida", "zh_Hans": "资金净头寸", "ja": "純資金ポジション"
    },
    "Projected balance": {
        "ru": "Прогнозный баланс", "es": "Saldo proyectado", "nl": "Verwachte marge",
        "fr": "Solde prévisionnel", "pt": "Saldo projetado", "zh_Hans": "预计结余", "ja": "予測残高"
    },
    "Expected cash margin": {
        "ru": "Ожидаемая денежная маржа", "es": "Margen de caja esperado", "nl": "Verwachte cashmarge",
        "fr": "Marge de trésorerie prévue", "pt": "Margem de caixa esperada", "zh_Hans": "预计流动资金差额", "ja": "予測資金マージン"
    },
    "Low Stock SKUs": {
        "ru": "Товары с низким остатком", "es": "Artículos con Stock Bajo", "nl": "Lage Voorraad Artikelen",
        "fr": "Articles en Rupture Proche", "pt": "Itens com Stock Baixo", "zh_Hans": "低库存预警商品", "ja": "在庫僅少商品"
    },
    "Low Stock Warnings": {
        "ru": "Предупреждения о низком запасе", "es": "Alertas de Stock Bajo", "nl": "Waarschuwingen Lage Voorraad",
        "fr": "Alertes Stock Faible", "pt": "Alertas de Stock Baixo", "zh_Hans": "库存短缺预警", "ja": "在庫僅少警告"
    },
    "Check inventory": {
        "ru": "Проверить остатки", "es": "Ver inventario", "nl": "Voorraad controleren",
        "fr": "Vérifier les stocks", "pt": "Verificar inventário", "zh_Hans": "检查当前库存", "ja": "在庫を確認"
    },
    "Scanned Records Awaiting Review": {
        "ru": "Сканы, ожидающие подтверждения", "es": "Documentos Pendientes de Revisión", "nl": "Documenten die Wachten op Goedkeuring",
        "fr": "Documents en Attente de Validation", "pt": "Documentos a Aguardar Revisão", "zh_Hans": "待审核扫描单据", "ja": "確認待ちのスキャン書類"
    },
    "View All Documents": {
        "ru": "Все документы", "es": "Ver Todos los Documentos", "nl": "Alle Documenten Weergeven",
        "fr": "Voir Tous les Documents", "pt": "Ver Todos os Documentos", "zh_Hans": "查看所有单据", "ja": "すべての書類を表示"
    },
    "Type": {
        "ru": "Тип", "es": "Tipo", "nl": "Type",
        "fr": "Type", "pt": "Tipo", "zh_Hans": "类型", "ja": "種別"
    },
    "Uploaded": {
        "ru": "Загружено", "es": "Subido", "nl": "Geüpload",
        "fr": "Téléversé", "pt": "Carregado", "zh_Hans": "上传于", "ja": "登録日時"
    },
    "Review & Commit": {
        "ru": "Проверить и сохранить", "es": "Revisar y Guardar", "nl": "Controleren & Opslaan",
        "fr": "Vérifier & Enregistrer", "pt": "Rever e Guardar", "zh_Hans": "审核并记账", "ja": "確認・元帳登録"
    },
    "No documents awaiting review. All uploaded scans have been confirmed!": {
        "ru": "Нет документов на проверку. Все загруженные сканы подтверждены!",
        "es": "¡No hay documentos pendientes de revisión! Todos los escaneos han sido confirmados.",
        "nl": "Geen documenten ter beoordeling. Alle geüploade scans zijn bevestigd!",
        "fr": "Aucun document en attente. Tous les scans téléversés ont été confirmés !",
        "pt": "Nenhum documento pendente. Todos os documentos foram confirmados!",
        "zh_Hans": "暂无待审核单据。所有上传的扫描件均已确认入账！",
        "ja": "確認待ちの書類はありません。すべてのスキャン書類が登録済みです。"
    },
    "Upcoming Tasks & Payments (Next 7 Days)": {
        "ru": "Ближайшие задачи и платежи (следующие 7 дней)", "es": "Próximas Tareas y Pagos (Siguientes 7 Días)", "nl": "Aankomende Taken & Betalingen (Komende 7 Dagen)",
        "fr": "Tâches & Échéances à Venir (7 Prochains Jours)", "pt": "Próximas Tarefas e Pagamentos (Próximos 7 Dias)", "zh_Hans": "未来7天任务与款项日程", "ja": "今後の予定＆支払期限 (直近7日間)"
    },
    "Open Full Calendar": {
        "ru": "Открыть весь календарь", "es": "Abrir Calendario Completo", "nl": "Volledige Agenda Openen",
        "fr": "Ouvrir le Calendrier Complet", "pt": "Abrir Calendário Completo", "zh_Hans": "打开完整日历", "ja": "全体カレンダーを表示"
    },
    "Due": {
        "ru": "Срок", "es": "Vence", "nl": "Vervaldatum",
        "fr": "Échéance", "pt": "Vencimento", "zh_Hans": "到期日", "ja": "期日"
    },
    "Due Date": {
        "ru": "Срок оплаты", "es": "Fecha de Vencimiento", "nl": "Vervaldatum",
        "fr": "Date d'Échéance", "pt": "Data de Vencimento", "zh_Hans": "付款到期日", "ja": "支払期限"
    },
    "Amount": {
        "ru": "Сумма", "es": "Importe", "nl": "Bedrag",
        "fr": "Montant", "pt": "Valor", "zh_Hans": "金额", "ja": "金額"
    },
    "View Bill": {
        "ru": "Смотреть счет", "es": "Ver Factura", "nl": "Factuur Bekijken",
        "fr": "Voir la Facture", "pt": "Ver Fatura", "zh_Hans": "查看账单", "ja": "請求書を表示"
    },
    "No tasks due in the next 7 days.": {
        "ru": "Нет запланированных задач на ближайшие 7 дней.", "es": "No hay tareas programadas para los próximos 7 días.", "nl": "Geen taken gepland voor de komende 7 dagen.",
        "fr": "Aucune tâche prévue dans les 7 prochains jours.", "pt": "Nenhuma tarefa agendada para os próximos 7 dias.", "zh_Hans": "未来7天内没有即将到期的任务。", "ja": "直近7日間に期限を迎えるタスクはありません。"
    },
    "Quick Actions": {
        "ru": "Быстрые действия", "es": "Acciones Rápidas", "nl": "Snelle Acties",
        "fr": "Actions Rapides", "pt": "Ações Rápidas", "zh_Hans": "快捷操作", "ja": "クイックアクション"
    },
    "Calendar Sync": {
        "ru": "Синхронизация календаря", "es": "Sincronizar Calendario", "nl": "Agenda Synchronisatie",
        "fr": "Synchronisation Calendrier", "pt": "Sincronização de Calendário", "zh_Hans": "日历同步订阅", "ja": "カレンダー同期"
    },
    "Inventory Stock": {
        "ru": "Складские запасы", "es": "Stock de Inventario", "nl": "Magazijnvoorraad",
        "fr": "Stock d'Entrepôt", "pt": "Stock de Armazém", "zh_Hans": "仓储库存", "ja": "倉庫在庫"
    },
    "Ask ERP AI Copilot": {
        "ru": "Спросить ERP AI Copilot", "es": "Preguntar a Copilot IA", "nl": "Vraag de ERP AI Copilot",
        "fr": "Demander au Copilot IA", "pt": "Perguntar ao Copilot IA", "zh_Hans": "向 ERP AI 提问", "ja": "ERP AIに質問"
    },
    "Ask questions in natural language. The AI agent scans company ledgers, calendars, and warehouse stock in real-time.": {
        "ru": "Задавайте вопросы на обычном языке. ИИ-агент сканирует бухгалтерские книги, календарь и остатки на складе.",
        "es": "Haga preguntas en lenguaje natural. El agente IA escanea libros contables, calendarios y almacén en tiempo real.",
        "nl": "Stel vragen in natuurlijke taal. De AI-agent controleert grootboeken, agenda's en voorraad in realtime.",
        "fr": "Posez des questions en langage naturel. L'agent IA analyse les grands livres, calendriers et stocks en temps réel.",
        "pt": "Faça perguntas em linguagem natural. O agente IA analisa livros contabilísticos, calendários e armazém em tempo real.",
        "zh_Hans": "支持自然语言对话，AI 代理实时查询企业账本、日历日程与库存变动。",
        "ja": "自然な言葉で質問できます。AIが台帳、カレンダー、倉庫在庫をリアルタイムに検索します。"
    },
    "What bills are due this week?": {
        "ru": "Какие счета нужно оплатить на этой неделе?", "es": "¿Qué facturas vencen esta semana?", "nl": "Welke rekeningen vervallen deze week?",
        "fr": "Quelles factures arrivent à échéance cette semaine ?", "pt": "Que faturas vencem esta semana?", "zh_Hans": "本周有哪些账单即将到期？", "ja": "今週期限を迎える請求書は何ですか？"
    },
    "Show low stock inventory items": {
        "ru": "Показать товары с низким остатком", "es": "Mostrar productos con stock bajo", "nl": "Toon artikelen met lage voorraad",
        "fr": "Afficher les articles en stock faible", "pt": "Mostrar itens com stock reduzido", "zh_Hans": "显示库存不足的商品", "ja": "在庫が少なくなっている商品を表示"
    },
    "What are our expected receivables?": {
        "ru": "Какие платежи мы ожидаем получить?", "es": "¿Cuáles son los cobros esperados?", "nl": "Welke betalingen verwachten we?",
        "fr": "Quels sont les paiements attendus ?", "pt": "Quais são os recebimentos esperados?", "zh_Hans": "近期预期收款有哪些？", "ja": "入金予定の売掛金はどうなっていますか？"
    },
    "Summarize company financial status": {
        "ru": "Составить сводку о финансовом состоянии компании", "es": "Resumir el estado financiero de la empresa", "nl": "Vat de financiële status van het bedrijf samen",
        "fr": "Résumer la situation financière de l'entreprise", "pt": "Resumir a situação financeira da empresa", "zh_Hans": "总结公司当前的财务与资金状况", "ja": "現在の財務・資金状況を要約してください"
    },
    "Hello!": {
        "ru": "Здравствуйте!", "es": "¡Hola!", "nl": "Hallo!",
        "fr": "Bonjour !", "pt": "Olá!", "zh_Hans": "您好！", "ja": "こんにちは！"
    },
    "I am your Sole Enterprise Orchestrator assistant. Ask me anything about your records, such as:": {
        "ru": "Я ваш ассистент Sole Enterprise Orchestrator. Спросите меня о чем угодно, например:",
        "es": "Soy su asistente de Sole Enterprise Orchestrator. Pregúnteme cualquier cosa sobre sus registros, como:",
        "nl": "Ik ben uw Sole Enterprise Orchestrator-assistent. Vraag me gerust iets over uw administratie, zoals:",
        "fr": "Je suis votre assistant Sole Enterprise Orchestrator. Posez-moi vos questions sur vos dossiers, par exemple :",
        "pt": "Sou o seu assistente Sole Enterprise Orchestrator. Pergunte-me qualquer coisa sobre os seus registos, como:",
        "zh_Hans": "我是您的 Sole Enterprise Orchestrator 智能业务助手。您可以询问任何关于公司账册的问题，例如：",
        "ja": "Sole Enterprise Orchestrator の業務アシスタントです。記録や台帳について何でもお尋ねください："
    },
    "Ask about invoices, stock, contracts...": {
        "ru": "Спросите о счетах, складе, договорах...", "es": "Pregunte sobre facturas, inventario, contratos...", "nl": "Vraag over facturen, voorraad, contracten...",
        "fr": "Interrogez sur les factures, les stocks, les contrats...", "pt": "Pergunte sobre faturas, stock, contratos...", "zh_Hans": "询问发票、库存、合同等问题...", "ja": "請求書、在庫、契約書について質問..."
    },
    "All caught up! No unread payment or contract alerts.": {
        "ru": "Все проверено! Нет непрочитанных уведомлений по платежам и договорам.",
        "es": "¡Todo al día! No hay alertas pendientes de pagos ni contratos.",
        "nl": "Helemaal bijgewerkt! Geen ongelezen betalings- of contractwaarschuwingen.",
        "fr": "Tout est à jour ! Aucune alerte de paiement ou de contrat non lue.",
        "pt": "Tudo em dia! Sem alertas pendentes de pagamentos ou contratos.",
        "zh_Hans": "一切就绪！暂无未读的付款或合同预警。",
        "ja": "すべて最新です！未読の支払や契約のアラートはありません。"
    },
    "Scan upcoming payments and trigger proactive reminders": {
        "ru": "Просканировать предстоящие платежи и создать напоминания", "es": "Escanear pagos próximos y generar recordatorios proactivos", "nl": "Aankomende betalingen scannen en proactieve herinneringen aanmaken",
        "fr": "Analyser les paiements à venir et déclencher les rappels proactifs", "pt": "Analisar pagamentos próximos e criar lembretes proativos", "zh_Hans": "扫描近期款项并触发主动提醒", "ja": "今後の支払期限をスキャンしてリマインダーを生成"
    },
    "All": {
        "ru": "Все", "es": "Todos", "nl": "Alle",
        "fr": "Tous", "pt": "Todos", "zh_Hans": "全部", "ja": "すべて"
    },
    "Needs Review": {
        "ru": "Требуют проверки", "es": "Requieren Revisión", "nl": "Beoordeling Nodig",
        "fr": "À Valider", "pt": "Requer Revisão", "zh_Hans": "待审核", "ja": "要確認"
    },
    "Vendor Invoices": {
        "ru": "Счета поставщиков", "es": "Facturas de Proveedores", "nl": "Leveranciersfacturen",
        "fr": "Factures Fournisseurs", "pt": "Faturas de Fornecedores", "zh_Hans": "供应商发票", "ja": "仕入先請求書"
    },
    "Document": {
        "ru": "Документ", "es": "Documento", "nl": "Document",
        "fr": "Document", "pt": "Documento", "zh_Hans": "单据文件", "ja": "書類"
    },
    "Detected Type": {
        "ru": "Определенный тип", "es": "Tipo Detectado", "nl": "Gedetecteerd Type",
        "fr": "Type Détecté", "pt": "Tipo Detetado", "zh_Hans": "识别类型", "ja": "検出種別"
    },
    "AI Status": {
        "ru": "Статус ИИ", "es": "Estado de la IA", "nl": "AI Status",
        "fr": "Statut de l'IA", "pt": "Estado da IA", "zh_Hans": "AI 处理状态", "ja": "AI解析状態"
    },
    "Actions": {
        "ru": "Действия", "es": "Acciones", "nl": "Acties",
        "fr": "Actions", "pt": "Ações", "zh_Hans": "操作", "ja": "操作"
    },
    "Synced to Ledgers": {
        "ru": "Синхронизировано с учетом", "es": "Sincronizado con Libros", "nl": "Gesynchroniseerd met Grootboek",
        "fr": "Synchronisé aux Livres", "pt": "Sincronizado com os Registos", "zh_Hans": "已记入系统账本", "ja": "元帳連携完了"
    },
    "Ready for Review": {
        "ru": "Готово к проверке", "es": "Listo para Revisión", "nl": "Klaar voor Beoordeling",
        "fr": "Prêt pour Validation", "pt": "Pronto para Revisão", "zh_Hans": "待审核确认", "ja": "確認待ち"
    },
    "AI Analyzing...": {
        "ru": "ИИ анализирует...", "es": "IA Analizando...", "nl": "AI Analyseert...",
        "fr": "IA en cours d'analyse...", "pt": "IA a analisar...", "zh_Hans": "AI 正在深度解析...", "ja": "AI解析中..."
    },
    "Error": {
        "ru": "Ошибка", "es": "Error", "nl": "Fout",
        "fr": "Erreur", "pt": "Erro", "zh_Hans": "处理异常", "ja": "エラー"
    },
    "Inspect": {
        "ru": "Просмотр", "es": "Inspeccionar", "nl": "Inspecteren",
        "fr": "Inspecter", "pt": "Inspecionar", "zh_Hans": "查阅审核", "ja": "詳細確認"
    },
    "No scanned documents found matching your filter.": {
        "ru": "Нет отсканированных документов, соответствующих вашему фильтру.",
        "es": "No se encontraron documentos escaneados que coincidan con su filtro.",
        "nl": "Geen gescande documenten gevonden die aan uw filter voldoen.",
        "fr": "Aucun document numérisé ne correspond à votre filtre.",
        "pt": "Nenhum documento digitalizado encontrado com os filtros selecionados.",
        "zh_Hans": "未找到符合筛选条件的扫描单据。",
        "ja": "該当するスキャン書類が見つかりませんでした。"
    },
    "Upload your first document": {
        "ru": "Загрузите ваш первый документ", "es": "Suba su primer documento", "nl": "Upload uw eerste document",
        "fr": "Téléversez votre premier document", "pt": "Carregue o seu primeiro documento", "zh_Hans": "上传您的首张单据", "ja": "最初の書類をアップロード"
    },
    "Click to upload or drag & drop": {
        "ru": "Нажмите для загрузки или перетащите файл", "es": "Haga clic para subir o arrastre y suelte", "nl": "Klik om te uploaden of sleep bestanden hierheen",
        "fr": "Cliquez pour téléverser ou glissez-déposez", "pt": "Clique para carregar ou arraste e solte", "zh_Hans": "点击选择文件或直接拖放至此处", "ja": "クリックして選択またはファイルをドロップ"
    },
    "PDF, PNG, JPG, or WEBP (Scans, contracts, receipts)": {
        "ru": "PDF, PNG, JPG или WEBP (сканы, договоры, чеки)", "es": "PDF, PNG, JPG o WEBP (escaneos, contratos, recibos)", "nl": "PDF, PNG, JPG of WEBP (scans, contracten, bonnen)",
        "fr": "PDF, PNG, JPG ou WEBP (scans, contrats, reçus)", "pt": "PDF, PNG, JPG ou WEBP (digitalizações, contratos, recibos)", "zh_Hans": "支持 PDF, PNG, JPG 或 WEBP 格式 (发票、合同、收据等)", "ja": "PDF, PNG, JPG, WEBP対応 (スキャン、契約書、領収書)"
    },
    "Multimodal AI": {
        "ru": "Мультимодальный ИИ", "es": "IA Multimodal", "nl": "Multimodale AI",
        "fr": "IA Multimodale", "pt": "IA Multimodal", "zh_Hans": "多模态视觉 AI", "ja": "マルチモーダルAI"
    },
    "Accurate reading of tables, totals, IBANs, and handwritten stamps.": {
        "ru": "Точное считывание таблиц, сумм, IBAN и рукописных штампов.", "es": "Lectura precisa de tablas, totales, IBAN y sellos manuscritos.", "nl": "Nauwkeurige herkenning van tabellen, totalen, IBANs en stempels.",
        "fr": "Lecture précise des tableaux, totaux, IBAN et cachets manuscrits.", "pt": "Leitura precisa de tabelas, totais, IBANs e carimbos manuais.", "zh_Hans": "高精度识别表格数据、结算金额、银行账号与手写签章。", "ja": "表、合計金額、口座番号、押印・手書きを高精度に読み取り。"
    },
    "Auto Task Creation": {
        "ru": "Автоматическое создание задач", "es": "Creación Automática de Tareas", "nl": "Automatische Takencreatie",
        "fr": "Création Automatique de Tâches", "pt": "Criação Automática de Tarefas", "zh_Hans": "自动排期生成任务", "ja": "タスク自動生成"
    },
    "Schedules payment due dates and contract renewals directly into your calendar.": {
        "ru": "Планирует сроки оплаты и продления договоров прямо в вашем календаре.", "es": "Programa vencimientos de pago y renovaciones directamente en su calendario.", "nl": "Plant betalingstermijnen en contractverlengingen direct in uw agenda.",
        "fr": "Planifie les dates d'échéance et de renouvellement dans votre calendrier.", "pt": "Agenda prazos de pagamento e renovações de contratos diretamente no seu calendário.", "zh_Hans": "将付款到期日和合同续签提醒直接同步至全员日历。", "ja": "支払期日や契約更新日をカレンダーに自動登録。"
    },
    "Reminds your team before payments are due and flags overdue bills.": {
        "ru": "Напоминает вашей команде до наступления срока оплаты и отмечает просроченные счета.", "es": "Recuerda a su equipo antes de los vencimientos y señala facturas atrasadas.", "nl": "Herinnert uw team voor de vervaldatum en markeert achterstallige facturen.",
        "fr": "Avertit votre équipe avant l'échéance et signale les factures en retard.", "pt": "Lembra a sua equipa antes do vencimento e sinaliza faturas em atraso.", "zh_Hans": "在款项到期前主动提醒团队，并自动追踪逾期发票。", "ja": "支払期日前にチームへ通知し、超過した請求書を強調表示。"
    },
    "Cancel": {
        "ru": "Отмена", "es": "Cancelar", "nl": "Annuleren",
        "fr": "Annuler", "pt": "Cancelar", "zh_Hans": "取消", "ja": "キャンセル"
    },
    "Process with AI": {
        "ru": "Обработать с помощью ИИ", "es": "Procesar con IA", "nl": "Verwerken met AI",
        "fr": "Traiter avec l'IA", "pt": "Processar com IA", "zh_Hans": "开始 AI 智能解析", "ja": "AIで解析開始"
    },
    "Verify Document": {
        "ru": "Проверить документ", "es": "Verificar Documento", "nl": "Document Verifiëren",
        "fr": "Vérifier le Document", "pt": "Verificar Documento", "zh_Hans": "单据核验", "ja": "書類の検証"
    },
    "Verify & Review": {
        "ru": "Проверка и согласование", "es": "Verificar y Revisar", "nl": "Verifiëren & Beoordelen",
        "fr": "Vérifier & Réviser", "pt": "Verificar e Rever", "zh_Hans": "核对与审核", "ja": "検証・レビュー"
    },
    "Confirmed & Committed": {
        "ru": "Подтверждено и сохранено", "es": "Confirmado y Guardado", "nl": "Bevestigd & Opgeslagen",
        "fr": "Confirmé & Enregistré", "pt": "Confirmado e Guardado", "zh_Hans": "已审核入账", "ja": "確認・確定済み"
    },
    "Verification Required": {
        "ru": "Требуется проверка", "es": "Verificación Requerida", "nl": "Verificatie Vereist",
        "fr": "Vérification Requise", "pt": "Verificação Necessária", "zh_Hans": "需要人工审核", "ja": "要確認"
    },
    "Re-run AI extraction": {
        "ru": "Повторить извлечение данных с помощью ИИ", "es": "Volver a ejecutar extracción con IA", "nl": "AI-extractie opnieuw uitvoeren",
        "fr": "Réexécuter l'extraction IA", "pt": "Reexecutar extração com IA", "zh_Hans": "重新运行 AI 数据提取", "ja": "AI解析を再実行"
    },
    "Re-Extract": {
        "ru": "Извлечь заново", "es": "Re-extraer", "nl": "Opnieuw Extraheren",
        "fr": "Réextraire", "pt": "Reextrair", "zh_Hans": "重新提取", "ja": "再解析"
    },
    "Original Scanned Document": {
        "ru": "Оригинал отсканированного документа", "es": "Documento Escaneado Original", "nl": "Origineel Gescand Document",
        "fr": "Document Numérisé Original", "pt": "Documento Digitalizado Original", "zh_Hans": "原始扫描单据预览", "ja": "原本スキャン画像"
    },
    "Open Fullscreen": {
        "ru": "Открыть на весь экран", "es": "Abrir en Pantalla Completa", "nl": "Volledig Scherm Openen",
        "fr": "Ouvrir en Plein Écran", "pt": "Abrir em Ecrã Inteiro", "zh_Hans": "全屏预览", "ja": "全画面表示"
    },
    "Extracted Structured Record": {
        "ru": "Извлеченные структурированные данные", "es": "Registro Estructurado Extraído", "nl": "Geëxtraheerde Gestructureerde Gegevens",
        "fr": "Données Structurées Extraites", "pt": "Registo Estruturado Extraído", "zh_Hans": "已提取结构化记录", "ja": "抽出された構造化データ"
    },
    "Review AI extracted details before committing to company ledgers.": {
        "ru": "Проверьте данные, извлеченные ИИ, перед внесением в бухгалтерские книги компании.",
        "es": "Revise los detalles extraídos por la IA antes de confirmarlos en los libros de la empresa.",
        "nl": "Controleer de door AI geëxtraheerde gegevens voordat u ze opslaat in het grootboek.",
        "fr": "Vérifiez les données extraites par l'IA avant de les enregistrer dans les livres de l'entreprise.",
        "pt": "Reveja os dados extraídos pela IA antes de os confirmar nos registos da empresa.",
        "zh_Hans": "在将数据正式记入企业账本前，请核对 AI 提取的关键字段。",
        "ja": "会社の元帳に登録する前に、AIが抽出した内容をご確認ください。"
    },
    "Locked & Synced": {
        "ru": "Зафиксировано и синхронизировано", "es": "Bloqueado y Sincronizado", "nl": "Vergrendeld & Gesynchroniseerd",
        "fr": "Verrouillé & Synchronisé", "pt": "Bloqueado e Sincronizado", "zh_Hans": "已锁定并同步", "ja": "確定・同期済み"
    },
    "Document Type": {
        "ru": "Тип документа", "es": "Tipo de Documento", "nl": "Documenttype",
        "fr": "Type de Document", "pt": "Tipo de Documento", "zh_Hans": "单据类型", "ja": "書類種別"
    },
    "Vendor Invoice (Outgoing Payment)": {
        "ru": "Счет поставщика (исходящий платеж)", "es": "Factura de Proveedor (Pago Saliente)", "nl": "Leveranciersfactuur (Uitgaande Betaling)",
        "fr": "Facture Fournisseur (Paiement Sortant)", "pt": "Fatura de Fornecedor (Pagamento a Emitir)", "zh_Hans": "供应商发票 (对外付款)", "ja": "仕入先請求書 (支払対象)"
    },
    "Customer Invoice (Incoming Payment)": {
        "ru": "Счет клиенту (входящий платеж)", "es": "Factura de Cliente (Cobro Entrante)", "nl": "Klantfactuur (Inkomende Betaling)",
        "fr": "Facture Client (Paiement Entrant)", "pt": "Fatura de Cliente (Recebimento)", "zh_Hans": "客户销售发票 (收款款项)", "ja": "顧客向け請求書 (入金対象)"
    },
    "Contract / Agreement": {
        "ru": "Договор / Соглашение", "es": "Contrato / Acuerdo", "nl": "Contract / Overeenkomst",
        "fr": "Contrat / Accord", "pt": "Contrato / Acordo", "zh_Hans": "商务合同 / 协议", "ja": "契約書 / 協定書"
    },
    "Consignment / Delivery Note": {
        "ru": "Накладная / Доставка", "es": "Albarán / Nota de Entrega", "nl": "Leveringsbon / Vrachtbrief",
        "fr": "Bordereau / Bon de Livraison", "pt": "Guia de Remessa / Entrega", "zh_Hans": "发货单 / 提货运单", "ja": "納品書 / 運送状"
    },
    "Expense Receipt / Petty Cash": {
        "ru": "Чек на расходы / Мелкая касса", "es": "Recibo de Gastos / Caja Chica", "nl": "Uitgavenbon / Kleine Kas",
        "fr": "Reçu de Dépense / Petite Caisse", "pt": "Recibo de Despesa / Caixa Pequena", "zh_Hans": "费用凭证 / 零用发票", "ja": "経費領収書 / 小口現金"
    },
    "General Document": {
        "ru": "Общий документ", "es": "Documento General", "nl": "Algemeen Document",
        "fr": "Document Général", "pt": "Documento Geral", "zh_Hans": "通用常规单据", "ja": "一般書類"
    },
    "Document / Invoice Number": {
        "ru": "Номер документа / счета", "es": "Número de Documento / Factura", "nl": "Document- / Factuurnummer",
        "fr": "Numéro de Document / Facture", "pt": "Número de Documento / Fatura", "zh_Hans": "单据编号 / 发票号码", "ja": "書類番号 / 請求書番号"
    },
    "Counterparty Details": {
        "ru": "Реквизиты контрагента", "es": "Detalles de la Contraparte", "nl": "Gegevens van de Relatie",
        "fr": "Détails du Partenaire", "pt": "Dados da Entidade", "zh_Hans": "往来企业详细信息", "ja": "取引先詳細情報"
    },
    "Vendor / Supplier": {
        "ru": "Поставщик / Подрядчик", "es": "Proveedor", "nl": "Leverancier",
        "fr": "Fournisseur", "pt": "Fornecedor", "zh_Hans": "供应商 / 供货商", "ja": "仕入先 / サプライヤー"
    },
    "Customer / Client": {
        "ru": "Клиент / Покупатель", "es": "Cliente", "nl": "Klant",
        "fr": "Client", "pt": "Cliente", "zh_Hans": "客户 / 委托方", "ja": "顧客 / クライアント"
    },
    "Business Partner": {
        "ru": "Деловой партнер", "es": "Socio Comercial", "nl": "Zakenpartner",
        "fr": "Partenaire Commercial", "pt": "Parceiro de Negócios", "zh_Hans": "战略合作伙伴", "ja": "ビジネスパートナー"
    },
    "Logistics / Carrier": {
        "ru": "Логистика / Перевозчик", "es": "Logística / Transportista", "nl": "Logistiek / Vervoerder",
        "fr": "Logistique / Transporteur", "pt": "Logística / Transportadora", "zh_Hans": "物流公司 / 承运方", "ja": "物流会社 / 運送業者"
    },
    "Company / Entity Name": {
        "ru": "Название компании / организации", "es": "Nombre de la Empresa", "nl": "Bedrijfsnaam",
        "fr": "Nom de l'Entreprise", "pt": "Nome da Empresa", "zh_Hans": "企业 / 机构全称", "ja": "会社名 / 法人名"
    },
    "Tax / VAT ID": {
        "ru": "ИНН / НДС", "es": "NIF / CIF / IVA", "nl": "BTW-nummer",
        "fr": "Numéro de TVA", "pt": "NIF / IVA", "zh_Hans": "统一纳税人识别号 / 增值税号", "ja": "税務登録番号 / インボイス番号"
    },
    "Bank IBAN": {
        "ru": "Банковский счет IBAN", "es": "IBAN Bancario", "nl": "IBAN Bankrekening",
        "fr": "IBAN Bancaire", "pt": "IBAN Bancário", "zh_Hans": "银行结算账户 / IBAN", "ja": "銀行口座番号 / IBAN"
    },
    "Email": {
        "ru": "Эл. почта", "es": "Correo Electrónico", "nl": "E-mail",
        "fr": "E-mail", "pt": "E-mail", "zh_Hans": "电子邮箱", "ja": "メールアドレス"
    },
    "Phone": {
        "ru": "Телефон", "es": "Teléfono", "nl": "Telefoon",
        "fr": "Téléphone", "pt": "Telefone", "zh_Hans": "联系电话", "ja": "電話番号"
    },
    "Issue Date": {
        "ru": "Дата выставления", "es": "Fecha de Emisión", "nl": "Uitgiftedatum",
        "fr": "Date d'Émission", "pt": "Data de Emissão", "zh_Hans": "开票 / 签署日期", "ja": "発行日"
    },
    "Payment Due Date *": {
        "ru": "Срок оплаты *", "es": "Fecha de Vencimiento *", "nl": "Vervaldatum van Betaling *",
        "fr": "Date d'Échéance du Paiement *", "pt": "Data de Vencimento do Pagamento *", "zh_Hans": "付款截止到期日 *", "ja": "支払期限 *"
    },
    "Contract End / Renewal *": {
        "ru": "Окончание / продление договора *", "es": "Fin / Renovación del Contrato *", "nl": "Contracteinde / Verlenging *",
        "fr": "Fin / Renouvellement du Contrat *", "pt": "Fim / Renovação do Contrato *", "zh_Hans": "合同终止 / 续签截止日 *", "ja": "契約満了 / 更新期限 *"
    },
    "Expected Delivery Date *": {
        "ru": "Ожидаемая дата доставки *", "es": "Fecha Prevista de Entrega *", "nl": "Verwachte Leverdatum *",
        "fr": "Date de Livraison Prévue *", "pt": "Data Prevista de Entrega *", "zh_Hans": "预期到货日期 *", "ja": "納品予定日 *"
    },
    "Notice / Grace Period (Days)": {
        "ru": "Срок уведомления (дни)", "es": "Período de Preaviso (Días)", "nl": "Opzegtermijn (Dagen)",
        "fr": "Période de Préavis (Jours)", "pt": "Prazo de Pré-aviso (Dias)", "zh_Hans": "提前通知窗口期 (天数)", "ja": "事前通知期間 (日数)"
    },
    "Currency": {
        "ru": "Валюта", "es": "Moneda", "nl": "Valuta",
        "fr": "Devise", "pt": "Moeda", "zh_Hans": "结算币种", "ja": "通貨"
    },
    "Subtotal": {
        "ru": "Подитог", "es": "Subtotal", "nl": "Subtotaal",
        "fr": "Sous-total", "pt": "Subtotal", "zh_Hans": "不含税小计", "ja": "税抜小計"
    },
    "Tax / VAT": {
        "ru": "НДС / Налог", "es": "IVA / Impuesto", "nl": "BTW / Belasting",
        "fr": "TVA / Taxe", "pt": "IVA / Imposto", "zh_Hans": "增值税 / 税额", "ja": "消費税額"
    },
    "Total Amount": {
        "ru": "Итоговая сумма", "es": "Importe Total", "nl": "Totaalbedrag",
        "fr": "Montant Total", "pt": "Valor Total", "zh_Hans": "总金额 (价税合计)", "ja": "合計金額"
    },
    "Line Items / Products": {
        "ru": "Позиции счета / товары", "es": "Líneas de la Factura / Productos", "nl": "Factuurregels / Producten",
        "fr": "Lignes de Facturation / Produits", "pt": "Linhas da Fatura / Produtos", "zh_Hans": "明细项目 / 商品清单", "ja": "明細行 / 取扱商品"
    },
    "Add Item": {
        "ru": "Добавить позицию", "es": "Añadir Línea", "nl": "Regel Toevoegen",
        "fr": "Ajouter une Ligne", "pt": "Adicionar Linha", "zh_Hans": "添加明细项", "ja": "行を追加"
    },
    "Description": {
        "ru": "Описание", "es": "Descripción", "nl": "Omschrijving",
        "fr": "Description", "pt": "Descrição", "zh_Hans": "项目描述", "ja": "品名・摘要"
    },
    "SKU / Code": {
        "ru": "Артикул / Код", "es": "SKU / Código", "nl": "SKU / Code",
        "fr": "SKU / Code", "pt": "SKU / Código", "zh_Hans": "商品编码 / SKU", "ja": "商品コード / SKU"
    },
    "Qty": {
        "ru": "Кол-во", "es": "Cant.", "nl": "Aantal",
        "fr": "Qté", "pt": "Qtd.", "zh_Hans": "数量", "ja": "数量"
    },
    "Price": {
        "ru": "Цена", "es": "Precio", "nl": "Prijs",
        "fr": "Prix", "pt": "Preço", "zh_Hans": "单价", "ja": "単価"
    },
    "Line Total": {
        "ru": "Сумма по строке", "es": "Total Línea", "nl": "Regeltotaal",
        "fr": "Total Ligne", "pt": "Total da Linha", "zh_Hans": "项目总额", "ja": "金額"
    },
    "Calendar Task & Reminder Automation": {
        "ru": "Автоматизация задач календаря и напоминаний", "es": "Automatización de Tareas y Recordatorios de Calendario", "nl": "Automatisering van Agendataken & Herinneringen",
        "fr": "Automatisation des Tâches et Rappels du Calendrier", "pt": "Automatização de Tarefas e Lembretes de Calendário", "zh_Hans": "日历任务与到期提醒自动化", "ja": "カレンダータスク＆通知の自動化"
    },
    "Approving this record will automatically create a scheduled event on your calendar and dispatch proactive payment reminders.": {
        "ru": "Подтверждение этой записи автоматически создаст запланированное событие в календаре и настроит упреждающие напоминания об оплате.",
        "es": "Aprobar este registro creará automáticamente un evento en su calendario y enviará recordatorios proactivos de pago.",
        "nl": "Het goedkeuren van dit document maakt automatisch een agendataak aan en verstuurt proactieve herinneringen.",
        "fr": "La validation de ce document créera automatiquement un événement dans votre calendrier et enverra des rappels de paiement.",
        "pt": "A aprovação deste registo criará automaticamente um evento no seu calendário e enviará lembretes proativos de pagamento.",
        "zh_Hans": "确认审核此单据将自动在全员日历中生成排期日程，并按时推送主动付款/收款提醒。",
        "ja": "この書類を承認すると、カレンダーに自動で予定が登録され、支払期限の事前通知が設定されます。"
    },
    "Task Title": {
        "ru": "Название задачи", "es": "Título de la Tarea", "nl": "Taaktitel",
        "fr": "Titre de la Tâche", "pt": "Título da Tarefa", "zh_Hans": "任务事项名称", "ja": "タスク名"
    },
    "Scheduled Due Date": {
        "ru": "Запланированный срок", "es": "Fecha Límite Programada", "nl": "Geplande Vervaldatum",
        "fr": "Date d'Échéance Prévue", "pt": "Data de Vencimento Agendada", "zh_Hans": "预定到期执行日", "ja": "予定期限日"
    },
    "Back to List": {
        "ru": "Назад к списку", "es": "Volver a la Lista", "nl": "Terug naar Lijst",
        "fr": "Retour à la Liste", "pt": "Voltar à Lista", "zh_Hans": "返回单据列表", "ja": "一覧に戻る"
    },
    "Confirm & Commit to Ledgers": {
        "ru": "Подтвердить и занести в учет", "es": "Confirmar y Guardar en Libros", "nl": "Bevestigen & Opslaan in Grootboek",
        "fr": "Confirmer & Enregistrer dans les Livres", "pt": "Confirmar e Guardar nos Registos", "zh_Hans": "审核确认并正式入账", "ja": "確認して元帳に反映"
    },
    "Scan New Bill / Invoice": {
        "ru": "Сканировать новый счет", "es": "Escanear Nueva Factura", "nl": "Nieuwe Factuur Scannen",
        "fr": "Scanner une Nouvelle Facture", "pt": "Digitalizar Nova Fatura", "zh_Hans": "扫描新发票 / 账单", "ja": "新しい請求書をスキャン"
    },
    "Unpaid vendor bills": {
        "ru": "Неоплаченные счета поставщиков", "es": "Facturas de proveedores impagadas", "nl": "Onbetaalde leveranciersfacturen",
        "fr": "Factures fournisseurs impayées", "pt": "Faturas de fornecedores não pagas", "zh_Hans": "待付供应商账单", "ja": "未払いの仕入先請求書"
    },
    "All Invoices": {
        "ru": "Все счета", "es": "Todas las Facturas", "nl": "Alle Facturen",
        "fr": "Toutes les Factures", "pt": "Todas as Faturas", "zh_Hans": "全部发票", "ja": "すべての請求書"
    },
    "Outgoing Payables (Vendor Bills)": {
        "ru": "Исходящие счета (поставщики)", "es": "Facturas a Pagar (Proveedores)", "nl": "Te Betalen Facturen (Leveranciers)",
        "fr": "Factures à Payer (Fournisseurs)", "pt": "Faturas a Pagar (Fornecedores)", "zh_Hans": "应付款发票 (供应商对账单)", "ja": "買掛金請求書 (仕入先分)"
    },
    "Incoming Receivables (Customers)": {
        "ru": "Входящие счета (клиенты)", "es": "Facturas a Cobrar (Clientes)", "nl": "Te Ontvangen Facturen (Klanten)",
        "fr": "Factures à Recevoir (Clients)", "pt": "Faturas a Receber (Clientes)", "zh_Hans": "应收款发票 (客户结算单)", "ja": "売掛金請求書 (顧客請求分)"
    },
    "Overdue Only": {
        "ru": "Только просроченные", "es": "Solo Vencidas", "nl": "Alleen Vervallen",
        "fr": "En Retard Uniquement", "pt": "Apenas Vencidas", "zh_Hans": "仅显示已逾期", "ja": "期限超過のみ"
    },
    "Unpaid": {
        "ru": "Не оплачено", "es": "No Pagado", "nl": "Niet Betaald",
        "fr": "Non Payé", "pt": "Não Pago", "zh_Hans": "未付款 / 未结清", "ja": "未払い"
    },
    "Settled / Paid": {
        "ru": "Оплачено / Закрыто", "es": "Pagado / Liquidado", "nl": "Betaald / Voldaan",
        "fr": "Payé / Réglé", "pt": "Pago / Liquidado", "zh_Hans": "已结清 / 已付讫", "ja": "決済済み / 支払完了"
    },
    "Invoice #": {
        "ru": "Номер счета", "es": "N.º Factura", "nl": "Factuurnummer",
        "fr": "N° Facture", "pt": "N.º da Fatura", "zh_Hans": "发票号码", "ja": "請求書番号"
    },
    "Direction": {
        "ru": "Направление", "es": "Dirección", "nl": "Richting",
        "fr": "Sens", "pt": "Sentido", "zh_Hans": "收付方向", "ja": "収支方向"
    },
    "Counterparty": {
        "ru": "Контрагент", "es": "Contraparte", "nl": "Tegenpartij",
        "fr": "Tiers / Partenaire", "pt": "Entidade", "zh_Hans": "往来企业", "ja": "取引先"
    },
    "Status": {
        "ru": "Статус", "es": "Estado", "nl": "Status",
        "fr": "Statut", "pt": "Estado", "zh_Hans": "状态", "ja": "ステータス"
    },
    "Outgoing Bill": {
        "ru": "Исходящий счет", "es": "Factura Saliente", "nl": "Uitgaande Factuur",
        "fr": "Facture Sortante", "pt": "Fatura a Pagar", "zh_Hans": "对外付款账单", "ja": "支払請求書"
    },
    "Incoming": {
        "ru": "Входящий", "es": "Entrante", "nl": "Inkomend",
        "fr": "Entrant", "pt": "Entrada", "zh_Hans": "应收款项", "ja": "入金分"
    },
    "Overdue!": {
        "ru": "Просрочено!", "es": "¡Vencido!", "nl": "Vervallen!",
        "fr": "En Retard !", "pt": "Vencido!", "zh_Hans": "已逾期！", "ja": "期日超過！"
    },
    "Paid": {
        "ru": "Оплачено", "es": "Pagado", "nl": "Betaald",
        "fr": "Payé", "pt": "Pago", "zh_Hans": "已付款", "ja": "支払済"
    },
    "Partially Paid": {
        "ru": "Частично оплачено", "es": "Parcialmente Pagado", "nl": "Gedeeltelijk Betaald",
        "fr": "Partiellement Payé", "pt": "Parcialmente Pago", "zh_Hans": "部分付款", "ja": "一部入金・支払済"
    },
    "View Details": {
        "ru": "Подробнее", "es": "Ver Detalles", "nl": "Details Bekijken",
        "fr": "Voir les Détails", "pt": "Ver Detalhes", "zh_Hans": "查看详情", "ja": "詳細を見る"
    },
    "No invoices found.": {
        "ru": "Счета не найдены.", "es": "No se encontraron facturas.", "nl": "Geen facturen gevonden.",
        "fr": "Aucune facture trouvée.", "pt": "Nenhuma fatura encontrada.", "zh_Hans": "未找到符合条件的发票记录。", "ja": "請求書が見つかりませんでした。"
    },
    "Outgoing Bill (We Owe)": {
        "ru": "Счет к оплате (наш долг)", "es": "Factura a Pagar (Nosotros Debemos)", "nl": "Te Betalen Factuur (Wij Moeten Betalen)",
        "fr": "Facture à Payer (Nous Devons)", "pt": "Fatura a Pagar (Nós Devemos)", "zh_Hans": "应付账单 (公司负债)", "ja": "支払請求書 (買掛金)"
    },
    "Incoming Receivable": {
        "ru": "Входящая дебиторка", "es": "Cobro Entrante", "nl": "Inkomende Vorderingen",
        "fr": "Créance Entrante", "pt": "Recebimento Pendente", "zh_Hans": "待收账款 (客户欠款)", "ja": "回収予定売掛金"
    },
    "Paid in Full": {
        "ru": "Оплачено полностью", "es": "Pagado en su Totalidad", "nl": "Volledig Betaald",
        "fr": "Payé en Totalité", "pt": "Pago na Totalidade", "zh_Hans": "全额结清", "ja": "完済・全額受領"
    },
    "View Source Scan": {
        "ru": "Открыть скан документа", "es": "Ver Escaneo Original", "nl": "Originele Scan Bekijken",
        "fr": "Voir le Scan d'Origine", "pt": "Ver Digitalização Original", "zh_Hans": "查看原始单据扫描件", "ja": "原本スキャンを表示"
    },
    "Invoice Line Items": {
        "ru": "Позиции счета", "es": "Líneas de la Factura", "nl": "Factuurregels",
        "fr": "Lignes de la Facture", "pt": "Linhas da Fatura", "zh_Hans": "发票明细行", "ja": "請求書明細"
    },
    "item(s)": {
        "ru": "поз.", "es": "artículo(s)", "nl": "item(s)",
        "fr": "article(s)", "pt": "item(ns)", "zh_Hans": "项明细", "ja": "項目"
    },
    "Standard single line invoice": {
        "ru": "Стандартный однострочный счет", "es": "Factura estándar de una línea", "nl": "Standaard factuur met één regel",
        "fr": "Facture standard sur une seule ligne", "pt": "Fatura padrão de uma única linha", "zh_Hans": "标准单条目发票", "ja": "標準単一行請求書"
    },
    "Payment History": {
        "ru": "История платежей", "es": "Historial de Pagos", "nl": "Betalingsgeschiedenis",
        "fr": "Historique des Paiements", "pt": "Histórico de Pagamentos", "zh_Hans": "交易付款历史记录", "ja": "支払・入金履歴"
    },
    "Date": {
        "ru": "Дата", "es": "Fecha", "nl": "Datum",
        "fr": "Date", "pt": "Data", "zh_Hans": "交易日期", "ja": "日付"
    },
    "Method": {
        "ru": "Способ", "es": "Método", "nl": "Methode",
        "fr": "Méthode", "pt": "Método", "zh_Hans": "支付途径", "ja": "支払方法"
    },
    "Reference": {
        "ru": "Номер операции", "es": "Referencia", "nl": "Referentie",
        "fr": "Référence", "pt": "Referência", "zh_Hans": "流水凭证号", "ja": "参照番号"
    },
    "No payments recorded yet for this invoice.": {
        "ru": "По этому счету еще не записано ни одного платежа.",
        "es": "No hay pagos registrados aún para esta factura.",
        "nl": "Nog geen betalingen geregistreerd voor deze factuur.",
        "fr": "Aucun paiement enregistré pour l'instant pour cette facture.",
        "pt": "Nenhum pagamento registado ainda para esta fatura.",
        "zh_Hans": "本发票尚未录入任何款项收付记录。",
        "ja": "この請求書に対する支払履歴はまだありません。"
    },
    "Financial Breakdown": {
        "ru": "Финансовая сводка", "es": "Desglose Financiero", "nl": "Financiële Uitsplitsing",
        "fr": "Détail Financier", "pt": "Discriminação Financeira", "zh_Hans": "资金结算构成", "ja": "財務明細内訳"
    },
    "Total Invoiced": {
        "ru": "Всего выставлено", "es": "Total Facturado", "nl": "Totaal Gefactureerd",
        "fr": "Total Facturé", "pt": "Total Faturado", "zh_Hans": "开票结算总额", "ja": "請求総額"
    },
    "Total Paid": {
        "ru": "Всего оплачено", "es": "Total Pagado", "nl": "Totaal Betaald",
        "fr": "Total Payé", "pt": "Total Pago", "zh_Hans": "已结算支付总额", "ja": "支払済総額"
    },
    "Remaining Due": {
        "ru": "Остаток к оплате", "es": "Restante por Pagar", "nl": "Resterend Bedrag",
        "fr": "Reste à Payer", "pt": "Restante a Pagar", "zh_Hans": "待付剩余余额", "ja": "残高 / 未払残高"
    },
    "Record a Settlement Payment": {
        "ru": "Записать платеж", "es": "Registrar un Pago", "nl": "Betaling Registreren",
        "fr": "Enregistrer un Paiement", "pt": "Registar um Pagamento", "zh_Hans": "录入转账收付流水", "ja": "支払・入金の記録"
    },
    "Amount to Pay (€)": {
        "ru": "Сумма платежа (€)", "es": "Importe a Pagar (€)", "nl": "Te Betalen Bedrag (€)",
        "fr": "Montant à Régler (€)", "pt": "Valor a Pagar (€)", "zh_Hans": "本次结算金额 (€)", "ja": "決済金額 (€)"
    },
    "Payment Method": {
        "ru": "Способ оплаты", "es": "Método de Pago", "nl": "Betaalmethode",
        "fr": "Moyen de Paiement", "pt": "Método de Pagamento", "zh_Hans": "结算方式", "ja": "決済手段"
    },
    "Bank Transfer / Wire": {
        "ru": "Банковский перевод", "es": "Transferencia Bancaria", "nl": "Bankoverschrijving",
        "fr": "Virement Bancaire", "pt": "Transferência Bancária", "zh_Hans": "银行电汇 / 支票转账", "ja": "銀行振込"
    },
    "Credit / Debit Card": {
        "ru": "Банковская карта", "es": "Tarjeta de Crédito / Débito", "nl": "Creditcard / Betaalpas",
        "fr": "Carte Bancaire", "pt": "Cartão de Crédito / Débito", "zh_Hans": "信用卡 / 储蓄卡", "ja": "クレジットカード / デビットカード"
    },
    "Direct Debit": {
        "ru": "Прямое списание", "es": "Domiciliación Bancaria", "nl": "Automatische Incasso",
        "fr": "Prélèvement Automatique", "pt": "Débito Direto", "zh_Hans": "银行自动扣款", "ja": "口座振替"
    },
    "Cash": {
        "ru": "Наличные", "es": "Efectivo", "nl": "Contant",
        "fr": "Espèces", "pt": "Numerário / Dinheiro", "zh_Hans": "现金现款", "ja": "現金"
    },
    "Other": {
        "ru": "Другое", "es": "Otro", "nl": "Overig",
        "fr": "Autre", "pt": "Outro", "zh_Hans": "其他方式", "ja": "その他"
    },
    "Transaction Ref / Cheque No.": {
        "ru": "Номер транзакции / чека", "es": "Ref. de Transacción / N.º Cheque", "nl": "Transactiereferentie / Chequenummer",
        "fr": "Réf. Transaction / N° de Chèque", "pt": "Ref. de Transação / N.º de Cheque", "zh_Hans": "转账交易流水号 / 支票号", "ja": "取引参照番号 / 小切手番号"
    },
    "Notes (optional)": {
        "ru": "Примечания (необязательно)", "es": "Notas (opcional)", "nl": "Notities (optioneel)",
        "fr": "Notes (facultatif)", "pt": "Notas (opcional)", "zh_Hans": "备注说明 (选填)", "ja": "備考 (任意)"
    },
    "Save Payment Record": {
        "ru": "Сохранить запись о платеже", "es": "Guardar Registro de Pago", "nl": "Betaling Opslaan",
        "fr": "Enregistrer le Paiement", "pt": "Guardar Registo de Pagamento", "zh_Hans": "保存付款流水", "ja": "支払記録を保存"
    },
    "Expense Receipts & Petty Cash": {
        "ru": "Чеки расходов и мелкая касса", "es": "Recibos de Gastos y Caja Chica", "nl": "Bonnetjes & Kleine Kas",
        "fr": "Reçus de Dépenses & Petite Caisse", "pt": "Recibos de Despesas e Caixa Pequena", "zh_Hans": "费用凭证与零用金管理", "ja": "経費領収書＆小口現金"
    },
    "Receipts & Expense Vouchers": {
        "ru": "Чеки и квитанции расходов", "es": "Recibos y Comprobantes de Gastos", "nl": "Bonnen & Uitgavenbewijzen",
        "fr": "Reçus & Bons de Dépense", "pt": "Recibos e Comprovativos de Despesa", "zh_Hans": "开支收据与报销凭据", "ja": "領収証・経費伝票"
    },
    "Petty cash receipts, office supplies, travel expenses, and small disbursements.": {
        "ru": "Чеки мелкой кассы, канцелярские товары, командировочные расходы и мелкие выплаты.",
        "es": "Recibos de caja chica, material de oficina, gastos de viaje y desembolsos menores.",
        "nl": "Kassabonnen, kantoorbenodigdheden, reiskosten en kleine uitgaven.",
        "fr": "Reçus de petite caisse, fournitures de bureau, frais de déplacement et menues dépenses.",
        "pt": "Recibos de caixa pequena, material de escritório, despesas de viagem e pequenos pagamentos.",
        "zh_Hans": "零用现金收据、办公用品采购、差旅报销与日常小额支出。",
        "ja": "小口現金、事務用品、旅費交通費、雑費などの支出伝票。"
    },
    "Total Recorded Expenses": {
        "ru": "Всего записанных расходов", "es": "Total de Gastos Registrados", "nl": "Totaal Geregistreerde Uitgaven",
        "fr": "Total des Dépenses Enregistrées", "pt": "Total de Despesas Registadas", "zh_Hans": "累计已记录费用总额", "ja": "経費累計総額"
    },
    "Category": {
        "ru": "Категория", "es": "Categoría", "nl": "Categorie",
        "fr": "Catégorie", "pt": "Categoria", "zh_Hans": "费用分类", "ja": "カテゴリー"
    },
    "Counterparty / Vendor": {
        "ru": "Контрагент / Поставщик", "es": "Contraparte / Proveedor", "nl": "Relatie / Leverancier",
        "fr": "Tiers / Fournisseur", "pt": "Entidade / Fornecedor", "zh_Hans": "结算单位 / 商户", "ja": "取引先 / 仕入先"
    },
    "No expense receipts recorded yet.": {
        "ru": "Чеки расходов еще не записаны.", "es": "No hay recibos de gastos registrados aún.", "nl": "Nog geen bonnetjes geregistreerd.",
        "fr": "Aucun reçu de dépense enregistré pour l'instant.", "pt": "Nenhum recibo de despesa registado ainda.", "zh_Hans": "暂未记录任何费用收据。", "ja": "経費領収書はまだ登録されていません。"
    },
    "Record Cash Expense": {
        "ru": "Записать расход", "es": "Registrar Gasto en Efectivo", "nl": "Contante Uitgave Registreren",
        "fr": "Enregistrer une Dépense", "pt": "Registar Despesa em Dinheiro", "zh_Hans": "登记现金日常开支", "ja": "現金支出の登録"
    },
    "Expense Category": {
        "ru": "Категория расходов", "es": "Categoría de Gasto", "nl": "Uitgavencategorie",
        "fr": "Catégorie de Dépense", "pt": "Categoria de Despesa", "zh_Hans": "报销费用科目", "ja": "経費科目"
    },
    "Total Amount (€)": {
        "ru": "Итоговая сумма (€)", "es": "Importe Total (€)", "nl": "Totaalbedrag (€)",
        "fr": "Montant Total (€)", "pt": "Valor Total (€)", "zh_Hans": "支出金额 (€)", "ja": "合計金額 (€)"
    },
    "Tax Amount (€)": {
        "ru": "Сумма налога (€)", "es": "Importe de Impuestos (€)", "nl": "BTW-bedrag (€)",
        "fr": "Montant de la Taxe (€)", "pt": "Valor do Imposto (€)", "zh_Hans": "税额 (€)", "ja": "税額 (€)"
    },
    "Vendor / Counterparty (optional)": {
        "ru": "Поставщик / Контрагент (необязательно)", "es": "Proveedor / Contraparte (opcional)", "nl": "Leverancier / Relatie (optioneel)",
        "fr": "Fournisseur / Tiers (facultatif)", "pt": "Fornecedor / Entidade (opcional)", "zh_Hans": "往来供应商 (选填)", "ja": "仕入先 / 取引先 (任意)"
    },
    "None / General Store": {
        "ru": "Нет / Общий магазин", "es": "Ninguno / Tienda General", "nl": "Geen / Algemene Winkel",
        "fr": "Aucun / Magasin Général", "pt": "Nenhum / Loja Geral", "zh_Hans": "无 / 零售商超", "ja": "なし / 一般店舗"
    },
    "Notes": {
        "ru": "Примечания", "es": "Notas", "nl": "Notities",
        "fr": "Notes", "pt": "Notas", "zh_Hans": "备注文档", "ja": "備考"
    },
    "Add Expense Record": {
        "ru": "Добавить запись расхода", "es": "Añadir Registro de Gasto", "nl": "Uitgave Toevoegen",
        "fr": "Ajouter la Dépense", "pt": "Adicionar Registo de Despesa", "zh_Hans": "录入费用凭证", "ja": "経費記録を追加"
    },
    "Add Product SKU": {
        "ru": "Добавить товар (SKU)", "es": "Añadir SKU de Producto", "nl": "Product-SKU Toevoegen",
        "fr": "Ajouter un Produit (SKU)", "pt": "Adicionar SKU de Produto", "zh_Hans": "新增商品 SKU", "ja": "商品SKUを追加"
    },
    "Total Product SKUs": {
        "ru": "Всего артикулов (SKU)", "es": "Total de SKUs de Producto", "nl": "Totaal Product-SKUs",
        "fr": "Total des Produits (SKU)", "pt": "Total de SKUs de Produtos", "zh_Hans": "现有商品 SKU 种类", "ja": "商品SKU総数"
    },
    "SKU / Code": {
        "ru": "Артикул / Код", "es": "SKU / Código", "nl": "SKU / Code",
        "fr": "SKU / Code", "pt": "SKU / Código", "zh_Hans": "商品编码 / SKU", "ja": "商品コード / SKU"
    },
    "Product Name": {
        "ru": "Наименование товара", "es": "Nombre del Producto", "nl": "Productnaam",
        "fr": "Nom du Produit", "pt": "Nome do Produto", "zh_Hans": "商品名称", "ja": "商品名"
    },
    "Cost / Sale": {
        "ru": "Закупка / Продажа", "es": "Coste / Venta", "nl": "Inkoop / Verkoop",
        "fr": "Coût / Vente", "pt": "Custo / Venda", "zh_Hans": "成本价 / 销售价", "ja": "原価 / 売価"
    },
    "On Hand": {
        "ru": "В наличии", "es": "En Stock", "nl": "Op Voorraad",
        "fr": "En Stock", "pt": "Em Stock", "zh_Hans": "在库可用数量", "ja": "現在庫"
    },
    "Stock Status": {
        "ru": "Статус запасов", "es": "Estado de Stock", "nl": "Voorraadstatus",
        "fr": "Statut du Stock", "pt": "Estado do Stock", "zh_Hans": "库存健康度", "ja": "在庫状態"
    },
    "Reorder Needed": {
        "ru": "Требуется дозаказ", "es": "Reorden Necesaria", "nl": "Nabestelling Nodig",
        "fr": "Réapprovisionnement Nécessaire", "pt": "Reposição Necessária", "zh_Hans": "需要补货采购", "ja": "要発注"
    },
    "In Stock": {
        "ru": "В наличии", "es": "En Stock", "nl": "Op Voorraad",
        "fr": "En Stock", "pt": "Em Stock", "zh_Hans": "库存充足", "ja": "在庫あり"
    },
    "No products found in warehouse inventory.": {
        "ru": "Товары на складе не найдены.", "es": "No se encontraron productos en el inventario.", "nl": "Geen producten gevonden in het magazijn.",
        "fr": "Aucun produit trouvé dans l'entrepôt.", "pt": "Nenhum produto encontrado no armazém.", "zh_Hans": "仓库中暂无任何商品库存。", "ja": "倉庫在庫に登録された商品はありません。"
    },
    "Add New Inventory Product": {
        "ru": "Добавить новый товар на склад", "es": "Añadir Nuevo Producto al Inventario", "nl": "Nieuw Product Toevoegen aan Magazijn",
        "fr": "Ajouter un Nouveau Produit à l'Inventaire", "pt": "Adicionar Novo Produto ao Inventário", "zh_Hans": "录入新库存商品", "ja": "新規在庫商品の登録"
    },
    "SKU Code *": {
        "ru": "Код SKU *", "es": "Código SKU *", "nl": "SKU-code *",
        "fr": "Code SKU *", "pt": "Código SKU *", "zh_Hans": "商品 SKU 编码 *", "ja": "SKUコード *"
    },
    "Unit of Measure": {
        "ru": "Единица измерения", "es": "Unidad de Medida", "nl": "Eenheid",
        "fr": "Unité de Mesure", "pt": "Unidade de Medida", "zh_Hans": "计量单位", "ja": "単位"
    },
    "Product / Item Name *": {
        "ru": "Название товара / позиции *", "es": "Nombre del Producto / Artículo *", "nl": "Product- / Artikelnaam *",
        "fr": "Nom du Produit / Article *", "pt": "Nome do Produto / Item *", "zh_Hans": "商品 / 物料名称 *", "ja": "商品・品目名 *"
    },
    "Cost Price (€)": {
        "ru": "Цена закупки (€)", "es": "Precio de Coste (€)", "nl": "Inkoopprijs (€)",
        "fr": "Prix de Revient (€)", "pt": "Preço de Custo (€)", "zh_Hans": "进货采购单价 (€)", "ja": "仕入原価 (€)"
    },
    "Sale Price (€)": {
        "ru": "Цена продажи (€)", "es": "Precio de Venta (€)", "nl": "Verkoopprijs (€)",
        "fr": "Prix de Vente (€)", "pt": "Preço de Venda (€)", "zh_Hans": "销售售价 (€)", "ja": "販売価格 (€)"
    },
    "Initial Stock": {
        "ru": "Начальный остаток", "es": "Stock Inicial", "nl": "Initiële Voorraad",
        "fr": "Stock Initial", "pt": "Stock Inicial", "zh_Hans": "初始入库库存", "ja": "初期在庫数量"
    },
    "Reorder Point": {
        "ru": "Точка дозаказа", "es": "Punto de Reorden", "nl": "Bestelniveau",
        "fr": "Seuil de Réapprovisionnement", "pt": "Ponto de Encomenda", "zh_Hans": "安全库存下限", "ja": "発注点"
    },
    "Save Product": {
        "ru": "Сохранить товар", "es": "Guardar Producto", "nl": "Product Opslaan",
        "fr": "Enregistrer le Produit", "pt": "Guardar Produto", "zh_Hans": "保存商品档案", "ja": "商品を保存"
    },
    "Waybill / Consignment #": {
        "ru": "Номер накладной / рейса", "es": "N.º de Albarán / Envío", "nl": "Vrachtbrief- / Leveringsnummer",
        "fr": "N° de Bordereau / Lettre de Voiture", "pt": "N.º de Guia / Remessa", "zh_Hans": "运单号 / 送货单号", "ja": "運送状 / 納品伝票番号"
    },
    "Carrier": {
        "ru": "Перевозчик", "es": "Transportista", "nl": "Vervoerder",
        "fr": "Transporteur", "pt": "Transportadora", "zh_Hans": "承运物流", "ja": "配送業者"
    },
    "Delivery Date": {
        "ru": "Дата доставки", "es": "Fecha de Entrega", "nl": "Leverdatum",
        "fr": "Date de Livraison", "pt": "Data de Entrega", "zh_Hans": "交付日期", "ja": "納品日"
    },
    "Scan Waybill / Delivery Note": {
        "ru": "Сканировать накладную", "es": "Escanear Albarán / Nota de Entrega", "nl": "Vrachtbrief / Afleverbon Scannen",
        "fr": "Scanner le Bordereau / Bon de Livraison", "pt": "Digitalizar Guia de Remessa", "zh_Hans": "扫描物流运单 / 送货单", "ja": "納品伝票・運送状をスキャン"
    },
    "No consignments recorded.": {
        "ru": "Накладные не зарегистрированы.", "es": "No hay albaranes registrados.", "nl": "Geen leveringen geregistreerd.",
        "fr": "Aucun bordereau enregistré.", "pt": "Nenhuma guia de remessa registada.", "zh_Hans": "暂未登记任何送货单据。", "ja": "納品伝票は登録されていません。"
    },
    "From": {
        "ru": "Отправитель", "es": "De", "nl": "Van",
        "fr": "De", "pt": "De", "zh_Hans": "发货方", "ja": "発送元"
    },
    "Scheduled Date": {
        "ru": "Запланированная дата", "es": "Fecha Programada", "nl": "Geplande Datum",
        "fr": "Date Prévue", "pt": "Data Agendada", "zh_Hans": "计划交接日", "ja": "予定日"
    },
    "Confirm & Stock In": {
        "ru": "Подтвердить и оприходовать", "es": "Confirmar y Dar Entrada", "nl": "Bevestigen & Inboeken",
        "fr": "Confirmer & Mettre en Stock", "pt": "Confirmar e Dar Entrada", "zh_Hans": "确认验收入库", "ja": "検収・入庫を確定"
    },
    "Manifest Items": {
        "ru": "Товарные позиции манифеста", "es": "Artículos del Manifiesto", "nl": "Goederenlijst",
        "fr": "Articles du Manifeste", "pt": "Itens do Manifesto", "zh_Hans": "托运清单商品明细", "ja": "積載品明細"
    },
    "Expected Qty": {
        "ru": "Ожидаемое кол-во", "es": "Cant. Esperada", "nl": "Verwachte Hoeveelheid",
        "fr": "Qté Attendue", "pt": "Qtd. Esperada", "zh_Hans": "应收数量", "ja": "予定数量"
    },
    "Received Qty": {
        "ru": "Полученное кол-во", "es": "Cant. Recibida", "nl": "Ontvangen Hoeveelheid",
        "fr": "Qté Reçue", "pt": "Qtd. Recebida", "zh_Hans": "实收数量", "ja": "受領数量"
    },
    "No items listed.": {
        "ru": "Позиции отсутствуют.", "es": "No hay artículos listados.", "nl": "Geen artikelen vermeld.",
        "fr": "Aucun article répertorié.", "pt": "Nenhum item listado.", "zh_Hans": "无明细物品项。", "ja": "品目が登録されていません。"
    },
    "Inventory Stock Movements Log": {
        "ru": "Журнал перемещения запасов", "es": "Registro de Movimientos de Inventario", "nl": "Voorraadmutatieoverzicht",
        "fr": "Historique des Mouvements de Stock", "pt": "Registo de Movimentos de Stock", "zh_Hans": "库存出入库变动审计日志", "ja": "在庫移動履歴ログ"
    },
    "Timestamp": {
        "ru": "Время записи", "es": "Hora", "nl": "Tijdstip",
        "fr": "Horodatage", "pt": "Data/Hora", "zh_Hans": "时间戳", "ja": "タイムスタンプ"
    },
    "Product": {
        "ru": "Товар", "es": "Producto", "nl": "Product",
        "fr": "Produit", "pt": "Produto", "zh_Hans": "商品物料", "ja": "対象商品"
    },
    "Qty Adjusted": {
        "ru": "Изменение кол-ва", "es": "Cant. Ajustada", "nl": "Aangepaste Hoeveelheid",
        "fr": "Qté Ajustée", "pt": "Qtd. Ajustada", "zh_Hans": "变动调整量", "ja": "数量変動"
    },
    "New Balance": {
        "ru": "Новый остаток", "es": "Nuevo Saldo", "nl": "Nieuw Saldo",
        "fr": "Nouveau Solde", "pt": "Novo Saldo", "zh_Hans": "变动后结存", "ja": "調整後残高"
    },
    "Live iCalendar (.ics) Sync Feed": {
        "ru": "Прямая ссылка синхронизации iCalendar (.ics)", "es": "Feed de Sincronización iCalendar (.ics)", "nl": "Live iCalendar (.ics) Synchronisatielink",
        "fr": "Flux de Synchronisation iCalendar (.ics)", "pt": "Ligação de Sincronização iCalendar (.ics)", "zh_Hans": "实时 iCalendar (.ics) 订阅同步源", "ja": "iCalendar (.ics) リアルタイム同期フィード"
    },
    "Copy URL": {
        "ru": "Скопировать ссылку", "es": "Copiar Enlace", "nl": "Link Kopiëren",
        "fr": "Copier le Lien", "pt": "Copiar Ligação", "zh_Hans": "复制订阅链接", "ja": "URLをコピー"
    },
    "Copied!": {
        "ru": "Скопировано!", "es": "¡Copiado!", "nl": "Gekopieerd!",
        "fr": "Copié !", "pt": "Copiado!", "zh_Hans": "已复制到剪贴板！", "ja": "コピーしました！"
    },
    "Download .ics": {
        "ru": "Скачать .ics", "es": "Descargar .ics", "nl": ".ics Downloaden",
        "fr": "Télécharger .ics", "pt": "Descarregar .ics", "zh_Hans": "下载 .ics 日历文件", "ja": ".ics ファイルをダウンロード"
    },
    "Legend:": {
        "ru": "Обозначения:", "es": "Leyenda:", "nl": "Legenda:",
        "fr": "Légende :", "pt": "Legenda:", "zh_Hans": "日程色标说明：", "ja": "凡例："
    },
    "Outgoing Payment Due": {
        "ru": "Срок исходящего платежа", "es": "Pago Pendiente", "nl": "Uitgaande Betaling Vervalt",
        "fr": "Échéance de Paiement Sortant", "pt": "Pagamento a Vencer", "zh_Hans": "对外款项到期日", "ja": "買掛金支払期日"
    },
    "Expected Incoming Payment": {
        "ru": "Ожидаемый входящий платеж", "es": "Cobro Esperado", "nl": "Verwachte Inkomende Betaling",
        "fr": "Paiement Entrant Attendu", "pt": "Recebimento Esperado", "zh_Hans": "预期客户回款日", "ja": "売掛金回収期日"
    },
    "Contract Renewal / Notice": {
        "ru": "Продление / уведомление по договору", "es": "Renovación / Aviso de Contrato", "nl": "Contractverlenging / Kennisgeving",
        "fr": "Renouvellement / Préavis de Contrat", "pt": "Renovação / Aviso de Contrato", "zh_Hans": "合同续约 / 到期通知", "ja": "契約更新・通知期限"
    },
    "Consignment Delivery": {
        "ru": "Доставка по накладной", "es": "Entrega de Albarán", "nl": "Levering van Goederen",
        "fr": "Livraison de Marchandises", "pt": "Entrega de Guia", "zh_Hans": "货品交付验收日", "ja": "納品予定日"
    },
    "Admin Task": {
        "ru": "Административная задача", "es": "Tarea Administrativa", "nl": "Administratieve Taak",
        "fr": "Tâche Administrative", "pt": "Tarefa Administrativa", "zh_Hans": "常规行政事务", "ja": "一般総務タスク"
    },
    "Pending Action Tasks": {
        "ru": "Задачи, ожидающие выполнения", "es": "Tareas Pendientes de Acción", "nl": "Openstaande Taken",
        "fr": "Tâches en Attente d'Action", "pt": "Tarefas Pendentes", "zh_Hans": "待处理行动任务", "ja": "未完了タスク一覧"
    },
    "Mark as completed": {
        "ru": "Отметить как выполненное", "es": "Marcar como completada", "nl": "Als voltooid markeren",
        "fr": "Marquer comme terminée", "pt": "Marcar como concluída", "zh_Hans": "标记为已完成", "ja": "完了済みにする"
    },
    "No pending tasks. Everything is up to date!": {
        "ru": "Нет ожидающих задач. Все дела выполнены!", "es": "¡No hay tareas pendientes! Todo está al día.", "nl": "Geen openstaande taken. Alles is bijgewerkt!",
        "fr": "Aucune tâche en attente. Tout est à jour !", "pt": "Nenhuma tarefa pendente. Tudo em dia!", "zh_Hans": "暂无待办任务。所有日程均已处理完毕！", "ja": "未完了タスクはありません。すべて対応済みです！"
    },
    "Add Counterparty": {
        "ru": "Добавить контрагента", "es": "Añadir Contraparte", "nl": "Relatie Toevoegen",
        "fr": "Ajouter un Tiers", "pt": "Adicionar Entidade", "zh_Hans": "新增往来单位", "ja": "取引先を追加"
    },
    "Company Name": {
        "ru": "Название компании", "es": "Nombre de la Empresa", "nl": "Bedrijfsnaam",
        "fr": "Nom de l'Entreprise", "pt": "Nome da Empresa", "zh_Hans": "企业全称", "ja": "企業名"
    },
    "Contact": {
        "ru": "Контакты", "es": "Contacto", "nl": "Contact",
        "fr": "Contact", "pt": "Contacto", "zh_Hans": "联系方式", "ja": "連絡先"
    },
    "No counterparties registered yet.": {
        "ru": "Контрагенты еще не зарегистрированы.", "es": "No hay contrapartes registradas aún.", "nl": "Nog geen relaties geregistreerd.",
        "fr": "Aucun tiers enregistré pour l'instant.", "pt": "Nenhuma entidade registada ainda.", "zh_Hans": "尚未登记任何往来企业。", "ja": "取引先はまだ登録されていません。"
    },
    "Entity Name *": {
        "ru": "Название организации *", "es": "Nombre de la Empresa *", "nl": "Bedrijfsnaam *",
        "fr": "Nom de l'Entité *", "pt": "Nome da Entidade *", "zh_Hans": "单位全称 *", "ja": "法人名 *"
    },
    "Tax / VAT Number": {
        "ru": "Номер ИНН / НДС", "es": "NIF / CIF / IVA", "nl": "BTW-nummer",
        "fr": "Numéro de TVA", "pt": "NIF / IVA", "zh_Hans": "税号 / 组织机构代码", "ja": "税務番号"
    },
    "Bank Name": {
        "ru": "Название банка", "es": "Nombre del Banco", "nl": "Banknaam",
        "fr": "Nom de la Banque", "pt": "Nome do Banco", "zh_Hans": "开户银行名称", "ja": "銀行名"
    },
    "Billing / Physical Address": {
        "ru": "Юридический / фактический адрес", "es": "Dirección de Facturación / Física", "nl": "Factuur- / Vestigingsadres",
        "fr": "Adresse de Facturation / Siège", "pt": "Endereço de Faturação / Físico", "zh_Hans": "注册 / 实际营业地址", "ja": "請求先・事業所所在地"
    },
    "Save Counterparty": {
        "ru": "Сохранить контрагента", "es": "Guardar Contraparte", "nl": "Relatie Opslaan",
        "fr": "Enregistrer le Tiers", "pt": "Guardar Entidade", "zh_Hans": "保存往来档案", "ja": "取引先を保存"
    },
    "Register Contract": {
        "ru": "Зарегистрировать договор", "es": "Registrar Contrato", "nl": "Contract Registreren",
        "fr": "Enregistrer un Contrat", "pt": "Registar Contrato", "zh_Hans": "登记新合同", "ja": "契約書を登録"
    },
    "Contract Title / #": {
        "ru": "Название договора / №", "es": "Título del Contrato / N.º", "nl": "Contracttitel / -nummer",
        "fr": "Titre du Contrat / N°", "pt": "Título do Contrato / N.º", "zh_Hans": "合同名称 / 编号", "ja": "契約名 / 契約番号"
    },
    "Period (Start &rarr; End)": {
        "ru": "Срок (Начало &rarr; Окончание)", "es": "Período (Inicio &rarr; Fin)", "nl": "Looptijd (Begin &rarr; Einde)",
        "fr": "Période (Début &rarr; Fin)", "pt": "Período (Início &rarr; Fim)", "zh_Hans": "有效周期 (起始 &rarr; 截止)", "ja": "契約期間 (開始 &rarr; 終了)"
    },
    "Renewal Terms": {
        "ru": "Условия продления", "es": "Condiciones de Renovación", "nl": "Verlengingsvoorwaarden",
        "fr": "Conditions de Renouvellement", "pt": "Termos de Renovação", "zh_Hans": "续签与终止条款", "ja": "更新条項"
    },
    "Auto-renews": {
        "ru": "Автопродление", "es": "Auto-renovación", "nl": "Automatisch verlengd",
        "fr": "Renouvellement automatique", "pt": "Auto-renovação", "zh_Hans": "自动续期", "ja": "自動更新"
    },
    "notice": {
        "ru": "уведомление", "es": "preaviso", "nl": "kennisgeving",
        "fr": "préavis", "pt": "aviso", "zh_Hans": "提前通知", "ja": "事前通知"
    },
    "Fixed Term": {
        "ru": "Фиксированный срок", "es": "Plazo Fijo", "nl": "Vaste Looptijd",
        "fr": "Durée Déterminée", "pt": "Prazo Fixo", "zh_Hans": "固定期限", "ja": "定期契約"
    },
    "No contracts registered yet.": {
        "ru": "Договоры еще не зарегистрированы.", "es": "No hay contratos registrados aún.", "nl": "Nog geen contracten geregistreerd.",
        "fr": "Aucun contrat enregistré pour l'instant.", "pt": "Nenhum contrato registado ainda.", "zh_Hans": "尚未登记任何合同协议。", "ja": "契約書はまだ登録されていません。"
    },
    "Register New Contract": {
        "ru": "Регистрация нового договора", "es": "Registrar Nuevo Contrato", "nl": "Nieuw Contract Registreren",
        "fr": "Enregistrer un Nouveau Contrat", "pt": "Registar Novo Contrato", "zh_Hans": "归档新合同", "ja": "新規契約の登録"
    },
    "Contract Title *": {
        "ru": "Название договора *", "es": "Título del Contrato *", "nl": "Contracttitel *",
        "fr": "Titre du Contrat *", "pt": "Título do Contrato *", "zh_Hans": "合同主题名称 *", "ja": "契約名称 *"
    },
    "Counterparty *": {
        "ru": "Контрагент *", "es": "Contraparte *", "nl": "Tegenpartij *",
        "fr": "Tiers / Partenaire *", "pt": "Entidade *", "zh_Hans": "合作单位 *", "ja": "契約先 *"
    },
    "Start Date": {
        "ru": "Дата начала", "es": "Fecha de Inicio", "nl": "Ingangsdatum",
        "fr": "Date de Début", "pt": "Data de Início", "zh_Hans": "生效起始日期", "ja": "契約開始日"
    },
    "End / Expiry Date": {
        "ru": "Дата окончания / истечения", "es": "Fecha de Fin / Vencimiento", "nl": "Eind- / Vervaldatum",
        "fr": "Date de Fin / Expiration", "pt": "Data de Fim / Caducidade", "zh_Hans": "到期截止日期", "ja": "契約終了日"
    },
    "Notice Period (Days)": {
        "ru": "Срок уведомления (дни)", "es": "Período de Preaviso (Días)", "nl": "Opzegtermijn (Dagen)",
        "fr": "Préavis (Jours)", "pt": "Prazo de Aviso (Dias)", "zh_Hans": "通知解约期 (天)", "ja": "解約申入期間 (日)"
    },
    "Auto-renews?": {
        "ru": "Автопродление?", "es": "¿Se auto-renueva?", "nl": "Automatisch verlengen?",
        "fr": "Renouvellement auto ?", "pt": "Renovação automática?", "zh_Hans": "是否自动续签？", "ja": "自動更新あり？"
    },
    "Save Contract": {
        "ru": "Сохранить договор", "es": "Guardar Contrato", "nl": "Contract Opslaan",
        "fr": "Enregistrer le Contrat", "pt": "Guardar Contrato", "zh_Hans": "保存合同归档", "ja": "契約を保存"
    },
    "Mark All as Read": {
        "ru": "Отметить все как прочитанные", "es": "Marcar Todo como Leído", "nl": "Alles als Gelezen Markeren",
        "fr": "Tout Marquer comme Lu", "pt": "Marcar Tudo como Lido", "zh_Hans": "全部标为已读", "ja": "すべて既読にする"
    },
    "View Record": {
        "ru": "Перейти к записи", "es": "Ver Registro", "nl": "Record Bekijken",
        "fr": "Voir l'Enregistrement", "pt": "Ver Registo", "zh_Hans": "查看关联记录", "ja": "該当データを確認"
    },
    "No reminders or alerts recorded yet.": {
        "ru": "Напоминаний и уведомлений пока нет.", "es": "No hay recordatorios o alertas registrados aún.", "nl": "Nog geen herinneringen of meldingen geregistreerd.",
        "fr": "Aucun rappel ou alerte enregistré pour l'instant.", "pt": "Nenhum lembrete ou alerta registado ainda.", "zh_Hans": "暂无任何提醒与告警记录。", "ja": "通知やアラートはまだありません。"
    },
    "No address registered": {
        "ru": "Адрес не указан", "es": "Sin dirección registrada", "nl": "Geen adres geregistreerd",
        "fr": "Aucune adresse enregistrée", "pt": "Nenhum endereço registado", "zh_Hans": "未登记地址", "ja": "住所未登録"
    },
    "Ongoing": {
        "ru": "Бессрочный", "es": "Indefinido", "nl": "Doorlopend",
        "fr": "Indéterminé", "pt": "Indeterminado", "zh_Hans": "长期有效", "ja": "継続・無期限"
    },
    "Direct": {
        "ru": "Прямая поставка", "es": "Directo", "nl": "Direct",
        "fr": "Direct", "pt": "Direto", "zh_Hans": "直接交付", "ja": "自社・直送"
    },
    "General Store / Cash": {
        "ru": "Розничный магазин / Наличные", "es": "Comercio General / Efectivo", "nl": "Winkel / Contant",
        "fr": "Commerce Général / Espèces", "pt": "Comércio Geral / Dinheiro", "zh_Hans": "普通商户 / 现金", "ja": "一般店舗 / 現金"
    },
    "Standard single line invoice": {
        "ru": "Стандартный однострочный счет", "es": "Factura estándar de línea única", "nl": "Standaard factuur met één regel",
        "fr": "Facture standard à ligne unique", "pt": "Fatura padrão de linha única", "zh_Hans": "标准单项发票", "ja": "単一品目請求書"
    },
    "No items listed.": {
        "ru": "Товары не указаны.", "es": "No hay artículos listados.", "nl": "Geen artikelen vermeld.",
        "fr": "Aucun article répertorié.", "pt": "Nenhum item listado.", "zh_Hans": "暂无清单明细。", "ja": "品目が登録されていません。"
    },
    "General": {
        "ru": "Основная", "es": "General", "nl": "Algemeen",
        "fr": "Général", "pt": "Geral", "zh_Hans": "常规", "ja": "一般"
    },
    "Payment amount must be greater than zero.": {
        "ru": "Сумма платежа должна быть больше нуля.", "es": "El importe del pago debe ser mayor que cero.", "nl": "Het betalingsbedrag moet groter zijn dan nul.",
        "fr": "Le montant du paiement doit être supérieur à zéro.", "pt": "O valor do pagamento deve ser superior a zero.", "zh_Hans": "支付金额必须大于零。", "ja": "支払額は0より大きい必要があります。"
    },
    "Invalid payment amount.": {
        "ru": "Недопустимая сумма платежа.", "es": "Importe de pago no válido.", "nl": "Ongeldig betalingsbedrag.",
        "fr": "Montant de paiement invalide.", "pt": "Valor de pagamento inválido.", "zh_Hans": "支付金额无效。", "ja": "無効な支払金額です。"
    },
    "Please select a scanned PDF or image document.": {
        "ru": "Пожалуйста, выберите отсканированный PDF или изображение.", "es": "Por favor, seleccione un documento PDF escaneado o una imagen.", "nl": "Selecteer een gescand PDF- of afbeeldingsdocument.",
        "fr": "Veuillez sélectionner un document PDF ou une image numérisée.", "pt": "Por favor, selecione um documento PDF ou imagem digitalizada.", "zh_Hans": "请选择扫描版 PDF 或图片文件。", "ja": "スキャンしたPDFまたは画像ファイルを選択してください。"
    },
    "AI extraction re-run complete!": {
        "ru": "Повторное извлечение данных ИИ завершено!", "es": "¡Reextracción por IA completada!", "nl": "AI-extractie opnieuw uitgevoerd!",
        "fr": "Ré-extraction par IA terminée !", "pt": "Reextração por IA concluída!", "zh_Hans": "AI 重新解析完成！", "ja": "AIによる再解析が完了しました！"
    },
    "All notifications marked as read.": {
        "ru": "Все уведомления помечены как прочитанные.", "es": "Todas las notificaciones marcadas como leídas.", "nl": "Alle meldingen gemarkeerd als gelezen.",
        "fr": "Toutes les notifications marquées comme lues.", "pt": "Todas as notificações marcadas como lidas.", "zh_Hans": "所有通知已标记为已读。", "ja": "すべての通知を既読にしました。"
    },
    "Reminders check complete. All payments, contracts, and inventory are in order!": {
        "ru": "Проверка напоминаний завершена. Все платежи, контракты и складские запасы в порядке!", "es": "¡Comprobación de recordatorios completa! Todos los pagos, contratos e inventario están al día.", "nl": "Herinneringencontrole voltooid. Alle betalingen, contracten en voorraad zijn in orde!",
        "fr": "Vérification des rappels terminée. Tous les paiements, contrats et stocks sont en ordre !", "pt": "Verificação de lembretes concluída. Todos os pagamentos, contratos e stock estão em ordem!", "zh_Hans": "提醒检查完毕。所有账单、合同与仓库库存均正常！", "ja": "リマインダー確認が完了しました。すべての支払、契約、在庫は正常です！"
    },
    "This consignment has already been received and stocked.": {
        "ru": "Эта партия уже принята и оприходована на складе.", "es": "Este envío ya ha sido recibido y almacenado.", "nl": "Deze zending is al ontvangen en op voorraad genomen.",
        "fr": "Cet envoi a déjà été réceptionné et stocké.", "pt": "Esta remessa já foi recebida e armazenada.", "zh_Hans": "该发货单货物已经入库入册。", "ja": "この委託貨物は既に検品・入庫済みです。"
    },
    "Track product inventory levels, consignment deliveries, and automated stock movements.": {
        "ru": "Контроль остатков на складе, поставок по накладным и автоматических движений товаров.",
        "es": "Control de niveles de inventario, entregas de consignaciones y movimientos automáticos de stock.",
        "nl": "Volg voorraadniveaus, leveringen van zendingen en automatische voorraadmutaties.",
        "fr": "Suivi des niveaux de stock, des livraisons et des mouvements automatiques d'inventaire.",
        "pt": "Acompanhe os níveis de stock, entregas de remessas e movimentos automáticos de inventário.",
        "zh_Hans": "实时跟踪商品库存水平、发货单交付及自动化出入库变动记录。",
        "ja": "商品在庫数、納品書受領、および自動入出庫履歴を追跡・管理します。"
    },
    "Manage delivery receipts, waybills, and stock intake operations.": {
        "ru": "Управление товарными накладными, путевыми листами и операциями оприходования на склад.",
        "es": "Gestione albaranes de entrega, hojas de ruta y operaciones de recepción de existencias.",
        "nl": "Beheer leveringsbonnen, vrachtbrieven en inslagoperaties in het magazijn.",
        "fr": "Gérez les récépissés de livraison, lettres de voiture et opérations de réception en stock.",
        "pt": "Faça a gestão de guias de entrega, guias de transporte e operações de entrada em armazém.",
        "zh_Hans": "管理送货回单、物流运单及仓库验收入库作业流程。",
        "ja": "納品書、運送状、および倉庫への受入入庫業務を管理します。"
    },
    "Unified operational schedule with payment deadlines, contract renewals, and delivery waybills.": {
        "ru": "Единый операционный график со сроками платежей, продления договоров и поставок.",
        "es": "Calendario operativo unificado con plazos de pago, renovaciones de contratos y albaranes de entrega.",
        "nl": "Geïntegreerde operationele planning met betalingstermijnen, contractverlengingen en vrachtbrieven.",
        "fr": "Planning opérationnel unifié avec échéances de paiement, renouvellements de contrats et bons de livraison.",
        "pt": "Calendário operacional unificado com prazos de pagamento, renovações de contratos e guias de entrega.",
        "zh_Hans": "集款项到期日、商业合同续约期与物流交付排期于一体的统一业务日程。",
        "ja": "支払期日、契約更新通知、納品スケジュールを統合管理する業務カレンダー。"
    },
    "Master registry of vendors, customers, contractors, banking IBANs, and tax details.": {
        "ru": "Главный реестр поставщиков, клиентов, подрядчиков, банковских IBAN и налоговых данных.",
        "es": "Registro maestro de proveedores, clientes, contratistas, cuentas IBAN y datos fiscales.",
        "nl": "Centraal register van leveranciers, klanten, aannemers, IBAN-rekeningen en fiscale gegevens.",
        "fr": "Registre central des fournisseurs, clients, prestataires, coordonnées IBAN et données fiscales.",
        "pt": "Registo central de fornecedores, clientes, prestadores, contas IBAN e dados fiscais.",
        "zh_Hans": "集中管理供应商、客户、承包商的企业档案、银行 IBAN 账户及税务代码。",
        "ja": "仕入先、顧客、取引業者、銀行IBAN口座、税務情報の統合マスター台帳。"
    },
    "Track key commercial agreements, auto-renewals, and required notice decision deadlines.": {
        "ru": "Отслеживание ключевых коммерческих договоров, автопродлений и сроков уведомлений.",
        "es": "Seguimiento de acuerdos comerciales clave, renovaciones automáticas y plazos de preaviso.",
        "nl": "Volg belangrijke commerciële overeenkomsten, automatische verlengingen en opzegtermijnen.",
        "fr": "Suivi des accords commerciaux clés, reconductions tacites et délais de préavis obligatoires.",
        "pt": "Acompanhe acordos comerciais chave, renovações automáticas e prazos de aviso prévio.",
        "zh_Hans": "跟踪核心商务协议、自动续签条款及关键解约/续约决策通知期限。",
        "ja": "主要な商談契約、自動更新条項、解約通知期限を確実に追跡・管理します。"
    },
    "Payment due dates, contract renewals, overdue bills, and inventory warnings.": {
        "ru": "Сроки платежей, продление договоров, просроченные счета и предупреждения по складу.",
        "es": "Fechas de vencimiento de pago, renovaciones de contrato, facturas vencidas y alertas de stock.",
        "nl": "Vervaldatums van betalingen, contractverlengingen, achterstallige facturen en voorraadwaarschuwingen.",
        "fr": "Échéances de paiement, renouvellements de contrats, factures en retard et alertes de stock.",
        "pt": "Prazos de pagamento, renovações de contratos, faturas em atraso e alertas de stock.",
        "zh_Hans": "账单付款截止期、合同到期续约预警、逾期应付未付及低库存预警。",
        "ja": "支払期日、契約更新期限、期日超過請求書、在庫僅少アラートを通知します。"
    },
    "Track outgoing supplier bills, incoming customer invoices, and payment statuses.": {
        "ru": "Отслеживание исходящих счетов поставщиков, входящих счетов клиентов и статусов оплат.",
        "es": "Seguimiento de facturas de proveedores, facturas de clientes y estados de pago.",
        "nl": "Volg uitgaande leveranciersfacturen, inkomende klantfacturen en betalingsstatussen.",
        "fr": "Suivi des factures fournisseurs à payer, factures clients à encaisser et états de règlement.",
        "pt": "Acompanhe faturas a pagar de fornecedores, faturas a receber de clientes e estados de pagamento.",
        "zh_Hans": "跟踪供应商采购账单、客户销售发票及实时款项收付与核销状态。",
        "ja": "仕入先への支払請求書、顧客からの入金予定請求書、および決済ステータスを追跡。"
    },
    "Ingest, analyze with Multimodal AI, verify, and automatically schedule into ledgers.": {
        "ru": "Загрузка, анализ мультимодальным ИИ, проверка и автоматическое внесение в регистры.",
        "es": "Carga, análisis con IA multimodal, verificación y programación automática en libros contables.",
        "nl": "Inlezen, analyseren met multimodale AI, verifiëren en automatisch inboeken in de administratie.",
        "fr": "Importation, analyse par IA multimodale, vérification et intégration automatique dans les journaux.",
        "pt": "Importação, análise com IA multimodal, verificação e agendamento automático nos livros.",
        "zh_Hans": "摄取单据、多模态 AI 智能解析、人工核对并一键自动记账入册。",
        "ja": "書類の取り込み、マルチモーダルAI解析、検証、そして台帳・カレンダーへの自動登録。"
    },
    "Upload incoming invoices, contracts, receipts, or consignment slips. The AI agent will extract structured data and prepare calendar tasks.": {
        "ru": "Загрузите счета, договоры, чеки или накладные. ИИ-агент извлечет данные и создаст задачи в календаре.",
        "es": "Suba facturas, contratos, recibos o albaranes. El agente de IA extraerá los datos estructurados y creará tareas en el calendario.",
        "nl": "Upload facturen, contracten, bonnen of vrachtbrieven. De AI-agent extraheert gestructureerde gegevens en maakt agendataken aan.",
        "fr": "Téléversez factures, contrats, reçus ou bons de livraison. L'agent IA extraira les données structurées et planifiera les tâches.",
        "pt": "Carregue faturas, contratos, recibos ou guias de remessa. O agente IA extrairá os dados e criará tarefas no calendário.",
        "zh_Hans": "上传发票、合同、收据或发货单。AI 智能体将自动提取结构化数据并生成关联的日程待办事项。",
        "ja": "請求書、契約書、領収書、納品書を登録してください。AIが構造化データを抽出しカレンダー予定を作成します。"
    },
    "Executive Overview & Agent Dashboard": {
        "ru": "Обзор руководства и панель агента", "es": "Resumen Ejecutivo y Panel del Agente", "nl": "Directieoverzicht & Agent Dashboard",
        "fr": "Vue d'Ensemble Exécutive & Tableau de Bord de l'Agent", "pt": "Visão Geral Executiva e Painel do Agente", "zh_Hans": "经营总览与智能工作台", "ja": "経営サマリー＆エージェントダッシュボード"
    },
    "Scanned Documents & AI Ingestion": {
        "ru": "Скан-копии документов и обработка ИИ", "es": "Documentos Escaneados e Ingesta por IA", "nl": "Gescande Documenten & AI-Verwerking",
        "fr": "Documents Numérisés & Traitement IA", "pt": "Documentos Digitalizados e Processamento por IA", "zh_Hans": "扫描单据与 AI 智能解析", "ja": "スキャン書類＆AI取り込み"
    },
    "Unit Price": {
        "ru": "Цена за ед.", "es": "Precio Unitario", "nl": "Eenheidsprijs",
        "fr": "Prix Unitaire", "pt": "Preço Unitário", "zh_Hans": "单价", "ja": "単価"
    },
    "SKU": {
        "ru": "Артикул", "es": "SKU", "nl": "SKU",
        "fr": "SKU", "pt": "SKU", "zh_Hans": "SKU编码", "ja": "SKUコード"
    },
    # Model Choices - Document Types & Statuses
    "Vendor Invoice (Payable)": {
        "ru": "Счет поставщика (К оплате)", "es": "Factura de Proveedor (Por Pagar)", "nl": "Inkoopfactuur (Te Betalen)",
        "fr": "Facture Fournisseur (À Payer)", "pt": "Fatura de Fornecedor (A Pagar)", "zh_Hans": "供应商发票 (应付账款)", "ja": "仕入請求書 (買掛金)"
    },
    "Customer Invoice (Receivable)": {
        "ru": "Счет клиенту (К получению)", "es": "Factura de Cliente (Por Cobrar)", "nl": "Verkoopfactuur (Te Ontvangen)",
        "fr": "Facture Client (À Recevoir)", "pt": "Fatura de Cliente (A Receber)", "zh_Hans": "客户发票 (应收账款)", "ja": "顧客請求書 (売掛金)"
    },
    "General / Unclassified": {
        "ru": "Общий / Не классифицирован", "es": "General / No Clasificado", "nl": "Algemeen / Niet Geclassificeerd",
        "fr": "Général / Non Classé", "pt": "Geral / Não Classificado", "zh_Hans": "常规 / 未分类", "ja": "一般 / 未分類"
    },
    "Receipt / Expense Voucher": {
        "ru": "Чек / Квитанция о расходах", "es": "Recibo / Comprobante de Gastos", "nl": "Kassabon / Uitgavenbewijs",
        "fr": "Reçu / Justificatif de Dépenses", "pt": "Recibo / Comprovativo de Despesa", "zh_Hans": "收据 / 费用凭单", "ja": "領収書 / 経費伝票"
    },
    "Confirmed & Synced": {
        "ru": "Подтверждено и синхронизировано", "es": "Confirmado y Sincronizado", "nl": "Bevestigd en Gesynchroniseerd",
        "fr": "Confirmé et Synchronisé", "pt": "Confirmado e Sincronizado", "zh_Hans": "已确认并同步", "ja": "確認・同期完了"
    },
    "Processing Failed": {
        "ru": "Ошибка обработки", "es": "Error de Procesamiento", "nl": "Verwerking Mislukt",
        "fr": "Échec du Traitement", "pt": "Falha no Processamento", "zh_Hans": "处理失败", "ja": "処理失敗"
    },
    "Processing with AI": {
        "ru": "Обработка с помощью ИИ", "es": "Procesando con IA", "nl": "AI-verwerking Bezig",
        "fr": "Traitement par IA en cours", "pt": "Processando com IA", "zh_Hans": "AI 正在解析处理", "ja": "AI処理中"
    },
    # Model Choices - Accounting Invoices
    "Vendor Bill (Outgoing Payment)": {
        "ru": "Счет от поставщика (Исходящий платеж)", "es": "Factura de Proveedor (Pago Saliente)", "nl": "Inkoopfactuur (Uitgaande Betaling)",
        "fr": "Facture Fournisseur (Paiement Sortant)", "pt": "Fatura de Fornecedor (Pagamento a Emitir)", "zh_Hans": "供应商账单 (支出款项)", "ja": "仕入先請求書 (支払予定)"
    },
    "Overdue": {
        "ru": "Просрочено", "es": "Vencido", "nl": "Achterstallig",
        "fr": "En Retard", "pt": "Vencido", "zh_Hans": "已逾期", "ja": "期限超過"
    },
    "Disputed": {
        "ru": "Оспаривается", "es": "En Disputa", "nl": "Betwist",
        "fr": "Contesté", "pt": "Contestado", "zh_Hans": "有争议", "ja": "異議あり"
    },
    # Model Choices - Warehouse & Consignments
    "Inward Receipt (Supplier Delivery)": {
        "ru": "Входящая поставка (Приемка от поставщика)", "es": "Recepción de Entrada (Entrega de Proveedor)", "nl": "Inkomende Levering (Levering van Leverancier)",
        "fr": "Réception Entrante (Livraison Fournisseur)", "pt": "Recebimento de Entrada (Entrega do Fornecedor)", "zh_Hans": "入库单 (供应商交货)", "ja": "入荷受入 (仕入先納品)"
    },
    "Outward Dispatch (Customer Delivery)": {
        "ru": "Исходящая отгрузка (Доставка клиенту)", "es": "Despacho de Salida (Entrega a Cliente)", "nl": "Uitgaande Verzending (Levering aan Klant)",
        "fr": "Expédition Sortante (Livraison Client)", "pt": "Expedição de Saída (Entrega ao Cliente)", "zh_Hans": "出库发货 (客户配送)", "ja": "出荷発送 (顧客納品)"
    },
    "Expected / In Transit": {
        "ru": "Ожидается / В пути", "es": "Esperado / En Tránsito", "nl": "Verwacht / Onderweg",
        "fr": "Attendu / En Transit", "pt": "Esperado / Em Trânsito", "zh_Hans": "在途 / 预期到达", "ja": "輸送中 / 入荷待ち"
    },
    "Received & Stocked": {
        "ru": "Получено и оприходовано", "es": "Recibido y Almacenado", "nl": "Ontvangen en Opgeslagen",
        "fr": "Reçu et Mis en Stock", "pt": "Recebido e Armazenado", "zh_Hans": "已收货入库", "ja": "受領・入庫済"
    },
    "Discrepancy Noted": {
        "ru": "Выявлены расхождения", "es": "Discrepancia Detectada", "nl": "Afwijking Opgemerkt",
        "fr": "Écart Constaté", "pt": "Divergência Observada", "zh_Hans": "发现差异", "ja": "不一致あり"
    },
    "Rejected": {
        "ru": "Отклонено", "es": "Rechazado", "nl": "Afgewezen",
        "fr": "Rejeté", "pt": "Rejeitado", "zh_Hans": "已拒收", "ja": "却下"
    },
    "Purchase Receipt / Inward": {
        "ru": "Поступление от закупки / Приход", "es": "Recepción de Compra / Entrada", "nl": "Inkoopontvangst / Inkomend",
        "fr": "Réception d'Achat / Entrée", "pt": "Recebimento de Compra / Entrada", "zh_Hans": "采购入库 / 进货", "ja": "仕入入庫 / 受入"
    },
    "Sales Shipment / Outward": {
        "ru": "Отгрузка продаж / Расход", "es": "Envío de Venta / Salida", "nl": "Verkoopverzending / Uitgaand",
        "fr": "Expédition de Vente / Sortie", "pt": "Envio de Venda / Saída", "zh_Hans": "销售出库 / 出货", "ja": "売发出庫 / 出荷"
    },
    "Stock Count / Adjustment": {
        "ru": "Инвентаризация / Корректировка", "es": "Conteo de Inventario / Ajuste", "nl": "Voorraadtelling / Correctie",
        "fr": "Inventaire / Ajustement", "pt": "Contagem de Estoque / Ajuste", "zh_Hans": "盘点库存 / 调整", "ja": "棚卸 / 在庫調整"
    },
    "Return to Supplier / Customer Return": {
        "ru": "Возврат поставщику / Возврат от покупателя", "es": "Devolución a Proveedor / Devolución de Cliente", "nl": "Retour naar Leverancier / Klantretour",
        "fr": "Retour Fournisseur / Retour Client", "pt": "Devolução ao Fornecedor / Devolução do Cliente", "zh_Hans": "退回供应商 / 客户退货", "ja": "仕入先返品 / 顧客返品"
    },
    # Model Choices - Administration & Counterparties
    "Bank / Financial Institution": {
        "ru": "Банк / Финансовая организация", "es": "Banco / Institución Financiera", "nl": "Bank / Financiële Instelling",
        "fr": "Banque / Établissement Financier", "pt": "Banco / Instituição Financeira", "zh_Hans": "银行 / 金融机构", "ja": "銀行 / 金融機関"
    },
    "Draft": {
        "ru": "Черновик", "es": "Borrador", "nl": "Concept",
        "fr": "Brouillon", "pt": "Rascunho", "zh_Hans": "草稿", "ja": "下書き"
    },
    "Active": {
        "ru": "Действующий", "es": "Activo", "nl": "Actief",
        "fr": "Actif", "pt": "Ativo", "zh_Hans": "生效中", "ja": "有効"
    },
    "Pending Renewal": {
        "ru": "Ожидает продления", "es": "Renovación Pendiente", "nl": "Verlenging In Afwachting",
        "fr": "En Attente de Renouvellement", "pt": "Renovação Pendente", "zh_Hans": "待续约", "ja": "更新待ち"
    },
    "Expired": {
        "ru": "Истек", "es": "Expirado", "nl": "Verlopen",
        "fr": "Expiré", "pt": "Expirado", "zh_Hans": "已到期", "ja": "期限切れ"
    },
    "Terminated": {
        "ru": "Расторгнут", "es": "Rescindido", "nl": "Beëindigd",
        "fr": "Résilié", "pt": "Rescindido", "zh_Hans": "已终止", "ja": "解約済"
    },
    # Model Choices - Calendar Tasks
    "Outgoing Payment Due (Payable)": {
        "ru": "Срок исходящего платежа (Кредиторка)", "es": "Vencimiento de Pago Saliente (Por Pagar)", "nl": "Uitgaande Betaling Vervallen (Te Betalen)",
        "fr": "Échéance de Paiement Fournisseur (À Payer)", "pt": "Pagamento Pendente (A Pagar)", "zh_Hans": "应付支出款到期", "ja": "支払期日 (買掛金)"
    },
    "Expected Payment (Receivable)": {
        "ru": "Ожидаемый платеж (Дебиторка)", "es": "Pago Esperado (Por Cobrar)", "nl": "Verwachte Betaling (Te Ontvangen)",
        "fr": "Paiement Attendu (À Recevoir)", "pt": "Pagamento Esperado (A Receber)", "zh_Hans": "应收回款预期", "ja": "入金予定 (売掛金)"
    },
    "Consignment / Delivery Due": {
        "ru": "Срок поставки / отгрузки", "es": "Vencimiento de Envío / Entrega", "nl": "Zending / Levering Verwacht",
        "fr": "Échéance Expédition / Livraison", "pt": "Prazo de Envio / Entrega", "zh_Hans": "发货 / 交付到期", "ja": "納品・発送期日"
    },
    "Administrative Task": {
        "ru": "Административная задача", "es": "Tarea Administrativa", "nl": "Administratieve Taak",
        "fr": "Tâche Administrative", "pt": "Tarefa Administrativa", "zh_Hans": "行政管理任务", "ja": "総務・管理タスク"
    },
    "Low": {
        "ru": "Низкий", "es": "Bajo", "nl": "Laag",
        "fr": "Bas", "pt": "Baixo", "zh_Hans": "低", "ja": "低"
    },
    "Medium": {
        "ru": "Средний", "es": "Medio", "nl": "Gemiddeld",
        "fr": "Moyen", "pt": "Médio", "zh_Hans": "中", "ja": "中"
    },
    "High": {
        "ru": "Высокий", "es": "Alto", "nl": "Hoog",
        "fr": "Haut", "pt": "Alto", "zh_Hans": "高", "ja": "高"
    },
    "Urgent": {
        "ru": "Срочный", "es": "Urgente", "nl": "Urgent",
        "fr": "Urgent", "pt": "Urgente", "zh_Hans": "紧急", "ja": "緊急"
    },
    "Pending": {
        "ru": "Ожидает", "es": "Pendiente", "nl": "In Afwachting",
        "fr": "En Attente", "pt": "Pendente", "zh_Hans": "待处理", "ja": "保留中"
    },
    "In Progress": {
        "ru": "В процессе", "es": "En Progreso", "nl": "In Uitvoering",
        "fr": "En Cours", "pt": "Em Andamento", "zh_Hans": "进行中", "ja": "進行中"
    },
    "Completed": {
        "ru": "Завершено", "es": "Completado", "nl": "Voltooid",
        "fr": "Terminé", "pt": "Concluído", "zh_Hans": "已完成", "ja": "完了"
    },
    "Cancelled": {
        "ru": "Отменено", "es": "Cancelado", "nl": "Geannuleerd",
        "fr": "Annulé", "pt": "Cancelado", "zh_Hans": "已取消", "ja": "キャンセル済"
    },
    # Model Choices - Reminders & Notifications
    "Info": {
        "ru": "Информация", "es": "Información", "nl": "Informatie",
        "fr": "Information", "pt": "Informação", "zh_Hans": "信息", "ja": "情報"
    },
    "Warning": {
        "ru": "Предупреждение", "es": "Advertencia", "nl": "Waarschuwing",
        "fr": "Avertissement", "pt": "Aviso", "zh_Hans": "警告", "ja": "警告"
    },
    "Critical / Urgent": {
        "ru": "Критический / Срочный", "es": "Crítico / Urgente", "nl": "Kritiek / Urgent",
        "fr": "Critique / Urgent", "pt": "Crítico / Urgente", "zh_Hans": "严重 / 紧急", "ja": "重大 / 緊急"
    },
    "Success": {
        "ru": "Успешно", "es": "Éxito", "nl": "Succes",
        "fr": "Succès", "pt": "Sucesso", "zh_Hans": "成功", "ja": "成功"
    },
    "Upcoming Payment Due": {
        "ru": "Предстоящий срок оплаты", "es": "Próximo Vencimiento de Pago", "nl": "Aankomende Betalingsdeadline",
        "fr": "Échéance de Paiement Proche", "pt": "Pagamento a Vencer", "zh_Hans": "即将到期的付款", "ja": "支払期日接近"
    },
    "Overdue Payment": {
        "ru": "Просроченный платеж", "es": "Pago Vencido", "nl": "Achterstallige Betaling",
        "fr": "Paiement en Retard", "pt": "Pagamento em Atraso", "zh_Hans": "逾期付款", "ja": "延滞支払"
    },
    "Contract Renewal": {
        "ru": "Продление договора", "es": "Renovación de Contrato", "nl": "Contractverlenging",
        "fr": "Renouvellement de Contrat", "pt": "Renovação de Contrato", "zh_Hans": "合同续约", "ja": "契約更新"
    },
    "Low Stock Alert": {
        "ru": "Предупреждение о низком остатке", "es": "Alerta de Stock Bajo", "nl": "Melding Laag Voorraadniveau",
        "fr": "Alerte Stock Faible", "pt": "Alerta de Estoque Baixo", "zh_Hans": "库存预警", "ja": "在庫僅少アラート"
    },
    "Document Analyzed": {
        "ru": "Документ проанализирован", "es": "Documento Analizado", "nl": "Document Geanalyseerd",
        "fr": "Document Analysé", "pt": "Documento Analisado", "zh_Hans": "单据已分析", "ja": "書類解析完了"
    },
    "General Alert": {
        "ru": "Общее оповещение", "es": "Alerta General", "nl": "Algemene Melding",
        "fr": "Alerte Générale", "pt": "Alerta Geral", "zh_Hans": "通用提示", "ja": "全般アラート"
    },
    # Model Choices - Chat & Admin
    "Assistant": {
        "ru": "Ассистент", "es": "Asistente", "nl": "Assistent",
        "fr": "Assistant", "pt": "Assistente", "zh_Hans": "助理", "ja": "アシスタント"
    },
    "System": {
        "ru": "Система", "es": "Sistema", "nl": "Systeem",
        "fr": "Système", "pt": "Sistema", "zh_Hans": "系统", "ja": "システム"
    },
    "User": {
        "ru": "Пользователь", "es": "Usuario", "nl": "Gebruiker",
        "fr": "Utilisateur", "pt": "Utilizador", "zh_Hans": "用户", "ja": "ユーザー"
    },
    "Addition": {
        "ru": "Добавление", "es": "Adición", "nl": "Toevoeging",
        "fr": "Ajout", "pt": "Adição", "zh_Hans": "添加", "ja": "追加"
    },
    "Change": {
        "ru": "Изменение", "es": "Modificación", "nl": "Wijziging",
        "fr": "Modification", "pt": "Modificação", "zh_Hans": "修改", "ja": "変更"
    },
    "Deletion": {
        "ru": "Удаление", "es": "Eliminación", "nl": "Verwijdering",
        "fr": "Suppression", "pt": "Eliminação", "zh_Hans": "删除", "ja": "削除"
    },
    # Dynamic Notification & Task Templates
    "New %(doc_type)s Processed": {
        "ru": "Новый документ «%(doc_type)s» обработан", "es": "Nuevo %(doc_type)s Procesado", "nl": "Nieuw %(doc_type)s Verwerkt",
        "fr": "Nouveau %(doc_type)s Traité", "pt": "Novo %(doc_type)s Processado", "zh_Hans": "新单据已处理: %(doc_type)s", "ja": "新規 %(doc_type)s 処理完了"
    },
    "Low Stock Alert: %(product)s": {
        "ru": "Предупреждение о низком остатке: %(product)s", "es": "Alerta de Stock Bajo: %(product)s", "nl": "Melding Laag Voorraadniveau: %(product)s",
        "fr": "Alerte Stock Faible : %(product)s", "pt": "Alerta de Estoque Baixo: %(product)s", "zh_Hans": "低库存预警: %(product)s", "ja": "在庫僅少アラート: %(product)s"
    },
    "OVERDUE: %(kind)s #%(number)s": {
        "ru": "ПРОСРОЧЕНО: %(kind)s #%(number)s", "es": "VENCIDO: %(kind)s #%(number)s", "nl": "ACHTERSTALLIG: %(kind)s #%(number)s",
        "fr": "EN RETARD : %(kind)s #%(number)s", "pt": "VENCIDO: %(kind)s #%(number)s", "zh_Hans": "逾期提醒: %(kind)s #%(number)s", "ja": "期限超過: %(kind)s #%(number)s"
    },
    "Payment Due in %(days)s day(s): #%(number)s": {
        "ru": "Срок оплаты через %(days)s дн.: #%(number)s", "es": "Vencimiento de Pago en %(days)s día(s): #%(number)s", "nl": "Betaling Vervalt over %(days)s dag(en): #%(number)s",
        "fr": "Paiement Dû dans %(days)s jour(s) : #%(number)s", "pt": "Pagamento a Vencer em %(days)s dia(s): #%(number)s", "zh_Hans": "付款在 %(days)s 天内到期: #%(number)s", "ja": "支払期日まであと %(days)s 日: #%(number)s"
    },
    "Payment Due TODAY: #%(number)s": {
        "ru": "Срок оплаты СЕГОДНЯ: #%(number)s", "es": "Vencimiento de Pago HOY: #%(number)s", "nl": "Betaling VANDAAG Vervallen: #%(number)s",
        "fr": "Paiement Dû AUJOURD'HUI : #%(number)s", "pt": "Pagamento a Vencer HOJE: #%(number)s", "zh_Hans": "今日到期付款: #%(number)s", "ja": "本日支払期日: #%(number)s"
    },
    "Contract Renewal Decision: %(counterparty)s": {
        "ru": "Решение о продлении договора: %(counterparty)s", "es": "Decisión de Renovación de Contrato: %(counterparty)s", "nl": "Beslissing Contractverlenging: %(counterparty)s",
        "fr": "Décision de Renouvellement de Contrat : %(counterparty)s", "pt": "Decisão de Renovação de Contrato: %(counterparty)s", "zh_Hans": "合同续约决策: %(counterparty)s", "ja": "契約更新判断: %(counterparty)s"
    },
    "Consignment Delivery Expected: #%(number)s": {
        "ru": "Ожидается поставка груза: #%(number)s", "es": "Entrega de Envío Esperada: #%(number)s", "nl": "Verwachte Levering Zending: #%(number)s",
        "fr": "Livraison de l'Expédition Attendue : #%(number)s", "pt": "Entrega de Remessa Esperada: #%(number)s", "zh_Hans": "预期交货到货: #%(number)s", "ja": "納品予定の荷物: #%(number)s"
    },
    "Outgoing Bill": {
        "ru": "Исходящий счет", "es": "Factura Saliente", "nl": "Uitgaande Factuur",
        "fr": "Facture Sortante", "pt": "Fatura a Pagar", "zh_Hans": "应付账单", "ja": "支払請求書"
    },
    "Incoming Payment": {
        "ru": "Входящий платеж", "es": "Pago Entrante", "nl": "Inkomende Betaling",
        "fr": "Paiement Entrant", "pt": "Recebimento Entrante", "zh_Hans": "应收款项", "ja": "入金予定"
    },
    "%(counterparty)s - #%(number)s confirmed and scheduled into calendar.": {
        "ru": "%(counterparty)s — #%(number)s подтвержден и добавлен в календарь.",
        "es": "%(counterparty)s - #%(number)s confirmado y programado en el calendario.",
        "nl": "%(counterparty)s - #%(number)s bevestigd en ingepland in de agenda.",
        "fr": "%(counterparty)s - #%(number)s confirmé et planifié dans le calendrier.",
        "pt": "%(counterparty)s - #%(number)s confirmado e agendado no calendário.",
        "zh_Hans": "%(counterparty)s - #%(number)s 已确认并排入日程。",
        "ja": "%(counterparty)s - #%(number)s が確認され、カレンダーに登録されました。"
    },
    "We owe %(counterparty)s %(amount)s %(currency)s. Due date was %(date)s (%(days)s days ago).": {
        "ru": "Задолженность перед %(counterparty)s: %(amount)s %(currency)s. Срок был %(date)s (%(days)s дн. назад).",
        "es": "Debemos a %(counterparty)s %(amount)s %(currency)s. La fecha límite era %(date)s (hace %(days)s días).",
        "nl": "We zijn %(counterparty)s %(amount)s %(currency)s verschuldigd. Vervaldatum was %(date)s (%(days)s dagen geleden).",
        "fr": "Nous devons à %(counterparty)s %(amount)s %(currency)s. L'échéance était le %(date)s (il y a %(days)s jours).",
        "pt": "Devemos a %(counterparty)s %(amount)s %(currency)s. O vencimento foi em %(date)s (há %(days)s dias).",
        "zh_Hans": "欠付 %(counterparty)s %(amount)s %(currency)s。到期日为 %(date)s (%(days)s 天前)。",
        "ja": "%(counterparty)s に対する債務 %(amount)s %(currency)s。期日は %(date)s (%(days)s 日前) でした。"
    },
    "Expected from %(counterparty)s %(amount)s %(currency)s. Due date was %(date)s (%(days)s days ago).": {
        "ru": "Ожидается от %(counterparty)s: %(amount)s %(currency)s. Срок был %(date)s (%(days)s дн. назад).",
        "es": "Esperado de %(counterparty)s %(amount)s %(currency)s. La fecha límite era %(date)s (hace %(days)s días).",
        "nl": "Verwacht van %(counterparty)s %(amount)s %(currency)s. Vervaldatum was %(date)s (%(days)s dagen geleden).",
        "fr": "Attendu de %(counterparty)s %(amount)s %(currency)s. L'échéance était le %(date)s (il y a %(days)s jours).",
        "pt": "Esperado de %(counterparty)s %(amount)s %(currency)s. O vencimento foi em %(date)s (há %(days)s dias).",
        "zh_Hans": "应收 %(counterparty)s %(amount)s %(currency)s。到期日为 %(date)s (%(days)s 天前)。",
        "ja": "%(counterparty)s からの回収予定 %(amount)s %(currency)s。期日は %(date)s (%(days)s 日前) でした。"
    },
    "Scheduled payment to %(counterparty)s for %(amount)s %(currency)s on %(date)s.": {
        "ru": "Запланирован платеж поставщику %(counterparty)s на сумму %(amount)s %(currency)s (дата: %(date)s).",
        "es": "Pago programado a %(counterparty)s por %(amount)s %(currency)s el %(date)s.",
        "nl": "Geplande betaling aan %(counterparty)s van %(amount)s %(currency)s op %(date)s.",
        "fr": "Paiement prévu à %(counterparty)s de %(amount)s %(currency)s le %(date)s.",
        "pt": "Pagamento agendado para %(counterparty)s de %(amount)s %(currency)s em %(date)s.",
        "zh_Hans": "已排定于 %(date)s 向 %(counterparty)s 支付 %(amount)s %(currency)s。",
        "ja": "%(date)s に %(counterparty)s への支払予定 %(amount)s %(currency)s。"
    },
    "Expected incoming payment from %(counterparty)s for %(amount)s %(currency)s on %(date)s.": {
        "ru": "Ожидается входящий платеж от %(counterparty)s на сумму %(amount)s %(currency)s (дата: %(date)s).",
        "es": "Cobro esperado de %(counterparty)s por %(amount)s %(currency)s el %(date)s.",
        "nl": "Verwachte betaling van %(counterparty)s van %(amount)s %(currency)s op %(date)s.",
        "fr": "Paiement entrant attendu de %(counterparty)s de %(amount)s %(currency)s le %(date)s.",
        "pt": "Recebimento esperado de %(counterparty)s de %(amount)s %(currency)s em %(date)s.",
        "zh_Hans": "预期于 %(date)s 收到来自 %(counterparty)s 的款项 %(amount)s %(currency)s。",
        "ja": "%(date)s に %(counterparty)s からの入金予定 %(amount)s %(currency)s。"
    },
    "Stock for '%(name)s' [%(sku)s] is down to %(qty)s %(uom)s (Reorder threshold: %(threshold)s).": {
        "ru": "Остаток товара «%(name)s» [%(sku)s] снизился до %(qty)s %(uom)s (Порог дозаказа: %(threshold)s).",
        "es": "El stock de '%(name)s' [%(sku)s] ha bajado a %(qty)s %(uom)s (Umbral de pedido: %(threshold)s).",
        "nl": "Voorraad van '%(name)s' [%(sku)s] is gedaald naar %(qty)s %(uom)s (Drempelwaarde: %(threshold)s).",
        "fr": "Le stock de '%(name)s' [%(sku)s] est descendu à %(qty)s %(uom)s (Seuil de réapprovisionnement : %(threshold)s).",
        "pt": "O estoque de '%(name)s' [%(sku)s] caiu para %(qty)s %(uom)s (Limite de reposição: %(threshold)s).",
        "zh_Hans": "商品 '%(name)s' [%(sku)s] 库存降至 %(qty)s %(uom)s (补货阈值: %(threshold)s)。",
        "ja": "商品「%(name)s」[%(sku)s] の在庫が %(qty)s %(uom)s に低下しました (発注閾値: %(threshold)s)。"
    },
    "Contract '%(title)s' expires on %(end_date)s. Notice deadline is %(notice_date)s (%(days)s days left).": {
        "ru": "Договор «%(title)s» истекает %(end_date)s. Срок уведомления: %(notice_date)s (осталось %(days)s дн.).",
        "es": "El contrato '%(title)s' vence el %(end_date)s. Plazo de aviso: %(notice_date)s (quedan %(days)s días).",
        "nl": "Contract '%(title)s' verloopt op %(end_date)s. Kennisgevingstermijn is %(notice_date)s (nog %(days)s dagen).",
        "fr": "Le contrat '%(title)s' expire le %(end_date)s. Date limite de préavis : %(notice_date)s (%(days)s jours restants).",
        "pt": "O contrato '%(title)s' expira em %(end_date)s. Prazo de aviso: %(notice_date)s (restam %(days)s dias).",
        "zh_Hans": "合同 '%(title)s' 于 %(end_date)s 到期。通知截止日为 %(notice_date)s (剩余 %(days)s 天)。",
        "ja": "契約「%(title)s」は %(end_date)s に満了します。通知期限は %(notice_date)s (残り %(days)s 日) です。"
    },
    "Expected delivery from %(counterparty)s scheduled for %(date)s.": {
        "ru": "Ожидается доставка от %(counterparty)s, запланированная на %(date)s.",
        "es": "Entrega esperada de %(counterparty)s programada para el %(date)s.",
        "nl": "Verwachte levering van %(counterparty)s gepland op %(date)s.",
        "fr": "Livraison attendue de %(counterparty)s prévue le %(date)s.",
        "pt": "Entrega esperada de %(counterparty)s agendada para %(date)s.",
        "zh_Hans": "预计于 %(date)s 收到来自 %(counterparty)s 的交货。",
        "ja": "%(counterparty)s からの納品が %(date)s に予定されています。"
    },
    "Pay Bill #%(number)s to %(counterparty)s": {
        "ru": "Оплатить счет #%(number)s контрагенту %(counterparty)s", "es": "Pagar Factura #%(number)s a %(counterparty)s", "nl": "Betaal Factuur #%(number)s aan %(counterparty)s",
        "fr": "Payer la Facture #%(number)s à %(counterparty)s", "pt": "Pagar Fatura #%(number)s a %(counterparty)s", "zh_Hans": "向 %(counterparty)s 支付账单 #%(number)s", "ja": "%(counterparty)s への請求書 #%(number)s の支払い"
    },
    "OVERDUE: Pay Bill #%(number)s to %(counterparty)s": {
        "ru": "ПРОСРОЧЕНО: Оплатить счет #%(number)s контрагенту %(counterparty)s", "es": "VENCIDO: Pagar Factura #%(number)s a %(counterparty)s", "nl": "ACHTERSTALLIG: Betaal Factuur #%(number)s aan %(counterparty)s",
        "fr": "EN RETARD : Payer la Facture #%(number)s à %(counterparty)s", "pt": "VENCIDO: Pagar Fatura #%(number)s a %(counterparty)s", "zh_Hans": "逾期款项: 向 %(counterparty)s 支付账单 #%(number)s", "ja": "期限超過: %(counterparty)s への請求書 #%(number)s の支払い"
    },
    "Expected Incoming Payment #%(number)s from %(counterparty)s": {
        "ru": "Ожидаемый платеж #%(number)s от %(counterparty)s", "es": "Cobro Esperado #%(number)s de %(counterparty)s", "nl": "Verwachte Betaling #%(number)s van %(counterparty)s",
        "fr": "Paiement Attendu #%(number)s de %(counterparty)s", "pt": "Recebimento Esperado #%(number)s de %(counterparty)s", "zh_Hans": "来自 %(counterparty)s 的应收账单 #%(number)s", "ja": "%(counterparty)s からの入金予定 #%(number)s"
    },
    "Inspect Incoming Delivery #%(number)s at Dock": {
        "ru": "Приемка и проверка доставки #%(number)s на складе", "es": "Inspeccionar Entrega de Entrada #%(number)s en Muelle", "nl": "Controleer Inkomende Levering #%(number)s aan het Dok",
        "fr": "Inspecter la Livraison Entrante #%(number)s au Quai", "pt": "Inspecionar Entrega de Entrada #%(number)s nas Docas", "zh_Hans": "在卸货区检验入库交货 #%(number)s", "ja": "搬入口にて入荷品 #%(number)s の検品"
    },
    "pcs": {
        "ru": "шт.", "es": "uds.", "nl": "stuks",
        "fr": "pcs", "pt": "unidades", "zh_Hans": "件", "ja": "個"
    },
    # Counterparty Management & Editing
    "Edit": {
        "ru": "Редактировать", "es": "Editar", "nl": "Bewerken",
        "fr": "Modifier", "pt": "Editar", "zh_Hans": "编辑", "ja": "編集"
    },
    "Edit Counterparty": {
        "ru": "Редактировать контрагента", "es": "Editar Contraparte", "nl": "Relatie Bewerken",
        "fr": "Modifier la Contrepartie", "pt": "Editar Contraparte", "zh_Hans": "编辑交易往来方", "ja": "取引先情報の編集"
    },
    "Save Changes": {
        "ru": "Сохранить изменения", "es": "Guardar Cambios", "nl": "Wijzigingen Opslaan",
        "fr": "Enregistrer les Modifications", "pt": "Salvar Alterações", "zh_Hans": "保存修改", "ja": "変更を保存"
    },
    "Registration Number": {
        "ru": "Регистрационный номер", "es": "Número de Registro", "nl": "Registratienummer",
        "fr": "Numéro d'Enregistrement", "pt": "Número de Registo", "zh_Hans": "公司注册号", "ja": "法人登録番号"
    },
    "SWIFT / BIC": {
        "ru": "SWIFT / BIC", "es": "SWIFT / BIC", "nl": "SWIFT / BIC",
        "fr": "SWIFT / BIC", "pt": "SWIFT / BIC", "zh_Hans": "SWIFT / BIC代码", "ja": "SWIFT / BICコード"
    },
    "Payment Terms (Days)": {
        "ru": "Срок оплаты (дней)", "es": "Plazo de Pago (Días)", "nl": "Betalingstermijn (Dagen)",
        "fr": "Conditions de Paiement (Jours)", "pt": "Condições de Pagamento (Dias)", "zh_Hans": "付款期限 (天)", "ja": "支払サイト (日数)"
    },
    "Counterparty '%(name)s' updated successfully.": {
        "ru": "Контрагент «%(name)s» успешно обновлен.", "es": "Contraparte '%(name)s' actualizada con éxito.", "nl": "Relatie '%(name)s' succesvol bijgewerkt.",
        "fr": "Contrepartie '%(name)s' mise à jour avec succès.", "pt": "Contraparte '%(name)s' atualizada com sucesso.", "zh_Hans": "往来方 '%(name)s' 已成功更新。", "ja": "取引先「%(name)s」を正常に更新しました。"
    },
    "Counterparty '%(name)s' created successfully.": {
        "ru": "Контрагент «%(name)s» успешно создан.", "es": "Contraparte '%(name)s' creada con éxito.", "nl": "Relatie '%(name)s' succesvol aangemaakt.",
        "fr": "Contrepartie '%(name)s' créée avec succès.", "pt": "Contraparte '%(name)s' criada com sucesso.", "zh_Hans": "往来方 '%(name)s' 已成功创建。", "ja": "取引先「%(name)s」を正常に登録しました。"
    },
}


def build():
    languages = ["ru", "es", "nl", "fr", "pt", "zh_Hans", "ja", "en"]

    for lang in languages:
        loc_dir = os.path.join(BASE_DIR, "locale", lang, "LC_MESSAGES")
        os.makedirs(loc_dir, exist_ok=True)

        po = polib.POFile()
        po.metadata = {
            'Project-Id-Version': '2.0',
            'Report-Msgid-Bugs-To': '',
            'POT-Creation-Date': '2026-10-02 23:00+0000',
            'PO-Revision-Date': '2026-10-02 23:00+0000',
            'Last-Translator': 'Antigravity AI',
            'Language-Team': f'{lang}',
            'Language': lang,
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

        for msgid, translations in COMMON_STRINGS.items():
            if lang == "en":
                msgstr = msgid
            else:
                msgstr = translations.get(lang, msgid)

            entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
            po.append(entry)

        po_path = os.path.join(loc_dir, "django.po")
        mo_path = os.path.join(loc_dir, "django.mo")
        po.save(po_path)
        po.save_as_mofile(mo_path)
        print(f"[{lang}] Compiled {len(po)} entries to {mo_path}")

    # Ensure zh_CN duplicate for compatibility
    zh_cn_dir = os.path.join(BASE_DIR, "locale", "zh_CN", "LC_MESSAGES")
    os.makedirs(zh_cn_dir, exist_ok=True)
    shutil.copyfile(os.path.join(BASE_DIR, "locale", "zh_Hans", "LC_MESSAGES", "django.po"), os.path.join(zh_cn_dir, "django.po"))
    shutil.copyfile(os.path.join(BASE_DIR, "locale", "zh_Hans", "LC_MESSAGES", "django.mo"), os.path.join(zh_cn_dir, "django.mo"))
    print("[zh_CN] Copied from zh_Hans")


if __name__ == '__main__':
    build()
