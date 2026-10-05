# Sole Enterprise Orchestrator 企业编排与财务管理智能体

[![License: MIT](https://img.shields.io/badge/开源协议-MIT-blue.svg)](LICENSE)
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

基于 **Python 3.11+**、**Django 5.x**、**Tailwind CSS** 与 **Google Gemini 多模态人工智能** 构建的企业级多语言单据管理、财务核算、仓储库存及日程自动化智能系统。

---

## 🌐 支持的语言环境 (国际化 i18n)

系统全部界面、数据字典与交互组件均已完成 **8 种语言** 的本地化支持：
- 🇬🇧 **English / 英语** (`en`)
- 🇷🇺 **Русский / 俄语** (`ru`)
- 🇪🇸 **Español / 西班牙语** (`es`)
- 🇳🇱 **Nederlands / 荷兰语** (`nl`)
- 🇫🇷 **Français / 法语** (`fr`)
- 🇵🇹 **Português / 葡萄牙语** (`pt`)
- 🇨🇳 **简体中文** (`zh-hans`)
- 🇯🇵 **日本語 / 日语** (`ja`)

您可以在页面顶部的地球图标下拉菜单中随时切换系统语言。

---

## 🌟 核心功能特性

1. **扫描单据智能摄取与多模态 AI 分析**:
   - 支持上传合同协议、供应商发票、费用收据及货物发货单（支持 PDF 与图像格式）。
   - 自动结构化提取往来企业、单据行项目、增值税额、银行 IBAN 账号以及关键到期日期。
   - 支持可插拔的多模型引擎 (**Google Gemini**、**OpenAI ChatGPT / GPT-4o**、**Anthropic Claude 3.7**、**DeepSeek V3 / R1**、**阿里通义千问 Qwen** 或本地私有化 **Ollama**)。

2. **双联并排核对与确认屏幕 (Side-by-Side Verification)**:
   - 分屏审核：左侧显示原始扫描件原貌，右侧呈现结构化可编辑表单。
   - 一键 **“确认并写入账册”**，自动同步供应商档案、会计凭证、仓储库存及日程待办事项。

3. **财务核算与现金流管控 (应收/应付)**:
   - **应付账款 (AP)**: 供应商采购账单及付款账期全流程追踪。
   - **应收账款 (AR)**: 客户销售发票及预期收款计划。
   - 多阶段支付记录（支持部分付款、全额结清、支付方式选择及银行流水号录入）。
   - 日常零用现金与小额报销凭证管理。

4. **智能仓储与物流送货单 (Consignments)**:
   - 包含 SKU 编号、在手库存数量以及安全补货预警线的商品目录。
   - 进货与出货发运单据管理。
   - 一键 **“确认并验收入库”**，自动增减物理库存并生成完整的库存变动审计日志 (`StockMovement`)。

5. **统一日程中心与实时 iCalendar 订阅流**:
   - 交互式 FullCalendar.js 日历，按业务类型自动颜色标记：
     - 🔴 **红色**: 供应商账单到期付款
     - 🟢 **绿色**: 客户销售货款预期入账
     - 🟣 **紫色**: 商业合同续约决策期/解约通知窗口
     - 🟠 **橙色**: 物流货物送达排期
     - 🔵 **蓝色**: 综合行政日常事务
   - **实时 iCal (.ics) 订阅**: 提供带令牌的安全链接 (`/calendar/feed.ics?token=...`)，可在 **Google 日历**、**Apple Calendar**、**Outlook** 或 **雷鸟 (Thunderbird)** 中一键订阅同步。

6. **前瞻性主动提醒与风控告警**:
   - 自动化日常巡检调度任务 (`manage.py run_reminders`):
     - 提前 7 天、3 天、1 天及当天触发付款提醒。
     - 逾期未付发票的紧急升格预警。
     - 商务合同即将到期续签提醒。
     - 仓库商品低库存预警。
   - 顶部导航栏提供未读消息铃铛与动态气泡。

7. **内嵌式 AI 业务智能助理 (Copilot)**:
   - 随时在右侧抽屉式面板中调出交互式对话助手。
   - 针对当前数据库实时账册进行自然语言问答（*“本周有哪些待付款项？”*、*“查看需要补货的商品”*、*“总结当前公司资金概况”*）。
   - 完整支持所有 8 种语言的自然语言问答与引导提示。

---

## 🚀 快速上手指南

### 🔰 前置准备：安装 Python（仅需一次）

本项目需要 **Python 3.11 或更高版本**（全面兼容 Python 3.11、3.12 及 3.13）。

1. 前往 [Python 官方下载页面](https://www.python.org/downloads/) 下载安装程序。
2. 运行安装程序。**关键步骤：** 在安装界面的第一个窗口中，务必勾选底部复选框：  
   ☑️ **Add python.exe to PATH**（将 Python 添加至环境变量）  
   *（若遗漏此步，终端将无法识别 `python` 指令！）*
3. 点击 **Install Now** 完成安装。
4. 在文件资源管理器中打开本项目文件夹。点击窗口顶部的地址栏，输入 `powershell`（或 `cmd`）并按 <kbd>Enter</kbd> 回车。终端窗口将在当前项目目录下直接打开。
5. 验证安装：
   ```powershell
   python --version
   ```
   *（终端应正确输出 `Python 3.11.x`、`3.12.x` 或 `3.13.x`）*。

---

### ⚡ 首次初始化配置（仅需 5 分钟）

在项目文件夹打开的终端中依次执行以下步骤：

#### 1. 创建并激活独立虚拟环境
```powershell
# 创建虚拟环境 (.venv)
python -m venv .venv

# 激活虚拟环境 (Windows PowerShell):
.\.venv\Scripts\Activate.ps1
```
> **Windows 用户提示：** 如果终端出现红色错误提示 *`在此系统上禁止运行脚本`*（*`running scripts is disabled on this system`*），请执行以下命令解除限制并重新激活：
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> .\.venv\Scripts\Activate.ps1
> ```
> *（或使用命令提示符 CMD：`.\.venv\Scripts\activate.bat`，macOS/Linux：`source .venv/bin/activate`）*。

激活成功后，终端提示符前缀将显示 `(.venv)`。

#### 2. 安装项目依赖
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. 配置 AI 助手（交互式向导）
运行我们的全自动多语言配置向导，选择您的 AI 模型提供商并保存 API 密钥：
```powershell
python setup_llm.py
```
- 支持 8 种语言：简体中文、English、Русский、Español、Nederlands、Français、Português、日本語。
- 兼容 **Google Gemini**（*可在 [Google AI Studio](https://aistudio.google.com/) 免费申请密钥*）、**Ollama**（*100% 免费本地离线运行*）、**OpenAI**、**Claude**、**DeepSeek** 或 **Qwen**（通义千问）。
- *（可选）* 亦可通过 Django 命令行（`python manage.py configure_llm --list`）或访问网页端 `/assistant/settings/` 进行设置。

#### 4. 初始化数据库与导入演示数据
```powershell
# 执行数据库表结构迁移
python manage.py migrate

# 导入业务演示数据（强烈推荐：自动填充真实发票、库存、往来单位与合同）
python manage.py seed_demo_data

# （可选）创建系统管理员用户以访问 /admin/
python manage.py createsuperuser
```

---

### 🏃 日常使用（随用随启）

完成首次配置后，今后每次需要使用系统时，**仅需执行两条指令**：

```powershell
# 1. 激活虚拟环境（若尚未激活）
.\.venv\Scripts\Activate.ps1

# 2. 启动本地开发服务器
python manage.py runserver
```

在浏览器中打开：**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** 🎉

---

### ❓ 常见问题与疑难解答

| 常见错误 / 现象 | 产生原因与解决办法 |
| :--- | :--- |
| **`python 不是内部或外部命令`** | 安装 Python 时未勾选 **Add to PATH**。重新运行 Python 安装包，选择 **Modify**（修改），勾选 **Add Python to environment variables** 并重启终端。 |
| **`无法加载文件 Activate.ps1，因为在此系统上禁止运行脚本`** | Windows 默认策略阻止了 PowerShell 脚本。执行 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`，或切换至 CMD 执行 `.\.venv\Scripts\activate.bat`。 |
| **`Error: That port is already in use`** | 8000 端口已被其他程序或之前的 Django 进程占用。指定其他端口启动即可：`python manage.py runserver 8080`。 |
| **`no such table: ...`** | 尚未执行数据库迁移。运行：`python manage.py migrate`。 |

---

## 🛠️ 运维与管理指令

- **交互式 AI 模型提供商配置向导**:
  ```powershell
  python setup_llm.py
  # 或: python manage.py configure_llm [--lang zh-hans]
  ```

- **重新编译多语言翻译词典 (.po 与 .mo)**:
  ```powershell
  python build_translations.py
  ```

- **执行主动到期与库存巡检**:
  ```powershell
  python manage.py run_reminders
  ```

- **运行全量自动化测试套件**:
  ```powershell
  python manage.py test
  ```

---

## 📄 开源许可证 (License)

本项目采用 **MIT 开源许可证** 进行授权 — 完整条款请参阅 [LICENSE](LICENSE) 文件。

