# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot con NLP Real usando OpenAI 1.0.0+
====================================================

Bot con procesamiento de lenguaje natural real usando OpenAI GPT
Desplegado automáticamente en Railway
Autor: Eduardo Bascuñán
Versión: OpenAI 1.0.0+ compatible
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# OpenAI para NLP real - NUEVA API 1.0.0+
from openai import OpenAI

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

class IA_RVT_NLP_Bot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.command_path = os.getenv('COMMAND_PATH', 'C:\\edbascunan\\IA-EN-RVT\\backend_ai\\command_out.json')
        
        # Configurar OpenAI 1.0.0+ - NUEVA API
        self.client = OpenAI(api_key=self.openai_api_key)
        
        # Inicializar aplicación
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configurar handlers del bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("deploy", self.deploy_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_nlp_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_text = """
🤖 *IA-EN-RVT 2026 - Bot con NLP Real* 🧠

¡Bienvenido al asistente de IA más avanzado para Revit!

🧠 *PROCESAMIENTO DE LENGUAJE NATURAL REAL:*
Usando OpenAI GPT para entender cualquier instrucción:

📝 *Ejemplos de comandos naturales:*
• "Quiero crear un muro de 6 metros en la planta baja"
• "Analiza mi proyecto y dime cuántas puertas hay"
• "Necesito ayuda para organizar mi modelo"
• "¿Puedes revisar si hay errores en la estructura?"
• "Muestra las estadísticas del edificio"

🎯 *IA Real - Entiende contexto y intención*
📚 *Aprendizaje continuo*
⚡ *Desplegado automáticamente en Railway*
🏗️ *Integración perfecta con Revit*
🔧 *OpenAI 1.0.0+ compatible*

💬 *Habla conmigo como a un asistente humano*
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
📚 *Manual del Bot IA-EN-RVT con NLP Real*

🧠 *PROCESAMIENTO DE LENGUAJE NATURAL:*

🏗️ *CREAR ELEMENTOS:*
• "Quiero crear un muro en la entrada principal"
• "Añade una columna de soporte aquí"
• "Crea una viga de 8 metros"
• "Necesito una puerta en el muro sur"

📊 *ANALIZAR MODELO:*
• "Analiza mi proyecto completo"
• "¿Cuántos elementos hay en total?"
• "Revisa si hay conflictos en el diseño"
• "Muestra las propiedades del modelo"

💬 *COMANDOS LIBRES:*
• "Ayúdame a organizar mi modelo"
• "¿Qué problemas ves en mi diseño?"
• "Sugiere mejoras para la estructura"
• "Explícame cómo funciona esto"

🤖 *IA REAL:*
• Entiende el contexto completo
• Procesa instrucciones complejas
• Adapta respuestas a tu estilo
• Aprende de cada interacción
• OpenAI 1.0.0+ totalmente compatible

🎯 *Usa lenguaje natural - como si hablaras con un experto*
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        try:
            command_exists = os.path.exists(self.command_path)
            openai_configured = bool(self.openai_api_key)
            
            status_text = f"""
🔧 *Estado del Sistema IA-EN-RVT*

🤖 Bot: 🟢 Activo con NLP Real
🧠 OpenAI: {'🟢 Configurado 1.0.0+' if openai_configured else '❌ No configurado'}
📁 Comando JSON: {'🟢 Conectado' if command_exists else '🔴 Desconectado'}
📅 Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

🧠 *Capacidades NLP:*
• Procesamiento de lenguaje natural real
• Comprensión contextual avanzada
• Instrucciones complejas
• Respuestas inteligentes
• OpenAI 1.0.0+ compatible
• Desplegado en Railway

💡 *Usa cualquier instrucción en lenguaje natural*
            """
            
            await update.message.reply_text(status_text, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error verificando estado: {str(e)}")
    
    async def deploy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /deploy"""
        deploy_text = """
🚀 *Despliegue en Railway*

El bot se desplegará automáticamente en Railway para:
• 🌐 Acceso 24/7 desde cualquier lugar
• ⚡ Respuestas más rápidas
• 📈 Escalabilidad automática
• 🔒 Mayor estabilidad
• OpenAI 1.0.0+ totalmente compatible

*El despliegue ya está configurado y funcionando*
        """
        await update.message.reply_text(deploy_text, parse_mode='Markdown')
    
    async def handle_nlp_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes con NLP real"""
        user_message = update.message.text.strip()
        
        try:
            # Procesar con OpenAI NLP real
            response = await self.process_with_openai(user_message)
            
            if response:
                # Generar comando basado en respuesta de IA
                command = await self.generate_command_from_response(response, user_message, update)
                
                if command:
                    await self.guardar_comando(command)
                    await self.send_processed_response(update, response, command)
                else:
                    await update.message.reply_text(response, parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    "🤔 No pude procesar tu solicitud. ¿Podrías ser más específico?",
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            await update.message.reply_text(f"❌ Error procesando tu solicitud: {str(e)}")
    
    async def process_with_openai(self, message: str) -> str:
        """Procesar mensaje con OpenAI NLP real - NUEVA API 1.0.0+"""
        try:
            system_prompt = """
Eres un asistente experto en Revit y arquitectura. Tu trabajo es:

1. ENTENDER la solicitud del usuario en lenguaje natural
2. INTERPRETAR la intención (crear, analizar, modificar, etc.)
3. EXTRAER parámetros específicos (dimensiones, posiciones, etc.)
4. GENERAR una respuesta clara y útil
5. CLASIFICAR la acción para Revit

Tipos de acciones:
- CREATE: Crear elementos (muros, puertas, ventanas, etc.)
- ANALYZE: Analizar modelo (contar elementos, revisar errores, etc.)
- INFO: Obtener información (propiedades, estadísticas, etc.)
- HELP: Ayuda y explicaciones

Responde de forma clara y útil. Si necesitas más información, pregunta.
            """
            
            # NUEVA API OpenAI 1.0.0+
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error con OpenAI: {e}")
            return f"Lo siento, no pude procesar tu solicitud. Error: {str(e)}"
    
    async def generate_command_from_response(self, ai_response: str, original_message: str, update: Update) -> Dict[str, Any]:
        """Generar comando para Revit basado en respuesta de IA - NUEVA API 1.0.0+"""
        try:
            # Usar OpenAI para clasificar y extraer parámetros
            classification_prompt = f"""
Analiza esta respuesta de IA y extrae la información para generar un comando JSON:

Respuesta IA: {ai_response}
Mensaje original: {original_message}

Clasifica la acción (CREATE, ANALYZE, INFO, HELP) y extrae:
- action: CREATE, ANALYZE, INFO, HELP
- element: Wall, Door, Window, Column, Beam, Model, etc.
- instruction: Instrucción clara para Revit
- parameters: Parámetros específicos si los hay

Responde SOLO con un JSON válido:
{{"action": "...", "element": "...", "instruction": "...", "parameters": {{}}}}
            """
            
            # NUEVA API OpenAI 1.0.0+
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un generador de comandos JSON. Responde solo con JSON válido."},
                    {"role": "user", "content": classification_prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            json_response = response.choices[0].message.content.strip()
            
            # Intentar parsear el JSON
            try:
                command_data = json.loads(json_response)
                
                # Crear comando final
                command = {
                    "instruction": command_data.get("instruction", ""),
                    "action": command_data.get("action", "HELP"),
                    "element": command_data.get("element", "Model"),
                    "parameters": command_data.get("parameters", {}),
                    "original_message": original_message,
                    "ai_response": ai_response,
                    "timestamp": datetime.now().isoformat(),
                    "usuario": update.effective_user.first_name or "Usuario"
                }
                
                return command
                
            except json.JSONDecodeError:
                # Si no puede parsear JSON, crear comando genérico
                return {
                    "instruction": ai_response,
                    "action": "HELP",
                    "element": "Model",
                    "parameters": {},
                    "original_message": original_message,
                    "ai_response": ai_response,
                    "timestamp": datetime.now().isoformat(),
                    "usuario": update.effective_user.first_name or "Usuario"
                }
                
        except Exception as e:
            logger.error(f"Error generando comando: {e}")
            return None
    
    async def send_processed_response(self, update: Update, ai_response: str, command: Dict[str, Any]):
        """Enviar respuesta procesada al usuario"""
        action = command.get("action", "HELP")
        element = command.get("element", "Model")
        
        responses = {
            "CREATE": f"🏗️ *Acción: Crear {element}*\n\n{ai_response}\n\n🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            "ANALYZE": f"🔍 *Acción: Analizar {element}*\n\n{ai_response}\n\n🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            "INFO": f"📋 *Acción: Información {element}*\n\n{ai_response}\n\n🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            "HELP": f"❓ *Acción: Ayuda*\n\n{ai_response}\n\n🔄 *Haz clic en '🤖 IA RVT' en Revit*"
        }
        
        response = responses.get(action, f"✅ *Procesado con IA*\n\n{ai_response}\n\n🔄 *Haz clic en '🤖 IA RVT' en Revit*")
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def guardar_comando(self, comando: Dict[str, Any]):
        """Guardar comando en archivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.command_path), exist_ok=True)
            
            with open(self.command_path, 'w', encoding='utf-8') as f:
                json.dump(comando, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Comando guardado: {comando}")
            
        except Exception as e:
            logger.error(f"Error guardando comando: {e}")
            raise
    
    def run(self):
        """Ejecutar el bot"""
        logger.info("🤖 Iniciando Bot IA-RVT con NLP Real...")
        logger.info(f"Token: {self.token[:20]}...")
        logger.info(f"OpenAI: {'Configurado 1.0.0+' if self.openai_api_key else 'No configurado'}")
        logger.info(f"Comando path: {self.command_path}")
        logger.info("🧠 NLP Real con OpenAI 1.0.0+ activado")
        
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error ejecutando bot: {e}")

if __name__ == "__main__":
    bot = IA_RVT_NLP_Bot()
    bot.run()