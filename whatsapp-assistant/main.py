"""
main.py – Servidor FastAPI para el asistente WhatsApp de Babylone42
Maneja el webhook de Meta y coordina la IA con el cliente de WhatsApp.
"""

import os
import json
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

from ai_assistant import AIAssistant
from whatsapp_client import WhatsAppClient

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Babylone42 WhatsApp Assistant")

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "babylone42_secret_webhook")

assistant = AIAssistant()
whatsapp = WhatsAppClient()


# ──────────────────────────────────────────
# GET /webhook  →  Verificación del webhook por Meta
# ──────────────────────────────────────────
@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("✅ Webhook verificado por Meta.")
        return PlainTextResponse(content=challenge, status_code=200)

    logger.warning("❌ Webhook: token inválido.")
    raise HTTPException(status_code=403, detail="Token de verificación incorrecto.")


# ──────────────────────────────────────────
# POST /webhook  →  Recibir mensajes de WhatsApp
# ──────────────────────────────────────────
@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()
    logger.info("📩 Evento recibido: %s", json.dumps(body, indent=2))

    try:
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        # Solo procesar si hay mensajes
        if "messages" not in value:
            return {"status": "no_message"}

        message = value["messages"][0]
        phone_number = message["from"]
        message_id = message["id"]
        message_type = message.get("type", "")

        # Solo procesar mensajes de texto
        if message_type != "text":
            logger.info("⏭ Tipo de mensaje no soportado: %s", message_type)
            return {"status": "ignored"}

        user_text = message["text"]["body"]
        logger.info("📨 Mensaje de %s: %s", phone_number, user_text)

        # Marcar como leído (doble check azul)
        await whatsapp.mark_as_read(message_id)

        # Obtener respuesta de la IA
        ai_response = await assistant.get_response(phone_number, user_text)
        logger.info("🤖 Respuesta IA: %s", ai_response)

        # Enviar respuesta al usuario
        await whatsapp.send_message(phone_number, ai_response)

    except (KeyError, IndexError) as e:
        logger.warning("⚠️ Estructura de mensaje inesperada: %s", e)

    return {"status": "ok"}


# ──────────────────────────────────────────
# Health check
# ──────────────────────────────────────────
@app.get("/")
async def root():
    return {"status": "running", "service": "Babylone42 WhatsApp Assistant"}
