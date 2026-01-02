# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Zuko CORREGIDO
===================================

Bot de Telegram con esquema JSON mínimo compatible con PYREVIT
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

class ZukoBotFixed:
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
        self.app.add_handler(CommandHandler("crear_muro", self.crear_muro_command))
        self.app.add_handler(CommandHandler("muro_rapido", self.muro_rapido_command))
        self.app.add_handler(CommandHandler("analizar", self.analizar_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_text = """
🏗️ *IA-EN-RVT 2026 - Bot Zuko CORREGIDO* ✅

¡Sistema corregido y funcionando!

🔧 *Comandos disponibles:*
• `/crear_muro x1 y1 x2 y2 [altura]` - Crear muro
• `/muro_rapido` - Muro de prueba
• `/analizar` - Analizar modelo
• `/status` - Estado del sistema

📝 *Ejemplo:*
`/crear_muro 0 0 5 0 3.5`

El esquema JSON ha sido corregido para PYREVIT.
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
📚 *Manual - Bot Zuko CORREGIDO*

🏗️ *Comandos:*
• `/crear_muro inicio_x inicio_y fin_x fin_y [altura]`
• `/muro_rapido` - Muro de prueba (4m x 3.2m)
• `/analizar` - Analizar elementos del modelo
• `/status` - Estado del sistema

📝 *Ejemplos:*
• `/crear_muro 0 0 5 0 3.5`
• `/crear_muro 2 1 6 3 4.0`
• `/muro_rapido`

✅ *Esquema JSON corregido para PYREVIT*
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        comando_existe = os.path.exists(self.command_path)
        estado_archivo = "🟢 Existe" if comando_existe else "🔴 No existe"
        
        status_text = f"""
🔧 *Estado del Sistema*

Bot: 🟢 Activo
Archivo comando: {estado_archivo}
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Versión: IA-EN-RVT 2026 CORREGIDO

📝 *Esquema JSON compatible con PYREVIT*
        """
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def crear_muro_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Crear muro con parámetros específicos"""
        if len(context.args) < 4:
            await update.message.reply_text(
                "❌ *Uso incorrecto*\n\n"
                "📋 *Uso:* `/crear_muro inicio_x inicio_y fin_x fin_y [altura]`\n\n"
                "📝 *Ejemplos:*\n"
                "• `/crear_muro 0 0 5 0 3.5`\n"
                "• `/crear_muro 2 1 6 3 4.0`\n"
                "• `/muro_rapido` (para prueba rápida)",
                parse_mode='Markdown'
            )
            return
        
        try:
            inicio_x, inicio_y, fin_x, fin_y = map(float, context.args[:4])
            altura = float(context.args[4]) if len(context.args) > 4 else 3.0
            
            # ESQUEMA JSON MINIMO COMPATIBLE CON PYREVIT
            comando = {
                "accion": "CREATE",
                "elemento": "Wall",
                "payload": {
                    "inicio": {"x": inicio_x, "y": inicio_y},
                    "fin": {"x": fin_x, "y": fin_y},
                    "altura_m": altura
                }
            }
            
            await self.guardar_comando(comando)
            
            await update.message.reply_text(
                f"🧱 *MURO CREADO* ✅\n\n"
                f"📍 *Inicio:* ({inicio_x}, {inicio_y})\n"
                f"📍 *Fin:* ({fin_x}, {fin_y})\n"
                f"📏 *Altura:* {altura}m\n\n"
                f"📝 *Esquema JSON corregido*\n"
                f"🔄 *Haz clic en 'Zuko' en Revit*",
                parse_mode='Markdown'
            )
            
        except ValueError:
            await update.message.reply_text("❌ Error: Coordenadas inválidas")
        except Exception as e:
            logger.error(f"Error creando muro: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def muro_rapido_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muro rápido de prueba"""
        # ESQUEMA JSON MINIMO
        comando = {
            "accion": "CREATE",
            "elemento": "Wall",
            "payload": {
                "inicio": {"x": 0, "y": 0},
                "fin": {"x": 4, "y": 0},
                "altura_m": 3.2
            }
        }
        
        await self.guardar_comando(comando)
        await update.message.reply_text(
            "🚀 *MURO RÁPIDO* ✅\n\n"
            "📏 *Dimensiones:* 4m x 3.2m\n"
            "📍 *Posición:* Desde origen (0,0)\n\n"
            "📝 *Esquema JSON corregido*\n"
            "🔄 *Haz clic en 'Zuko' en Revit*",
            parse_mode='Markdown'
        )
    
    async def analizar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Analizar modelo de Revit"""
        # ESQUEMA JSON MINIMO
        comando = {
            "accion": "ANALYZE",
            "elemento": "Model",
            "payload": {}
        }
        
        await self.guardar_comando(comando)
        await update.message.reply_text(
            "🔍 *ANÁLISIS PREPARADO* ✅\n\n"
            "📊 *Se analizarán elementos del modelo*\n\n"
            "📝 *Esquema JSON corregido*\n"
            "🔄 *Haz clic en 'Zuko' en Revit*",
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes de texto"""
        user_message = update.message.text.lower()
        
        if any(word in user_message for word in ['hola', 'hello', 'buenas']):
            response = "¡Hola! Soy Zuko corregido. Usa /help para ver comandos disponibles."
        elif 'muro' in user_message:
            response = "Para crear muros: /crear_muro inicio_x inicio_y fin_x fin_y altura o /muro_rapido"
        elif 'corregido' in user_message:
            response = "✅ El esquema JSON ha sido corregido para ser compatible con PYREVIT."
        else:
            response = "🤖 Bot Zuko CORREGIDO\n\nUsa /help para ver comandos disponibles."
        
        await update.message.reply_text(response)
    
    async def guardar_comando(self, comando: Dict[str, Any]):
        """Guardar comando en archivo JSON"""
        try:
            # Asegurar directorio existe
            os.makedirs(os.path.dirname(self.command_path), exist_ok=True)
            
            with open(self.command_path, 'w', encoding='utf-8') as f:
                json.dump(comando, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Comando guardado (esquema corregido): {comando}")
            
        except Exception as e:
            logger.error(f"Error guardando comando: {e}")
            raise
    
    def run(self):
        """Ejecutar el bot"""
        logger.info("🤖 Iniciando Bot Zuko CORREGIDO...")
        logger.info(f"Token: {self.token[:20]}...")
        logger.info(f"Comando path: {self.command_path}")
        logger.info("📝 Usando esquema JSON mínimo compatible con PYREVIT")
        
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error ejecutando bot: {e}")

if __name__ == "__main__":
    bot = ZukoBotFixed()
    bot.run()