"""
whatsapp_client.py – Cliente para la Meta WhatsApp Cloud API
Envía mensajes y gestiona el estado de lectura.
"""

import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
META_API_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}"


class WhatsAppClient:

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json",
        }

    async def send_message(self, to: str, text: str) -> dict:
        """Envía un mensaje de texto a un número de WhatsApp."""
        url = f"{META_API_URL}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            if response.status_code != 200:
                logger.error("❌ Error al enviar mensaje: %s", response.text)
            else:
                logger.info("✅ Mensaje enviado a %s", to)
            return response.json()

    async def mark_as_read(self, message_id: str) -> dict:
        """Marca un mensaje como leído (doble check azul)."""
        url = f"{META_API_URL}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            return response.json()
