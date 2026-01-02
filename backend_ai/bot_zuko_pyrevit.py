# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Principal Zuko para PYREVIT
===============================================

Bot de Telegram optimizado para PYREVIT con IA avanzada
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

class ZukoBotPYREVIT:
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
        self.app.add_handler(CommandHandler("pyrevit", self.pyrevit_command))
        self.app.add_handler(CommandHandler("muro_rapido", self.muro_rapido_command))
        self.app.add_handler(CommandHandler("instalar", self.instalar_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_text = """
🏗️ *IA-EN-RVT 2026 - Bot Zuko PYREVIT* 🤖

¡Bienvenido al asistente de IA avanzado para Revit con PYREVIT!

🔧 *Comandos PYREVIT:*
• `/pyrevit` - Verificar conexión PYREVIT
• `/crear_muro` - Crear muro en Revit
• `/muro_rapido` - Muro de prueba rápido
• `/analizar` - Analizar modelo

📱 *Comandos del Bot:*
• `/start` - Iniciar bot
• `/help` - Mostrar ayuda
• `/status` - Estado del sistema
• `/instalar` - Instrucciones de instalación

💬 Escribe tu mensaje para conversar con IA.
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
📚 *Manual Completo - Bot Zuko PYREVIT*

🏗️ *Comandos PYREVIT:*
• `/pyrevit` - Verificar conexión con PYREVIT
• `/crear_muro inicio_x inicio_y fin_x fin_y altura` - Crear muro personalizado
• `/muro_rapido` - Crear muro de prueba (4m x 3.2m)
• `/analizar` - Analizar elementos del modelo

🔧 *Instalación PYREVIT:*
• `/instalar` - Ver instrucciones de instalación

📋 *Ejemplos de uso:*
• `/crear_muro 0 0 5 0 3.5` - Muro de 5m x 3.5m
• `/muro_rapido` - Prueba rápida
• `/analizar` - Ver estadísticas del modelo

🤖 *Respuestas de IA disponibles*
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        pyrevit_conectado = os.path.exists(self.command_path)
        estado_pyrevit = "🟢 Conectado" if pyrevit_conectado else "🔴 Desconectado"
        
        status = {
            "bot": "🟢 Activo",
            "pyrevit": estado_pyrevit,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "IA-EN-RVT 2026 PYREVIT"
        }
        
        status_text = f"""
🔧 *Estado del Sistema*

Bot: {status['bot']}
PYREVIT: {status['pyrevit']}
Timestamp: {status['timestamp']}
Versión: {status['version']}

💡 *Para usar PYREVIT:*
1. Instalar extensión con `/instalar`
2. Abrir Revit 2026
3. Usar comandos del bot
4. Hacer clic en "Zuko" en Revit
        """
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def pyrevit_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /pyrevit - Verificar PYREVIT"""
        if os.path.exists(self.command_path):
            await update.message.reply_text(
                "✅ *PYREVIT CONECTADO*\n\n"
                "La extensión está instalada y funcionando.\n"
                "Usa los comandos para enviar tareas a Revit.\n\n"
                "🎯 *Comandos disponibles:*\n"
                "• `/crear_muro` - Crear muro personalizado\n"
                "• `/muro_rapido` - Prueba rápida\n"
                "• `/analizar` - Analizar modelo",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "❌ *PYREVIT NO CONECTADO*\n\n"
                "Instala la extensión primero:\n"
                "1. Ejecutar `/instalar`\n"
                "2. Reiniciar Revit\n"
                "3. Recargar extensiones PYREVIT",
                parse_mode='Markdown'
            )
    
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
            
            comando = {
                "accion": "CREATE",
                "elemento": "Wall",
                "payload": {
                    "inicio": {"x": inicio_x, "y": inicio_y},
                    "fin": {"x": fin_x, "y": fin_y},
                    "altura_m": altura
                },
                "timestamp": datetime.now().isoformat(),
                "estado": "PENDIENTE",
                "usuario": update.effective_user.first_name or "Usuario",
                "fuente": "telegram_bot",
                "descripcion": f"Muro personalizado: ({inicio_x},{inicio_y}) → ({fin_x},{fin_y}) - {altura}m"
            }
            
            await self.guardar_comando(comando)
            
            await update.message.reply_text(
                f"🧱 *MURO PERSONALIZADO CREADO*\n\n"
                f"📍 *Inicio:* ({inicio_x}, {inicio_y})\n"
                f"📍 *Fin:* ({fin_x}, {fin_y})\n"
                f"📏 *Altura:* {altura}m\n\n"
                f"✅ *Comando enviado a PYREVIT*\n"
                f"🔄 *Abre Revit y haz clic en 'Zuko'*",
                parse_mode='Markdown'
            )
            
        except ValueError:
            await update.message.reply_text("❌ Error: Coordenadas inválidas")
        except Exception as e:
            logger.error(f"Error creando muro: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def muro_rapido_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muro rápido de prueba"""
        comando = {
            "accion": "CREATE",
            "elemento": "Wall",
            "payload": {
                "inicio": {"x": 0, "y": 0},
                "fin": {"x": 4, "y": 0},
                "altura_m": 3.2
            },
            "timestamp": datetime.now().isoformat(),
            "estado": "PENDIENTE",
            "usuario": update.effective_user.first_name or "Usuario",
            "fuente": "telegram_bot",
            "descripcion": "Muro de prueba rápida - 4m x 3.2m"
        }
        
        await self.guardar_comando(comando)
        await update.message.reply_text(
            "🚀 *MURO RÁPIDO PREPARADO*\n\n"
            "📏 *Dimensiones:* 4m x 3.2m\n"
            "📍 *Posición:* Desde origen (0,0)\n\n"
            "✅ *Comando enviado a PYREVIT*\n"
            "🔄 *Haz clic en 'Zuko' en Revit*",
            parse_mode='Markdown'
        )
    
    async def analizar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Analizar modelo de Revit"""
        comando = {
            "accion": "ANALYZE",
            "elemento": "Model",
            "payload": {},
            "timestamp": datetime.now().isoformat(),
            "estado": "PENDIENTE",
            "usuario": update.effective_user.first_name or "Usuario",
            "fuente": "telegram_bot",
            "descripcion": "Análisis del modelo actual"
        }
        
        await self.guardar_comando(comando)
        await update.message.reply_text(
            "🔍 *ANÁLISIS PREPARADO*\n\n"
            "📊 *Se analizarán:*\n"
            "• Cantidad de muros\n"
            "• Niveles del proyecto\n"
            "• Puertas y ventanas\n"
            "• Elementos del modelo\n\n"
            "✅ *Comando enviado a PYREVIT*\n"
            "🔄 *Haz clic en 'Zuko' en Revit*",
            parse_mode='Markdown'
        )
    
    async def instalar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Instrucciones de instalación PYREVIT"""
        instruccion_text = """
🔧 *INSTALACIÓN PYREVIT IA-EN-RVT 2026*

📋 *Pasos de instalación:*

1️⃣ *Instalar PYREVIT:*
   • Descargar desde: github.com/eirannejad/pyRevit
   • Instalar en el sistema

2️⃣ *Instalar extensión:*
   • Ejecutar: `python instalar_pyrevit.py`
   • O copiar carpeta manualmente

3️⃣ *Configurar Revit:*
   • Abrir Revit 2026
   • PYREVIT > Extensions > Reload
   • Buscar pestaña "IaEnRvt"

4️⃣ *Conectar bot:*
   • Usar comandos del bot
   • Hacer clic en "Zuko" en Revit

💡 *¿Problemas?*
   • Verificar PYREVIT instalado
   • Reiniciar Revit
   • Usar `/status` para verificar
        """
        await update.message.reply_text(instruccion_text, parse_mode='Markdown')
    
    async def revit_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando legacy para compatibilidad"""
        await update.message.reply_text(
            "🔄 *Usa `/pyrevit` para comandos PYREVIT*\n\n"
            "Los comandos han sido actualizados para PYREVIT.\n"
            "Usa `/help` para ver todos los comandos disponibles.",
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes de texto"""
        user_message = update.message.text.lower()
        
        # Respuestas específicas para PYREVIT
        if any(word in user_message for word in ['hola', 'hello', 'buenas', 'buenos']):
            response = "¡Hola! Soy Zuko, tu asistente de IA para Revit con PYREVIT. ¿En qué puedo ayudarte? Usa /help para ver comandos."
        elif 'pyrevit' in user_message:
            response = "PYREVIT es el sistema que usamos. Usa /pyrevit para verificar conexión o /instalar para configurar."
        elif 'muro' in user_message:
            response = "Para crear muros: /crear_muro inicio_x inicio_y fin_x fin_y altura o /muro_rapido para prueba rápida."
        elif 'instalar' in user_message:
            response = "Usa /instalar para ver instrucciones de instalación de PYREVIT."
        elif 'analizar' in user_message:
            response = "Usa /analizar para obtener estadísticas del modelo actual de Revit."
        else:
            response = "🤖 ¡Hola! Soy Zuko, el bot de IA para Revit con PYREVIT.\n\nUsa /help para comandos disponibles o /status para verificar el sistema."
        
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
        logger.info("🤖 Iniciando Bot Zuko PYREVIT...")
        logger.info(f"Token: {self.token[:20]}...")
        logger.info(f"Comando path: {self.command_path}")
        
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error ejecutando bot: {e}")

if __name__ == "__main__":
    bot = ZukoBotPYREVIT()
    bot.run()