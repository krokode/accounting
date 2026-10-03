# Sole Enterprise Orchestrator & Agente de Gestão Contabilística

[![License: MIT](https://img.shields.io/badge/Licença-MIT-blue.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django: 5.x](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)

<p align="center">
  <strong>Translations / Документация / Traducciones / Vertalingen / Traductions / Traduções / 语言版本 / 言語:</strong><br>
  <a href="README.md">🇬🇧 English</a> &bull;
  <a href="README.ru.md">🇷🇺 Русский</a> &bull;
  <a href="README.es.md">🇪🇸 Español</a> &bull;
  <a href="README.nl.md">🇳🇱 Nederlands</a> &bull;
  <a href="README.fr.md">🇫🇷 Français</a> &bull;
  <a href="README.pt.md">🇵🇹 Português</a> &bull;
  <a href="README.zh-hans.md">🇨🇳 简体中文</a> &bull;
  <a href="README.ja.md">🇯🇵 日本語</a>
</p>

---

Um sistema inteligente e multilíngue de gestão de documentos empresariais, contabilidade, controlo de armazém e automação de calendário, desenvolvido com **Python 3.11+**, **Django 5.x**, **Tailwind CSS** e **IA Multimodal Google Gemini**.

---

## 🌐 Idiomas Suportados (Internacionalização i18n)

A aplicação está totalmente traduzida e pronta a utilizar em **8 idiomas**:
- 🇬🇧 **English / Inglês** (`en`)
- 🇷🇺 **Русский / Russo** (`ru`)
- 🇪🇸 **Español / Espanhol** (`es`)
- 🇳🇱 **Nederlands / Holandês** (`nl`)
- 🇫🇷 **Français / Francês** (`fr`)
- 🇵🇹 **Português** (`pt`)
- 🇨🇳 **简体中文 / Chinês Simplificado** (`zh-hans`)
- 🇯🇵 **日本語 / Japonês** (`ja`)

Alterne o idioma a qualquer momento através do menu suspenso com globo na barra de navegação superior.

---

## 🌟 Principais Funcionalidades

1. **Digitalização de Documentos e IA Multimodal**:
   - Processamento de ficheiros PDF digitalizados e fotos de contratos, faturas de fornecedores, recibos e guias de remessa.
   - Extração precisa de entidades, linhas de artigos, detalhe de IVA, contas bancárias IBAN e prazos de liquidação.
   - Potenciado por motores Multi-LLM flexíveis (**Google Gemini**, **OpenAI ChatGPT / GPT-4o**, **Anthropic Claude 3.7**, **DeepSeek V3 / R1**, **Alibaba Qwen** ou **Ollama local**).

2. **Ecrã de Verificação Lado a Lado (Side-by-Side)**:
   - Revisão em ecrã dividido: digitalização original à esquerda, formulário estruturado editável à direita.
   - 1 clique em **«Confirmar e Registar nos Livros»** sincroniza de imediato fornecedores, contas correntes, inventário e tarefas no calendário.

3. **Contabilidade e Fluxo de Caixa (Contas a Pagar e a Receber)**:
   - **Contas a Pagar (AP)**: Faturas de compras a fornecedores com monitorização de vencimentos.
   - **Contas a Receber (AR)**: Faturas emitidas e pagamentos esperados de clientes.
   - Registo detalhado de liquidações (pagamentos parciais, liquidação total, modo de pagamento, referência bancária).
   - Gestão de despesas miúdas, recibos avulsos e caixa pequena.

4. **Armazém e Guias de Remessa**:
   - Catálogo de artigos com códigos SKU, stock em armazém e avisos de ponto de encomenda mínimo.
   - Guias de transporte e receção de mercadorias de entrada e saída.
   - 1 clique em **«Confirmar e Dar Entrada»** atualiza imediatamente o stock e cria histórico de auditoria (`StockMovement`).

5. **Calendário Integrado e Sincronização iCalendar em Tempo Real**:
   - Vista interativa FullCalendar.js classificada por cores:
     - 🔴 **Vermelho**: Vencimento de fatura de fornecedor
     - 🟢 **Verde**: Recebimento esperado de cliente
     - 🟣 **Roxo**: Prazo para decisão ou renovação de contrato
     - 🟠 **Laranja**: Entrega de mercadoria agendada
     - 🔵 **Azul**: Tarefa administrativa geral
   - **Feed iCal (.ics) em direto**: URL seguro com token (`/calendar/feed.ics?token=...`) para subscrição direta no **Google Calendar**, **Apple Calendar**, **Microsoft Outlook** ou **Thunderbird**.

6. **Lembretes e Alertas Proativos**:
   - Verificação diária automática (`manage.py run_reminders`):
     - Lembretes a D-7, D-3, D-1 e na própria data de vencimento.
     - Notificações críticas para faturas em atraso.
     - Prazos de aviso prévio para contratos comerciais.
     - Alertas de rutura ou stock baixo.
   - Ícone de sino com notificações no topo da página.

7. **Copiloto IA Integrado**:
   - Assistente conversacional acessível no painel lateral de qualquer ecrã.
   - Perguntas em linguagem natural ligadas aos dados em tempo real (*«Que faturas vencem esta semana?»*, *«Mostrar produtos com pouco stock»*, *«Resumo da saúde financeira»*).
   - Suporte completo em todos os 8 idiomas.

---

## 🚀 Guia de Início Rápido

### 1. Ativar o Ambiente Virtual
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Configurar Ambiente e Provedores de IA
Copie o ficheiro `.env.example` para `.env` ou execute o assistente interativo automatizado:
```powershell
python setup_llm.py
```
*(Suporta Português, English, Русский, Español, Nederlands, Français, 简体中文 e 日本語)*.

Também pode configurar via comando Django ou através do painel web em **`/assistant/settings/`**:
```powershell
# Listar provedores disponíveis e estado das credenciais
python manage.py configure_llm --list

# Configurar e testar de forma não interativa
python manage.py configure_llm --provider deepseek --api-key sk-xxxx --model deepseek-chat --test
```

### 3. Aplicar Migrações e Carregar Dados de Exemplo
```powershell
python manage.py migrate
```

Se desejar criar um superutilizador para acesso de administração:
```powershell
python manage.py createsuperuser
```

Se desejar preencher o sistema com dados de teste para experimentação:
```powershell
python manage.py seed_demo_data
```

### 4. Iniciar o Servidor de Desenvolvimento
```powershell
python manage.py runserver
```
Aceda a **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** no seu navegador.

---

## 🛠️ Comandos de Gestão

- **Assistente Interativo de Configuração de Modelos IA**:
  ```powershell
  python setup_llm.py
  # ou: python manage.py configure_llm [--lang pt]
  ```

- **Compilar Ficheiros de Tradução (.po e .mo)**:
  ```powershell
  python build_translations.py
  ```

- **Executar Verificação de Lembretes**:
  ```powershell
  python manage.py run_reminders
  ```

- **Executar Bateria de Testes Automatizados**:
  ```powershell
  python manage.py test
  ```

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** — consulte o ficheiro [LICENSE](LICENSE) para obter mais informações.

