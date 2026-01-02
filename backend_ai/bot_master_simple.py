#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 IA-EN-RVT 2026 - Bot Master Simplificado
==========================================

Sistema BIM Autónomo con Inteligencia Artificial para Revit 2026
Versión simplificada y funcional

Autor: Eduardo Bascuñán
Fecha: 01 de enero de 2026
Versión: 2.0.0 - Simplificado y Funcional
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class IARVTBotSimple:
    """Bot Simplificado del Sistema IA-EN-RVT"""
    
    def __init__(self, token: str):
        self.token = token
        self.application = None
        self.commands_processed = 0
        
    def get_system_prompt(self) -> str:
        """Obtener prompt del sistema para IA"""
        return """
Eres IA-EN-RVT, un asistente especializado en BIM y Revit 2026.

Tu función es ayudar con:
- Modelado BIM y diseño arquitectónico
- Comandos para Revit 2026
- Análisis de modelos estructurales
- Automatización de procesos BIM
- Interpretación de comandos de lenguaje natural

Siempre responde de forma profesional y técnica, enfocándote en soluciones BIM prácticas.
        """
    
    async def safe_reply(self, update: Update, message: str):
        """Enviar mensaje de forma segura"""
        try:
            await update.message.reply_text(message)
        except Exception as e:
            logger.error(f"Error enviando mensaje: {e}")
            await update.message.reply_text("Error al enviar respuesta. Por favor, intenta de nuevo.")
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_message = f"""
🤖 ¡Bienvenido al Sistema IA-EN-RVT 2026!

🏗️ Sistema BIM Autónomo con IA para Revit 2026

✨ Características:
• Control de Revit mediante lenguaje natural
• Análisis de modelos BIM automático
• Comandos por voz, texto, imágenes y videos
• Niveles de autonomía configurables

📱 Comandos Disponibles:
/start - Iniciar sistema
/status - Estado del sistema
/help - Ayuda detallada

💬 Ejemplos de Comandos:
• "Crea un muro de 3 metros en nivel 1"
• "Analiza el modelo actual"
• "Genera reporte de materiales"

¿Listo para revolucionar tu workflow BIM? 🚀
        """
        await self.safe_reply(update, welcome_message)
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_message = """
📚 Ayuda Completa - IA-EN-RVT 2026

📱 Comandos Principales:
/start - Iniciar sistema
/status - Ver estado del sistema
/help - Esta ayuda

🗣️ Comandos de Voz:
Envía mensajes de voz con comandos como:
• "Crea estructura de hormigón"
• "Analiza conflictos en el modelo"
• "Genera planos de secciones"

📷 Análisis de Imágenes:
Envía imágenes de planos o modelos para:
• Detectar elementos BIM
• Sugerir mejoras
• Identificar problemas

⚡ Powered by Múltiples IA:
• GROK (x.ai) - API gratuita
• MINIMAX - API china gratuita  
• CLAUDE - Anthropic Premium
• ChatGPT - OpenAI
• DEEPSEEK - IA principal avanzada
• OLLAMA - Modelos locales gratuitos

¡El futuro del BIM está aquí! 🚀
        """
        await self.safe_reply(update, help_message)
        
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        status_message = f"""
📊 Estado del Sistema IA-EN-RVT 2026

🟢 Estado: Operativo
🤖 Bot: Activo
📈 Comandos procesados: {self.commands_processed}
🕐 Hora actual: {current_time}

⚡ Sistema listo para procesar comandos BIM 🚀
        """
        await self.safe_reply(update, status_message)
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejador de mensajes de usuario"""
        self.commands_processed += 1
        
        user_message = update.message.text
        user_name = update.message.from_user.first_name or "Usuario"
        
        logger.info(f"Mensaje recibido de {user_name}: {user_message[:100]}")
        
        # Respuesta básica del bot
        response_message = f"""
🤖 Hola {user_name}!

He recibido tu mensaje: "{user_message}"

Como IA-EN-RVT, estoy aquí para ayudarte con:
• Modelado BIM y diseño arquitectónico
• Comandos para Revit 2026
• Análisis de modelos estructurales
• Automatización de procesos BIM

Actualmente el sistema está en modo básico.
Próximamente se integrarán múltiples proveedores de IA.

¿Hay algo específico en lo que pueda ayudarte? 🚀
        """
        
        await self.safe_reply(update, response_message)
    
    def setup_handlers(self):
        """Configurar manejadores de comandos"""
        if not self.application:
            self.application = Application.builder().token(self.token).build()
            
            # Registrar comandos
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("status", self.status_command))
            
            # Registrar manejador de mensajes
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
    
    def run(self):
        """Ejecutar el bot"""
        try:
            self.setup_handlers()
            
            logger.info("🤖 Iniciando IA-EN-RVT Bot...")
            logger.info(f"📱 Token configurado: {self.token[:20]}...")
            
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            logger.error(f"❌ Error iniciando el bot: {e}")
            raise

def main():
    """Función principal"""
    # Obtener token del bot
    token = os.getenv('TELEGRAM_TOKEN')
    
    if not token:
        logger.error("❌ TELEGRAM_TOKEN no encontrado en variables de entorno")
        logger.info("💡 Configura el token en el archivo .env")
        return
    
    # Crear y ejecutar bot
    try:
        bot = IARVTBotSimple(token)
        bot.run()
    except KeyboardInterrupt:
        logger.info("👋 Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")

if __name__ == "__main__":
    main()