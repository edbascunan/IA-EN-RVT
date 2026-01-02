# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Master Principal
=====================================

Bot master que integra todas las funcionalidades:
- NLP con OpenAI
- Sistema de memoria RAG
- Procesamiento multimodal
- Integración con PYREVIT

Autor: Eduardo Bascuñán
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

from config import ConfigClass
from memory_manager import MemoryManager
from rag_system import RAGSystem

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class IA_RVT_BotMaster:
    """Bot Master principal del sistema IA_RVT"""
    
    def __init__(self, config=None):
        """Inicializar Bot Master"""
        self.config = config or ConfigClass
        self.bot_config = self.config.get_bot_config()
        
        # Inicializar componentes principales
        self.memory_manager = MemoryManager(self.config)
        self.rag_system = RAGSystem(self.config)
        
        # Estados del bot
        self.active_sessions = {}  # Sesiones activas de usuarios
        self.autonomy_level = 3    # Nivel de autonomía (1-5)
        
        # Inicializar aplicación Telegram
        self.app = Application.builder().token(self.bot_config['token']).build()
        self.setup_handlers()
        
        logger.info("🤖 Bot Master IA_RVT inicializado")
    
    def setup_handlers(self):
        """Configurar handlers del bot"""
        # Comandos básicos
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("memory", self.memory_command))
        self.app.add_handler(CommandHandler("autonomy", self.autonomy_command))
        
        # Comandos de procesamiento
        self.app.add_handler(CommandHandler("docs", self.docs_command))
        self.app.add_handler(CommandHandler("youtube", self.youtube_command))
        self.app.add_handler(CommandHandler("image", self.image_command))
        
        # Comandos de análisis
        self.app.add_handler(CommandHandler("analyze", self.analyze_command))
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        
        # Manejo de mensajes
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.app.add_handler(MessageHandler(filters.ATTACHMENT, self.handle_attachment))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user = update.effective_user
        
        welcome_text = f"""
🏗️ *IA-EN-RVT 2026 - Bot Master* 🧠

¡Bienvenido {user.first_name}!

🤖 *SISTEMA BIM AUTÓNOMO COMPLETO:*

🧠 *Capacidades Avanzadas:*
• Procesamiento de Lenguaje Natural Real
• Memoria Ilimitada con RAG
• Procesamiento Multimodal (texto, imagen, video, audio)
• Integración Directa con Revit 2026
• Aprendizaje Continuo

📋 *Ejemplos de Comandos:*
• "Crear un muro de 6 metros en la entrada principal"
• "Analiza mi proyecto y busca conflictos"
• "Aprende de este documento PDF"
• "Procesa este video de YouTube"
• "Muestra las estadísticas del modelo"

⚡ *Nivel de Autonomía:* {self.autonomy_level}/5

💬 *Comandos Disponibles:*
• /help - Manual completo
• /status - Estado del sistema
• /memory - Gestionar memoria
• /docs - Procesar documentos
• /youtube - Analizar videos
• /analyze - Análisis avanzado

🎯 *¡Comienza a hablar en lenguaje natural!*
        """
        
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)
        
        # Inicializar sesión de usuario
        self._initialize_user_session(user.id, user.first_name)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
📚 *Manual Completo IA-EN-RVT*

🏗️ *COMANDOS DE MODELADO:*
• "Crear muro desde (0,0) hasta (5,0) altura 3.5m"
• "Añadir columna en posición específica"
• "Dibujar viga de 8 metros"
• "Colocar puerta en muro sur"

🔍 *COMANDOS DE ANÁLISIS:*
• "Analizar modelo completo"
• "Buscar conflictos en estructura"
• "Contar elementos por categoría"
• "Revisar cumplimiento normativo"

📚 *PROCESAMIENTO DE DOCUMENTOS:*
• /docs - Subir y procesar PDFs
• "Aprende de este manual técnico"
• "Indexar este documento de normas"

🎥 *PROCESAMIENTO MULTIMEDIA:*
• /youtube [URL] - Analizar videos
• /image - Procesar imágenes/planos
• "Extraer información de este plano"

🧠 *GESTIÓN DE MEMORIA:*
• /memory stats - Ver estadísticas
• "Buscar en historial de conversaciones"
• "Recuperar información previa"

⚙️ *CONFIGURACIÓN:*
• /autonomy [1-5] - Nivel de autonomía
• /status - Estado del sistema
• /stats - Estadísticas avanzadas

🎯 *Consejo: Usa lenguaje natural como si hablaras con un experto en BIM*
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        try:
            # Obtener estadísticas
            memory_stats = self.memory_manager.get_memory_stats()
            rag_stats = self.rag_system.get_multimodal_stats()
            
            # Verificar estado de archivos
            command_path_exists = os.path.exists(self.bot_config['command_path'])
            
            status_text = f"""
🔧 *Estado del Sistema IA-EN-RVT*

🤖 *Bot Master:*
• Estado: 🟢 Activo
• Usuario: {update.effective_user.first_name}
• Sesión: {self.active_sessions.get(update.effective_user.id, 'No inicializada')}

🧠 *Sistema de Memoria:*
• Conversaciones: {memory_stats.get('total_conversations', 0)}
• Conocimiento BIM: {memory_stats.get('knowledge_items', 0)}
• Vector Store: {memory_stats.get('vector_store_size', 0)} elementos

🎯 *Sistema RAG Multimodal:*
• Estado: 🟢 Activo
• Vector Store: {rag_stats.get('vector_store', {}).get('vector_store_size', 0)} elementos
• Memoria: {rag_stats.get('memory', {}).get('memory_usage', 'Desconocida')}

📁 *Integración Revit:*
• Comando JSON: {'🟢 Conectado' if command_path_exists else '🔴 Desconectado'}
• Nivel Autonomía: {self.autonomy_level}/5

📅 *Última Actualización:*
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error en status: {e}")
            await update.message.reply_text(f"❌ Error verificando estado: {str(e)}")
    
    async def memory_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /memory"""
        user_id = update.effective_user.id
        session_id = f"user_{user_id}"
        
        try:
            # Obtener historial de conversación
            history = self.memory_manager.get_conversation_history(session_id, limit=5)
            
            if history:
                memory_text = "🧠 *Historial de Conversación:*\n\n"
                for i, conv in enumerate(history, 1):
                    memory_text += f"{i}. *Usuario:* {conv['message']}\n"
                    memory_text += f"   *Respuesta:* {conv['response'][:100]}...\n\n"
            else:
                memory_text = "🧠 *No hay historial de conversación*"
            
            # Añadir estadísticas
            stats = self.memory_manager.get_memory_stats()
            memory_text += f"\n📊 *Estadísticas:*\n"
            memory_text += f"• Total conversaciones: {stats.get('total_conversations', 0)}\n"
            memory_text += f"• Conocimiento BIM: {stats.get('knowledge_items', 0)}"
            
            await update.message.reply_text(memory_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error en memory: {e}")
            await update.message.reply_text(f"❌ Error accediendo a memoria: {str(e)}")
    
    async def autonomy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /autonomy"""
        if not context.args:
            await update.message.reply_text(
                f"⚙️ *Nivel de Autonomía Actual:* {self.autonomy_level}/5\n\n"
                "Niveles:\n"
                "1 - Manual (solo sugerencias)\n"
                "2 - Semi-automático (confirmación requerida)\n"
                "3 - Automático (con registro)\n"
                "4 - Alto nivel (decisiones complejas)\n"
                "5 - Autónomo completo\n\n"
                "Uso: /autonomy [número 1-5]",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            new_level = int(context.args[0])
            if 1 <= new_level <= 5:
                old_level = self.autonomy_level
                self.autonomy_level = new_level
                
                await update.message.reply_text(
                    f"✅ *Autonomía actualizada*\n"
                    f"• Nivel anterior: {old_level}/5\n"
                    f"• Nuevo nivel: {new_level}/5\n\n"
                    f"🎯 El sistema ahora ejecutará acciones {'manualmente' if new_level <= 2 else 'automáticamente'}",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text("❌ Nivel debe estar entre 1 y 5")
                
        except ValueError:
            await update.message.reply_text("❌ Nivel inválido. Use: /autonomy [número 1-5]")
    
    async def docs_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /docs"""
        docs_text = """
📚 *Procesamiento de Documentos*

Para procesar un documento:

1️⃣ *Subir archivo* (PDF, DOCX, TXT, CSV)
2️⃣ *El sistema automáticamente:*
   • Extraerá el texto
   • Lo dividirá en chunks
   • Lo indexará en el vector store
   • Lo añadirá a la memoria

3️⃣ *Podrás consultar:*
   • "Buscar información sobre X en los documentos"
   • "Resume el contenido de los PDFs"
   • "Extrae datos específicos"

💡 *Ejemplo:* Sube un manual de Revit y pregunta sobre familias de muros.

📎 *Sube tu documento ahora*
        """
        
        await update.message.reply_text(docs_text, parse_mode=ParseMode.MARKDOWN)
    
    async def youtube_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /youtube"""
        if not context.args:
            youtube_text = """
🎥 *Procesamiento de Videos YouTube*

Para analizar un video de YouTube:

1️⃣ *Enviar URL del video:*
   /youtube https://youtube.com/watch?v=...

2️⃣ *El sistema:*
   • Extraerá transcripción
   • Indexará el contenido
   • Lo añadirá a la base de conocimiento

3️⃣ *Podrás preguntar:*
   • "¿Qué técnicas se explican en el video?"
   • "Resume las mejores prácticas mostradas"
   • "Extrae información sobre X tema"

📺 *Envía la URL de un video educativo sobre BIM*
            """
        else:
            url = context.args[0]
            result = self.rag_system.process_video_youtube(url)
            
            if result["success"]:
                youtube_text = f"""
✅ *Video procesado exitosamente*

📹 *ID:* {result.get('video_id', 'N/A')}
🔗 *URL:* {result.get('url', 'N/A')}
📊 *Chunks indexados:* {result.get('chunks', 0)}

🎯 *Ahora puedes consultar el contenido del video*
                """
            else:
                youtube_text = f"❌ Error procesando video: {result.get('error', 'Error desconocido')}"
        
        await update.message.reply_text(youtube_text, parse_mode=ParseMode.MARKDOWN)
    
    async def image_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /image"""
        image_text = """
🖼️ *Procesamiento de Imágenes*

Para procesar una imagen (plano, screenshot, foto):

1️⃣ *Enviar imagen directamente*
2️⃣ *El sistema:*
   • Analizará el contenido
   • Extraerá texto con OCR (si aplica)
   • Indexará la información

3️⃣ *Podrás preguntar:*
   • "¿Qué elementos hay en esta imagen?"
   • "Extrae las medidas mostradas"
   • "Analiza la estructura del plano"

📎 *Envía una imagen para analizarla*
        """
        
        await update.message.reply_text(image_text, parse_mode=ParseMode.MARKDOWN)
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /analyze"""
        analyze_text = """
🔍 *Análisis Avanzado del Sistema*

📊 *Estadísticas de Memoria:*
• Total conversaciones almacenadas
• Conocimiento BIM por categorías
• Uso de vectores de memoria

📚 *Base de Conocimiento:*
• Documentos procesados
• Videos de YouTube indexados
• Imágenes analizadas

🎯 *Rendimiento:*
• Tiempo de respuesta promedio
• Precisión de consultas RAG
• Eficiencia de búsqueda vectorial

💡 *Usa /stats para ver métricas detalladas*
        """
        
        await update.message.reply_text(analyze_text, parse_mode=ParseMode.MARKDOWN)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /stats"""
        try:
            memory_stats = self.memory_manager.get_memory_stats()
            rag_stats = self.rag_system.get_multimodal_stats()
            
            stats_text = f"""
📊 *Estadísticas Detalladas*

🧠 *Memoria:*
• Conversaciones: {memory_stats.get('total_conversations', 0)}
• Elementos de conocimiento: {memory_stats.get('knowledge_items', 0)}
• Tamaño vector store: {memory_stats.get('vector_store_size', 0)}

📚 *Categorías de Conocimiento:*
"""
            
            categories = memory_stats.get('categories', {})
            for category, count in categories.items():
                stats_text += f"• {category}: {count} elementos\n"
            
            stats_text += f"""
🎯 *Sistema RAG:*
• Estado: {rag_stats.get('status', 'Desconocido')}
• Vector store multimodal: {rag_stats.get('vector_store', {}).get('vector_store_size', 0)}

⚡ *Rendimiento:*
• Nivel de autonomía: {self.autonomy_level}/5
• Sesiones activas: {len(self.active_sessions)}
• Última actualización: {datetime.now().strftime('%H:%M:%S')}
            """
            
            await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error en stats: {e}")
            await update.message.reply_text(f"❌ Error obteniendo estadísticas: {str(e)}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes de texto"""
        user_message = update.message.text.strip()
        user = update.effective_user
        
        try:
            # Obtener contexto del usuario
            user_context = self._get_user_context(user.id, user.first_name)
            
            # Procesar con RAG y memoria
            result = self.rag_system.generate_contextual_response(
                query=user_message,
                user_context=user_context
            )
            
            if result["success"]:
                response = result["response"]
                sources = result.get("sources", [])
                
                # Añadir información de fuentes si hay
                if sources:
                    response += f"\n\n📚 *Fuentes consultadas:* {len(sources)}"
                
                # Generar comando BIM si es relevante
                if self._should_generate_bim_command(user_message):
                    bim_command = self._generate_bim_command(result, user_context)
                    if bim_command:
                        await self._save_bim_command(bim_command)
                        response += f"\n\n🔄 *Comando BIM generado*\n👆 Haz clic en '🤖 IA RVT' en Revit"
                
                await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text(
                    f"❌ Error procesando mensaje: {result.get('error', 'Error desconocido')}"
                )
                
        except Exception as e:
            logger.error(f"Error manejando mensaje: {e}")
            await update.message.reply_text(f"❌ Error interno: {str(e)}")
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar fotos/imágenes"""
        photo = update.message.photo[-1]  # Imagen de mayor resolución
        
        try:
            # Por ahora, confirmar recepción
            # En implementación completa, descargar y procesar