# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Propuesta 2: Chatbot Avanzado RAG + Memoria
============================================================

Chatbot avanzado con RAG (Retrieval-Augmented Generation) y memoria vectorial.
Basado en repositorios de referencia con memoria ilimitada usando LangChain + FAISS.

Características:
- RAG con embeddings y búsqueda vectorial
- Memoria persistente con SQLite + FAISS
- Base de conocimiento BIM integrada
- Contexto contextual avanzado
- Aprendizaje continuo

Autor: Eduardo Bascuñán
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

from openai import OpenAI
from dotenv import load_dotenv

# Importar sistema RAG
import sys
sys.path.append('../..')
from backend_ai.memory_manager import MemoryManager
from backend_ai.rag_system import RAGSystem
from backend_ai.config import ConfigClass

# Cargar configuración
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ChatbotRAGMemoria:
    """Chatbot Avanzado con RAG y Memoria Vectorial"""
    
    def __init__(self):
        """Inicializar chatbot RAG + Memoria"""
        # Configuración
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.command_path = os.getenv('COMMAND_PATH', 'backend_ai/shared/command_out.json')
        
        # Verificar configuración
        if not self.token or not self.openai_api_key:
            raise ValueError("TELEGRAM_TOKEN y OPENAI_API_KEY son requeridos")
        
        # Inicializar OpenAI
        self.client = OpenAI(api_key=self.openai_api_key)
        
        # Inicializar sistemas avanzados
        self.config = ConfigClass
        self.memory_manager = MemoryManager(self.config)
        self.rag_system = RAGSystem(self.config)
        
        # Estados del bot
        self.active_sessions = {}
        self.query_count = 0
        
        # Inicializar aplicación
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()
        
        # Añadir conocimiento BIM base
        self._initialize_bim_knowledge()
        
        logger.info("🧠 Chatbot RAG + Memoria IA_RVT inicializado")
    
    def setup_handlers(self):
        """Configurar handlers del bot"""
        # Comandos básicos
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        
        # Comandos de memoria y RAG
        self.app.add_handler(CommandHandler("memory", self.memory_command))
        self.app.add_handler(CommandHandler("search", self.search_command))
        self.app.add_handler(CommandHandler("learn", self.learn_command))
        self.app.add_handler(CommandHandler("context", self.context_command))
        
        # Comandos de análisis avanzado
        self.app.add_handler(CommandHandler("analyze", self.analyze_command))
        self.app.add_handler(CommandHandler("insights", self.insights_command))
        
        # Manejo de mensajes
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_advanced_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user = update.effective_user
        
        welcome_text = f"""
🧠 *IA_RVT - Chatbot RAG + Memoria Avanzado* 🚀

¡Hola {user.first_name}!

🤖 *TECNOLOGÍA AVANZADA:*
• RAG (Retrieval-Augmented Generation) con embeddings
• Memoria vectorial persistente con FAISS
• Base de conocimiento BIM integrada
• Contexto contextual profundo
• Aprendizaje continuo automático

📚 *CAPACIDADES ÚNICAS:*
• Búsqueda semántica en historial completo
• Recuperación de información por contexto
• Análisis de patrones en conversaciones
• Sugerencias basadas en conocimiento previo
• Respuestas con fuentes y referencias

🔍 *EJEMPLOS AVANZADOS:*
• "¿Qué muro creamos ayer con dimensiones similares?"
• "Busca información sobre muros estructurales"
• "Analiza los patrones de mis proyectos"
• "¿Qué elementos suelen tener conflictos?"
• "Muestra el historial de análisis"

⚡ *COMANDOS AVANZADOS:*
• /search [consulta] - Búsqueda semántica
• /learn [tema] - Añadir conocimiento
• /context - Ver contexto actual
• /insights - Análisis de patrones
• /memory - Memoria completa
        """
        
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)
        
        # Inicializar sesión con contexto RAG
        self._initialize_rag_session(user.id, user.first_name)
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /search para búsqueda semántica"""
        if not context.args:
            await update.message.reply_text(
                "🔍 *Búsqueda Semántica RAG*\n\n"
                "Uso: /search [consulta]\n"
                "Ejemplo: /search muros estructurales",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        query = ' '.join(context.args)
        
        try:
            # Búsqueda en memoria
            memory_results = self.memory_manager.retrieve_relevant_memory(
                query, 
                limit=5
            )
            
            # Búsqueda en base de conocimiento
            knowledge_results = self.memory_manager.search_bim_knowledge(query)
            
            # Formatear resultados
            search_text = f"🔍 *Resultados para: '{query}'*\n\n"
            
            if memory_results:
                search_text += "🧠 *Memoria relevante:*\n"
                for i, result in enumerate(memory_results, 1):
                    relevance = result.get('relevance', 'Media')
                    search_text += f"{i}. [{relevance}] {result['content'][:100]}...\n"
                search_text += "\n"
            
            if knowledge_results:
                search_text += "📚 *Conocimiento BIM:*\n"
                for i, result in enumerate(knowledge_results, 1):
                    search_text += f"{i}. {result['topic']}: {result['content'][:80]}...\n"
            
            if not memory_results and not knowledge_results:
                search_text += "❌ No se encontraron resultados relevantes"
            
            await update.message.reply_text(search_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            await update.message.reply_text(f"❌ Error en búsqueda: {str(e)}")
    
    async def learn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /learn para añadir conocimiento"""
        if not context.args:
            await update.message.reply_text(
                "📚 *Añadir Conocimiento*\n\n"
                "Uso: /learn [categoría] [contenido]\n"
                "Ejemplo: /learn muros Los muros estructurales requieren cimientos profundos",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ Formato incorrecto\n"
                "Uso: /learn [categoría] [contenido]",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        category = context.args[0]
        content = ' '.join(context.args[1:])
        
        try:
            # Añadir a memoria
            self.memory_manager.add_bim_knowledge(
                category=category,
                topic=f"Aprendido de {update.effective_user.first_name}",
                content=content,
                source="usuario"
            )
            
            await update.message.reply_text(
                f"✅ *Conocimiento añadido*\n\n"
                f"📂 Categoría: {category}\n"
                f"💭 Contenido: {content[:100]}...\n\n"
                f"🧠 El sistema ahora recordará esta información",
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            logger.error(f"Error añadiendo conocimiento: {e}")
            await update.message.reply_text(f"❌ Error añadiendo conocimiento: {str(e)}")
    
    async def context_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /context para ver contexto actual"""
        user_id = update.effective_user.id
        session_id = f"user_{user_id}"
        
        try:
            # Obtener historial
            history = self.memory_manager.get_conversation_history(session_id, limit=10)
            
            context_text = "🎯 *Contexto Actual de la Sesión:*\n\n"
            
            if history:
                context_text += "🧠 *Últimas interacciones:*\n"
                for i, conv in enumerate(history[-5:], 1):
                    context_text += f"{i}. *Tú:* {conv['message'][:60]}...\n"
                    context_text += f"   *Yo:* {conv['response'][:60]}...\n\n"
            else:
                context_text += "📝 *Sesión nueva - Sin contexto previo*\n"
            
            # Añadir estadísticas de memoria
            stats = self.memory_manager.get_memory_stats()
            context_text += f"\n📊 *Estadísticas de memoria:*\n"
            context_text += f"• Total conversaciones: {stats.get('total_conversations', 0)}\n"
            context_text += f"• Conocimiento BIM: {stats.get('knowledge_items', 0)}"
            
            await update.message.reply_text(context_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error obteniendo contexto: {e}")
            await update.message.reply_text(f"❌ Error obteniendo contexto: {str(e)}")
    
    async def insights_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /insights para análisis de patrones"""
        user_id = update.effective_user.id
        session_id = f"user_{user_id}"
        
        try:
            # Obtener historial completo
            history = self.memory_manager.get_conversation_history(session_id, limit=100)
            
            if not history:
                await update.message.reply_text("📊 *No hay suficientes datos para análisis*")
                return
            
            insights_text = "📊 *Análisis de Patrones:*\n\n"
            
            # Análisis básico de patrones
            messages = [conv['message'] for conv in history]
            responses = [conv['response'] for conv in history]
            
            # Contar tipos de acciones
            create_count = sum(1 for msg in messages if any(word in msg.lower() for word in ['crear', 'añadir', 'insertar']))
            analyze_count = sum(1 for msg in messages if any(word in msg.lower() for word in ['analizar', 'revisar', 'buscar']))
            query_count = len(messages) - create_count - analyze_count
            
            insights_text += f"🎯 *Patrones identificados:*\n"
            insights_text += f"• Creación de elementos: {create_count}\n"
            insights_text += f"• Análisis: {analyze_count}\n"
            insights_text += f"• Consultas generales: {query_count}\n\n"
            
            # Palabras más frecuentes
            all_text = ' '.join(messages).lower()
            common_words = ['muro', 'puerta', 'ventana', 'analizar', 'modelo']
            word_counts = {word: all_text.count(word) for word in common_words if word in all_text}
            
            if word_counts:
                insights_text += "📈 *Elementos más consultados:*\n"
                for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
                    insights_text += f"• {word.title()}: {count} veces\n"
            
            await update.message.reply_text(insights_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error generando insights: {e}")
            await update.message.reply_text(f"❌ Error generando insights: {str(e)}")
    
    async def handle_advanced_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes con RAG avanzado"""
        user_message = update.message.text.strip()
        user = update.effective_user
        
        try:
            # Obtener contexto completo
            user_context = {
                'user_id': user.id,
                'user_name': user.first_name,
                'session_id': f"user_{user.id}"
            }
            
            # Procesar con RAG contextual
            result = self.rag_system.generate_contextual_response(
                query=user_message,
                user_context=user_context
            )
            
            if result["success"]:
                response = result["response"]
                
                # Añadir información de contexto usado
                context_used = result.get('context_used', 0)
                if context_used > 0:
                    response += f"\n\n🧠 *Contexto utilizado:* {context_used} elementos"
                
                # Añadir fuentes si las hay
                sources = result.get('sources', [])
                if sources:
                    response += f"\n📚 *Fuentes consultadas:* {len(sources)}"
                
                await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
                self.query_count += 1
            else:
                await update.message.reply_text(
                    f"❌ Error procesando consulta: {result.get('error', 'Error desconocido')}"
                )
                
        except Exception as e:
            logger.error(f"Error procesando mensaje avanzado: {e}")
            await update.message.reply_text(f"❌ Error interno: {str(e)}")
    
    def _initialize_bim_knowledge(self):
        """Inicializar conocimiento BIM base"""
        bim_knowledge = [
            ("muros", "Muros estructurales", "Los muros estructurales deben estar anclados a la cimentación"),
            ("muros", "Tipos de muros", "Muros de carga, muros de cerramiento, muros cortina"),
            ("puertas", "Dimensiones estándar", "Puertas interiores: 0.80m, 0.90m, 1.00m"),
            ("ventanas", "Dimensiones estándar", "Ventanas comunes: 1.20x1.00m, 1.50x1.20m"),
            ("normas", "Código de construcción", "Cumplir con códigos locales de construcción"),
            ("análisis", "Clash detection", "Detectar interferencias entre elementos del modelo"),
            ("modelado", "Niveles", "Usar niveles coherentes para todo el proyecto")
        ]
        
        for category, topic, content in bim_knowledge:
            self.memory_manager.add_bim_knowledge(category, topic, content, "sistema_base")
    
    def _initialize_rag_session(self, user_id: int, user_name: str):
        """Inicializar sesión RAG"""
        session_id = f"user_{user_id}"
        self.active_sessions[user_id] = {
            'session_id': session_id,
            'user_name': user_name,
            'initialized_at': datetime.now().isoformat(),
            'query_count': 0
        }
    
    def run(self):
        """Ejecutar el chatbot"""
        logger.info("🧠 Iniciando Chatbot RAG + Memoria...")
        logger.info(f"Token: {self.token[:20]}...")
        logger.info(f"OpenAI: {'Configurado' if self.openai_api_key else 'No configurado'}")
        logger.info("🧠 RAG + Memoria vectorial activado")
        
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error ejecutando chatbot: {e}")

if __name__ == "__main__":
    bot = ChatbotRAGMemoria()
    bot.run()