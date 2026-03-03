"""
ai_assistant.py – Cerebro del asistente Babylone42
Gestiona conversaciones con memoria por usuario usando OpenAI GPT-4o.
"""

import os
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Eres el asistente virtual de Babylone42, una empresa especializada en inteligencia artificial aplicada a negocios B2B.

## Tu rol
- Presentar los servicios de Babylone42 de forma clara y persuasiva.
- Responder preguntas frecuentes sobre la empresa.
- Capturar información de leads interesados (nombre, empresa, necesidad).
- Ayudar a agendar demos o diagnósticos gratuitos.
- Siempre ser profesional, conciso y orientado a resultados.

## Sobre Babylone42
- **¿Quiénes somos?**: Empresa de consultoría e implementación de IA para negocios. Ayudamos a empresas a automatizar procesos, aumentar productividad y reducir costos con IA.
- **Servicios principales**:
  1. 🤖 Automatización de procesos con IA (chatbots, workflows, RPA)
  2. 📊 Análisis de datos e IA predictiva
  3. 🎓 Formaciones en IA para equipos empresariales
  4. 🔧 Consultoría estratégica de transformación digital
- **Diagnóstico IA Gratuito**: Ofrecemos una sesión de diagnóstico gratuita de 30 min para identificar oportunidades de IA en tu empresa.
- **Contacto**: info@babylone42.fr | www.babylone42.fr
- **Ubicación**: Francia (servicio en francés, español e inglés)

## Flujo de conversación
1. Saluda calurosamente y pregunta cómo puedes ayudar.
2. Si el usuario muestra interés en los servicios, captura:
   - Nombre completo
   - Empresa
   - Principal necesidad o problema
3. Propón siempre el **Diagnóstico IA Gratuito** como primer paso.
4. Si quiere agendar, pídeles que envíen su email para que el equipo les contacte.

## Reglas
- Responde siempre en el idioma del usuario (francés, español o inglés).
- Mensajes cortos y directos (máximo 3 párrafos por respuesta).
- Usa emojis con moderación para dar calidez.
- Si no sabes algo, di que lo consultarás con el equipo y pedirás que dejen su email.
- NUNCA inventes precios específicos sin confirmar con el equipo.
"""


class AIAssistant:
    """
    Asistente con memoria de conversación por número de teléfono.
    Cada usuario tiene su propio historial de mensajes.
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.conversations: dict[str, list[dict]] = {}
        self.max_history = 20  # Máximo de mensajes por usuario en memoria

    def _get_history(self, phone: str) -> list[dict]:
        """Obtiene o inicializa el historial de un usuario."""
        if phone not in self.conversations:
            self.conversations[phone] = []
        return self.conversations[phone]

    def _add_message(self, phone: str, role: str, content: str):
        """Añade un mensaje al historial del usuario."""
        history = self._get_history(phone)
        history.append({"role": role, "content": content})
        # Mantener solo los últimos N mensajes para no exceder el contexto
        if len(history) > self.max_history:
            self.conversations[phone] = history[-self.max_history:]

    async def get_response(self, phone: str, user_message: str) -> str:
        """
        Genera una respuesta de IA para el mensaje del usuario.
        
        Args:
            phone: Número de teléfono del usuario (identificador único)
            user_message: Texto recibido del usuario
            
        Returns:
            Respuesta generada por GPT-4o
        """
        # Añadir mensaje del usuario al historial
        self._add_message(phone, "user", user_message)

        # Construir mensajes para OpenAI
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *self._get_history(phone),
        ]

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
            )
            ai_text = response.choices[0].message.content.strip()

            # Guardar respuesta en historial
            self._add_message(phone, "assistant", ai_text)
            return ai_text

        except Exception as e:
            logger.error("❌ Error OpenAI: %s", e)
            return (
                "Lo siento, estoy teniendo dificultades técnicas en este momento. "
                "Por favor, contacta directamente a info@babylone42.fr. 🙏"
            )

    def clear_history(self, phone: str):
        """Limpia el historial de conversación de un usuario."""
        if phone in self.conversations:
            del self.conversations[phone]
            logger.info("🗑️ Historial limpiado para %s", phone)
