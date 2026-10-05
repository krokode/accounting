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

### 🔰 Pré-requisitos: Instalar o Python (Uma única vez)

Este projeto requer o **Python 3.11 ou superior** (Python 3.11, 3.12 e 3.13 são totalmente suportados).

1. Descarregue o instalador na [página oficial de downloads do Python](https://www.python.org/downloads/).
2. Execute o instalador. **PASSO FUNDAMENTAL:** No primeiro ecrã, marque a caixa:  
   ☑️ **Add python.exe to PATH**  
   *(Se ignorar este passo, o terminal não reconhecerá o comando `python`!)*
3. Clique em **Install Now**.
4. Abra a pasta do projeto no Explorador de Ficheiros. Clique na barra de endereço no topo, digite `powershell` (ou `cmd`) e pressione <kbd>Enter</kbd>. Uma janela de terminal abrirá diretamente nesta pasta.
5. Verifique a instalação:
   ```powershell
   python --version
   ```
   *(Deverá apresentar `Python 3.11.x`, `3.12.x` ou `3.13.x`)*.

---

### ⚡ Configuração Inicial (5 Minutos)

Execute estes passos uma única vez no seu terminal a partir da pasta do projeto:

#### 1. Criar e Ativar o Ambiente Isolado
```powershell
# Criar o ambiente virtual (.venv)
python -m venv .venv

# Ativar (Windows PowerShell):
.\.venv\Scripts\Activate.ps1
```
> **Dica para Windows:** Se surgir uma mensagem a vermelho informando que *`a execução de scripts foi desativada neste sistema`* (*`running scripts is disabled on this system`*), execute o seguinte comando e tente ativar novamente:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> .\.venv\Scripts\Activate.ps1
> ```
> *(Ou utilize a Linha de Comandos CMD: `.\.venv\Scripts\activate.bat`, ou em macOS/Linux: `source .venv/bin/activate`)*.

Quando o ambiente estiver ativo, verá `(.venv)` no início da linha de comandos.

#### 2. Instalar Dependências
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configurar Assistente de IA (Assistente Interativo)
Execute o nosso assistente interativo multilingue para selecionar o seu provedor de IA e configurar a chave de API:
```powershell
python setup_llm.py
```
- Disponível em 8 idiomas: Português, English, Русский, Español, Nederlands, Français, 简体中文, 日本語.
- Funciona com **Google Gemini** (*plano gratuito disponível em [Google AI Studio](https://aistudio.google.com/)*), **Ollama** (*100% gratuito & local sem ligação à internet*), **OpenAI**, **Claude**, **DeepSeek** ou **Qwen**.
- *(Opcional)* Também pode configurar via CLI do Django (`python manage.py configure_llm --list`) ou no painel web em `/assistant/settings/`.

#### 4. Inicializar a Base de Dados e Carregar Dados de Demonstração
```powershell
# Criar tabelas na base de dados
python manage.py migrate

# Carregar dados de demonstração (recomendado: cria faturas, inventário, entidades e contratos)
python manage.py seed_demo_data

# (Opcional) Criar um utilizador administrador para aceder a /admin/
python manage.py createsuperuser
```

---

### 🏃 Utilização no Dia a Dia (Iniciar a Aplicação a Qualquer Momento)

No futuro, para iniciar a aplicação precisa de executar apenas **dois comandos**:

```powershell
# 1. Ativar o ambiente (se não estiver já ativo)
.\.venv\Scripts\Activate.ps1

# 2. Iniciar o servidor
python manage.py runserver
```

Abra o seu navegador em: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** 🎉

---

### ❓ Resolução de Problemas & Perguntas Frequentes

| Problema | Causa e Resolução Simples |
| :--- | :--- |
| **`python não é reconhecido como um comando interno ou externo`** | O Python foi instalado sem marcar a caixa **Add to PATH**. Execute o instalador do Python novamente, escolha **Modify**, marque **Add Python to environment variables** e reinicie o terminal. |
| **`Não é possível carregar o ficheiro Activate.ps1 porque a execução de scripts está desativada`** | O Windows bloqueia scripts do PowerShell por predefinição. Execute `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`, ou mude para a Linha de Comandos (CMD) e execute `.\.venv\Scripts\activate.bat`. |
| **`Error: That port is already in use`** | A porta 8000 já está em utilização por outra aplicação ou sessão anterior. Inicie noutra porta: `python manage.py runserver 8080`. |
| **`no such table: ...`** | A base de dados ainda não foi inicializada. Execute: `python manage.py migrate`. |

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

