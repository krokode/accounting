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

### 🔰 事前準備：Python のインストール（初回のみ）

本プロジェクトには **Python 3.11 以上** が必要です（Python 3.11、3.12、3.13 すべてに対応）。

1. [Python 公式ダウンロードページ](https://www.python.org/downloads/) からインストーラーをダウンロードします。
2. インストーラーを起動します。**極めて重要な手順：** 最初の画面で下部にあるチェックボックスを必ずオンにしてください：  
   ☑️ **Add python.exe to PATH**（PATH に python.exe を追加）  
   *（この手順を忘れると、ターミナルで `python` コマンドが認識されなくなります！）*
3. **Install Now** をクリックしてインストールを完了します。
4. エクスプローラーで本プロジェクトのフォルダーを開きます。上部のアドレスバーをクリックし、`powershell`（または `cmd`）と入力して <kbd>Enter</kbd> を押します。フォルダー内で直接ターミナルが開きます。
5. インストールを確認します：
   ```powershell
   python --version
   ```
   *（`Python 3.11.x`、`3.12.x`、または `3.13.x` と表示されれば成功です）*。

---

### ⚡ 初回セットアップ（5 分で完了）

プロジェクトフォルダーで開いたターミナルで以下の手順を 1 回だけ実行します：

#### 1. 独立した仮想環境の作成と有効化
```powershell
# 仮想環境 (.venv) の作成
python -m venv .venv

# 仮想環境の有効化 (Windows PowerShell):
.\.venv\Scripts\Activate.ps1
```
> **Windows のヒント：** もしターミナルに赤字で *`このシステムではスクリプトの実行が無効になっているため`*（*`running scripts is disabled on this system`*）と表示された場合は、次のコマンドを 1 度実行してから再度有効化してください：
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> .\.venv\Scripts\Activate.ps1
> ```
> *（またはコマンドプロンプト CMD: `.\.venv\Scripts\activate.bat`、macOS/Linux: `source .venv/bin/activate` を使用可能）*。

有効化に成功すると、ターミナルの行頭に `(.venv)` と表示されます。

#### 2. 依存パッケージのインストール
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. AI アシスタントの設定（対話型ウィザード）
多言語セットアップウィザードを実行し、希望する AI プロバイダーの選択と API キーの設定を行います：
```powershell
python setup_llm.py
```
- 8 言語に対応：日本語、English、Русский、Español、Nederlands、Français、Português、简体中文。
- **Google Gemini**（*[Google AI Studio](https://aistudio.google.com/) で無料枠を利用可能*）、**Ollama**（*完全無料・オフラインのローカル実行*）、**OpenAI**、**Claude**、**DeepSeek**、**Qwen** に対応。
- *（任意）* Django 管理コマンド（`python manage.py configure_llm --list`）やウェブ画面 `/assistant/settings/` からも設定できます。

#### 4. データベースの初期化とデモデータの投入
```powershell
# データベーステーブルの作成
python manage.py migrate

# デモデータの投入（推奨：請求書、在庫、取引先、契約書を自動生成）
python manage.py seed_demo_data

# （任意）管理画面 /admin/ アクセス用のスーパーユーザーを作成
python manage.py createsuperuser
```

---

### 🏃 日常的な起動方法（いつでも起動可能）

初期セットアップ完了後、今後アプリを起動する際は **以下の 2 コマンドを実行するだけ** です：

```powershell
# 1. 仮想環境の有効化（まだ有効化されていない場合）
.\.venv\Scripts\Activate.ps1

# 2. 開発サーバーの起動
python manage.py runserver
```

ブラウザで **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** を開きます 🎉

---

### ❓ トラブルシューティング（よくある質問）

| エラー・現象 | 原因と簡単な解決策 |
| :--- | :--- |
| **`python は内部コマンドまたは外部コマンドとして認識されていません`** | Python インストール時に **Add to PATH** にチェックを入れていません。Python インストーラーを再起動し、**Modify** を選択して **Add Python to environment variables** にチェックを入れてからターミナルを再起動してください。 |
| **`このシステムではスクリプトの実行が無効になっているため、Activate.ps1 を読み込めません`** | Windows のデフォルトポリシーで PowerShell スクリプトが制限されています。`Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` を実行するか、CMD に切り替えて `.\.venv\Scripts\activate.bat` を実行してください。 |
| **`Error: That port is already in use`** | ポート 8000 が他のアプリや前回の Django プロセスで使用中です。別のポートで起動してください：`python manage.py runserver 8080`。 |
| **`no such table: ...`** | データベースのマイグレーションが未実行です。`python manage.py migrate` を実行してください。 |

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

