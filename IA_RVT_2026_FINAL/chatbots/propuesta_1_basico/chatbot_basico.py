# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Propuesta 1: Chatbot Básico NLP
================================================

Chatbot básico con NLP mejorado y memoria de conversación simple.
Basado en el bot actual pero con mejoras en procesamiento de lenguaje natural.

Características:
- NLP con OpenAI GPT-4
- Memoria de conversación básica
- Procesamiento de comandos para Revit
- Interfaz Telegram mejorada

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

# Cargar configuración
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ChatbotBasico:
    """Chatbot Básico con NLP mejorado"""
    
    def __init__(self):
        """Inicializar chatbot básico"""
        # Configuración
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.command_path = os.getenv('COMMAND_PATH', 'backend_ai/shared/command_out.json')
        
        # Verificar configuración
        if not self.token or not self.openai_api_key:
            raise ValueError("TELEGRAM_TOKEN y OPENAI_API_KEY son requeridos")
        
        # Inicializar OpenAI
        self.client = OpenAI(api_key=self.openai_api_key)
        
        # Memoria de conversación básica (en memoria, no persistente)
        self.conversation_memory = {}
        self.conversation_limit = 50  # Últimas 50 interacciones
        
        # Estados del bot
        self.active_sessions = {}
        self.command_count = 0
        
        # Inicializar aplicación
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()
        
        logger.info("🤖 Chatbot Básico IA_RVT inicializado")
    
    def setup_handlers(self):
        """Configurar handlers del bot"""
        # Comandos básicos
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("clear", self.clear_command))
        self.app.add_handler(CommandHandler("memory", self.memory_command))
        
        # Comandos de BIM
        self.app.add_handler(CommandHandler("muro", self.muro_command))
        self.app.add_handler(CommandHandler("puerta", self.puerta_command))
        self.app.add_handler(CommandHandler("ventana", self.ventana_command))
        self.app.add_handler(CommandHandler("analizar", self.analizar_command))
        
        # Manejo de mensajes
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user = update.effective_user
        
        welcome_text = f"""
🤖 *IA_RVT - Chatbot Básico NLP* 🏗️

¡Hola {user.first_name}!

🧠 *CARACTERÍSTICAS:*
• Procesamiento de Lenguaje Natural con GPT-4
• Memoria de conversación integrada
• Comandos específicos para Revit
• Respuestas inteligentes y contextual

📝 *EJEMPLOS DE USO:*
• "Crear un muro de 6 metros en la entrada"
• "Analiza mi modelo y encuentra errores"
• "¿Cuántas puertas hay en el proyecto?"
• "Ayúdame a organizar el modelo"

⚡ *COMANDOS RÁPIDOS:*
• /muro - Crear muro específico
• /puerta - Colocar puerta
• /ventana - Insertar ventana
• /analizar - Análisis del modelo
• /clear - Limpiar conversación
• /memory - Ver historial

💬 *¡Comienza a hablar en lenguaje natural!*
        """
        
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)
        
        # Inicializar sesión
        self._initialize_session(user.id, user.first_name)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
📚 *Manual del Chatbot Básico*

🏗️ *COMANDOS DE MODELADO:*
• /muro [largo] [alto] - Crear muro específico
• /puerta [ancho] [alto] - Insertar puerta
• /ventana [ancho] [alto] - Insertar ventana

💬 *LENGUAJE NATURAL:*
• "Quiero crear un muro de 6 metros"
• "Añade una puerta en la pared sur"
• "Analiza mi proyecto completo"
• "¿Qué elementos hay en total?"

🔍 *ANÁLISIS:*
• /analizar - Revisar modelo
• "Busca conflictos en el diseño"
• "Cuenta los elementos por categoría"
• "Revisa la estructura"

🧠 *MEMORIA:*
• /memory - Ver historial de conversación
• /clear - Limpiar memoria de la sesión
• Sistema recuerda contexto durante la conversación

⚙️ *ESTADO:*
• /status - Ver estado del sistema
• Comandos procesados: {self.command_count}

💡 *Tip: Usa lenguaje natural como si hablaras con un experto*
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        user = update.effective_user
        session = self.active_sessions.get(user.id, {})
        
        status_text = f"""
🔧 *Estado del Chatbot Básico*

🤖 *Bot:* 🟢 Activo
👤 *Usuario:* {user.first_name}
📱 *Session ID:* {user.id}

🧠 *Memoria:*
• Conversaciones en sesión: {len(self.conversation_memory.get(user.id, []))}
• Límite de memoria: {self.command_count} comandos
• Estado: {'🟢 Activa' if user.id in self.active_sessions else '🔴 Inactiva'}

📊 *Estadísticas:*
• Total comandos procesados: {self.command_count}
• Sesiones activas: {len(self.active_sessions)}

🔗 *Integración:*
• Comando JSON: {'🟢 Conectado' if os.path.exists(self.command_path) else '🔴 Desconectado'}

📅 *Última actividad:*
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /clear"""
        user_id = update.effective_user.id
        
        # Limpiar memoria del usuario
        if user_id in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        # Remover sesión activa
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
        
        await update.message.reply_text(
            "✅ *Memoria limpiada*\n\n🧠 Conversación reiniciada\n🔄 Sesión nueva iniciada",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def memory_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /memory"""
        user_id = update.effective_user.id
        user_memory = self.conversation_memory.get(user_id, [])
        
        if not user_memory:
            await update.message.reply_text("🧠 *No hay historial en esta sesión*")
            return
        
        memory_text = "🧠 *Historial de Conversación:*\n\n"
        
        # Mostrar últimas 10 interacciones
        for i, conv in enumerate(user_memory[-10:], 1):
            memory_text += f"{i}. *Usuario:* {conv['user']}\n"
            memory_text += f"   *Bot:* {conv['bot'][:80]}...\n\n"
        
        memory_text += f"\n📊 *Total interacciones: {len(user_memory)}*"
        
        await update.message.reply_text(memory_text, parse_mode=ParseMode.MARKDOWN)
    
    async def muro_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /muro"""
        if not context.args:
            await update.message.reply_text(
                "🏗️ *Comando Muro*\n\n"
                "Uso: /muro [largo] [alto]\n"
                "Ejemplo: /muro 6 3.5",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            largo = float(context.args[0]) if len(context.args) > 0 else 6.0
            alto = float(context.args[1]) if len(context.args) > 1 else 3.0
            
            # Generar comando BIM
            command = {
                "schema": "IA_RVT_BIM_COMMAND_v1",
                "action": "CREATE_WALL",
                "element": "Wall",
                "parameters": {
                    "length_m": largo,
                    "height_m": alto,
                    "wall_type": "Muro Estructural - 200mm",
                    "level": "Nivel 1"
                },
                "instruction": f"Crear muro de {largo}m x {alto}m",
                "timestamp": datetime.now().isoformat()
            }
            
            await self._save_command(command)
            self.command_count += 1
            
            await update.message.reply_text(
                f"🏗️ *Muro creado*\n\n"
                f"📏 Dimensiones: {largo}m x {alto}m\n"
                f"🔄 Comando guardado\n\n"
                f"👆 Haz clic en '🤖 IA RVT' en Revit",
                parse_mode=ParseMode.MARKDOWN
            )
            
        except ValueError:
            await update.message.reply_text(
                "❌ Error: Valores inválidos\n"
                "Uso: /muro [largo] [alto]",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def puerta_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /puerta"""
        if not context.args:
            await update.message.reply_text(
                "🚪 *Comando Puerta*\n\n"
                "Uso: /puerta [ancho] [alto]\n"
                "Ejemplo: /puerta 0.9 2.1",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            ancho = float(context.args[0]) if len(context.args) > 0 else 0.9
            alto = float(context.args[1]) if len(context.args) > 1 else 2.1
            
            command = {
                "schema": "IA_RVT_BIM_COMMAND_v1",
                "action": "CREATE_DOOR",
                "element": "Door",
                "parameters": {
                    "width_m": ancho,
                    "height_m": alto,
                    "door_type": "Puerta Estándar - 90cm",
                    "level": "Nivel 1"
                },
                "instruction": f"Colocar puerta de {ancho}m x {alto}m",
                "timestamp": datetime.now().isoformat()
            }
            
            await self._save_command(command)
            self.command_count += 1
            
            await update.message.reply_text(
                f"🚪 *Puerta creada*\n\n"
                f"📏 Dimensiones: {ancho}m x {alto}m\n"
                f"🔄 Comando guardado\n\n"
                f"👆 Haz clic en '🤖 IA RVT' en Revit",
                parse_mode=ParseMode.MARKDOWN
            )
            
        except ValueError:
            await update.message.reply_text(
                "❌ Error: Valores inválidos\n"
                "Uso: /puerta [ancho] [alto]",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def ventana_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /ventana"""
        if not context.args:
            await update.message.reply_text(
                "🪟 *Comando Ventana*\n\n"
                "Uso: /ventana [ancho] [alto]\n"
                "Ejemplo: /ventana 1.2 1.5",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            ancho = float(context.args[0]) if len(context.args) > 0 else 1.2
            alto = float(context.args[1]) if len(context.args) > 1 else 1.5
            
            command = {
                "schema": "IA_RVT_BIM_COMMAND_v1",
                "action": "CREATE_WINDOW",
                "element": "Window",
                "parameters": {
                    "width_m": ancho,
                    "height_m": alto,
                    "window_type": "Ventana Estándar - 120cm",
                    "level": "Nivel 1"
                },
                "instruction": f"Insertar ventana de {ancho}m x {alto}m",
                "timestamp": datetime.now().isoformat()
            }
            
            await self._save_command(command)
            self.command_count += 1
            
            await update.message.reply_text(
                f"🪟 *Ventana creada*\n\n"
                f"📏 Dimensiones: {ancho}m x {alto}m\n"
                f"🔄 Comando guardado\n\n"
                f"👆 Haz clic en '🤖 IA RVT' en Revit",
                parse_mode=ParseMode.MARKDOWN
            )
            
        except ValueError:
            await update.message.reply_text(
                "❌ Error: Valores inválidos\n"
                "Uso: /ventana [ancho] [alto]",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def analizar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /analizar"""
        command = {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "action": "ANALYZE_MODEL",
            "element": "Model",
            "parameters": {
                "analysis_type": "complete",
                "check_conflicts": True,
                "count_elements": True,
                "validate_standards": True
            },
            "instruction": "Analizar modelo completo del proyecto",
            "timestamp": datetime.now().isoformat()
        }
        
        await self._save_command(command)
        self.command_count += 1
        
        await update.message.reply_text(
            "🔍 *Análisis iniciado*\n\n"
            "📊 Se analizará:\n"
            "• Elementos del modelo\n"
            "• Posibles conflictos\n"
            "• Cumplimiento normativo\n\n"
            "🔄 Comando enviado a Revit\n\n"
            "👆 Haz clic en '🤖 IA RVT' en Revit",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes con NLP"""
        user_message = update.message.text.strip()
        user = update.effective_user
        
        try:
            # Obtener contexto de conversación
            conversation_context = self._get_conversation_context(user.id)
            
            # Procesar con OpenAI
            response = await self._process_with_openai(user_message, conversation_context)
            
            # Almacenar en memoria
            self._store_in_memory(user.id, user_message, response)
            
            # Generar comando si es relevante
            if self._should_generate_command(user_message):
                command = await self._generate_command_from_response(user_message, response)
                if command:
                    await self._save_command(command)
                    self.command_count += 1
                    response += f"\n\n🔄 *Comando BIM generado*\n👆 Haz clic en '🤖 IA RVT' en Revit"
            
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            await update.message.reply_text(f"❌ Error procesando mensaje: {str(e)}")
    
    async def _process_with_openai(self, message: str, context: str) -> str:
        """Procesar mensaje con OpenAI"""
        try:
            system_prompt = f"""
Eres un asistente experto en Revit y BIM. Tu trabajo es:

1. ENTENDER la solicitud del usuario en lenguaje natural
2. INTERPRETAR la intención (crear, analizar, modificar, etc.)
3. EXTRAER parámetros específicos cuando sea necesario
4. GENERAR una respuesta clara y útil
5. MANTENER un enfoque técnico y práctico

Contexto de conversación:
{context}

Responde de forma clara, técnica y útil. Si necesitas más información, pregunta.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error con OpenAI: {e}")
            return f"Lo siento, no pude procesar tu solicitud. Error: {str(e)}"
    
    def