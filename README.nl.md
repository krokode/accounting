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

## 🚀 Snelle Startgids

### 🔰 Vereisten: Python installeren (Eenmalig)

Dit project vereist **Python 3.11 of nieuwer** (Python 3.11, 3.12 en 3.13 worden allemaal ondersteund).

1. Download het installatiebestand van de [officiële Python-downloadpagina](https://www.python.org/downloads/).
2. Start het installatieprogramma. **CRUCIALE STAP:** Vink op het allereerste scherm het vakje aan:  
   ☑️ **Add python.exe to PATH**  
   *(Als u deze stap overslaat, herkent uw terminal het `python`-commando niet!)*
3. Klik op **Install Now**.
4. Open de projectmap in Windows Verkenner. Klik op de adresbalk bovenaan, typ `powershell` (of `cmd`) en druk op <kbd>Enter</kbd>. Er wordt direct in deze map een terminalvenster geopend.
5. Controleer uw installatie:
   ```powershell
   python --version
   ```
   *(Er moet `Python 3.11.x`, `3.12.x` of `3.13.x` worden weergegeven)*.

---

### ⚡ Eerste Keer Instellen (5 Minuten)

Voer deze stappen eenmalig uit in uw terminal vanuit de projectmap:

#### 1. Geïsoleerde omgeving aanmaken en activeren
```powershell
# Virtuele omgeving aanmaken (.venv)
python -m venv .venv

# Activeren (Windows PowerShell):
.\.venv\Scripts\Activate.ps1
```
> **Tip voor Windows:** Als u een rode foutmelding ziet met de tekst *`running scripts is disabled on this system`* (uitvoeren van scripts is uitgeschakeld), voer dan dit commando uit en activeer opnieuw:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> .\.venv\Scripts\Activate.ps1
> ```
> *(Of gebruik de Opdrachtprompt: `.\.venv\Scripts\activate.bat`, of macOS/Linux: `source .venv/bin/activate`)*.

Wanneer de omgeving actief is, ziet u `(.venv)` aan het begin van uw opdrachtprompt.

#### 2. Afhankelijkheden installeren
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. AI-Assistent configureren (Interactieve wizard)
Start onze meertalige installatiewizard om uw gewenste AI-provider te kiezen en uw API-sleutel in te stellen:
```powershell
python setup_llm.py
```
- Beschikbaar in alle 8 talen: Nederlands, English, Русский, Español, Français, Português, 简体中文, 日本語.
- Werkt met **Google Gemini** (*gratis niveau beschikbaar via [Google AI Studio](https://aistudio.google.com/)*), **Ollama** (*100% gratis & lokaal offline*), **OpenAI**, **Claude**, **DeepSeek** of **Qwen**.
- *(Optioneel)* U kunt ook configureren via de Django CLI (`python manage.py configure_llm --list`) of in het webdashboard op `/assistant/settings/`.

#### 4. Database initialiseren en demo-gegevens laden
```powershell
# Databasetabellen aanmaken
python manage.py migrate

# Demo-gegevens laden (aanbevolen: vult facturen, voorraad, relaties en contracten)
python manage.py seed_demo_data

# (Optioneel) Beheerder aanmaken voor toegang tot /admin/
python manage.py createsuperuser
```

---

### 🏃 Dagelijks Gebruik (De app op elk moment starten)

In de toekomst hoeft u om de applicatie te starten **slechts twee commando's** uit te voeren:

```powershell
# 1. Omgeving activeren (indien nog niet actief)
.\.venv\Scripts\Activate.ps1

# 2. Server starten
python manage.py runserver
```

Open uw webbrowser en ga naar: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** 🎉

---

### ❓ Probleemoplossing & Veelgestelde Vragen

| Probleem | Oorzaak & Eenvoudige Oplossing |
| :--- | :--- |
| **`python is not recognized as an internal or external command`** | Python is geïnstalleerd zonder het selectievakje **Add to PATH** aan te vinken. Start het Python-installatieprogramma opnieuw, kies **Modify**, vink **Add Python to environment variables** aan en herstart uw terminal. |
| **`File ... Activate.ps1 cannot be loaded because running scripts is disabled`** | Windows blokkeert PowerShell-scripts standaard. Voer `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` uit, of schakel over naar de Opdrachtprompt (CMD) en voer `.\.venv\Scripts\activate.bat` uit. |
| **`Error: That port is already in use`** | Poort 8000 is al in gebruik door een ander programma of eerdere sessie. Start op een andere poort: `python manage.py runserver 8080`. |
| **`no such table: ...`** | De database is nog niet geïnitialiseerd. Voer uit: `python manage.py migrate`. |

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

