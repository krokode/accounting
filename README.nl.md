# Sole Enterprise Orchestrator & Boekhouding AI-Agent

[![License: MIT](https://img.shields.io/badge/Licentie-MIT-blue.svg)](LICENSE)
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

Een intelligent, meertalig systeem voor bedrijfsdocumentenbeheer, boekhouding, magazijnbeheer en agenda-automatisering, gebouwd met **Python 3.11+**, **Django 5.x**, **Tailwind CSS** en **Google Gemini Multimodale AI**.

---

## 🌐 Ondersteunde Talen (Meertalig i18n)

De gehele applicatie is volledig geïnternationaliseerd in **8 talen**:
- 🇬🇧 **English / Engels** (`en`)
- 🇷🇺 **Русский / Russisch** (`ru`)
- 🇪🇸 **Español / Spaans** (`es`)
- 🇳🇱 **Nederlands** (`nl`)
- 🇫🇷 **Français / Frans** (`fr`)
- 🇵🇹 **Português / Portugees** (`pt`)
- 🇨🇳 **简体中文 / Vereenvoudigd Chinees** (`zh-hans`)
- 🇯🇵 **日本語 / Japans** (`ja`)

Wissel op elk gewenst moment van taal via het wereldbol-keuzemenu in de bovenste navigatiebalk.

---

## 🌟 Belangrijkste Functies

1. **Gescande Documenten & Multimodale AI**:
   - Verwerk gescande PDF's en foto's van contracten, leveranciersfacturen, bonnen en vrachtbrieven.
   - Nauwkeurige extractie van relaties, factuurregels, BTW-uitsplitsingen, IBAN-rekeningnummers en termijnen.
   - Aangedreven door flexibele Multi-LLM engines (**Google Gemini**, **OpenAI ChatGPT / GPT-4o**, **Anthropic Claude 3.7**, **DeepSeek V3 / R1**, **Alibaba Qwen** of **Lokale Ollama**).

2. **Zij-aan-Zij Verificatiescherm (Side-by-Side)**:
   - Split-screen overzicht: gescand brondocument links, bewerkbaar gestructureerd formulier rechts.
   - 1-klik **«Bevestigen & Boeken in Grootboek»** synchroniseert leveranciers, rekeningen, voorraad en agendataken automatisch.

3. **Boekhouding & Geldstroom (Crediteuren & Debiteuren)**:
   - **Crediteuren (AP)**: Te betalen leveranciersfacturen met bewaking van vervaldatums.
   - **Debiteuren (AR)**: Te ontvangen klantbetalingen.
   - Flexibele betalingsregistratie (deelbetalingen, volledige afhandeling, betaalmethoden, transactiereferenties).
   - Beheer van kasbonnen, onkostendeclaraties en kleine kas.

4. **Magazijn & Vrachtbrieven (Zendingen)**:
   - Voorraadcatalogus met SKU-codes, actuele voorraad en waarschuwingen bij een te laag bestelpunt.
   - Inkomende en uitgaande vrachtbrieven en leveringsbewijzen.
   - 1-klik **«Bevestigen & Inboeken»** past voorraadstanden direct aan en legt mutaties vast in `StockMovement`.

5. **Geïntegreerde Agenda & Taken met Live iCalendar-Feed**:
   - Interactieve FullCalendar.js weergave met kleurcodering:
     - 🔴 **Rood**: Te betalen factuur vervalt
     - 🟢 **Groen**: Verwachte inkomende klantbetaling
     - 🟣 **Paars**: Beslistermijn voor contractverlenging / opzegging
     - 🟠 **Oranje**: Geplande levering van vrachtbrief
     - 🔵 **Blauw**: Algemene administratieve taak
   - **Live iCal (.ics) Feed**: Veilige token-URL (`/calendar/feed.ics?token=...`) voor directe synchronisatie in **Google Agenda**, **Apple Calendar**, **Microsoft Outlook** of **Thunderbird**.

6. **Proactieve Herinneringen & Meldingen**:
   - Dagelijkse geautomatiseerde controle (`manage.py run_reminders`):
     - Herinneringen op T-7, T-3, T-1 dagen en op de vervaldatum.
     - Dringende escalaties voor vervallen facturen.
     - Opzegtermijnen voor zakelijke overeenkomsten.
     - Waarschuwingen voor lage voorraadstanden.
   - Live notificatie-belletje in de navigatiebalk.

7. **Geïntegreerde AI-Copilot**:
   - Conversatie-assistent bereikbaar via het zijpaneel op elke pagina.
   - Vragen in natuurlijke taal over actuele databasegegevens (*«Welke facturen moeten deze week betaald worden?»*, *«Toon lage voorraden»*, *«Vat de financiële status samen»*).
   - Volledige meertalige ondersteuning voor alle 8 talen.

---

## 🚀 Aan de Slag

### 1. Activeer Virtuele Omgeving
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Configureer Omgeving & AI-Providers
Kopieer `.env.example` naar `.env` of voer de geautomatiseerde interactieve installatiewizard uit:
```powershell
python setup_llm.py
```
*(Ondersteunt Nederlands, English, Русский, Español, Français, Português, 简体中文 en 日本語)*.

U kunt de configuratie ook beheren via het Django-beheercommando of via het webdashboard op **`/assistant/settings/`**:
```powershell
# Bekijk beschikbare providers en status van API-sleutels
python manage.py configure_llm --list

# Niet-interactief instellen en testen
python manage.py configure_llm --provider deepseek --api-key sk-xxxx --model deepseek-chat --test
```

### 3. Voer Migraties Uit & Laad Demo-Gegevens
```powershell
python manage.py migrate
```

Als u een superuser wilt aanmaken voor beheerderstoegang:
```powershell
python manage.py createsuperuser
```

Als u het systeem wilt vullen met voorbeeldgegevens om te testen:
```powershell
python manage.py seed_demo_data
```

### 4. Start de Ontwikkelserver
```powershell
python manage.py runserver
```
Bezoek **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in uw webbrowser.

---

## 🛠️ Beheercommando's

- **Interactieve AI-Provider Setup Wizard**:
  ```powershell
  python setup_llm.py
  # of: python manage.py configure_llm [--lang nl]
  ```

- **Taalbestanden Opnieuw Compileren (.po en .mo)**:
  ```powershell
  python build_translations.py
  ```

- **Herinneringencontrole Handmatig Uitvoeren**:
  ```powershell
  python manage.py run_reminders
  ```

- **Geautomatiseerde Testsuite Uitvoeren**:
  ```powershell
  python manage.py test
  ```

---

## 📄 Licentie

Dit project is gelicentieerd onder de **MIT-licentie** — zie het bestand [LICENSE](LICENSE) voor meer informatie.

