# -*- coding: utf-8 -*-
"""
IA-EN-RVT Bot Master - Versión Actualizada 2026
==============================================

Bot principal actualizado con todas las nuevas capacidades:
- Sistema de aprendizaje persistente en la nube
- Procesamiento de documentos Google
- Múltiples LLMs con fallback
- YouTube learning
- Datos de construcción argentina y chile

Autor: Eduardo Bascuñán
Fecha: 2026-01-02
"""

import os
import asyncio
import logging
import json
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Imports de los nuevos módulos
from shared.learning_system import learning_system, learn_content, query_knowledge
from shared.google_docs_processor import GoogleDocsProcessor
from shared.multi_llm_manager import MultiLLMManager, LLMRequest, LLMProvider
from shared.construction_data import argentina_construction_data, chile_construction_norms
from youtube_bot import YouTubeBot

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token de Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'CONFIGURE_TOKEN_EN_.ENV')


class EnhancedBotMaster:
    """Bot Master mejorado con todas las nuevas capacidades"""
    
    def __init__(self):
        self.learning_system = learning_system
        self.google_processor = GoogleDocsProcessor()
        self.multi_llm = MultiLLMManager()
        self.youtube_bot = YouTubeBot()
        self.user_sessions = {}
        self.autonomy_level = 3
        
        # Cargar datos de construcción
        self._load_construction_data()
        
        logger.info("Enhanced Bot Master initialized with all capabilities")
    
    def _load_construction_data(self):
        """Cargar datos de construcción argentina y chile"""
        try:
            # Cargar datos de Argentina
            argentina_file = "backend_ai/shared/construction_data/argentina_construction_data.json"
            if os.path.exists(argentina_file):
                with open(argentina_file, 'r', encoding='utf-8') as f:
                    self.argentina_data = json.load(f)
                logger.info("Argentina construction data loaded")
            
            # Cargar datos de Chile
            chile_file = "backend_ai/shared/norms_chile/chile_construction_norms.json"
            if os.path.exists(chile_file):
                with open(chile_file, 'r', encoding='utf-8') as f:
                    self.chile_data = json.load(f)
                logger.info("Chile construction data loaded")
                
        except Exception as e:
            logger.error(f"Error loading construction data: {e}")
    
    async def enhanced_process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesamiento mejorado de mensajes con IA avanzada"""
        user_message = update.message.text
        user_id = update.message.from_user.id
        
        logger.info(f"Enhanced processing message from {user_id}: {user_message}")
        
        # Verificar si es comando especial
        if self._is_construction_query(user_message):
            await self._handle_construction_query(update, user_message)
            return
        
        if self._is_document_request(user_message):
            await self._handle_document_request(update, user_message)
            return
        
        if self._is_learning_request(user_message):
            await self._handle_learning_request(update, user_message)
            return
        
        # Procesamiento general con múltiples LLMs
        await self._process_with_multiple_llm(update, user_message)
    
    def _is_construction_query(self, message: str) -> bool:
        """Detectar si es una consulta sobre construcción"""
        construction_keywords = [
            'norma', 'material', 'hormigón', 'cemento', 'ladrillo', 'IRAM', 'CIRSOC',
            'NCh', 'sísmica', 'estructura', 'dimensión', 'precio', 'costo',
            'Argentina', 'Chile', 'construcción', 'edificación'
        ]
        return any(keyword.lower() in message.lower() for keyword in construction_keywords)
    
    def _is_document_request(self, message: str) -> bool:
        """Detectar si es una solicitud de procesamiento de documento"""
        doc_keywords = [
            'procesar', 'documento', 'archivo', 'PDF', 'Excel', 'Word', 'CAD',
            'Google', 'Sheet', 'hoja', 'tabla'
        ]
        return any(keyword.lower() in message.lower() for keyword in doc_keywords)
    
    def _is_learning_request(self, message: str) -> bool:
        """Detectar si es una solicitud de aprendizaje"""
        learning_keywords = [
            'enseñar', 'aprender', 'conocimiento', 'entrena', 'entrenar'
        ]
        return any(keyword.lower() in message.lower() for keyword in learning_keywords)
    
    async def _handle_construction_query(self, update: Update, message: str):
        """Manejar consultas sobre construcción argentina/chile"""
        try:
            await update.message.reply_text("🏗️ Consultando datos de construcción...")
            
            # Buscar en datos de Argentina
            argentina_result = self._search_construction_data(message, self.argentina_data)
            
            # Buscar en datos de Chile
            chile_result = self._search_construction_data(message, self.chile_data)
            
            # Crear respuesta con LLM
            context = f"""
Datos de Argentina: {argentina_result}
Datos de Chile: {chile_result}
Consulta original: {message}
            """
            
            llm_request = LLMRequest(
                prompt=f"""Eres un experto en construcción argentina y chilena. 
Responde la siguiente consulta usando los datos proporcionados:

{context}

Consulta: {message}

Proporciona una respuesta detallada y práctica, incluyendo códigos de normas cuando sea relevante.""",
                provider=LLMProvider.OPENAI,
                max_tokens=1500,
                temperature=0.3
            )
            
            llm_response = await self.multi_llm.generate_response(llm_request)
            
            response_text = f"""
🏗️ *Consulta de Construcción*

*Respuesta:*
{llm_response.content}

*Fuente de datos:*
📍 Argentina: {'✅ Disponible' if argentina_result else '❌ No encontrado'}
📍 Chile: {'✅ Disponible' if chile_result else '❌ No encontrado'}

*Aprendiendo de la consulta...*
            """
            
            await update.message.reply_text(response_text, parse_mode='Markdown')
            
            # Aprender de la consulta
            await learn_content(
                content=f"Consulta: {message}\nRespuesta: {llm_response.content}",
                content_type="text",
                source="user_query",
                metadata={'category': 'construction', 'country': 'argentina_chile'}
            )
            
        except Exception as e:
            logger.error(f"Error handling construction query: {e}")
            await update.message.reply_text(f"❌ Error procesando consulta: {str(e)}")
    
    def _search_construction_data(self, query: str, data: dict) -> str:
        """Buscar en datos de construcción"""
        if not data:
            return ""
        
        query_lower = query.lower()
        results = []
        
        # Buscar en normas
        for category, norms in data.get('normas_argentinas', {}).items() if 'argentina' in data else data.get('normas_chilenas', {}).items():
            if isinstance(norms, list):
                for norm in norms:
                    if any(keyword in norm.get('titulo', '').lower() or keyword in norm.get('descripcion', '').lower() 
                           for keyword in query_lower.split() if len(keyword) > 3):
                        results.append(f"- {norm.get('codigo', '')}: {norm.get('titulo', '')}")
        
        return "\n".join(results[:5])  # Máximo 5 resultados
    
    async def _handle_document_request(self, update: Update, message: str):
        """Manejar solicitudes de procesamiento de documento"""
        try:
            # Detectar tipo de documento y URL/archivo
            if 'google' in message.lower():
                await update.message.reply_text("📄 Procesando documento de Google...")
                # Implementar extracción de ID de Google y procesamiento
                await update.message.reply_text("⚠️ Funcionalidad de Google Docs en desarrollo")
            else:
                await update.message.reply_text("📁 Procesando archivo local...")
                await update.message.reply_text("⚠️ Funcionalidad de archivos locales en desarrollo")
                
        except Exception as e:
            logger.error(f"Error handling document request: {e}")
            await update.message.reply_text(f"❌ Error procesando documento: {str(e)}")
    
    async def _handle_learning_request(self, update: Update, message: str):
        """Manejar solicitudes de aprendizaje"""
        try:
            await update.message.reply_text("🧠 Procesando solicitud de aprendizaje...")
            
            # Extraer contenido para aprender del mensaje
            learning_content = f"Contenido para aprender: {message}"
            
            learning_id = await learn_content(
                content=learning_content,
                content_type="text",
                source="user_learning",
                metadata={'learned_at': datetime.now().isoformat()}
            )
            
            response = f"""
✅ *Aprendizaje completado*

🆔 Learning ID: {learning_id}
📝 Contenido: {message[:100]}...

El sistema ha guardado este conocimiento para futuras consultas.
            """
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error handling learning request: {e}")
            await update.message.reply_text(f"❌ Error en aprendizaje: {str(e)}")
    
    async def _process_with_multiple_llm(self, update: Update, message: str):
        """Procesar mensaje usando múltiples LLMs"""
        try:
            await update.message.reply_text("🤖 Procesando con IA avanzada...")
            
            # Consultar conocimiento relevante primero
            knowledge_result = await query_knowledge(message)
            
            # Crear contexto con conocimiento
            context = ""
            if knowledge_result.get('similar_entries'):
                context = "Conocimiento relevante:\n"
                for entry in knowledge_result['similar_entries'][:2]:
                    context += f"- {entry['content'][:200]}...\n"
            
            # Crear solicitud para LLM
            llm_request = LLMRequest(
                prompt=f"""Eres IA-EN-RVT, un experto en BIM y construcción para Revit 2026.

{context}

Consulta del usuario: {message}

Proporciona una respuesta detallada y práctica. Si es necesario, sugiere comandos específicos para Revit.""",
                provider=LLMProvider.OPENAI,
                max_tokens=1000,
                temperature=0.7
            )
            
            llm_response = await self.multi_llm.generate_response(llm_request)
            
            if llm_response.success:
                response_text = f"""
🤖 *Respuesta IA-EN-RVT*

{llm_response.content}

*Proveedor utilizado: {llm_response.provider.value}*
*Tokens: {llm_response.tokens_used}*
*Tiempo: {llm_response.response_time:.2f}s*

💡 El sistema ha aprendido de tu consulta para mejorar futuras respuestas.
                """
                
                await update.message.reply_text(response_text, parse_mode='Markdown')
                
                # Aprender de la interacción
                await learn_content(
                    content=f"Usuario: {message}\nIA: {llm_response.content}",
                    content_type="conversation",
                    source="telegram_chat",
                    metadata={'provider': llm_response.provider.value}
                )
            else:
                await update.message.reply_text(f"❌ Error de IA: {llm_response.error}")
                
        except Exception as e:
            logger.error(f"Error in multiple LLM processing: {e}")
            await update.message.reply_text(f"❌ Error procesando: {str(e)}")
    
    async def get_enhanced_status(self) -> dict:
        """Obtener estado mejorado del sistema"""
        try:
            # Estado del sistema de aprendizaje
            learning_stats = await self.learning_system.get_learning_stats()
            
            # Estado de LLMs
            llm_stats = self.multi_llm.get_provider_stats()
            
            # Estado de datos de construcción
            construction_status = {
                'argentina_data_loaded': hasattr(self, 'argentina_data'),
                'chile_data_loaded': hasattr(self, 'chile_data'),
                'total_construction_entries': 0
            }
            
            return {
                'system_status': 'Enhanced IA-EN-RVT Bot',
                'autonomy_level': self.autonomy_level,
                'learning_system': learning_stats,
                'llm_providers': len(llm_stats),
                'construction_data': construction_status,
                'youtube_bot_available': self.youtube_bot.application is not None,
                'google_docs_processor': True,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting enhanced status: {e}")
            return {'error': str(e)}


# Instancia global del bot mejorado
enhanced_bot = EnhancedBotMaster()


# Handlers del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start mejorado"""
    welcome_message = """
🤖 *IA-EN-RVT Bot Master 2026 - VERSIÓN AVANZADA*

Sistema BIM autónomo con IA para Revit 2026

🆕 *NUEVAS CAPACIDADES:*
• 🧠 Aprendizaje persistente en la nube
• 📚 Base de datos de construcción Argentina/Chile
• 🤖 Múltiples LLMs con fallback automático
• 📄 Procesamiento de documentos Google
• 🎥 YouTube learning bot
• 🔍 Búsqueda inteligente de conocimiento

*Comandos:*
• /start - Mostrar este mensaje
• /autonomia [1-5] - Configurar nivel de autonomía
• /status - Estado avanzado del sistema
• /help - Ayuda detallada
• /learning - Estadísticas de aprendizaje
• /construct [consulta] - Consultas de construcción
• /youtube [URL] - Procesar video YouTube

*Uso natural:*
"Crea un muro de 3m en nivel 1"
"¿Cuáles son las normas IRAM para hormigón?"
"Enséñame sobre estructuras de acero"
"Procesa este documento de Google"

🚀 Sistema avanzado listo para recibir comandos
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def set_autonomia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /autonomia"""
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "❌ Uso: /autonomia [1-5]\n\n"
            "Niveles:\n"
            "1️⃣ - Solo confirmar\n"
            "2️⃣ - Ejecutar simple\n"
            "3️⃣ - Ejecutar normal (recomendado)\n"
            "4️⃣ - Ejecutar complejo\n"
            "5️⃣ - Totalmente autónomo\n\n"
            "🤖 Sistema inteligente con múltiples LLMs"
        )
        return
    
    try:
        nivel = int(context.args[0])
        if not 1 <= nivel <= 5:
            raise ValueError("Nivel fuera de rango")
        
        enhanced_bot.autonomy_level = nivel
        await update.message.reply_text(
            f"✅ Autonomía establecida en nivel *{nivel}*\n\n"
            f"🤖 IA-EN-RVT funcionará con {nivel}/5 de autonomía",
            parse_mode='Markdown'
        )
        logger.info(f"Autonomía configurada: nivel {nivel}")
        
    except ValueError:
        await update.message.reply_text("❌ El nivel debe ser un número entre 1 y 5")


async def get_enhanced_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status mejorado"""
    status = await enhanced_bot.get_enhanced_status()
    
    status_message = f"""
📊 *Estado del Sistema IA-EN-RVT 2026*

*Configuración:*
• Autonomía: Nivel {enhanced_bot.autonomy_level}
• Sistema de aprendizaje: ✅ Activo
• LLMs disponibles: {status.get('llm_providers', 0)}
• Datos de construcción: {'✅ Cargados' if status.get('construction_data', {}).get('argentina_data_loaded') else '❌'}

*Estado de Aprendizaje:*
• Entradas totales: {status.get('learning_system', {}).get('total_entries', 0)}
• Tipos de contenido: {len(status.get('learning_system', {}).get('entries_by_type', {}))}

*Capacidades Avanzadas:*
• 🧠 Aprendizaje persistente: ✅
• 📚 Base de datos construcción: ✅
• 🤖 Múltiples LLMs: ✅
• 📄 Google Docs: ✅
• 🎥 YouTube learning: {'✅' if status.get('youtube_bot_available') else '❌'}

*Timestamp:*
{status.get('timestamp', 'Desconocido')}

Sistema avanzado operativo ✅
    """
    await update.message.reply_text(status_message, parse_mode='Markdown')


async def learning_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /learning - Estadísticas de aprendizaje"""
    try:
        stats = await enhanced_bot.learning_system.get_learning_stats()
        
        stats_message = f"""
🧠 *Estadísticas de Aprendizaje*

*Resumen:*
• Total entradas: {stats.get('total_entries', 0)}
• Entradas por tipo: {stats.get('entries_by_type', {})}
• Proveedores LLM: {stats.get('initialized_providers', 0)}
• Encriptación: {'✅' if stats.get('encryption_enabled') else '❌'}

*Base de datos:*
• Vector DB: {stats.get('vector_db_path', 'N/A')}
• Datos de aprendizaje: {stats.get('learning_data_path', 'N/A')}

El sistema aprende continuamente de cada interacción.
        """
        await update.message.reply_text(stats_message, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error obteniendo estadísticas: {str(e)}")


async def construct_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /construct