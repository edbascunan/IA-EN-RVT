# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Principal Zuko
===================================

Bot de Telegram con IA avanzada para Revit
Autor: Eduardo Bascuñán
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any
import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

class ZukoBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.command_path = os.getenv('COMMAND_PATH', 'C:\\edbascunan\\IA-EN-RVT\\backend_ai\\shared\\command_out.json')
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        # Inicializar aplicación
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configurar handlers del bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("revit", self.revit_command))
        self.app.add_handler(CommandHandler("crear_muro", self.crear_muro_command))
        self.app.add_handler(CommandHandler("analizar", self.analizar_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_text = """
🏗️ *IA-EN-RVT 2026 - Bot Zuko* 🤖

¡Bienvenido al asistente de IA para Revit!

Comandos disponibles:
• /start - Iniciar bot
• /help - Mostrar ayuda
• /status - Estado del sistema
• /revit - Enviar comando a Revit
• /crear_muro - Crear muro en Revit
• /analizar - Analizar modelo Revit

💬 Simplemente escribe tu mensaje para conversar con IA.
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
📚 *Manual de Comandos - Bot Zuko*

🏗️ *Comandos de Revit:*
• `/revit [comando]` - Enviar comando a Revit
• `/crear_muro inicio_x inicio_y fin_x fin_y altura` - Crear muro
• `/analizar` - Analizar modelo actual

🤖 *Comandos de IA:*
• `/status` - Verificar estado del sistema
• Mensaje directo - Conversar con IA

📋 *Ejemplos:*
• `/crear_muro 0 0 5 0 3.5`
• `/revit CREATE Wall`
• `Analiza este plano`

El bot procesará tu solicitud y la ejecutará en Revit.
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        status = {
            "bot": "🟢 Activo",
            "revit": "🟡 Conectado" if os.path.exists(self.command_path) else "🔴 Desconectado",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "IA-EN-RVT 2026"
        }
        
        status_text = f"""
🔧 *Estado del Sistema*

Bot: {status['bot']}
Revit: {status['revit']}
Timestamp: {status['timestamp']}
Versión: {status['version']}

{'-' * 30}
        """
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def revit_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enviar comando personalizado a Revit"""
        if not context.args:
            await update.message.reply_text("❌ Uso: /revit [comando JSON]")
            return
        
        try:
            # Crear comando JSON
            comando = {
                "accion": "CREATE",
                "elemento": "Wall",
                "payload": {
                    "inicio": {"x": 0, "y": 0},
                    "fin": {"x": 3, "y": 0},
                    "altura_m": 3.0
                },
                "timestamp": datetime.now().isoformat(),
                "estado": "PENDIENTE"
            }
            
            # Guardar comando
            await self.guardar_comando(comando)
            
            await update.message.reply_text(
                f"✅ Comando enviado a Revit:\n```json\n{json.dumps(comando, indent=2)}\n```",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error enviando comando a Revit: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def crear_muro_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Crear muro con parámetros específicos"""
        if len(context.args) != 4:
            await update.message.reply_text(
                "❌ Uso: /crear_muro inicio_x inicio_y fin_x fin_y altura\n"
                "Ejemplo: /crear_muro 0 0 5 0 3.5"
            )
            return
        
        try:
            inicio_x, inicio_y, fin_x, fin_y = map(float, context.args[:4])
            altura = float(context.args[4]) if len(context.args) > 4 else 3.0
            
            comando = {
                "accion": "CREATE",
                "elemento": "Wall",
                "payload": {
                    "inicio": {"x": inicio_x, "y": inicio_y},
                    "fin": {"x": fin_x, "y": fin_y},
                    "altura_m": altura
                },
                "timestamp": datetime.now().isoformat(),
                "estado": "PENDIENTE"
            }
            
            await self.guardar_comando(comando)
            
            await update.message.reply_text(
                f"🧱 Muro creado:\n"
                f"Inicio: ({inicio_x}, {inicio_y})\n"
                f"Fin: ({fin_x}, {fin_y})\n"
                f"Altura: {altura}m\n\n"
                f"✅ Comando enviado a Revit"
            )
            
        except ValueError:
            await update.message.reply_text("❌ Error: Coordenadas inválidas")
        except Exception as e:
            logger.error(f"Error creando muro: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def analizar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Analizar modelo de Revit"""
        comando = {
            "accion": "ANALYZE",
            "elemento": "Model",
            "payload": {},
            "timestamp": datetime.now().isoformat(),
            "estado": "PENDIENTE"
        }
        
        await self.guardar_comando(comando)
        await update.message.reply_text("🔍 Analizando modelo Revit... ✅ Comando enviado")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes de texto"""
        user_message = update.message.text
        
        # Respuesta simple de IA
        if any(word in user_message.lower() for word in ['hola', 'hello', 'buenas']):
            response = "¡Hola! Soy Zuko, tu asistente de IA para Revit. ¿En qué puedo ayudarte?"
        elif 'muro' in user_message.lower():
            response = "Para crear un muro usa: /crear_muro inicio_x inicio_y fin_x fin_y altura\nEjemplo: /crear_muro 0 0 5 0 3.5"
        elif 'revit' in user_message.lower():
            response = "Puedo ayudarte con Revit. Usa /help para ver todos los comandos disponibles."
        else:
            response = "🤖 ¡Hola! Soy Zuko, el bot de IA para Revit.\n\nUsa /help para ver comandos disponibles o /status para verificar el sistema."
        
        await update.message.reply_text(response)
    
    async def guardar_comando(self, comando: Dict[str, Any]):
        """Guardar comando en archivo JSON"""
        try:
            # Asegurar directorio existe
            os.makedirs(os.path.dirname(self.command_path), exist_ok=True)
            
            with open(self.command_path, 'w', encoding='utf-8') as f:
                json.dump(comando, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Comando guardado: {comando}")
            
        except Exception as e:
            logger.error(f"Error guardando comando: {e}")
            raise
    
    def run(self):
        """Ejecutar el bot"""
        logger.info("🤖 Iniciando Bot Zuko...")
        logger.info(f"Token: {self.token[:20]}...")
        logger.info(f"Comando path: {self.command_path}")
        
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error ejecutando bot: {e}")

if __name__ == "__main__":
    bot = ZukoBot()
    bot.run()