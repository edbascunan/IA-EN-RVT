#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Master de Telegram con Múltiples IA
========================================================

Sistema BIM Autónomo con Inteligencia Artificial para Revit 2026
Bot Master con soporte para múltiples proveedores de IA

Autor: Eduardo Bascuñán
Fecha: 01 de enero de 2026
Versión: 2.0.1 - CORREGIDO Y FUNCIONAL
"""

import os
import sys
import logging
import asyncio
import html
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_providers import ai_manager
from orchestrator import orchestrator

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MarkdownEscaper:
    """Utilidad para escapar caracteres especiales de Markdown"""
    
    @staticmethod
    def escape_markdown(text: str) -> str:
        """Escapar caracteres especiales de Markdown V2"""
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text
    
    @staticmethod
    def clean_for_markdown(text: str) -> str:
        """Limpiar texto para uso seguro en Markdown"""
        # Reemplazar caracteres problemáticos
        text = text.replace('→', '->')
        text = text.replace('…', '...')
        text = html.unescape(text)
        return text
    
    @staticmethod
    def format_safe_message(text: str, use_markdown: bool = True) -> tuple:
        """Formatear mensaje de forma segura"""
        if not use_markdown:
            return (text, None)
        
        try:
            cleaned = MarkdownEscaper.clean_for_markdown(text)
            return (cleaned, 'Markdown')
        except Exception as e:
            logger.warning(f"Error limpiando Markdown: {e}")
            return (text, None)

class IARVTBotMaster:
    """Bot Master del Sistema IA-EN-RVT"""
    
    def __init__(self, token: str):
        self.token = token
        self.application = None
        self.autonomy_level = 3
        self.ai_manager = ai_manager
        self.markdown_escaper = MarkdownEscaper()
        
    def get_system_prompt(self) -> str:
        """Obtener prompt del sistema para IA"""
        return """Eres IA-EN-RVT, un asistente especializado en BIM y Revit 2026.

Tu función es ayudar con:
- Modelado BIM y diseño arquitectónico
- Comandos para Revit 2026
- Análisis de modelos estructurales
- Automatización de procesos BIM
- Interpretación de comandos de lenguaje natural

Siempre responde de forma profesional y técnica.
Mantén tus respuestas concisas y evita caracteres especiales."""
    
    async def safe_reply(self, update: Update, message: str, use_markdown: bool = True):
        """Enviar mensaje de forma segura con manejo de errores"""
        try:
            cleaned_message, parse_mode = self.markdown_escaper.format_safe_message(message, use_markdown)
            await update.message.reply_text(cleaned_message, parse_mode=parse_mode)
        except Exception as e:
            logger.error(f"Error enviando con Markdown: {e}")
            try:
                plain_message = message.replace('*', '').replace('_', '').replace('`', '')
                await update.message.reply_text(plain_message)
            except Exception as e2:
                logger.error(f"Error crítico: {e2}")
                await update.message.reply_text("Error al enviar respuesta. Intenta de nuevo.")
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        ai_status = self.ai_manager.get_status()
        
        welcome_message = f"""🤖 *Bienvenido al Sistema IA-EN-RVT 2026*

🏗️ *Sistema BIM Autónomo con IA para Revit 2026*

✨ *Características:*
• Control de Revit mediante lenguaje natural
• Análisis de modelos BIM automático
• Comandos por voz, texto, imágenes y videos
• Niveles de autonomía configurables

🧠 *IA Configurada:*
• *Principal:* {ai_status['default_provider'].upper()}
• *Proveedores activos:* {len(ai_status['providers'])}
• *OLLAMA:* {ai_status['ollama']['status']}

🎚️ *Nivel de Autonomía Actual:* {self.autonomy_level}/5

📱 *Comandos Disponibles:*
/start - Iniciar sistema
/autonomia [1-5] - Configurar autonomía
/status - Estado del sistema
/help - Ayuda detallada
/ia - Estado de proveedores IA
/apis - Listar proveedores
/test [proveedor] - Probar proveedor
/switch [proveedor] - Cambiar proveedor

💬 *Ejemplos:*
• "Crea un muro de 3 metros en nivel 1"
• "Analiza el modelo actual"
• "Genera reporte de materiales"

¿Listo para revolucionar tu workflow BIM? 🚀"""
        
        await self.safe_reply(update, welcome_message)
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_message = """📚 *Ayuda Completa - IA-EN-RVT 2026*

🎚️ *Niveles de Autonomía:*
1️⃣ Solo confirmar acciones
2️⃣ Ejecutar tareas simples
3️⃣ Ejecutar tareas normales (recomendado)
4️⃣ Ejecutar tareas complejas
5️⃣ Totalmente autónomo

📱 *Comandos:*
/start - Iniciar sistema
/autonomia [nivel] - Cambiar autonomía
/status - Ver estado
/help - Esta ayuda
/ia - Estado de IAs
/apis - Listar proveedores
/test [proveedor] - Probar API
/switch [proveedor] - Cambiar proveedor

⚡ *Powered by:*
• *GROK* - x.ai API (NUEVO)
• *MINIMAX* - API china (NUEVO)
• *CLAUDE* - Anthropic (MEJORADO)
• *ChatGPT* - OpenAI (MEJORADO)
• *DEEPSEEK* - IA principal
• *OLLAMA* - Modelos locales

¡El futuro del BIM está aquí! 🚀"""
        
        await self.safe_reply(update, help_message)
        
    async def ia_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /ia - Estado de proveedores"""
        status = self.ai_manager.get_status()
        
        providers_info = []
        for name, info in status['providers'].items():
            provider_type = "🌐 API" if info['type'] == "API" else "💻 Local"
            model_info = f" ({info['model']})" if 'model' in info else ""
            status_icon = "✅" if info.get('available', True) else "❌"
            providers_info.append(f"{status_icon} *{name.upper()}:* {provider_type}{model_info}")
            
        ollama_status = status['ollama']['status']
        
        ia_message = f"""🧠 *Estado de Proveedores IA*

🎯 *Proveedor Principal:* {status['default_provider'].upper()}
🔄 *Fallback Habilitado:* {"Sí" if status['fallback_enabled'] else "No"}
📊 *Total de Proveedores:* {len(status['providers'])}

*Proveedores Configurados:*
{chr(10).join(providers_info)}

📌 *OLLAMA:*
Estado: {ollama_status}
Host: {status['ollama']['host']}
Modelo: {status['ollama']['model']}

*Comandos disponibles:*
/test [proveedor] - Probar API
/switch [proveedor] - Cambiar proveedor

⚡ *Sistema listo para comandos BIM* 🚀"""
        
        await self.safe_reply(update, ia_message)
    
    async def apis_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /apis - Listar proveedores"""
        status = self.ai_manager.get_status()
        
        available = []
        configured = []
        
        all_providers = ['grok', 'minimax', 'claude', 'chatgpt', 'deepseek', 'ollama', 'openai', 'anthropic']
        
        for provider in all_providers:
            if provider in status['providers']:
                configured.append(f"✅ {provider.upper()}")
            else:
                available.append(f"⭕ {provider.upper()}")
        
        apis_message = f"""📋 *Listado de Proveedores de IA*

*Configurados:* {len(configured)}
{chr(10).join(configured)}

*Disponibles (sin configurar):* {len(available)}
{chr(10).join(available)}

*Activo:* {status['default_provider'].upper()}

*Para configurar:*
1. Obtén API key del proveedor
2. Agrega a .env: PROVEEDOR_API_KEY=tu_key
3. Reinicia el bot
4. Usa /switch [proveedor]

*Links de APIs:*
• GROK: https://x.ai
• MINIMAX: https://api.minimax.chat
• CLAUDE: https://anthropic.com
• ChatGPT: https://openai.com"""
        
        await self.safe_reply(update, apis_message)
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /test [proveedor]"""
        if len(context.args) == 0:
            await self.safe_reply(update, "❌ *Uso:* /test [proveedor]\n\nEjemplo: /test grok")
            return
        
        provider_name = context.args[0].lower()
        await self.safe_reply(update, f"🧪 Probando *{provider_name.upper()}*...")
        
        result = self.ai_manager.generate_response(
            message="¿Estás funcionando correctamente?",
            provider_name=provider_name,
            system_prompt="Responde brevemente si estás funcionando."
        )
        
        if result['success']:
            test_message = f"""✅ *Prueba Exitosa*

*Proveedor:* {result['provider'].upper()}
*Modelo:* {result['model']}
*Tokens:* {result['tokens_used']}

*Respuesta:*
{result['message'][:200]}...

El proveedor funciona correctamente."""
        else:
            test_message = f"""❌ *Prueba Fallida*

*Proveedor:* {provider_name.upper()}
*Error:* {result.get('error', 'Desconocido')}

Verifica:
1. API key configurada en .env
2. API key válida
3. Proveedor disponible"""
        
        await self.safe_reply(update, test_message)
    
    async def switch_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /switch [proveedor]"""
        if len(context.args) == 0:
            status = self.ai_manager.get_status()
            switch_message = f"""🔄 *Cambiar Proveedor Principal*

*Actual:* {status['default_provider'].upper()}

*Uso:* /switch [proveedor]

*Disponibles:*
{chr(10).join([f"• {p}" for p in status['providers'].keys()])}

*Ejemplo:* /switch grok"""
            await self.safe_reply(update, switch_message)
            return
        
        provider_name = context.args[0].lower()
        success = self.ai_manager.set_default_provider(provider_name)
        
        if success:
            switch_message = f"""✅ *Proveedor cambiado*

*Nuevo principal:* {provider_name.upper()}

Todos los comandos usarán este proveedor."""
        else:
            switch_message = f"""❌ *Error al cambiar*

*Solicitado:* {provider_name.upper()}

Proveedor no configurado.
Usa /apis para ver disponibles."""
        
        await self.safe_reply(update, switch_message)
        
    async def autonomy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /autonomia [nivel]"""
        try:
            if len(context.args) == 0:
                autonomy_message = f"""🎚️ *Nivel de Autonomía: {self.autonomy_level}/5*

*Usa:* /autonomia [1-5]

*Niveles:*
1 - Solo confirmar
2 - Ejecutar simple
3 - Ejecutar normal
4 - Ejecutar complejo
5 - Totalmente autónomo"""
                await self.safe_reply(update, autonomy_message)
                return
                
            level = int(context.args[0])
            if 1 <= level <= 5:
                self.autonomy_level = level
                autonomy_names = {
                    1: "Solo confirmar",
                    2: "Ejecutar simple", 
                    3: "Ejecutar normal",
                    4: "Ejecutar complejo",
                    5: "Totalmente autónomo"
                }
                
                response = f"""✅ *Autonomía: {level}/5*
📋 *{autonomy_names[level]}*

Sistema configurado."""
                await self.safe_reply(update, response)
            else:
                await self.safe_reply(update, "❌ Nivel debe estar entre 1 y 5")
        except (ValueError, IndexError):
            await self.safe_reply(update, "❌ Usa /autonomia [1-5]")
            
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        ai_status = self.ai_manager.get_status()
        
        status_message = f"""📊 *Estado del Sistema IA-EN-RVT 2026*

🟢 *Estado:* Operativo
🤖 *Bot:* Activo
🎚️ *Autonomía:* {self.autonomy_level}/5
🧠 *IA Principal:* {ai_status['default_provider'].upper()}
🔧 *Revit:* {'Conectado' if self.autonomy_level > 1 else 'Desconectado'}

📈 *Estadísticas:*
• Comandos: {update.message.message_id}
• Hora: {update.message.date.strftime('%H:%M:%S')}
• Versión: 2026.2.1
• Proveedores: {len(ai_status['providers'])}
• Fallback: {"Activo" if ai_status['fallback_enabled'] else "Inactivo"}

⚡ *Sistema listo* 🚀"""
        
        await self.safe_reply(update, status_message)
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes de texto - AGENTE AUTÓNOMO BIM"""
        user_message = update.message.text
        
        # Sincronizar autonomía con orquestador
        orchestrator.set_autonomy(self.autonomy_level)
        
        # Conectar IA al orquestador si no está conectada
        if orchestrator.ai_provider is None:
            orchestrator.set_ai_provider(self.ai_manager)
        
        await self.safe_reply(update, "🧠 *Procesando comando BIM...*")
        
        try:
            # Procesar con el orquestador (genera comando BIM real)
            resultado = orchestrator.process(user_message, usar_ia=True)
            
            if resultado.get("exito"):
                comando = resultado.get("comando", {})
                
                # Formato de respuesta según el estado
                if resultado.get("estado") == "ENVIADO_A_REVIT":
                    ai_response = f"""🤖 *IA-EN-RVT - Comando BIM Generado*

💬 *Tu mensaje:*
{user_message[:80]}...

🏗️ *Comando BIM:*
• Acción: {comando.get('accion')}
• Elemento: {comando.get('elemento')}
• Nivel: {comando.get('payload', {}).get('nivel', 'N/A')}

📋 *Payload:*
{self._format_payload(comando.get('payload', {}))}

✅ *Estado:* {resultado.get('estado')}
🎚️ *Autonomía:* {self.autonomy_level}/5
🔐 *Firma:* {comando.get('firma', 'N/A')}

📁 *Archivo:* command_out.json
⚡ *Ejecuta RunCommand en pyRevit para aplicar*"""
                
                elif resultado.get("estado") == "REQUIERE_CONFIRMACION":
                    ai_response = f"""🤖 *IA-EN-RVT - Requiere Confirmación*

💬 *Tu mensaje:*
{user_message[:80]}...

🏗️ *Comando preparado:*
• Acción: {comando.get('accion')}
• Elemento: {comando.get('elemento')}

⚠️ *Estado:* Requiere confirmación manual
🎚️ *Autonomía actual:* {self.autonomy_level}/5

💡 *Opciones:*
• Usa /confirmar para ejecutar
• Usa /cancelar para descartar
• Usa /autonomia 3 para modo automático"""
                
                else:
                    ai_response = f"""🤖 *IA-EN-RVT - Procesado*

💬 *Tu mensaje:*
{user_message[:80]}...

📊 *Resultado:* {resultado.get('mensaje')}
🎚️ *Autonomía:* {self.autonomy_level}/5"""
            
            else:
                # Error en el procesamiento
                ai_response = f"""🤖 *IA-EN-RVT - Error*

💬 *Tu mensaje:*
{user_message[:80]}...

❌ *Error:* {resultado.get('mensaje', 'Error desconocido')}

💡 *Sugerencias:*
• Intenta con un comando más específico
• Ejemplo: "Crea un muro de 3 metros en nivel 1"
• Usa /help para ver ejemplos"""
                
        except Exception as e:
            logger.error(f"Error en handle_message: {e}")
            ai_response = f"""🤖 *IA-EN-RVT - Error Temporal*

💬 *Tu mensaje:*
{user_message[:80]}...

⚠️ *Error:* {str(e)[:100]}

🔧 Intentando con procesamiento básico..."""
            
        await self.safe_reply(update, ai_response, use_markdown=True)
    
    def _format_payload(self, payload: dict) -> str:
        """Formatear payload para mostrar"""
        if not payload:
            return "  (vacío)"
        lines = []
        for key, value in list(payload.items())[:5]:  # Max 5 items
            lines.append(f"  • {key}: {value}")
        return "\n".join(lines)
    
    async def confirmar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /confirmar - Confirma comando pendiente"""
        resultado = orchestrator.confirmar_comando()
        if resultado.get("exito"):
            await self.safe_reply(update, f"✅ {resultado.get('mensaje')}")
        else:
            await self.safe_reply(update, f"❌ {resultado.get('mensaje')}")
    
    async def cancelar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /cancelar - Cancela comando pendiente"""
        resultado = orchestrator.cancelar_comando()
        await self.safe_reply(update, resultado.get('mensaje'))
        
    def run(self):
        """Ejecutar el bot"""
        try:
            self.application = Application.builder().token(self.token).build()
            
            # Agregar handlers
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("autonomia", self.autonomy_command))
            self.application.add_handler(CommandHandler("status", self.status_command))
            self.application.add_handler(CommandHandler("ia", self.ia_command))
            self.application.add_handler(CommandHandler("apis", self.apis_command))
            self.application.add_handler(CommandHandler("test", self.test_command))
            self.application.add_handler(CommandHandler("switch", self.switch_command))
            self.application.add_handler(CommandHandler("confirmar", self.confirmar_command))
            self.application.add_handler(CommandHandler("cancelar", self.cancelar_command))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            # Iniciar
            logger.info("🚀 Iniciando IA-EN-RVT Bot Master v2.0.1...")
            print("="*60)
            print("🤖 IA-EN-RVT 2026 - Bot Master v2.0.1 iniciado")
            print("="*60)
            print("🧠 Sistema de IA configurado:")
            
            ai_status = self.ai_manager.get_status()
            print(f"  • Proveedor principal: {ai_status['default_provider'].upper()}")
            print(f"  • Proveedores activos: {len(ai_status['providers'])}")
            print(f"  • OLLAMA: {ai_status['ollama']['status']}")
            print(f"  • Fallback: {'Habilitado' if ai_status['fallback_enabled'] else 'Deshabilitado'}")
            
            print("\n📱 Comandos disponibles:")
            print("  • /start - Iniciar")
            print("  • /help - Ayuda")
            print("  • /ia - Estado IAs")
            print("  • /apis - Listar proveedores")
            print("  • /test [proveedor] - Probar")
            print("  • /switch [proveedor] - Cambiar")
            print("  • /status - Estado")
            print("  • /autonomia [1-5] - Autonomía")
            
            print("\n🎚️ Autonomía: 3/5 (Normal)")
            print("✅ Markdown: CORREGIDO")
            print("✨ Proveedores: Grok, Minimax, Claude, ChatGPT")
            print("\n📱 Esperando comandos...")
            print("⚡ Ctrl+C para detener\n")
            print("="*60)
            
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            logger.error(f"❌ Error al iniciar: {e}")
            print(f"❌ Error: {e}")

def main():
    """Función principal"""
    token = os.getenv('TELEGRAM_TOKEN')
    
    if not token:
        print("❌ Error: TELEGRAM_TOKEN no encontrado en .env")
        return
    
    if token == 'tu_token_aqui':
        print("❌ Error: Configura tu token real en .env")
        return
    
    bot = IARVTBotMaster(token)
    bot.run()

if __name__ == "__main__":
    main()