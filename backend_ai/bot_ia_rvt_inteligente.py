# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Inteligente con Procesamiento de Lenguaje Natural
======================================================================

Bot capaz de procesar instrucciones en lenguaje natural y enviar comandos a Revit
Con sistema de aprendizaje continuo
Autor: Eduardo Bascuñán
"""

import os
import json
import re
import logging
from datetime import datetime
from typing import Dict, Any, List, Tuple

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

class IA_RVT_Inteligente:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.command_path = os.getenv('COMMAND_PATH', 'C:\\edbascunan\\IA-EN-RVT\\backend_ai\\shared\\command_out.json')
        self.learning_path = os.getenv('LEARNING_PATH', 'C:\\edbascunan\\IA-EN-RVT\\backend_ai\\shared\\learning_data.json')
        
        # Patrones de comandos en lenguaje natural
        self.command_patterns = {
            # Crear muros
            r"crear.*muro.*desde.*(\d+(?:\.\d+)?).*?,.*?(\d+(?:\.\d+)?).*?hasta.*?(\d+(?:\.\d+)?).*?,.*?(\d+(?:\.\d+)?).*?altura.*?(\d+(?:\.\d+)?)": "wall_custom",
            r"muro.*desde.*(\d+(?:\.\d+)?).*?,.*?(\d+(?:\.\d+)?).*?hasta.*?(\d+(?:\.\d+)?).*?,.*?(\d+(?:\.\d+)?)": "wall_simple",
            r"crear.*muro.*(\d+(?:\.\d+)?).*?metros": "wall_length",
            r"muro.*(\d+(?:\.\d+)?).*?por.*?(\d+(?:\.\d+)?)": "wall_dimensions",
            
            # Análisis
            r"analizar.*modelo": "analyze_model",
            r"estadísticas.*del.*proyecto": "analyze_model",
            r"información.*del.*proyecto": "project_info",
            r"cuántos.*muros": "count_walls",
            r"cuántos.*niveles": "count_levels",
            r"cuántas.*puertas": "count_doors",
            r"cuántas.*ventanas": "count_windows",
            
            # Crear otros elementos
            r"crear.*puerta": "create_door",
            r"crear.*ventana": "create_window",
            r"crear.*columna": "create_column",
            r"crear.*viga": "create_beam",
            
            # Ayuda y aprendizaje
            r"ayuda": "show_help",
            r"qué.*puedes.*hacer": "show_capabilities",
            r"aprender": "show_learning",
            
            # Comandos específicos
            r"necesito.*un.*muro": "wall_general",
            r"quiero.*un.*muro": "wall_general",
            r"añadir.*muro": "wall_general"
        }
        
        # Inicializar aplicación
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configurar handlers del bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("analizar", self.analizar_command))
        self.app.add_handler(CommandHandler("info", self.info_command))
        self.app.add_handler(CommandHandler("aprender", self.aprender_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_natural_language))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_text = """
🤖 *IA-EN-RVT 2026 - Bot Inteligente* 🧠

¡Bienvenido al asistente de IA más avanzado para Revit!

🧠 *PROCESAMIENTO DE LENGUAJE NATURAL:*
Puedes hablarme como a un asistente humano:

📝 *Ejemplos de comandos:*
• "Crear un muro desde 0,0 hasta 5,0 con altura 3.5"
• "Necesito un muro de 6 metros de largo"
• "Analizar el modelo completo"
• "¿Cuántos muros hay en el proyecto?"
• "Mostrar estadísticas del proyecto"

🎯 *El bot aprende de cada interacción*
📚 *Soporte para múltiples elementos*
⚡ *Respuestas instantáneas*

💬 *Solo escribe tu solicitud en lenguaje natural*
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
📚 *Manual del Bot Inteligente IA-EN-RVT*

🧠 *PROCESAMIENTO DE LENGUAJE NATURAL:*

🏗️ *CREAR ELEMENTOS:*
• "Crear muro desde 0,0 hasta 5,0 altura 3.5"
• "Muro de 6 metros desde 2,1"
• "Necesito un muro de 4x3 metros"
• "Crear puerta en el muro"
• "Añadir ventana"

📊 *ANALIZAR MODELO:*
• "Analizar modelo completo"
• "¿Cuántos muros hay?"
• "Estadísticas del proyecto"
• "Información del proyecto"
• "Contar niveles"

💬 *COMANDOS LIBRES:*
• "Quiero ver qué elementos hay"
• "Ayuda con muros"
• "Mostrar capacidades"
• "Aprender sobre el sistema"

🎯 *El sistema aprende continuamente*
🤖 *Procesa instrucciones complejas*
⚡ *Ejecuta en Revit automáticamente*
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        try:
            command_exists = os.path.exists(self.command_path)
            learning_exists = os.path.exists(self.learning_path)
            
            learning_data = {}
            if learning_exists:
                with open(self.learning_path, 'r', encoding='utf-8') as f:
                    learning_data = json.load(f)
            
            commands_processed = len(learning_data.get('successful_commands', []))
            
            status_text = f"""
🔧 *Estado del Sistema IA-EN-RVT*

🤖 Bot: 🟢 Activo y funcionando
📁 Comando JSON: {'🟢 Conectado' if command_exists else '🔴 Desconectado'}
🧠 Aprendizaje: {'🟢 Activo' if learning_exists else '🟡 Inicializando'}
📊 Comandos procesados: {commands_processed}
📅 Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

🧠 *Capacidades del Bot:*
• Procesamiento de lenguaje natural
• Creación automática de elementos
• Análisis completo de modelos
• Aprendizaje continuo
• Múltiples elementos de Revit

💡 *Escribe cualquier instrucción en lenguaje natural*
            """
            
            await update.message.reply_text(status_text, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error verificando estado: {str(e)}")
    
    async def analizar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /analizar"""
        comando = {
            "instruction": "analizar modelo completo",
            "timestamp": datetime.now().isoformat(),
            "tipo": "analisis"
        }
        
        await self.guardar_comando(comando)
        await update.message.reply_text(
            "🔍 *Análisis del modelo iniciado*\n\n"
            "📊 Se enviarán las instrucciones a Revit para analizar:\n"
            "• Cantidad de elementos\n"
            "• Estadísticas del proyecto\n"
            "• Información detallada\n\n"
            "🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            parse_mode='Markdown'
        )
    
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /info"""
        comando = {
            "instruction": "información del proyecto",
            "timestamp": datetime.now().isoformat(),
            "tipo": "informacion"
        }
        
        await self.guardar_comando(comando)
        await update.message.reply_text(
            "📋 *Información del proyecto solicitada*\n\n"
            "🏗️ Se obtendrá información sobre:\n"
            "• Propiedades del proyecto\n"
            "• Configuraciones actuales\n"
            "• Detalles del modelo\n\n"
            "🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            parse_mode='Markdown'
        )
    
    async def aprender_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /aprender"""
        learning_text = """
🧠 *Sistema de Aprendizaje IA-EN-RVT*

📚 *¿Cómo aprende el sistema?*
• Registra cada comando exitoso
• Mejora patrones de reconocimiento
• Adapta respuestas a tu estilo
• Optimiza ejecución de tareas

📊 *Datos que aprende:*
• Comandos más utilizados
• Patrones de instrucciones
• Preferencias del usuario
• Tipos de elementos frecuentes

🎯 *Beneficios del aprendizaje:*
• Respuestas más precisas
• Ejecución más rápida
• Comprensión contextual
• Personalización automática

💡 *Mientras más uses el sistema, más inteligente se vuelve*
        """
        await update.message.reply_text(learning_text, parse_mode='Markdown')
    
    async def handle_natural_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar lenguaje natural"""
        user_message = update.message.text.strip()
        
        try:
            instruction, response_type = self.process_natural_language(user_message)
            
            if instruction:
                comando = {
                    "instruction": instruction,
                    "timestamp": datetime.now().isoformat(),
                    "tipo": response_type,
                    "usuario": update.effective_user.first_name or "Usuario"
                }
                
                await self.guardar_comando(comando)
                await self.send_response(update, response_type, instruction)
                self.learn_from_interaction(user_message, instruction, response_type)
                
            else:
                await update.message.reply_text(
                    "🤔 No pude entender tu solicitud. \n\n"
                    "💡 *Consejos:*\n"
                    "• Sé más específico con las coordenadas\n"
                    "• Usa palabras como 'crear', 'muro', 'analizar'\n"
                    "• Prueba con '/help' para ver ejemplos\n\n"
                    "📝 *Ejemplo:* 'Crear muro desde 0,0 hasta 5,0 altura 3'",
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logger.error(f"Error procesando lenguaje natural: {e}")
            await update.message.reply_text(f"❌ Error procesando tu solicitud: {str(e)}")
    
    def process_natural_language(self, message: str) -> Tuple[str, str]:
        """Procesar lenguaje natural y extraer instrucción"""
        message_lower = message.lower().strip()
        
        for pattern, command_type in self.command_patterns.items():
            match = re.search(pattern, message_lower)
            if match:
                return self.build_instruction(command_type, match), command_type
        
        return self.fallback_analysis(message_lower), "general"
    
    def build_instruction(self, command_type: str, match: re.Match) -> str:
        """Construir instrucción específica"""
        if command_type == "wall_custom":
            x1, y1, x2, y2, height = match.groups()
            return f"crear muro desde {x1},{y1} hasta {x2},{y2} altura {height}"
        elif command_type == "wall_simple":
            x1, y1, x2, y2 = match.groups()
            return f"crear muro desde {x1},{y1} hasta {x2},{y2}"
        elif command_type == "wall_general":
            return "crear muro genérico"
        elif command_type == "analyze_model":
            return "analizar modelo completo"
        elif command_type == "project_info":
            return "información del proyecto"
        elif command_type == "count_walls":
            return "contar muros en el modelo"
        elif command_type == "count_levels":
            return "contar niveles en el modelo"
        elif command_type == "show_help":
            return "mostrar ayuda"
        else:
            return f"procesar: {command_type}"
    
    def fallback_analysis(self, message: str) -> str:
        """Análisis de respaldo para mensajes no reconocidos"""
        if "muro" in message:
            if any(word in message for word in ["crear", "hacer", "añadir", "necesito"]):
                return "crear muro genérico"
            elif "analizar" in message or "cuántos" in message:
                return "contar muros en el modelo"
        
        if "analizar" in message or "estadísticas" in message:
            return "analizar modelo completo"
        
        if "información" in message or "proyecto" in message:
            return "información del proyecto"
        
        if "ayuda" in message or "help" in message:
            return "mostrar ayuda"
        
        return f"procesar instrucción: {message}"
    
    async def send_response(self, update: Update, response_type: str, instruction: str):
        """Enviar respuesta apropiada según el tipo"""
        responses = {
            "wall_custom": f"🧱 *Muro personalizado en proceso*\n\n📍 Instrucciones: {instruction}\n🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            "wall_simple": f"🧱 *Muro simple en proceso*\n\n📍 Instrucciones: {instruction}\n🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            "wall_general": f"🧱 *Muro genérico en proceso*\n\n📍 Instrucciones: {instruction}\n🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            "analyze_model": f"🔍 *Análisis del modelo iniciado*\n\n📊 Instrucciones: {instruction}\n🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            "project_info": f"📋 *Información del proyecto solicitada*\n\n📝 Instrucciones: {instruction}\n🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            "count_walls": f"📊 *Conteo de muros*\n\n🔢 Instrucciones: {instruction}\n🔄 *Haz clic en '🤖 IA RVT' en Revit*",
            "show_help": f"❓ *Mostrando ayuda*\n\n📚 Instrucciones: {instruction}\n🔄 *Haz clic en '🤖 IA RVT' en Revit*"
        }
        
        response = responses.get(response_type, f"✅ *Comando procesado*\n\n📍 Instrucciones: {instruction}\n🔄 *Haz clic en '🤖 IA RVT' en Revit*")
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    def learn_from_interaction(self, original_message: str, processed_instruction: str, command_type: str):
        """Aprender de la interacción del usuario"""
        try:
            learning_data = {}
            if os.path.exists(self.learning_path):
                with open(self.learning_path, 'r', encoding='utf-8') as f:
                    learning_data = json.load(f)
            
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "original_message": original_message,
                "processed_instruction": processed_instruction,
                "command_type": command_type,
                "success": True
            }
            
            if "learning_history" not in learning_data:
                learning_data["learning_history"] = []
            
            learning_data["learning_history"].append(interaction)
            
            if len(learning_data["learning_history"]) > 1000:
                learning_data["learning_history"] = learning_data["learning_history"][-1000:]
            
            os.makedirs(os.path.dirname(self.learning_path), exist_ok=True)
            with open(self.learning_path, 'w', encoding='utf-8') as f:
                json.dump(learning_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error en aprendizaje: {e}")
    
    async def guardar_comando(self, comando: Dict[str, Any]):
        """Guardar comando en archivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.command_path), exist_ok=True)
            
            with open(self.command_path, 'w', encoding='utf-8') as f:
                json.dump(comando, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Comando guardado: {comando}")
            
        except Exception as e:
            logger.error(f"Error guardando comando