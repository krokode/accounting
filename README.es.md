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

### 1. Activar el Entorno Virtual
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Configurar Entorno y Proveedores de IA
Copie `.env.example` como `.env` o ejecute el asistente interactivo automatizado:
```powershell
python setup_llm.py
```
*(Compatible con Español, English, Русский, Nederlands, Français, Português, 简体中文 y 日本語)*.

También puede configurar proveedores mediante el comando Django o el panel web en **`/assistant/settings/`**:
```powershell
# Listar proveedores y estado de credenciales
python manage.py configure_llm --list

# Configurar y verificar de forma no interactiva
python manage.py configure_llm --provider deepseek --api-key sk-xxxx --model deepseek-chat --test
```

### 3. Aplicar Migraciones y Cargar Datos de Demostración
```powershell
python manage.py migrate
```

Si desea crear un superusuario para acceder a la administración:
```powershell
python manage.py createsuperuser
```

Si desea rellenar el sistema con datos de prueba para realizar pruebas:
```powershell
python manage.py seed_demo_data
```

### 4. Iniciar el Servidor de Desarrollo
```powershell
python manage.py runserver
```
Abra en su navegador: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**.

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

