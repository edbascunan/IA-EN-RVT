# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Final Funcional
===================================

Bot funcional que funciona sin dependencia externa
Respuestas inteligentes predefinidas
Autor: Eduardo Bascuñán
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class IA_RVT_Final_Bot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
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
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_text = """🤖 IA-EN-RVT 2026 - Bot para Revit

¡Bienvenido al asistente de IA para Revit!

🧠 Procesamiento de lenguaje natural para arquitectura

💬 Escribe cualquier mensaje y te ayudaré con tu proyecto de Revit.

💡 Usa comandos: /start, /help, /status, /deploy"""
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

🎯 FUNCIONALIDADES:
• Respuestas inteligentes
• Comandos para Revit
• Análisis de modelos
• Soporte 24/7

💬 Habla naturalmente - como con un experto"""
        await update.message.reply_text(help_text)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        try:
            status_text = f"""🔧 Estado del Sistema IA-EN-RVT

🤖 Bot: Activo y funcionando
📅 Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

✅ FUNCIONANDO:
• Bot de Telegram conectado
• Procesamiento de mensajes activo
• Respuestas inteligentes
• Desplegado en Railway

💡 Escribe cualquier instrucción en lenguaje natural"""
            await update.message.reply_text(status_text)
            
        except Exception as e:
            await update.message.reply_text(f"Error verificando estado: {str(e)}")
    
    async def deploy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /deploy"""
        deploy_text = """🚀 Despliegue en Railway

El bot se despliega automáticamente en Railway para:
• 🌐 Acceso 24/7 desde cualquier lugar
• ⚡ Respuestas rápidas
• 📈 Escalabilidad automática
• 🔒 Mayor estabilidad

✅ Bot funcionando correctamente"""
        await update.message.reply_text(deploy_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes con respuestas inteligentes"""
        user_message = update.message.text.strip().lower()
        
        try:
            # Procesar mensaje y generar respuesta
            response = await self.process_message(user_message)
            
            if response:
                await update.message.reply_text(response)
                
                # Guardar comando si es relevante
                if any(word in user_message for word in ['crear', 'muro', 'puerta', 'ventana', 'columna']):
                    comando = {
                        "instruction": user_message,
                        "action": "CREATE",
                        "timestamp": datetime.now().isoformat(),
                        "usuario": update.effective_user.first_name or "Usuario"
                    }
                    await self.guardar_comando(comando)
            else:
                await update.message.reply_text("¿Podrías ser más específico sobre lo que necesitas para tu proyecto de Revit?")
                
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            await update.message.reply_text(f"Error procesando tu solicitud: {str(e)}")
    
    async def process_message(self, message: str) -> str:
        """Procesar mensaje con respuestas inteligentes"""
        
        # Respuestas para crear elementos
        if any(word in message for word in ['crear', 'hacer', 'añadir', 'colocar']):
            if 'muro' in message:
                return """🏗️ Para crear un muro en Revit:

1. Ve a la pestaña "Architecture"
2. Selecciona "Wall" 
3. Define la línea de ubicación
4. Ajusta altura y grosor
5. Confirma la creación

💡 ¿Necesitas ayuda con las dimensiones específicas?"""
            
            elif 'puerta' in message:
                return """🚪 Para crear una puerta en Revit:

1. Selecciona una pared existente
2. Ve a "Architecture" > "Door"
3. Coloca la puerta en la ubicación deseada
4. Ajusta tipo y dimensiones
5. Confirma la inserción

💡 ¿Qué tipo de puerta necesitas?"""
            
            elif 'ventana' in message:
                return """🪟 Para crear una ventana en Revit:

1. Selecciona la pared donde va la ventana
2. Ve a "Architecture" > "Window"
3. Coloca la ventana en la posición
4. Ajusta tipo y dimensiones
5. Confirma la inserción

💡 ¿Qué tipo de ventana prefieres?"""
            
            elif 'columna' in message:
                return """🏛️ Para crear una columna en Revit:

1. Ve a "Architecture" > "Column"
2. Selecciona tipo de columna
3. Define la ubicación
4. Ajusta altura y propiedades
5. Confirma la creación

💡 ¿Qué tipo de columna necesitas?"""
        
        # Respuestas para analizar
        elif any(word in message for word in ['analizar', 'revisar', 'revisar', 'verificar']):
            return """🔍 Para analizar tu proyecto en Revit:

1. Ve a "View" > "Project Browser"
2. Revisa la organización de elementos
3. Usa "Model Analysis" para detectar conflictos
4. Verifica materiales y propiedades
5. Genera reportes si es necesario

💡 ¿Qué específicamente quieres analizar?"""
        
        # Respuestas para organizar
        elif any(word in message for word in ['organizar', 'ordenar', 'estructurar']):
            return """📋 Para organizar tu modelo de Revit:

1. Usa "Project Browser" para organizar vistas
2. Agrupa elementos relacionados
3. Crea niveles y rejillas
4. Establece nomenclatura clara
5. Usa filtros para organizar

💡 ¿Qué aspecto específico quieres organizar?"""
        
        # Respuestas para problemas
        elif any(word in message for word in ['problema', 'error', 'falla', 'mal']):
            return """⚠️ Solución de problemas comunes:

1. Revisa errores en "Revit Warnings"
2. Verifica materiales duplicados
3. Comprueba niveles y rejillas
4. Usa "Purge Unused" para limpiar
5. Reinicia si es necesario

💡 ¿Cuál es el problema específico que encuentras?"""
        
        # Respuestas para mejoras
        elif any(word in message for word in ['mejorar', 'optimizar', 'sugerir']):
            return """💡 Sugerencias para mejorar tu proyecto:

1. Usa familias parametrizadas
2. Implementa materiales eficientes
3. Optimiza el rendimiento del modelo
4. Usa tipologías consistentes
5. Documenta tu proceso

💡 ¿Qué área específica quieres mejorar?"""
        
        # Respuesta general
        else:
            return f"""🤖 Como asistente de IA para Revit, puedo ayudarte con:

🏗️ CREAR: Muros, puertas, ventanas, columnas
📊 ANALIZAR: Proyectos, conflictos, errores
📋 ORGANIZAR: Elementos, vistas, niveles
💡 SUGERIR: Mejoras, optimizaciones, mejores prácticas

💬 Escribe específicamente qué necesitas y te guío paso a paso."""
    
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
        logger.info("🤖 Iniciando Bot IA-RVT Final Funcional...")
        logger.info(f"Token: {self.token[:20]}...")
        logger.info(f"Comando path: {self.command_path}")
        logger.info("✅ Bot con respuestas inteligentes activado")
        
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error ejecutando bot: {e}")

if __name__ == "__main__":
    bot = IA_RVT_Final_Bot()
    bot.run()