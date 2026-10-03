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

### 1. Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Configure Environment & AI Model Provider
Copy `.env.example` to `.env` or run the automated interactive setup wizard:
```powershell
python setup_llm.py
```
*(Supports English, Русский, Español, Nederlands, Français, Português, 简体中文, and 日本語)*.

You can also configure via Django management command or web dashboard at **`/assistant/settings/`**:
```powershell
# List available providers and credentials status
python manage.py configure_llm --list

# Configure and test non-interactively
python manage.py configure_llm --provider deepseek --api-key sk-xxxx --model deepseek-chat --test
```

### 3. Apply Migrations & Seed Demo Data
```powershell
python manage.py migrate
```

if you want to create a superuser for admin access, run:
```powershell
python manage.py createsuperuser
```

if you want to populate the system with sample data for testing, run:
```powershell
python manage.py seed_demo_data
```

### 4. Run Development Server
```powershell
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

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

