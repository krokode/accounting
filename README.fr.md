# Sole Enterprise Orchestrator & Agent de Gestion Comptable

[![License: MIT](https://img.shields.io/badge/Licence-MIT-blue.svg)](LICENSE)
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

Un système intelligent et multilingue de gestion des documents d'entreprise, comptabilité, gestion des stocks et automatisation des calendriers, conçu avec **Python 3.11+**, **Django 5.x**, **Tailwind CSS** et l'**IA Multimodale Google Gemini**.

---

## 🌐 Langues Prises en Charge (Support Multilingue i18n)

L'intégralité de l'application est disponible en **8 langues** :
- 🇬🇧 **English / Anglais** (`en`)
- 🇷🇺 **Русский / Russe** (`ru`)
- 🇪🇸 **Español / Espagnol** (`es`)
- 🇳🇱 **Nederlands / Néerlandais** (`nl`)
- 🇫🇷 **Français** (`fr`)
- 🇵🇹 **Português / Portugais** (`pt`)
- 🇨🇳 **简体中文 / Chinois simplifié** (`zh-hans`)
- 🇯🇵 **日本語 / Japonais** (`ja`)

Basculez de langue à tout moment grâce au sélecteur avec drapeau situé dans la barre de navigation supérieure.

---

## 🌟 Fonctionnalités Clés

1. **Numérisation de Documents & IA Multimodale** :
   - Traitement des scans PDF et photos de contrats, factures fournisseurs, reçus et bons de livraison.
   - Extraction structurée des tiers, lignes d'articles, ventilation de TVA, numéros IBAN et dates d'échéance.
   - Alimenté par des moteurs Multi-LLM interchangeables (**Google Gemini**, **OpenAI ChatGPT / GPT-4o**, **Anthropic Claude 3.7**, **DeepSeek V3 / R1**, **Alibaba Qwen** ou **Ollama local**).

2. **Écran de Vérification Côte-à-Côte (Side-by-Side)** :
   - Revue sur écran partagé : scan original à gauche, formulaire éditable structuré à droite.
   - 1 clic sur **« Valider & Écrire aux Journaux »** synchronise automatiquement les tiers, le grand livre, le stock et l'agenda.

3. **Comptabilité & Trésorerie (Fournisseurs & Clients)** :
   - **Dettes Fournisseurs (AP)** : Factures fournisseurs à régler avec suivi des échéances.
   - **Créances Clients (AR)** : Factures clients et encaissements prévus.
   - Rapprochement de paiement échelonné (règlement partiel, solde total, moyen de paiement, référence bancaire).
   - Gestion des reçus de caisse, notes de frais et petite caisse.

4. **Entrepôt & Bons de Livraison (Consignations)** :
   - Répertoire des articles avec codes SKU, stock en rayon et alertes de seuil de réapprovisionnement.
   - Bons de livraison entrants et sortants.
   - 1 clic sur **« Confirmer la Réception »** ajuste immédiatement les stocks et génère l'historique d'audit (`StockMovement`).

5. **Calendrier Partagé & Flux iCalendar en Direct** :
   - Vue interactive FullCalendar.js avec code couleur :
     - 🔴 **Rouge** : Facture fournisseur arrivant à échéance
     - 🟢 **Vert** : Règlement client attendu
     - 🟣 **Violet** : Période de préavis ou renouvellement de contrat
     - 🟠 **Orange** : Livraison programmée de marchandises
     - 🔵 **Bleu** : Tâche administrative générale
   - **Flux iCal (.ics) en temps réel** : URL sécurisée par jeton (`/calendar/feed.ics?token=...`) pour abonnement direct dans **Google Agenda**, **Apple Calendar**, **Microsoft Outlook** ou **Thunderbird**.

6. **Rappels Proactifs & Alertes** :
   - Évaluateur quotidien automatique (`manage.py run_reminders`) :
     - Rappels à J-7, J-3, J-1 et le jour même de l'échéance.
     - Notifications critiques pour les factures impayées en retard.
     - Alertes de préavis de renouvellement de contrats.
     - Alertes de stock faible.
   - Cloche de notifications dans l'en-tête de la page.

7. **Copilote IA Intégré** :
   - Assistant conversationnel accessible en tiroir latéral sur n'importe quel écran.
   - Questions en langage naturel connectées aux données en temps réel (*« Quelles factures sont dues cette semaine ? »*, *« Afficher les stocks bas »*, *« Résumer la santé financière »*).
   - Prise en charge native des 8 langues.

---

## 🚀 Guide de Démarrage Rapide

### 🔰 Prérequis : Installer Python (Une seule fois)

Ce projet nécessite **Python 3.11 ou une version plus récente** (Python 3.11, 3.12 et 3.13 sont tous pris en charge).

1. Téléchargez le programme d'installation depuis la [page officielle de téléchargement de Python](https://www.python.org/downloads/).
2. Lancez l'installateur. **ÉTAPE CRUCIALE :** Sur le tout premier écran, cochez la case :  
   ☑️ **Add python.exe to PATH**  
   *(Si vous ignorez cette étape, votre terminal ne reconnaîtra pas la commande `python` !)*
3. Cliquez sur **Install Now**.
4. Ouvrez le dossier du projet dans l'Explorateur de fichiers. Cliquez sur la barre d'adresse en haut, tapez `powershell` (ou `cmd`) et appuyez sur <kbd>Entrée</kbd>. Une fenêtre de terminal s'ouvrira directement dans ce dossier.
5. Vérifiez l'installation :
   ```powershell
   python --version
   ```
   *(Elle doit afficher `Python 3.11.x`, `3.12.x` ou `3.13.x`)*.

---

### ⚡ Configuration Initiale (5 Minutes)

Exécutez ces étapes une seule fois dans votre terminal depuis le dossier du projet :

#### 1. Créer et activer l'environnement isolé
```powershell
# Créer l'environnement virtuel (.venv)
python -m venv .venv

# L'activer (Windows PowerShell) :
.\.venv\Scripts\Activate.ps1
```
> **Astuce pour Windows :** Si un texte rouge indique *`l'exécution de scripts est désactivée sur ce système`* (*`running scripts is disabled on this system`*), exécutez cette commande une fois puis réactivez :
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> .\.venv\Scripts\Activate.ps1
> ```
> *(Ou utilisez l'Invite de commandes CMD : `.\.venv\Scripts\activate.bat`, ou sous macOS/Linux : `source .venv/bin/activate`)*.

Une fois activé, l'indicateur `(.venv)` s'affichera au début de votre invite de commande.

#### 2. Installer les dépendances
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configurer l'Assistant IA (Assistant interactif)
Lancez notre assistant multilingue pour choisir votre fournisseur d'IA et renseigner votre clé API :
```powershell
python setup_llm.py
```
- Disponible en 8 langues : Français, English, Русский, Español, Nederlands, Português, 简体中文, 日本語.
- Fonctionne avec **Google Gemini** (*forfait gratuit disponible sur [Google AI Studio](https://aistudio.google.com/)*), **Ollama** (*100% gratuit & local sans connexion*), **OpenAI**, **Claude**, **DeepSeek** ou **Qwen**.
- *(Facultatif)* Vous pouvez aussi le configurer via la CLI Django (`python manage.py configure_llm --list`) ou sur le tableau de bord web à `/assistant/settings/`.

#### 4. Initialiser la base de données et charger les données de démonstration
```powershell
# Créer les tables de la base de données
python manage.py migrate

# Charger les données de démonstration (recommandé : remplit les factures, le stock, les tiers et les contrats)
python manage.py seed_demo_data

# (Facultatif) Créer un compte administrateur pour accéder à /admin/
python manage.py createsuperuser
```

---

### 🏃 Utilisation Quotidienne (Lancer l'application à tout moment)

À l'avenir, pour démarrer l'application, vous n'aurez besoin que de **deux commandes** :

```powershell
# 1. Activer l'environnement (s'il n'est pas déjà actif)
.\.venv\Scripts\Activate.ps1

# 2. Démarrer le serveur
python manage.py runserver
```

Ouvrez votre navigateur à l'adresse : **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** 🎉

---

### ❓ Dépannage & Questions Fréquentes

| Problème | Cause et solution rapide |
| :--- | :--- |
| **`python n'est pas reconnu en tant que commande interne ou externe`** | Python a été installé sans cocher la case **Add to PATH**. Relancez l'installateur Python, choisissez **Modify**, cochez **Add Python to environment variables** et redémarrez votre terminal. |
| **`Le fichier Activate.ps1 ne peut pas être chargé car l'exécution de scripts est désactivée`** | Windows bloque les scripts PowerShell par défaut. Exécutez `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`, ou utilisez l'Invite de commandes (CMD) : `.\.venv\Scripts\activate.bat`. |
| **`Error: That port is already in use`** | Le port 8000 est déjà utilisé par une autre application ou une session précédente. Démarrez sur un autre port : `python manage.py runserver 8080`. |
| **`no such table: ...`** | La base de données n'est pas encore initialisée. Exécutez : `python manage.py migrate`. |

---

## 🛠️ Commandes d'Administration

- **Assistant Interactif de Configuration des Modèles IA** :
  ```powershell
  python setup_llm.py
  # ou : python manage.py configure_llm [--lang fr]
  ```

- **Recompiler les Fichiers de Traduction (.po et .mo)** :
  ```powershell
  python build_translations.py
  ```

- **Déclencher la Vérification des Rappels** :
  ```powershell
  python manage.py run_reminders
  ```

- **Exécuter la Suite de Tests Automatisés** :
  ```powershell
  python manage.py test
  ```

---

## 📄 Licence

Ce projet est sous licence **MIT** — consultez le fichier [LICENSE](LICENSE) pour plus de détails.

