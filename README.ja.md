# Sole Enterprise Orchestrator＆経理・企業管理AIエージェント

[![License: MIT](https://img.shields.io/badge/ライセンス-MIT-blue.svg)](LICENSE)
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

スキャン書類のインテリジェント管理、仕訳・会計、在庫管理、およびカレンダー自動化を統合した企業向けERPシステムです。**Python 3.11+**、**Django 5.x**、**Tailwind CSS**、および **Google Gemini マルチモーダルAI** を採用しています。

---

## 🌐 対応言語（多言語 i18n サポート）

本システムはUI・各種マスター・通知を含め、**8言語** に完全対応しています：
- 🇬🇧 **English / 英語** (`en`)
- 🇷🇺 **Русский / ロシア語** (`ru`)
- 🇪🇸 **Español / スペイン語** (`es`)
- 🇳🇱 **Nederlands / オランダ語** (`nl`)
- 🇫🇷 **Français / フランス語** (`fr`)
- 🇵🇹 **Português / ポルトガル語** (`pt`)
- 🇨🇳 **简体中文 / 中国語** (`zh-hans`)
- 🇯🇵 **日本語** (`ja`)

ナビゲーションバー右上の地球儀アイコンからいつでも言語を切り替えることができます。

---

## 🌟 主な機能と特徴

1. **スキャン書類の自動取り込み＆マルチモーダルAI解析**:
   - 契約書、請求書、領収書、納品書などのスキャンPDFおよび画像に対応。
   - 取引先企業名、明細行、消費税・VAT内訳、銀行口座番号（IBAN）、支払期日を高精度に自動抽出。
   - 差し替え可能なマルチLLMエンジン（**Google Gemini**、**OpenAI ChatGPT / GPT-4o**、**Anthropic Claude 3.7**、**DeepSeek V3 / R1**、**Alibaba Qwen**、または社内ローカル **Ollama**）を搭載。

2. **2画面並列（Side-by-Side）検証スクリーン**:
   - 左側にスキャン原本のビューア、右側に編集可能な構造化フォームを配置。
   - **「確認して台帳に登録」** ボタンを1クリックするだけで、取引先マスター、仕訳帳、在庫、カレンダー予定が一括で同期されます。

3. **財務・会計＆キャッシュフロー管理（買掛金・売掛金）**:
   - **買掛金（AP）**: 仕入先からの請求書の期日管理と支払いステータス追跡。
   - **売掛金（AR）**: 顧客向け請求書の発行と入金予定管理。
   - 柔軟な支払消込（一部入金、全額完済、決済手段、取引参照番号の記録）。
   - 小口現金および経費伝票・レシートの管理。

4. **倉庫在庫＆納品・委託貨物管理**:
   - SKUコード、現在庫数、発注点アラートを備えた商品台帳。
   - 入庫・出庫納品書の管理。
   - **「検品して入庫登録」** 1クリックで物理在庫を即座に増減し、移動履歴監査ログ（`StockMovement`）を記録。

5. **統合カレンダー＆リアルタイム iCalendar 連携**:
   - 業務種別ごとに色分けされたインタラクティブな FullCalendar.js 表示：
     - 🔴 **赤**: 買掛金・請求書の支払期日
     - 🟢 **緑**: 売掛金・顧客からの入金予定日
     - 🟣 **紫**: 契約更新の検討・解約通知期日
     - 🟠 **オレンジ**: 貨物の配送・納品予定
     - 🔵 **青**: 一般的な総務・管理タスク
   - **リアルタイム iCal (.ics) フィード**: トークン付きURL（`/calendar/feed.ics?token=...`）を提供し、**Google カレンダー**、**Apple Calendar**、**Outlook**、**Thunderbird** に瞬時に登録・自動同期可能。

6. **事前アラート＆リマインダー通知**:
   - 日次自動評価タスク（`manage.py run_reminders`）:
     - 支払期日の7日前、3日前、前日、および当日リマインダー。
     - 支払遅延・期日超過請求書に対する緊急エスカレーション。
     - 契約更新通知期日の事前アラート。
     - 在庫僅少の自動通知。
   - ヘッダー右上に未読アラート通知ベルを設置。

7. **組み込み型 AI コパイロット（業務アシスタント）**:
   - サイドドロワーからワンクリックで呼び出せる対話型AI。
   - リアルタイム台帳データに基づき自然言語で即答（*「今週期限の支払いは？」「在庫が少ない商品を教えて」「財務状況を要約して」*）。
   - 8言語すべてにおいて母国語での対話に対応。

---

## 🚀 クイックスタートガイド

### 1. 仮想環境の有効化
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. 環境変数とAIモデルプロバイダーの設定
`.env.example` を `.env` にコピーするか、自動対話型セットアップウィザードを実行します：
```powershell
python setup_llm.py
```
*(日本語、English、Русский、Español、Nederlands、Français、Português、简体中文 に完全対応)*。

Django 管理コマンドやブラウザ管理画面 **`/assistant/settings/`** からもいつでも視覚的に設定・切替が可能です：
```powershell
# 利用可能なプロバイダー一覧とAPIキー登録状況を確認
python manage.py configure_llm --list

# 非対話型で即座に設定・接続テストを実行
python manage.py configure_llm --provider deepseek --api-key sk-xxxx --model deepseek-chat --test
```

### 3. マイグレーションの実行＆デモデータの投入
```powershell
python manage.py migrate
```

管理画面へのアクセス用スーパーユーザーを作成する場合：
```powershell
python manage.py createsuperuser
```

テスト用のサンプルデータをシステムに投入する場合：
```powershell
python manage.py seed_demo_data
```

### 4. 開発用サーバーの起動
```powershell
python manage.py runserver
```
ブラウザで **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** を開きます。

---

## 🛠️ 管理・運用コマンド

- **対話型 AI モデルセットアップウィザード**:
  ```powershell
  python setup_llm.py
  # または: python manage.py configure_llm [--lang ja]
  ```

- **言語翻訳カタログの再コンパイル (.po & .mo)**:
  ```powershell
  python build_translations.py
  ```

- **リマインダー・アラート確認の実行**:
  ```powershell
  python manage.py run_reminders
  ```

- **自動テストスイートの実行**:
  ```powershell
  python manage.py test
  ```

---

## 📄 ライセンス (License)

本プロジェクトは **MIT ライセンス** の下で公開されています — 詳細は [LICENSE](LICENSE) ファイルをご参照ください。

