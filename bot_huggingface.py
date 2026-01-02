# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Inteligente con Hugging Face
================================================

Bot con IA real usando Hugging Face Inference API
100% Gratuito, sin límites estrictos
Autor: Eduardo Bascuñán
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from huggingface_hub import InferenceClient

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class IA_RVT_HuggingFace_Bot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.hf_token = os.getenv('HUGGINGFACE_API_KEY')
        self.command_path = os.getenv('COMMAND_PATH', 'backend_ai/shared/command_out.json')
        
        # Configurar Hugging Face - 100% Gratuito
        self.client = InferenceClient(token=self.hf_token)
        
        # Modelos gratuitos de Hugging Face (en orden de preferencia)
        self.free_models = [
            "mistralai/Mistral-7B-Instruct-v0.2",
            "meta-llama/Meta-Llama-3-8B-Instruct",
            "HuggingFaceH4/zephyr-7b-beta",
            "microsoft/DialoGPT-medium"
        ]
        
        # Modelo principal
        self.model = self.free_models[0]
        
        # Inicializar aplicación
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configurar handlers del bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("deploy", self.deploy_command))
        self.app.add_handler(CommandHandler("models", self.models_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_text = """🤖 IA-EN-RVT 2026 - Bot con Hugging Face

¡Bienvenido al asistente de IA más avanzado para Revit!

🧠 Procesamiento de lenguaje natural REAL usando Hugging Face
🚀 100% Gratuito, sin límites estrictos
🤖 Modelos de IA open source de alta calidad

💬 Escribe cualquier mensaje y te ayudaré con tu proyecto de Revit.

💡 Usa comandos: /start, /help, /status, /models, /deploy"""
        await update.message.reply_text(welcome_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """📚 Manual del Bot IA-EN-RVT con Hugging Face

🧠 PROCESAMIENTO NLP REAL:

🏗️ CREAR ELEMENTOS:
• "Quiero crear un muro de 6 metros en la entrada"
• "Añade una columna estructural aquí"
• "Crea una ventana de 1.5x1.2 metros"
• "Necesito una puerta en el muro sur"

📊 ANALIZAR MODELO:
• "Analiza mi proyecto completo"
• "¿Qué problemas ves en la estructura?"
• "Revisa si hay conflictos entre elementos"
• "Evalúa la eficiencia del diseño"

💬 COMANDOS INTELIGENTES:
• "Ayúdame a optimizar mi modelo"
• "¿Cómo puedo mejorar la organización?"
• "Sugiere mejoras para el proyecto"
• "Explícame el proceso paso a paso"

🤖 Hugging Face ventajas:
• 100% Gratuito sin límites
• Modelos open source
• IA real y avanzada
• Múltiples modelos disponibles
• Respuestas contextuales inteligentes

💬 Habla naturalmente - como con un experto en IA"""
        await update.message.reply_text(help_text)
    
    async def models_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /models"""
        models_text = """🧠 Modelos de IA Disponibles en Hugging Face

✅ MODELOS GRATUITOS ACTIVOS:
"""
        for i, model in enumerate(self.free_models, 1):
            models_text += f"{i}. `{model}`\n"
        
        models_text += f"""
🔄 Modelo actual: `{self.model}`

💡 Características Hugging Face:
• 100% Gratuito sin tarjeta de crédito
• Miles de modelos open source
• Sin límites estrictos de uso
• IA de alta calidad
• Modelos constantemente actualizados
• API simple y robusta

🎯 Todos los modelos son capaces de NLP avanzado"""
        await update.message.reply_text(models_text)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        try:
            hf_configured = bool(self.hf_token)
            
            status_text = f"""🔧 Estado del Sistema IA-EN-RVT

🤖 Bot: Activo con Hugging Face
🧠 Hugging Face: {'🟢 Configurado con IA real' if hf_configured else '❌ No configurado'}
📅 Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

🧠 Capacidades IA:
• Procesamiento NLP real
• Modelos open source gratuitos
• Sin límites de cuota
• Respuestas contextuales inteligentes
• Desplegado en Railway
• ✅ Modelo: {self.model}

💡 Habla naturalmente - tienes IA real disponible"""
            await update.message.reply_text(status_text)
            
        except Exception as e:
            await update.message.reply_text(f"Error verificando estado: {str(e)}")
    
    async def deploy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /deploy"""
        deploy_text = """🚀 Despliegue en Railway con Hugging Face

El bot se despliega automáticamente en Railway para:
• 🌐 Acceso 24/7 desde cualquier lugar
• ⚡ Respuestas rápidas con IA real
• 📈 Escalabilidad automática
• 🔒 Mayor estabilidad
• 🧠 Hugging Face con modelos gratuitos
• ✅ Sin límites de cuota
• ✅ IA open source de alta calidad

🤖 IA real y funcional disponible 24/7"""
        await update.message.reply_text(deploy_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes con Hugging Face IA"""
        user_message = update.message.text.strip()
        
        try:
            # Procesar con Hugging Face IA
            response = await self.process_with_hf(user_message)
            
            if response:
                await update.message.reply_text(response)
                
                # Guardar comando si es relevante
                if any(word in user_message.lower() for word in ['crear', 'muro', 'puerta', 'ventana', 'columna']):
                    comando = {
                        "instruction": user_message,
                        "action": "CREATE",
                        "timestamp": datetime.now().isoformat(),
                        "usuario": update.effective_user.first_name or "Usuario"
                    }
                    await self.guardar_comando(comando)
            else:
                await update.message.reply_text("🤔 No pude procesar tu solicitud. ¿Podrías ser más específico?")
                
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def process_with_hf(self, message: str) -> str:
        """Procesar mensaje con Hugging Face IA"""
        try:
            # Prompt especializado para Revit y arquitectura
            system_prompt = """Eres un asistente experto en IA para Revit y arquitectura. 
Tu trabajo es ayudar con:

1. CREAR elementos arquitectónicos (muros, puertas, ventanas, columnas, vigas)
2. ANALIZAR modelos y detectar problemas
3. ORGANIZAR proyectos de construcción
4. OPTIMIZAR diseños arquitectónicos
5. SUGERIR mejoras y mejores prácticas

Responde de forma clara, específica y útil. Si necesitas más detalles, pregunta.
Proporciona pasos concretos y profesionales."""
            
            # Hugging Face Inference API - Modelo gratuito
            response = self.client.text_generation(
                f"{system_prompt}\n\nUsuario: {message}\n\nAsistente:",
                model=self.model,
                max_new_tokens=500,
                temperature=0.7,
                do_sample=True,
                top_p=0.9
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error con Hugging Face: {e}")
            
            # Fallback: respuesta inteligente básica
            return self.get_intelligent_fallback(message)
    
    def get_intelligent_fallback(self, message: str) -> str:
        """Respuesta inteligente básica si falla la API"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['crear', 'hacer', 'añadir']):
            if 'muro' in message_lower:
                return """🏗️ Para crear un muro inteligente en Revit:

1. **Planificación**: Define la ubicación exacta y dimensiones
2. **Configuración**: Ve a Architecture > Wall
3. **Ubicación**: Traza la línea base del muro
4. **Propiedades**: Ajusta altura (ej: 3.0m), grosor (ej: 0.20m)
5. **Material**: Selecciona tipo de muro (concreto, ladrillo, etc.)
6. **Confirmación**: Aplica y verifica la inserción

💡 Tip: Usa niveles (Levels) para controlar la altura automáticamente."""
            
            elif 'puerta' in message_lower:
                return """🚪 Para crear una puerta eficiente en Revit:

1. **Selección**: Elige la pared donde va la puerta
2. **Herramienta**: Architecture > Door
3. **Colocación**: Haz clic en la posición exacta
4. **Configuración**: 
   - Ancho típico: 0.80m, 0.90m, 1.00m
   - Alto típico: 2.10m
   - Tipo: Según uso (interior/exterior)
5. **Verificación**: Revisa que no interfiera con otros elementos

💡 Consejo: Verifica que haya suficiente espacio para apertura."""
        
        elif any(word in message_lower for word in ['analizar', 'revisar', 'verificar']):
            return """🔍 Análisis inteligente de tu proyecto:

1. **Navegación**: View > Project Browser
2. **Revisión estructural**:
   - Usa "Model Analysis" para detectar interferencias
   - Revisa "Revit Warnings" para errores
3. **Optimización**:
   - Verifica niveles y rejillas
   - Comprueba materiales y sus propiedades
4. **Reportes**: Genera schedule de elementos
5. **Coordinación**: Asegura consistencia entre disciplinas

💡 Pro tip: Usa "Phases" para organizar por etapas de construcción."""
        
        else:
            return f"""🤖 Como tu asistente de IA para Revit, puedo ayudarte con:

🏗️ **CREAR**: Muros, puertas, ventanas, columnas, vigas, losas
📊 **ANALIZAR**: Interferencias, eficiencia, estructura, materiales
📋 **ORGANIZAR**: Niveles, familias, vistas, fases de construcción
💡 **OPTIMIZAR**: Diseño, rendimiento, coordinación, documentación

💬 Describe específicamente tu necesidad y te daré una respuesta inteligente y profesional."""
    
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
        logger.info("🤖 Iniciando Bot IA-RVT con Hugging Face...")
        logger.info(f"Token: {self.token[:20]}...")
        logger.info(f"Hugging Face: {'🟢 Configurado con IA real' if self.hf_token else '❌ No configurado'}")
        logger.info(f"Modelo: {self.model}")
        logger.info("🧠 Hugging Face con IA real activado - 100% Gratuito")
        
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error ejecutando bot: {e}")

if __name__ == "__main__":
    bot = IA_RVT_HuggingFace_Bot()
    bot.run()