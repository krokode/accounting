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

## 🚀 Démarrage Rapide

### 1. Activer l'Environnement Virtuel
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Configurer l'Environnement & les Fournisseurs d'IA
Copiez `.env.example` vers `.env` ou exécutez l'assistant interactif de configuration :
```powershell
python setup_llm.py
```
*(Prend en charge le Français, English, Русский, Español, Nederlands, Português, 简体中文 et 日本語)*.

Vous pouvez également configurer les modèles via la commande Django ou l'interface web sur **`/assistant/settings/`** :
```powershell
# Afficher les fournisseurs disponibles et le statut des clés
python manage.py configure_llm --list

# Configuration et test non interactifs
python manage.py configure_llm --provider deepseek --api-key sk-xxxx --model deepseek-chat --test
```

### 3. Appliquer les Migrations & Charger les Données de Démonstration
```powershell
python manage.py migrate
```

Si vous souhaitez créer un superutilisateur pour l'accès administrateur :
```powershell
python manage.py createsuperuser
```

Si vous souhaitez peupler le système avec des données d'exemple pour les tests :
```powershell
python manage.py seed_demo_data
```

### 4. Lancer le Serveur de Développement
```powershell
python manage.py runserver
```
Consultez **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** dans votre navigateur.

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

