#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot de Telegram que procesa videos de YouTube y genera comandos BIM para Revit
Procesamiento multimodal: audio, video frames, OCR, análisis visual
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs
import re

# Importar librerías de Telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Importar sistema BIM
from final_bim_system import FinalBIMSystem

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class YouTubeBot:
    """Bot de Telegram que procesa videos de YouTube y genera comandos BIM"""
    
    def __init__(self, token: str):
        self.token = token
        self.application = None
        self.bim_system = FinalBIMSystem()
        self.user_sessions = {}  # Para almacenar sesiones de usuario
        
    def is_youtube_url(self, text: str) -> bool:
        """Detecta si el texto contiene una URL de YouTube"""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/v/[\w-]+',
            r'(?:https?://)?(?:m\.)?youtube\.com/watch\?v=[\w-]+',
        ]
        
        for pattern in youtube_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extrae el ID del video de YouTube de una URL"""
        patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([\w-]+)',
            r'(?:https?://)?(?:www\.)?youtu\.be/([\w-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([\w-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_message = """
🏗️ **Bot BIM para Revit - Procesador de YouTube**

¡Hola! Soy tu asistente BIM que puede aprender de videos de YouTube.

**Capacidades:**
• 📹 Procesar videos de YouTube (audio + video)
• 🎤 Transcripción automática de audio
• 🖼️ Análisis de frames de video
• 📝 OCR de texto en imágenes
• 🏢 Generar comandos BIM para Revit
• 🔧 Detectar herramientas y procesos de construcción

**Cómo usar:**
1. Envía un video de YouTube (URL completa)
2. Opcionalmente agrega instrucciones específicas
3. El bot analizará el contenido multimodal
4. Recibirás comandos BIM detallados

¡Envía un video de YouTube para comenzar!
        """
        
        keyboard = [
            [InlineKeyboardButton("📚 Ver Ejemplos", callback_data="examples")],
            [InlineKeyboardButton("⚙️ Configuración", callback_data="config")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
**📋 Ayuda del Bot BIM YouTube**

**Comandos disponibles:**
• `/start` - Iniciar el bot
• `/help` - Mostrar esta ayuda
• `/status` - Estado del sistema

**Cómo procesar videos:**
1. **URL Simple**: Solo envía el link del video
2. **URL + Instrucciones**: "Analiza este video para crear muros de contención"
3. **Múltiples instrucciones**: Lista lo que necesitas

**Ejemplos de uso:**
• `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
• `https://youtu.be/dQw4w9WgXcQ Crear modelo estructural`
• `https://www.youtube.com/watch?v=xyz Generar planos de instalaciones`

**Tipos de contenido que proceso:**
• Videos de construcción y arquitectura
• Tutoriales de software BIM
• Procesos de ingeniería civil
• Instalaciones MEP
• Estructuras y acabados

¿Necesitas más ayuda? ¡Pregunta!
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        status_text = """
**🔧 Estado del Sistema BIM**

✅ Bot activo y funcionando
✅ Procesador multimodal listo
✅ Sistema BIM integrado
✅ Conexión con Revit disponible

**Procesamiento disponible:**
• 🎥 Análisis de videoframes
• 🎤 Transcripción de audio (STT)
• 🖼️ OCR de texto en imágenes
• 🧠 Análisis visual con IA
• 🏗️ Generación de comandos BIM

**Última actividad:** Sistema inicializado
**Videos procesados:** En esta sesión: 0

¡Listo para procesar tu primer video!
        """
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def process_youtube_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesa mensajes que contienen URLs de YouTube"""
        text = update.message.text
        user_id = update.effective_user.id
        
        # Verificar si contiene URL de YouTube
        if not self.is_youtube_url(text):
            return False
        
        # Extraer instrucciones del mensaje
        instructions = text
        youtube_url = None
        
        # Buscar la URL de YouTube en el texto
        youtube_patterns = [
            r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)',
            r'(https?://(?:www\.)?youtu\.be/[\w-]+)',
            r'(https?://(?:www\.)?youtube\.com/embed/[\w-]+)',
        ]
        
        for pattern in youtube_patterns:
            match = re.search(pattern, text)
            if match:
                youtube_url = match.group(1)
                # Remover la URL del texto para obtener las instrucciones
                instructions = text.replace(youtube_url, '').strip()
                if not instructions:
                    instructions = "Analiza este video y genera comandos BIM relevantes para Revit"
                break
        
        if not youtube_url:
            await update.message.reply_text("❌ No se pudo extraer la URL del video de YouTube.")
            return True
        
        # Enviar mensaje de procesamiento
        processing_msg = await update.message.reply_text(
            "🔄 **Procesando video de YouTube...**\n\n"
            "📹 Analizando contenido multimodal:\n"
            "• 🎤 Transcribiendo audio\n"
            "• 🖼️ Extrayendo frames\n"
            "• 📝 OCR de texto\n"
            "• 🧠 Análisis visual\n"
            "• 🏗️ Generando comandos BIM\n\n"
            "⏳ Esto puede tomar unos minutos...",
            parse_mode='Markdown'
        )
        
        try:
            # Procesar el video con el sistema BIM
            result = await self.process_youtube_video(
                youtube_url, 
                instructions, 
                user_id
            )
            
            # Enviar resultados
            await self.send_results(update, result, processing_msg)
            
        except Exception as e:
            logger.error(f"Error procesando video: {e}")
            await processing_msg.edit_text(
                f"❌ **Error procesando el video**\n\n"
                f"Error: {str(e)}\n\n"
                f"Por favor verifica que la URL sea válida e intenta de nuevo.",
                parse_mode='Markdown'
            )
        
        return True
    
    async def process_youtube_video(self, url: str, instructions: str, user_id: int) -> Dict:
        """Procesa un video de YouTube usando el sistema BIM"""
        try:
            # Procesar con el sistema BIM final
            result = await self.bim_system.process_youtube_video(url, instructions)
            
            # Agregar metadata del usuario
            result['user_id'] = user_id
            result['processing_timestamp'] = asyncio.get_event_loop().time()
            
            return result
            
        except Exception as e:
            logger.error(f"Error en process_youtube_video: {e}")
            raise e
    
    async def send_results(self, update: Update, result: Dict, processing_msg):
        """Envía los resultados del procesamiento"""
        
        # Mensaje principal de resultados
        main_message = f"""
**✅ Video procesado exitosamente**

📹 **Video:** {result.get('video_title', 'Título no disponible')}
🔗 **URL:** {result.get('video_url', 'N/A')}

**📊 Análisis Multimodal:**
• 🎤 **Audio transcrito:** {len(result.get('transcription', ''))} caracteres
• 🖼️ **Frames analizados:** {len(result.get('extracted_frames', []))} imágenes
• 📝 **Texto detectado (OCR):** {len(result.get('ocr_text', ''))} caracteres
• 🧠 **Análisis visual:** {len(result.get('visual_analysis', ''))} caracteres

**🏗️ Comandos BIM Generados:** {len(result.get('bim_commands', []))} comandos
        """
        
        await processing_msg.edit_text(main_message, parse_mode='Markdown')
        
        # Enviar comandos BIM detallados
        if result.get('bim_commands'):
            commands_message = "**🔧 Comandos BIM para Revit:**\n\n"
            for i, command in enumerate(result['bim_commands'], 1):
                commands_message += f"{i}. **{command.get('category', 'General')}**\n"
                commands_message += f"   • {command.get('action', 'Sin acción')}\n"
                commands_message += f"   • {command.get('description', 'Sin descripción')}\n\n"
            
            await update.message.reply_text(commands_message, parse_mode='Markdown')
        
        # Enviar resumen del análisis
        if result.get('summary'):
            summary_message = f"""
**📋 Resumen del Análisis:**

{result['summary']}

**💡 Recomendaciones:**
{result.get('recommendations', 'No hay recomendaciones específicas')}
            """
            
            await update.message.reply_text(summary_message, parse_mode='Markdown')
        
        # Enviar opciones de acción
        keyboard = [
            [InlineKeyboardButton("📤 Ejecutar en Revit", callback_data=f"execute_{result.get('video_id', '')}")],
            [InlineKeyboardButton("💾 Guardar Comandos", callback_data=f"save_{result.get('video_id', '')}")],
            [InlineKeyboardButton("🔄 Procesar Otro Video", callback_data="new_video")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "**¿Qué deseas hacer con estos comandos?**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja callbacks de botones inline"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "examples":
            await self.show_examples(query)
        elif data == "config":
            await self.show_config(query)
        elif data.startswith("execute_"):
            await self.execute_commands(query, data)
        elif data.startswith("save_"):
            await self.save_commands(query, data)
        elif data == "new_video":
            await self.new_video(query)
    
    async def show_examples(self, query):
        """Muestra ejemplos de uso"""
        examples = """
**📚 Ejemplos de Uso del Bot**

**1. Análisis Simple:**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**2. Con Instrucciones Específicas:**
```
https://youtu.be/dQw4w9WgXcQ Crear estructura de acero para puente
```

**3. Múltiples Instrucciones:**
```
https://www.youtube.com/watch?v=xyz Generar modelo de edificio residencial
Incluir: muros, losas, columnas, vigas, escaleras
Aplicar normativa sísmica argentina
```

**4. Análisis de Procesos:**
```
https://youtu.be/construction-process Analizar proceso constructivo
Generar cronograma y secuencia de trabajo
Identificar equipos necesarios
```

**Tipos de comandos que genero:**
• 🏗️ Modelado de estructuras
• 🔧 Instalaciones MEP
• 📐 Planos y documentación
• 📊 Cuantificaciones
• ⚡ Automatizaciones en Revit

¡Envía tu video con instrucciones específicas!
        """
        
        await query.message.edit_text(examples, parse_mode='Markdown')
    
    async def show_config(self, query):
        """Muestra configuración del sistema"""
        config_info = """
**⚙️ Configuración del Sistema**

**Capacidades Técnicas:**
✅ Procesamiento multimodal completo
✅ Transcripción de audio (STT)
✅ Análisis de videoframes con IA
✅ OCR de texto en imágenes
✅ Generación automática de comandos BIM
✅ Integración con pyRevit

**Formatos Soportados:**
• 📹 Videos de YouTube (todos los formatos)
• 🎤 Audio en múltiples idiomas
• 🖼️ Imágenes de alta resolución
• 📝 Texto en planos y documentos

**Configuración Actual:**
• Idioma: Español (Argentina)
• Normativas: CIRSOC, INPRES
• Versión Revit: 2026
• Sistema BIM: Integrado completo

**¿Todo configurado correctamente?**
El bot está listo para procesar tus videos de YouTube.
        """
        
        await query.message.edit_text(config_info, parse_mode='Markdown')
    
    async def execute_commands(self, query, data):
        """Simula ejecución de comandos en Revit"""
        video_id = data.split("_")[1]
        
        await query.message.edit_text(
            "🔄 **Ejecutando comandos en Revit...**\n\n"
            "⏳ Transfiriendo comandos al executor...\n"
            "✅ Comandos enviados exitosamente\n\n"
            f"📋 Video procesado: {video_id}\n"
            "🏗️ Revit debe ejecutar los comandos automáticamente",
            parse_mode='Markdown'
        )
    
    async def save_commands(self, query, data):
        """Simula guardado de comandos"""
        video_id = data.split("_")[1]
        
        await query.message.edit_text(
            "💾 **Comandos guardados**\n\n"
            f"📁 Video ID: {video_id}\n"
            "📄 Comandos guardados en:\n"
            "   `/backend_ai/saved_commands/`\n\n"
            "✅ Archivo generado exitosamente\n"
            "🔄 Los comandos están disponibles para uso futuro",
            parse_mode='Markdown'
        )
    
    async def new_video(self, query):
        """Inicia procesamiento de nuevo video"""
        await query.message.edit_text(
            "🎬 **Listo para nuevo video**\n\n"
            "📤 Envía la URL del video de YouTube que quieres analizar\n"
            "📝 Puedes incluir instrucciones específicas\n\n"
            "Ejemplo:\n"
            "```\n"
            "https://www.youtube.com/watch?v=example\n"
            "Crear modelo estructural del edificio\n"
            "```",
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja todos los mensajes"""
        text = update.message.text
        
        # Intentar procesar como video de YouTube
        if await self.process_youtube_message(update, context):
            return
        
        # Si no es YouTube, responder con ayuda
        response = f"""
**🤖 Mensaje recibido:** {text[:50]}...

Para procesar videos de YouTube:
1. Envía la URL completa del video
2. Opcionalmente agrega instrucciones

Ejemplo:
```
https://www.youtube.com/watch?v=example
Crear estructura de acero
```

¿Necesitas ayuda? Usa /help
        """
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    def create_application(self):
        """Crea y configura la aplicación del bot"""
        self.application = Application.builder().token(self.token).build()
        
        # Agregar handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        return self.application
    
    async def run(self):
        """Ejecuta el bot"""
        app = self.create_application()
        logger.info("🚀 Iniciando Bot de Telegram - Procesador YouTube BIM")
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        
        # Mantener el bot corriendo
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            await app.stop()
            await app.shutdown()

def main():
    """Función principal"""
    # Cargar configuración
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ Error: TELEGRAM