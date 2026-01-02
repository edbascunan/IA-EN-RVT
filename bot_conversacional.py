# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Conversacional Inteligente
==============================================

Bot con conversación fluida y IA inteligente real
Múltiples proveedores de IA para máxima calidad
Autor: Eduardo Bascuñán
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class IA_RVT_Conversational_Bot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.hf_token = os.getenv('HUGGINGFACE_API_KEY')
        self.openrouter_key = os.getenv('OPENAI_API_KEY')  # Usar la key de OpenRouter
        self.command_path = os.getenv('COMMAND_PATH', 'backend_ai/shared/command_out.json')
        
        # Inicializar aplicación
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configurar handlers del bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("deploy", self.deploy_command))
        self.app.add_handler(CommandHandler("ai", self.ai_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_text = """🤖 ¡Hola! Soy tu asistente de IA para Revit

Soy mucho más que un bot básico. Puedo:

🧠 **Conversar contigo naturalmente** sobre tu proyecto
💡 **Entender lo que realmente necesitas** y darte consejos inteligentes
🏗️ **Ayudarte con Revit** de forma conversacional y natural
🎯 **Aprender de nuestras conversaciones** para darte mejores respuestas

💬 **Prueba hablarme normalmente:**
• "Hola, ¿cómo estás?"
• "¿Puedes ayudarme con mi proyecto de Revit?"
• "Estoy teniendo problemas con los muros"
• "¿Qué opinas de este diseño?"

🎯 ¡Vamos a conversar! Soy tu asistente de IA personal para arquitectura."""
        await update.message.reply_text(welcome_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """📚 ¿Cómo puedo ayudarte?

🗣️ **Conversa conmigo naturalmente:**

💬 **Ejemplos de conversación:**
• "Hola, ¿podrías ayudarme con Revit?"
• "Estoy diseñando una casa, ¿qué me sugieres?"
• "¿Cómo organizo mejor mi proyecto?"
• "Tengo una duda sobre las columnas estructurales"
• "¿Qué es mejor para eficiencia energética?"

🧠 **Lo que hago:**
• Converso como un asistente humano
• Entiendo el contexto de tu proyecto
• Doy consejos inteligentes y específicos
• Te explico procesos paso a paso
• Adapto mis respuestas a tu estilo

🤖 **Uso IA avanzada** para entenderte mejor

💡 **Escribe como me hablarías a mí - ¡soy muy inteligente!**"""
        await update.message.reply_text(help_text)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        try:
            status_text = f"""🔧 Mi estado actual:

🤖 **Yo:** Estoy aquí y listo para conversar
🧠 **Mi IA:** Funcionando y procesando tu lenguaje natural
💬 **Conversación:** Fluida y contextual
🎯 **Especialización:** Revit, arquitectura y construcción

💡 **Estoy preparado para:**
• Conversar naturalmente contigo
• Entender tus necesidades específicas
• Dar consejos inteligentes para tu proyecto
• Adaptar mis respuestas a tu estilo

💬 **¿Sobre qué quieres hablar?**"""
            await update.message.reply_text(status_text)
            
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def deploy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /deploy"""
        deploy_text = """🚀 Soy tu bot de IA personal

Estoy aquí 24/7 para:
• Conversar contigo sobre tu proyecto
• Entender lo que necesitas
• Darte consejos inteligentes
• Ayudarte con Revit de forma natural

💬 **¡Empecemos a conversar!** Escribe lo que necesites."""
        await update.message.reply_text(deploy_text)
    
    async def ai_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /ai"""
        ai_text = """🧠 Mis capacidades de IA:

✅ **Entiendo lenguaje natural completo**
✅ **Contexto conversacional**
✅ **Conocimiento experto en arquitectura**
✅ **Respuestas personalizadas**
✅ **Aprendizaje de nuestras conversaciones**

💬 **¿Qué quieres que sepamos conversando?**"""
        await update.message.reply_text(ai_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes con conversación inteligente"""
        user_message = update.message.text.strip()
        
        try:
            # Procesar mensaje con IA conversacional
            response = await self.generate_conversational_response(user_message)
            
            if response:
                await update.message.reply_text(response)
                
                # Guardar comando si es relevante
                if any(word in user_message.lower() for word in ['crear', 'muro', 'puerta', 'ventana', 'columna']):
                    comando = {
                        "instruction": user_message,
                        "action": "CREATE",
                        "timestamp": datetime.now().isoformat(),
                        "usuario": update.effective_user.first_name or "Usuario"
                    }
                    await self.guardar_comando(comando)
            else:
                await update.message.reply_text("🤔 Hmm, ¿podrías ser más específico? Estoy aquí para ayudarte con tu proyecto.")
                
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            await update.message.reply_text("🤖 Tuve un pequeño problema, pero estoy aquí para ayudarte. ¿Sobre qué quieres conversar?")
    
    async def generate_conversational_response(self, message: str) -> str:
        """Generar respuesta conversacional inteligente"""
        
        # Si tenemos Hugging Face, usarlo
        if self.hf_token:
            try:
                return await self.call_huggingface(message)
            except Exception as e:
                logger.warning(f"Hugging Face failed: {e}")
        
        # Si tenemos OpenRouter, usarlo
        if self.openrouter_key:
            try:
                return await self.call_openrouter(message)
            except Exception as e:
                logger.warning(f"OpenRouter failed: {e}")
        
        # Fallback conversacional inteligente
        return self.generate_smart_response(message)
    
    async def call_huggingface(self, message: str) -> str:
        """Llamar a Hugging Face API"""
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": message,
            "parameters": {
                "max_length": 500,
                "temperature": 0.8,
                "do_sample": True,
                "top_p": 0.9
            },
            "model": "microsoft/DialoGPT-medium"
        }
        
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result and len(result) > 0:
                return result[0].get('generated_text', '').replace(message, '').strip()
        
        raise Exception("No response from Hugging Face")
    
    async def call_openrouter(self, message: str) -> str:
        """Llamar a OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ia-en-rvt.railway.app",
            "X-Title": "IA-EN-RVT Bot"
        }
        
        payload = {
            "model": "meta-llama/llama-3.2-3b-instruct:free",
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un asistente de IA conversacional y experto en Revit y arquitectura. Responde de forma natural, amigable y útil. Tienes conocimiento profundo sobre construcción, diseño arquitectónico y uso de software BIM."
                },
                {
                    "role": "user", 
                    "content": message
                }
            ],
            "max_tokens": 400,
            "temperature": 0.8
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result and 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
        
        raise Exception("No response from OpenRouter")
    
    def generate_smart_response(self, message: str) -> str:
        """Generar respuesta inteligente conversacional"""
        message_lower = message.lower()
        
        # Saludo natural
        if any(word in message_lower for word in ['hola', 'buenos', 'buenas', 'saludos']):
            return """¡Hola! 😊 Me da mucho gusto conocerte. 

Soy tu asistente de IA para Revit y arquitectura. Estoy aquí para conversar contigo sobre tu proyecto y ayudarte de la manera más natural posible.

💬 **¿En qué puedo ayudarte hoy?** Puedes contarme sobre tu proyecto, hacer preguntas sobre Revit, o simplemente platicar sobre arquitectura. ¡Soy muy bueno conversando!"""
        
        # Preguntas sobre Revit
        elif any(word in message_lower for word in ['revit', 'software', 'programa']):
            return """¡Ah, Revit! 🎯 Es mi especialidad. Puedo ayudarte con:

🏗️ **Elementos arquitectónicos**: Muros, puertas, ventanas, columnas
📊 **Análisis de modelos**: Detectar problemas, optimizar diseño
📋 **Organización**: Niveles, familias, vistas, coordinación
💡 **Mejores prácticas**: Técnicas profesionales, eficiencia

💬 **¿Qué específicamente quieres hacer en Revit?** Puedes ser tan específico como quieras, ¡entiendo perfectamente el software!"""
        
        # Proyectos de construcción
        elif any(word in message_lower for word in ['proyecto', 'construcción', 'edificio', 'casa']):
            return """¡Me encanta hablar de proyectos! 🏢 

Cada proyecto tiene sus propios desafíos y posibilidades. Puedo ayudarte con:

📐 **Diseño**: Distribución, espacios, circulación
🔧 **Técnica**: Estructura, instalaciones, materiales
📊 **Análisis**: Eficiencia, costos, sostenibilidad
🎯 **Organización**: Fases, coordinación, documentación

💬 **¿Cómo va tu proyecto?** ¿En qué etapa estás? Me encanta escuchar sobre las ideas y desafíos de cada proyecto."""
        
        # Preguntas técnicas
        elif any(word in message_lower for word in ['cómo', 'qué', 'por qué', 'dónde']):
            return """¡Excelente pregunta! 🤔 Me gusta cuando alguien quiere entender los detalles técnicos.

📚 **Puedo explicarte paso a paso** cualquier proceso de Revit o arquitectura.

🔍 **¿Podrías ser más específico?** Por ejemplo:
• ¿Sobre qué elemento específico?
• ¿En qué parte del proceso?
• ¿Hay algo particular que te está costando trabajo?

💡 **Tengo mucha experiencia** ayudando con estos temas, así que seguro puedo darte una respuesta útil y clara."""
        
        # Problemas o dificultades
        elif any(word in message_lower for word in ['problema', 'error', 'dificultad', 'no funciona', 'no puedo']):
            return """Entiendo que estés teniendo dificultades. 🤗 No te preocupes, esos momentos son normales en cualquier proyecto.

🔧 **Vamos a solucionarlo juntos:**

1. **Cuéntame exactamente** qué está pasando
2. **¿En qué paso** te atascaste?
3. **¿Has intentado** alguna solución?

💡 **Con años de experiencia**, he visto casi todos los problemas posibles en Revit. Seguro podemos encontrar una solución que funcione para ti.

💬 **¿Qué está pasando exactamente?**"""
        
        # Conversación general
        else:
            responses = [
                """Interesante lo que me comentas. 🧠 Me gusta cuando la gente piensa creativamente sobre sus proyectos.

💬 **¿Podrías contarme más detalles?** Siempre aprendo algo nuevo cuando converso con personas que están trabajando en proyectos reales.

🎯 **¿Hay algo específico** en lo que pueda ayudarte ahora?""",
                
                """Me parece fascinante. 😄 Siempre me emociona escuchar sobre los retos y ideas que tienen los profesionales.

🏗️ **Como experto en IA para arquitectura**, puedo ayudarte desde múltiples ángulos.

💬 **¿Qué más te gustaría que sepamos conversando?**""",
                
                """¡Eso suena genial! 🚀 Me encanta cuando las personas tienen visión clara de lo que quieren lograr.

📊 **Puedo ayudarte a:**
• Evaluar la viabilidad técnica
• Sugerir mejoras o alternativas
• Optimizar el diseño
• Planificar la implementación

💬 **¿En qué aspecto específico** te gustaría que nos enfoquemos?"""
            ]
            
            import random
            return random.choice(responses)
    
    async def guardar_comando(self, comando: Dict[str, Any]):
        """Guardar comando en archivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.command_path), exist_ok=True)
            
            with open(self.command_path, 'w', encoding='utf-8') as f:
                json.dump(comando, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Comando guardado: {comando}")
            
        except Exception as e:
            logger.error(f"Error guardando comando: {e}")
    
    def run(self):
        """Ejecutar el bot"""
        logger.info("🤖 Iniciando Bot IA-RVT Conversacional Inteligente...")
        logger.info(f"Token: {self.token[:20]}...")
        logger.info(f"Hugging Face: {'🟢 Configurado' if self.hf_token else '❌ No configurado'}")
        logger.info(f"OpenRouter: {'🟢 Configurado' if self.openrouter_key else '❌ No configurado'}")
        logger.info("💬 Bot conversacional inteligente activado")
        
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error ejecutando bot: {e}")

if __name__ == "__main__":
    bot = IA_RVT_Conversational_Bot()
    bot.run()