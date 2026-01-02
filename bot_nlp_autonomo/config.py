import os
from openai import OpenAI

# Configurar OpenAI con SDK 1.0.0+
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Configuración del bot
CONFIG = {
    "model": "gpt-4o-mini",  # Modelo eficiente y económico
    "temperature": 0.3,      # Consistencia en respuestas
    "max_tokens": 1000,      # Límite de respuesta
    "system_prompt": """Eres un asistente técnico especializado en BIM (Building Information Modeling) y automatización de Revit.

Tu trabajo es:
1. Entender comandos en lenguaje natural sobre tareas de BIM/Revit
2. Proporcionar instrucciones claras y precisas
3. Sugerir comandos específicos cuando sea relevante
4. Responder preguntas técnicas sobre modelado BIM

Siempre sé conciso y útil. Si no estás seguro, indícalo claramente."""
}