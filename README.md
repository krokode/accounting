# Sole Enterprise Orchestrator & Accounting Management Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
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

An intelligent, multilingual company records management, accounting, warehouse, and calendar automation system built with **Python 3.11+**, **Django 5.x**, **Tailwind CSS**, and **Google Gemini Multimodal AI**.

---

## 🌐 Supported Languages (Multilingual i18n)

The entire application is internationalized and available in **8 languages**:
- 🇬🇧 **English** (`en`)
- 🇷🇺 **Русский / Russian** (`ru`)
- 🇪🇸 **Español / Spanish** (`es`)
- 🇳🇱 **Nederlands / Dutch** (`nl`)
- 🇫🇷 **Français / French** (`fr`)
- 🇵🇹 **Português / Portuguese** (`pt`)
- 🇨🇳 **简体中文 / Simplified Chinese** (`zh-hans`)
- 🇯🇵 **日本語 / Japanese** (`ja`)

Switch languages at any time via the globe dropdown selector in the top navbar.

---

## 🌟 Key Capabilities

1. **Scanned Document Ingestion & Multimodal AI**:
   - Ingest scanned PDFs and photos of contracts, vendor invoices, receipts, and consignment slips.
   - Extracts structured counterparties, line items, VAT/tax breakdowns, banking IBANs, and critical dates.
   - Powered by pluggable Multi-LLM engines (**Google Gemini**, **OpenAI ChatGPT / GPT-4o**, **Anthropic Claude 3.7**, **DeepSeek V3 / R1**, **Alibaba Qwen**, or **Local Ollama**).

2. **Side-by-Side Verification Screen**:
   - Split-screen review: embedded document scan on the left, editable structured form on the right.
   - 1-click **"Confirm & Commit to Ledgers"** automatically synchronizes vendors, accounts, inventory, and calendar tasks.

3. **Accounting & Cash Flow (AP / AR)**:
   - **Accounts Payable (AP)**: Outgoing vendor bills with due-date tracking.
   - **Accounts Receivable (AR)**: Expected incoming customer invoices.
   - Multi-stage payment recording (Partial payment, Full settlement, Payment method, Transaction ref).
   - Petty cash and expense vouchers management.

4. **Warehouse & Consignments**:
   - Inventory catalog with SKU, on-hand counts, and reorder point threshold alerts.
   - Inward and outward consignment waybills.
   - 1-click **"Confirm & Stock In"** automatically adjusts inventory balances and creates audit trail records (`StockMovement`).

5. **Unified Calendar & Tasks with Live iCalendar Feed**:
   - Interactive FullCalendar.js view color-coded by event type:
     - 🔴 **Red**: Outgoing payment due
     - 🟢 **Green**: Expected incoming customer payment
     - 🟣 **Purple**: Contract renewal decision window
     - 🟠 **Orange**: Consignment delivery
     - 🔵 **Blue**: General administrative task
   - **Live iCal (.ics) Feed**: Secure tokenized URL (`/calendar/feed.ics?token=...`) allows instant subscription in **Google Calendar**, **Apple Calendar**, **Microsoft Outlook**, or **Thunderbird**.

6. **Proactive Payment Reminders & Alerts**:
   - Automated daily evaluator (`manage.py run_reminders`):
     - Upcoming bills due at T-7, T-3, T-1, and on due date.
     - Critical escalation for overdue invoices.
     - Contract renewal notice deadlines.
     - Low-stock inventory warnings.
   - Live notification dropdown in the top navbar.

7. **Embedded AI Copilot**:
   - Conversational assistant embedded in the application drawer.
   - Natural language queries against real-time database ledgers (*"What bills are due this week?"*, *"Show low stock items"*, *"Summarize financial health"*).
   - Fully multilingual across all 8 supported languages with active model indicator and direct settings control.

---

## 🚀 Quick Start Guide

### 🔰 Prerequisites: Install Python (One-Time)

This project requires **Python 3.11 or newer** (Python 3.11, 3.12, or 3.13 are all supported).

1. Download the installer from the [official Python downloads page](https://www.python.org/downloads/).
2. Run the installer. **CRITICAL STEP:** On the very first screen, check the box:  
   ☑️ **Add python.exe to PATH**  
   *(If you miss this step, your terminal won't recognize the `python` command!)*
3. Click **Install Now**.
4. Open your project folder in File Explorer. Click the address bar at the top, type `powershell` (or `cmd`), and press <kbd>Enter</kbd>. A terminal window will open directly in this folder.
5. Verify your installation:
   ```powershell
   python --version
   ```
   *(It should display `Python 3.11.x`, `3.12.x`, or `3.13.x`)*.

---

### ⚡ First-Time Setup (5 Minutes)

Run these steps once in your terminal from the project folder:

#### 1. Create and Activate an Isolated Environment
```powershell
# Create the virtual environment (.venv)
python -m venv .venv

# Activate it (Windows PowerShell):
.\.venv\Scripts\Activate.ps1
```
> **Tip for Windows:** If you see red text saying *`running scripts is disabled on this system`*, run this command once and try activating again:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> .\.venv\Scripts\Activate.ps1
> ```
> *(Or use Command Prompt: `.\.venv\Scripts\activate.bat`, or macOS/Linux: `source .venv/bin/activate`)*.

When activated, you will see `(.venv)` at the beginning of your command line prompt.

#### 2. Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configure AI Assistant (Interactive Wizard)
Run our multilingual setup wizard to choose your AI provider and configure your API key:
```powershell
python setup_llm.py
```
- Available in all 8 languages: English, Русский, Español, Nederlands, Français, Português, 简体中文, 日本語.
- Works with **Google Gemini** (*free tier available at [Google AI Studio](https://aistudio.google.com/)*), **Ollama** (*100% free & local*), **OpenAI**, **Claude**, **DeepSeek**, or **Qwen**.
- *(Optional)* You can also configure via Django CLI (`python manage.py configure_llm --list`) or the web UI at `/assistant/settings/`.

#### 4. Initialize Database & Load Demo Data
```powershell
# Create database tables
python manage.py migrate

# Seed demo data (recommended: populates invoices, inventory, counterparties & contracts)
python manage.py seed_demo_data

# (Optional) Create an admin user to access /admin/
python manage.py createsuperuser
```

---

### 🏃 Everyday Use (Starting the App Anytime)

Whenever you want to use the application in the future, you **only** need to run:

```powershell
# 1. Activate the environment (if not already active)
.\.venv\Scripts\Activate.ps1

# 2. Start the server
python manage.py runserver
```

Open your browser and navigate to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** 🎉

---

### ❓ Troubleshooting & Common Issues

| Issue | Cause & Easy Fix |
| :--- | :--- |
| **`python is not recognized as an internal or external command`** | Python was installed without the **Add to PATH** checkbox. Rerun the Python installer, choose **Modify**, check **Add Python to environment variables**, and restart your terminal. |
| **`File ... Activate.ps1 cannot be loaded because running scripts is disabled`** | Windows blocks PowerShell scripts by default. Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`, or switch to Command Prompt and run `.\.venv\Scripts\activate.bat`. |
| **`Error: That port is already in use`** | Another application (or previous Django session) is using port 8000. Start on a different port: `python manage.py runserver 8080`. |
| **`no such table: ...`** | The database has not been initialized yet. Run `python manage.py migrate`. |

---

## 🛠️ Management Commands

- **Interactive AI Provider Setup Wizard**:
  ```powershell
  python setup_llm.py
  # or: python manage.py configure_llm [--lang en/ru/es/nl/fr/pt/zh-hans/ja]
  ```

- **Rebuild Language Catalogs (.po & .mo)**:
  ```powershell
  python build_translations.py
  ```

- **Run Proactive Reminders Check**:
  ```powershell
  python manage.py run_reminders
  ```

- **Run Automated Test Suite**:
  ```powershell
  python manage.py test
  ```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
