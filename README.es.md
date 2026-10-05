# Sole Enterprise Orchestrator y Agente de Gestión Contable

[![License: MIT](https://img.shields.io/badge/Licencia-MIT-blue.svg)](LICENSE)
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

Un sistema inteligente y multilingüe para la gestión documental empresarial, contabilidad, control de almacén y automatización de calendarios, desarrollado con **Python 3.11+**, **Django 5.x**, **Tailwind CSS** y **Google Gemini Multimodal AI**.

---

## 🌐 Idiomas Compatibles (Soporte Multilingüe i18n)

Toda la aplicación está completamente internacionalizada en **8 idiomas**:
- 🇬🇧 **English** (`en`)
- 🇷🇺 **Русский / Ruso** (`ru`)
- 🇪🇸 **Español** (`es`)
- 🇳🇱 **Nederlands / Holandés** (`nl`)
- 🇫🇷 **Français / Francés** (`fr`)
- 🇵🇹 **Português / Portugués** (`pt`)
- 🇨🇳 **简体中文 / Chino simplificado** (`zh-hans`)
- 🇯🇵 **日本語 / Japonés** (`ja`)

Cambie de idioma en cualquier momento desde el selector de globo terráqueo en la barra de navegación superior.

---

## 🌟 Capacidades Principales

1. **Ingesta de Documentos Escaneados e IA Multimodal**:
   - Ingesta de archivos PDF escaneados e imágenes de contratos, facturas de proveedores, recibos y albaranes de entrega.
   - Extrae con precisión contrapartes, partidas, desglose de IVA/impuestos, códigos IBAN y fechas límite.
   - Desarrollado sobre motores intercambiables Multi-LLM (**Google Gemini**, **OpenAI ChatGPT / GPT-4o**, **Anthropic Claude 3.7**, **DeepSeek V3 / R1**, **Alibaba Qwen** u **Ollama local**).

2. **Pantalla de Verificación Paralela (Side-by-Side)**:
   - Revisión dividida: visor del documento escaneado a la izquierda, formulario interactivo estructurado a la derecha.
   - El botón **«Confirmar y Registrar en Libros»** sincroniza automáticamente proveedores, libros contables, inventario y tareas de calendario con 1 solo clic.

3. **Contabilidad y Flujo de Caja (Cuentas a Pagar y Cobrar)**:
   - **Cuentas a Pagar (AP)**: Facturas de compras a proveedores con control de vencimiento.
   - **Cuentas a Cobrar (AR)**: Facturas emitidas e ingresos esperados de clientes.
   - Registro de pagos en varias fases (pago parcial, liquidación completa, método de pago, referencia bancaria).
   - Gestión de recibos de gastos menores y caja chica.

4. **Almacén y Albaranes de Entrega**:
   - Catálogo de inventario con SKU, recuento disponible y avisos de punto de pedido bajo mínimos.
   - Albaranes y hojas de entrega de entrada y salida.
   - El botón **«Confirmar e Ingresar a Stock»** actualiza el saldo de inventario y genera asientos de auditoría (`StockMovement`).

5. **Calendario Unificado y Sincronización iCalendar en Vivo**:
   - Vista interactiva FullCalendar.js clasificada por color:
     - 🔴 **Rojo**: Factura de proveedor por vencer
     - 🟢 **Verde**: Cobro entrante previsto de cliente
     - 🟣 **Morado**: Plazo de decisión o renovación de contrato
     - 🟠 **Naranja**: Entrega de mercancía / albarán
     - 🔵 **Azul**: Tarea administrativa general
   - **Canal iCal (.ics) en vivo**: URL segura con token (`/calendar/feed.ics?token=...`) para suscripción directa en **Google Calendar**, **Apple Calendar**, **Microsoft Outlook** o **Thunderbird**.

6. **Recordatorios y Alertas Proactivas**:
   - Evaluador automático diario (`manage.py run_reminders`):
     - Vencimientos a T-7, T-3, T-1 días y en la fecha límite.
     - Alertas críticas de facturas impagadas / vencidas.
     - Plazos de aviso para renovación de contratos comerciales.
     - Alertas de existencias bajas en almacén.
   - Menú de notificaciones («campana») en el encabezado.

7. **Copiloto con IA Integrado**:
   - Asistente conversacional disponible en el panel lateral en cualquier pantalla.
   - Consultas en lenguaje natural conectadas a la base de datos en tiempo real (*«¿Qué facturas vencen esta semana?»*, *«Mostrar existencias bajas»*, *«Resumir estado financiero»*).
   - Soporte multilingüe en los 8 idiomas.

---

## 🚀 Guía de Inicio Rápido

### 🔰 Requisitos previos: Instalar Python (Una sola vez)

Este proyecto requiere **Python 3.11 o superior** (compatible con Python 3.11, 3.12 y 3.13).

1. Descargue el instalador desde la [página oficial de descargas de Python](https://www.python.org/downloads/).
2. Ejecute el instalador. **PASO CRÍTICO:** En la primera pantalla, marque la casilla:  
   ☑️ **Add python.exe to PATH**  
   *(¡Si omite este paso, su terminal no reconocerá el comando `python`!)*
3. Haga clic en **Install Now**.
4. Abra la carpeta del proyecto en el Explorador de archivos. Haga clic en la barra de direcciones superior, escriba `powershell` (o `cmd`) y presione <kbd>Enter</kbd>. Se abrirá una ventana de terminal directamente en esta carpeta.
5. Verifique la instalación:
   ```powershell
   python --version
   ```
   *(Debe mostrar `Python 3.11.x`, `3.12.x` o `3.13.x`)*.

---

### ⚡ Configuración inicial (5 minutos)

Ejecute estos pasos una sola vez en su terminal dentro de la carpeta del proyecto:

#### 1. Crear y activar el entorno aislado
```powershell
# Crear el entorno virtual (.venv)
python -m venv .venv

# Activar en Windows PowerShell:
.\.venv\Scripts\Activate.ps1
```
> **Consejo para Windows:** Si aparece un mensaje en rojo indicando que *`la ejecución de scripts está deshabilitada en este sistema`* (*`running scripts is disabled on this system`*), ejecute este comando y vuelva a activar:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> .\.venv\Scripts\Activate.ps1
> ```
> *(O use el Símbolo del sistema: `.\.venv\Scripts\activate.bat`, o en macOS/Linux: `source .venv/bin/activate`)*.

Cuando esté activado, verá `(.venv)` al inicio de la línea de comandos.

#### 2. Instalar dependencias
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configurar el Asistente de IA (Asistente interactivo)
Ejecute nuestro asistente de configuración multilingüe para elegir el proveedor de IA y configurar su clave de API:
```powershell
python setup_llm.py
```
- Disponible en 8 idiomas: Español, English, Русский, Nederlands, Français, Português, 简体中文, 日本語.
- Funciona con **Google Gemini** (*nivel gratuito disponible en [Google AI Studio](https://aistudio.google.com/)*), **Ollama** (*100% gratuito y local sin conexión*), **OpenAI**, **Claude**, **DeepSeek** o **Qwen**.
- *(Opcional)* También puede configurar mediante la CLI de Django (`python manage.py configure_llm --list`) o en la interfaz web en `/assistant/settings/`.

#### 4. Inicializar base de datos y cargar datos de demostración
```powershell
# Crear tablas de base de datos
python manage.py migrate

# Cargar datos de demostración (recomendado: crea facturas, inventario, contrapartes y contratos)
python manage.py seed_demo_data

# (Opcional) Crear un usuario administrador para acceder a /admin/
python manage.py createsuperuser
```

---

### 🏃 Uso cotidiano (Iniciar la aplicación en cualquier momento)

En el futuro, para iniciar la aplicación solo necesita ejecutar **dos comandos**:

```powershell
# 1. Activar el entorno (si aún no está activo)
.\.venv\Scripts\Activate.ps1

# 2. Iniciar el servidor
python manage.py runserver
```

Abra su navegador y acceda a: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** 🎉

---

### ❓ Solución de problemas comunes

| Problema | Causa y solución rápida |
| :--- | :--- |
| **`python no se reconoce como un comando interno o externo`** | Python se instaló sin marcar la casilla **Add to PATH**. Vuelva a ejecutar el instalador de Python, elija **Modify**, marque **Add Python to environment variables** y reinicie la terminal. |
| **`No se puede cargar el archivo Activate.ps1 porque la ejecución de scripts está deshabilitada`** | Windows bloquea los scripts de PowerShell de forma predeterminada. Ejecute `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`, o cambie al Símbolo del sistema y ejecute `.\.venv\Scripts\activate.bat`. |
| **`Error: That port is already in use`** | El puerto 8000 está ocupado por otra aplicación o sesión previa. Inicie en otro puerto: `python manage.py runserver 8080`. |
| **`no such table: ...`** | La base de datos aún no ha sido inicializada. Ejecute `python manage.py migrate`. |

---

## 🛠️ Comandos de Gestión

- **Asistente Interactivo de Configuración de IA**:
  ```powershell
  python setup_llm.py
  # o bien: python manage.py configure_llm [--lang es]
  ```

- **Compilar Catálogos de Traducción (.po y .mo)**:
  ```powershell
  python build_translations.py
  ```

- **Ejecutar Comprobación de Recordatorios**:
  ```powershell
  python manage.py run_reminders
  ```

- **Ejecutar Batería de Pruebas Automatizadas**:
  ```powershell
  python manage.py test
  ```

---

## 📄 Licencia

Este proyecto está distribuido bajo la **Licencia MIT** — consulte el archivo [LICENSE](LICENSE) para más detalles.

