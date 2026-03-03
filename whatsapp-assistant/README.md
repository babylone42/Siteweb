# 🤖 Babylone42 – WhatsApp AI Assistant

Asistente inteligente que responde por WhatsApp usando la **Meta WhatsApp Cloud API** y **OpenAI GPT-4o**, construido en Python con FastAPI.

---

## 🏗 Arquitectura

```
WhatsApp Usuario
       │
       ▼
 Meta Cloud API ──► Webhook POST /webhook
                         │
                    FastAPI Server (Python)
                         │
                    ai_assistant.py (GPT-4o)
                         │
                    whatsapp_client.py
                         │
                    Meta Cloud API ──► Respuesta al usuario
```

**Stack:**
- **FastAPI** – servidor web ligero
- **OpenAI GPT-4o** – cerebro del asistente
- **Meta WhatsApp Cloud API** – canal oficial gratuito
- **ngrok** – túnel local para testing
- **python-dotenv** – manejo de secrets

---

## 📋 Funcionalidades

- ✅ Responder preguntas frecuentes sobre Babylone42
- ✅ Capturar leads (nombre, empresa, necesidad)
- ✅ Gestionar solicitudes de citas/demos
- ✅ Memoria de conversación por usuario
- ✅ Marcar mensajes como leídos (doble check azul)

---

## 🚀 Instalación rápida

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 3. Arrancar el servidor
```bash
uvicorn main:app --reload --port 8000
```

### 4. Exponer con ngrok (para testing)
```bash
ngrok http 8000
# Copiar la URL https://xxxx.ngrok.io
```

### 5. Registrar webhook en Meta
- URL: `https://xxxx.ngrok.io/webhook`
- Verify Token: el valor de `VERIFY_TOKEN` en tu `.env`

---

## 📂 Estructura del proyecto

```
whatsapp-assistant/
├── main.py               # Servidor FastAPI + webhook
├── ai_assistant.py       # Lógica de IA (GPT-4o)
├── whatsapp_client.py    # Envío de mensajes via Meta API
├── requirements.txt      # Dependencias Python
├── .env.example          # Plantilla de variables de entorno
├── .gitignore            # Excluye .env y __pycache__
└── README.md             # Este archivo
```

---

## 🔐 Pasos en Meta Developers (prerequisito)

### Paso A – Crear App
1. → [developers.facebook.com](https://developers.facebook.com)
2. **Mis Apps → Crear App → Business**
3. Nombre: `Babylone42-WhatsApp-Assistant`
4. Vincular cuenta Facebook Business
5. **Agregar producto → WhatsApp → Configurar**

### Paso B – Obtener credenciales
En **WhatsApp → Configuración de la API**:
- `Phone Number ID`
- `WhatsApp Business Account ID`
- `Access Token` (temporal para testing, permanente para producción)

### Paso C – Agregar número de prueba
- Agrega tu número personal como destino en el sandbox
- El número real de Babylone42 se configura después como origen

### Paso D – Webhook
- URL: `https://[tu-ngrok].ngrok.io/webhook`
- Verify Token: valor de `VERIFY_TOKEN` en `.env`

---

## 🔑 Variables de entorno (.env)

| Variable | Descripción |
|---|---|
| `OPENAI_API_KEY` | API Key de OpenAI ([platform.openai.com](https://platform.openai.com)) |
| `WHATSAPP_TOKEN` | Access Token de Meta WhatsApp |
| `PHONE_NUMBER_ID` | ID del número de teléfono en Meta |
| `VERIFY_TOKEN` | Token secreto para verificar el webhook |

---

## 📞 Contacto

**Babylone42** – [babylone42.fr](https://babylone42.fr)
