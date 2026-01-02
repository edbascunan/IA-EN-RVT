# -*- coding: utf-8 -*-
"""
IA-EN-RVT YouTube Bot
====================

Bot secundario para procesamiento de contenido de YouTube
que enseña al bot principal todo lo que procesa.

Autor: Eduardo Bascuñán
Fecha: 2026-01-02
"""

import os
import asyncio
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yt_dlp
import whisper
from pathlib import Path

# Learning System Integration
from shared.learning_system import learn_content

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot de YouTube (si existe)
YOUTUBE_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN_YOUTUBE_BOT', 'CREATE_YOUTUBE_BOT_TOKEN')

# YouTube API
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')


class YouTubeProcessor:
    """Procesador de contenido de YouTube"""
    
    def __init__(self):
        self.youtube_service = None
        self.whisper_model = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Inicializar servicios de YouTube y Whisper"""
        try:
            # Inicializar YouTube API
            if YOUTUBE_API_KEY:
                self.youtube_service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
                logger.info("YouTube API initialized")
            
            # Inicializar Whisper
            try:
                self.whisper_model = whisper.load_model("base")
                logger.info("Whisper model loaded")
            except Exception as e:
                logger.warning(f"Whisper not available: {e}")
                
        except Exception as e:
            logger.error(f"Error initializing services: {e}")
    
    async def process_youtube_video(self, url: str) -> dict:
        """Procesar video de YouTube y enseñar al sistema"""
        try:
            logger.info(f"Processing YouTube video: {url}")
            
            # Configurar yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'audioquality': '192',
                'outtmpl': 'backend_ai/shared/youtube_data/%(id)s.%(ext)s',
                'quiet': True,
            }
            
            # Descargar audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                audio_file = f"backend_ai/shared/youtube_data/{info['id']}.mp3"
            
            # Transcribir audio con Whisper
            transcription = ""
            if self.whisper_model:
                result = self.whisper_model.transcribe(audio_file)
                transcription = result['text']
            
            # Crear contenido para aprender
            content_parts = []
            content_parts.append(f"Video de YouTube: {info.get('title', 'Sin título')}")
            content_parts.append(f"Canal: {info.get('uploader', 'Desconocido')}")
            content_parts.append(f"Descripción: {info.get('description', 'Sin descripción')}")
            
            if transcription:
                content_parts.append(f"Transcripción: {transcription}")
            
            # Información adicional
            content_parts.append(f"Duración: {info.get('duration', 0)} segundos")
            content_parts.append(f"Vistas: {info.get('view_count', 0)}")
            content_parts.append(f"Fecha: {info.get('upload_date', 'Desconocida')}")
            
            content = "\n".join(content_parts)
            
            # Enseñar al sistema
            learning_id = await learn_content(
                content=content,
                content_type="video",
                source="youtube",
                metadata={
                    'url': url,
                    'video_id': info['id'],
                    'title': info.get('title'),
                    'channel': info.get('uploader'),
                    'duration': info.get('duration'),
                    'view_count': info.get('view_count'),
                    'has_transcription': bool(transcription),
                    'processed_at': asyncio.get_event_loop().time()
                }
            )
            
            logger.info(f"YouTube video processed, learning ID: {learning_id}")
            
            return {
                'success': True,
                'learning_id': learning_id,
                'video_info': {
                    'title': info.get('title'),
                    'channel': info.get('uploader'),
                    'duration': info.get('duration'),
                    'has_transcription': bool(transcription)
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing YouTube video: {e}")
            return {'success': False, 'error': str(e)}
    
    async def search_youtube_videos(self, query: str, max_results: int = 5) -> dict:
        """Buscar videos en YouTube"""
        try:
            if not self.youtube_service:
                return {'success': False, 'error': 'YouTube API not available'}
            
            search_response = self.youtube_service.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=max_results,
                order="relevance"
            ).execute()
            
            videos = []
            for item in search_response['items']:
                video_info = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channel': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                videos.append(video_info)
            
            return {'success': True, 'videos': videos}
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return {'success': False, 'error': f'YouTube API error: {e}'}
        except Exception as e:
            logger.error(f"Error searching YouTube videos: {e}")
            return {'success': False, 'error': str(e)}


class YouTubeBot:
    """Bot de Telegram para procesamiento de YouTube"""
    
    def __init__(self):
        self.processor = YouTubeProcessor()
        self.application = None
        self._initialize_bot()
    
    def _initialize_bot(self):
        """Inicializar bot de Telegram"""
        if YOUTUBE_BOT_TOKEN == 'CREATE_YOUTUBE_BOT_TOKEN':
            logger.warning("YouTube bot token not configured")
            return
        
        self.application = Application.builder().token(YOUTUBE_BOT_TOKEN).build()
        
        # Registrar handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("process", self.process_video))
        self.application.add_handler(CommandHandler("search", self.search_videos))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("YouTube bot initialized")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_message = """
🎥 *YouTube Learning Bot*

Este bot procesa videos de YouTube y enseña todo al sistema IA-EN-RVT.

*Comandos disponibles:*
• /start - Mostrar este mensaje
• /help - Ayuda detallada
• /process [URL] - Procesar video de YouTube
• /search [términos] - Buscar videos

*Uso:*
Envía una URL de YouTube para procesarla y enseñar al sistema.
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_message = """
📚 *Ayuda del YouTube Learning Bot*

*Funcionalidades:*
• Procesamiento automático de videos de YouTube
• Transcripción de audio con Whisper
• Enseñanza al sistema IA-EN-RVT
• Búsqueda de contenido relevante

*Comandos:*
• `/process [URL]` - Procesar video específico
• `/search [términos]` - Buscar y procesar videos

*Ejemplos:*
• `/process https://www.youtube.com/watch?v=dQw4w9WgXcQ`
• `/search tutoriales construcción BIM`

El bot extrae audio, transcribe y enseña todo al sistema principal.
        """
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def process_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesar video de YouTube"""
        if not context.args:
            await update.message.reply_text("❌ Proporciona una URL de YouTube")
            return
        
        url = context.args[0]
        await update.message.reply_text("🎥 Procesando video de YouTube...")
        
        result = await self.processor.process_youtube_video(url)
        
        if result['success']:
            video_info = result['video_info']
            response = f"""
✅ *Video procesado exitosamente*

📺 *Título:* {video_info['title']}
📺 *Canal:* {video_info['channel']}
⏱️ *Duración:* {video_info['duration']} segundos
📝 *Transcripción:* {'Sí' if video_info['has_transcription'] else 'No'}

🧠 El contenido ha sido enseñado al sistema IA-EN-RVT
🆔 Learning ID: {result['learning_id']}
            """
            await update.message.reply_text(response, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ Error procesando video: {result['error']}")
    
    async def search_videos(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Buscar videos en YouTube"""
        if not context.args:
            await update.message.reply_text("❌ Proporciona términos de búsqueda")
            return
        
        query = " ".join(context.args)
        await update.message.reply_text(f"🔍 Buscando videos sobre: {query}")
        
        result = await self.processor.search_youtube_videos(query)
        
        if result['success']:
            videos = result['videos']
            if videos:
                response = f"🔍 *Resultados para '{query}':*\n\n"
                for i, video in enumerate(videos[:3], 1):
                    response += f"{i}. *{video['title']}*\n"
                    response += f"   Canal: {video['channel']}\n"
                    response += f"   URL: {video['url']}\n\n"
                
                await update.message.reply_text(response, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ No se encontraron videos")
        else:
            await update.message.reply_text(f"❌ Error buscando videos: {result['error']}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes de texto"""
        message = update.message.text
        
        # Detectar URLs de YouTube
        if 'youtube.com' in message or 'youtu.be' in message:
            await update.message.reply_text("🎥 URL de YouTube detectada. Procesando...")
            result = await self.processor.process_youtube_video(message)
            
            if result['success']:
                await update.message.reply_text("✅ Video procesado y enseñado al sistema")
            else:
                await update.message.reply_text(f"❌ Error: {result['error']}")
        else:
            await update.message.reply_text("💡 Envía una URL de YouTube para procesarla")
    
    def run(self):
        """Ejecutar el bot"""
        if not self.application:
            logger.error("YouTube bot not initialized")
            return
        
        logger.info("Starting YouTube Learning Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


# Instancia global del bot
youtube_bot = YouTubeBot()


if __name__ == "__main__":
    youtube_bot.run()