# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Simple con OpenRouter
==========================================

Bot simple y funcional con OpenRouter
Modelo corregido - Despliegue urgente
Autor: Eduardo Bascuñán
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class IA_RVT_Simple_Bot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.command_path = os.getenv('COMMAND_PATH', 'backend_ai/shared/command_out.json')
        
        # Configurar OpenRouter
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Modelo que funciona en OpenRouter
        self.model = "gpt-3.5-turbo"
        
        # Inicializar aplicación
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configurar handlers del bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_text = """🤖 IA-EN-RVT 2026 - Bot con OpenRouter

¡Bienvenido al asistente de IA para Revit!

🧠 Procesamiento de lenguaje natural real usando OpenRouter

💬 Escribe cualquier mensaje y te ayudaré con tu proyecto de Revit.

💡 Usa comandos: /start, /help, /status"""
        await update.message.reply_text(welcome_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """📚 Manual del Bot IA-EN-RVT

🧠 PROCESAMIENTO NLP:

🏗️ CREAR ELEMENTOS:
• "Quiero crear un muro de 6 metros"
• "Añade una columna aquí"
• "Crea una puerta en el muro"

📊 ANALIZAR MODELO:
• "Analiza mi proyecto"
• "¿Cuántos elementos hay?"
• "Revisa errores en el diseño"

💬 COMANDOS LIBRES:
• "Ayúdame a organizar mi modelo"
• "¿Qué problemas ves?"
• "Sugiere mejoras"

🤖 OpenRouter ventajas:
• Modelos gratuitos
• Sin límites de cuota
• Múltiples proveedores

💬 Habla naturalmente - como con un experto"""
        await update.message.reply_text(help_text)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        try:
            openrouter_configured = bool(self.api_key)
            
            status_text = f"""🔧 Estado del Sistema IA-EN-RVT

🤖 Bot: Activo con OpenRouter
🌐 OpenRouter: {'Configurado' if openrouter_configured else 'No configurado'}
📅 Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

🌐 Capacidades:
• NLP real con OpenRouter
• Modelos disponibles
• Sin límites de cuota
• Desplegado en Railway
• Modelo: {self.model}

💡 Escribe cualquier instrucción en lenguaje natural"""
            await update.message.reply_text(status_text)
            
        except Exception as e:
            await update.message.reply_text(f"Error verificando estado: {str(e)}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes con OpenRouter"""
        user_message = update.message.text.strip()
        
        try:
            # Procesar con OpenRouter
            response = await self.process_with_openrouter(user_message)
            
            if response:
                await update.message.reply_text(response)
            else:
                await update.message.reply_text("No pude procesar tu solicitud. ¿Podrías ser más específico?")
                
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def process_with_openrouter(self, message: str) -> str:
        """Procesar mensaje con OpenRouter"""
        try:
            system_prompt = """Eres un asistente experto en Revit y arquitectura. 
Ayuda al usuario con:
1. Crear elementos (muros, puertas, ventanas, columnas)
2. Analizar modelos (contar elementos, revisar errores)
3. Organizar proyectos
4. Sugerir mejoras de diseño

Responde de forma clara y útil."""
            
            # OpenRouter API con modelo corregido
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error con OpenRouter: {e}")
            return f"Error con OpenRouter: {str(e)}"
    
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
        logger.info("🤖 Iniciando Bot IA-RVT Simple con OpenRouter...")
        logger.info(f"Token: {self.token[:20]}...")
        logger.info(f"OpenRouter: {'Configurado' if self.api_key else 'No configurado'}")
        logger.info(f"Modelo: {self.model}")
        
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error ejecutando bot: {e}")

if __name__ == "__main__":
    bot = IA_RVT_Simple_Bot()
    bot.run()