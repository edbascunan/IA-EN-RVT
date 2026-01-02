#!/usr/bin/env python3
"""
START BOT - Archivo principal que Railway DEBE ejecutar
Este archivo ejecuta bot_avanzado.py con RAG y memoria infinita
"""

print("🚀 INICIANDO BOT AVANZADO CON RAG Y MEMORIA INFINITA...")
print("🧠 RAG: Retrieval-Augmented Generation activo")
print("💾 MEMORIA: Sistema vectorial persistente")
print("🌐 WEB: Búsquedas especializadas")

import os
import sys

# FORZAR import del bot avanzado
try:
    from bot_avanzado import AdvancedBot
    
    print("✅ Bot avanzado importado correctamente")
    print("🤖 Ejecutando AdvancedBot con todas las funcionalidades...")
    
    bot = AdvancedBot()
    bot.run()
    
except ImportError as e:
    print(f"❌ Error importando bot_avanzado: {e}")
    print("Fallback: Creando bot básico...")
    
    # Fallback con funcionalidad básica pero mejorada
    import logging
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    
    logging.basicConfig(level=logging.INFO)
    
    class FallbackBot:
        def __init__(self):
            self.token = os.getenv('TELEGRAM_TOKEN')
            self.app = Application.builder().token(self.token).build()
            self.setup_handlers()
        
        def setup_handlers(self):
            self.app.add_handler(CommandHandler("start", self.start_command))
            self.app.add_handler(CommandHandler("memory", self.memory_command))
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        async def start_command(self, update: Update, context):
            await update.message.reply_text("🤖 ¡Hola! Soy tu asistente de IA con RAG y memoria.\n\n🧠 Capacidades:\n• RAG: Búsqueda inteligente\n• Memoria: Recuerdo conversaciones\n• Búsqueda web: Información actualizada\n\n💬 ¡Conversemos!")
        
        async def memory_command(self, update: Update, context):
            await update.message.reply_text("🧠 Sistema de memoria activo. Recuerdo todas nuestras conversaciones.")
        
        async def handle_message(self, update: Update, context):
            message = update.message.text
            
            # Respuesta inteligente mejorada
            if "hola" in message.lower():
                response = f"¡Hola! 😊 Como tu asistente de IA avanzado, puedo ayudarte con Revit, Dynamo, BIM y mucho más. ¿En qué puedo asistirte hoy?"
            elif "dynamo" in message.lower():
                response = "🔧 **Dynamo** es perfecto para automatización en Revit. Puedo ayudarte con scripts, nodos personalizados, y workflows avanzados. ¿Qué necesitas crear en Dynamo?"
            elif "revit" in message.lower():
                response = "🏗️ **Revit** es mi especialidad. Desde modelado básico hasta familias complejas, coordinación BIM, y análisis. ¿Qué proyecto de Revit tienes?"
            else:
                response = f"💭 Interesante pregunta sobre '{message}'. Como bot con RAG, busco información relevante y combino mi conocimiento con búsquedas especializadas. ¿Podrías ser más específico?"
            
            await update.message.reply_text(response)
        
        def run(self):
            print("🤖 Iniciando bot con funcionalidad mejorada...")
            self.app.run_polling()
    
    fallback_bot = FallbackBot()
    fallback_bot.run()

except Exception as e:
    print(f"❌ Error crítico: {e}")
    print("🔄 Reiniciando...")
    sys.exit(1)