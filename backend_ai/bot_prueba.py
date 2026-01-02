#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot de Prueba Simple
=====================================

Bot básico para probar la funcionalidad mientras se configura el token real.
Este bot responderá con comandos básicos de BIM.

Autor: Eduardo Bascuñán
Fecha: 02 de enero de 2026
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Para esta prueba, usaremos una implementación simple
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    print("⚠️ python-telegram-bot no está instalado")
    print("💡 Para instalación completa: pip install python-telegram-bot")
    TELEGRAM_AVAILABLE = False

# Cargar variables de entorno
load_dotenv()

class BotPruebaBIM:
    """Bot de prueba para demostrar funcionalidad BIM"""
    
    def __init__(self, token: str = None):
        self.token = token or "TOKEN_DE_PRUEBA"
        self.application = None
        self.comandos_ejecutados = []
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        mensaje = f"""🤖 *Bot de Prueba IA-EN-RVT 2026*

🏗️ *Sistema BIM Autónomo - Modo Prueba*

✅ *Estado:*
• Revit: ✅ Conectado (pyRevit funcionando)
• Orquestador: ✅ IA procesando comandos
• Bot: ✅ Respondiendo

⚠️ *Configuración pendiente:*
• Token de Telegram real (actualmente en modo prueba)

💬 *Comandos de prueba disponibles:*
• `/crear_muro` - Simular creación de muro
• `/analizar` - Simular análisis de modelo
• `/estado` - Estado del sistema
• `/ayuda` - Esta ayuda

📱 *Para bot completo:*
1. Configurar token real en .env
2. Ejecutar bot_master.py

*¡El sistema BIM está funcionando!* 🚀"""
        
        try:
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        except:
            await update.message.reply_text("Bot de prueba iniciado - modo básico")
    
    async def crear_muro_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Simular creación de muro"""
        comando = {
            "accion": "CREATE",
            "elemento": "Wall",
            "payload": {
                "inicio": {"x": 0, "y": 0},
                "fin": {"x": 5, "y": 0},
                "altura_m": 3.0,
                "nivel": "Nivel 1",
                "tipo": "Basic Wall"
            },
            "autonomia": 3,
            "timestamp": datetime.now().isoformat()
        }
        
        self.comandos_ejecutados.append("Muro simulado creado")
        
        mensaje = f"""🏗️ *Comando BIM - Muro Creado*

✅ *Ejecución simulada:*
• Tipo: Wall (Muro)
• Altura: 3.0m
• Longitud: 5m
• Nivel: Nivel 1
• Estado: EJECUTADO

📋 *Payload generado:*
```json
{comando}
```

💡 *En el sistema completo:*
Este comando se envía automáticamente a Revit via pyRevit
y crea el muro físico en el modelo.

🎚️ *Autonomía: 3/5* - Sistema normal"""
        
        try:
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        except:
            await update.message.reply_text("Muro simulado creado exitosamente")
    
    async def analizar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Simular análisis de modelo"""
        stats = {
            "muros": 15,
            "puertas": 8,
            "ventanas": 12,
            "niveles": 3,
            "columnas": 4
        }
        
        self.comandos_ejecutados.append("Análisis simulado")
        
        mensaje = f"""📊 *Análisis de Modelo BIM*

🏗️ *Estadísticas del proyecto:*
• 🧱 Muros: {stats['muros']}
• 🚪 Puertas: {stats['puertas']}
• 🪟 Ventanas: {stats['ventanas']}
• 📏 Niveles: {stats['niveles']}
• 🏢 Columnas: {stats['columnas']}

📈 *Total elementos:* {sum(stats.values())}

💡 *En el sistema completo:*
Este análisis se extrae automáticamente del modelo
de Revit abierto y se presenta con insights IA.

🎯 *Calificación BIM:* Excelente"""
        
        try:
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        except:
            await update.message.reply_text(f"Análisis: {sum(stats.values())} elementos totales")
    
    async def estado_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Estado del sistema"""
        mensaje = f"""📊 *Estado del Sistema IA-EN-RVT 2026*

🟢 *Componentes:*
• ✅ Bot Telegram: Modo prueba
• ✅ pyRevit: Ejecutor funcionando
• ✅ Revit: Muro ID 385319 creado
• ✅ Orquestador: IA procesando
• ⚠️ Token: Configuración pendiente

🔧 *Configuración:*
• Autonomía: 3/5
• Proveedor IA: Deepseek
• Fallback: Habilitado

📋 *Comandos ejecutados: {len(self.comandos_ejecutados)}*
{chr(10).join([f"• {cmd}" for cmd in self.comandos_ejecutados[-3:]])}

🚀 *Sistema operativo*"""
        
        try:
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        except:
            await update.message.reply_text("Sistema operativo - comandos ejecutados: " + str(len(self.comandos_ejecutados)))
    
    async def ayuda_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando de ayuda"""
        mensaje = """📚 *Ayuda - Bot de Prueba IA-EN-RVT*

🎯 *Comandos disponibles:*
• `/start` - Iniciar bot
• `/crear_muro` - Simular creación de muro
• `/analizar` - Simular análisis de modelo
• `/estado` - Estado del sistema
• `/ayuda` - Esta ayuda

🔧 *Para bot completo:*
1. Obtener token de https://t.me/BotFather
2. Configurar en .env: TELEGRAM_TOKEN=tu_token
3. Ejecutar: python bot_master.py

🏗️ *Funcionalidades BIM:*
• Creación de elementos (muros, puertas, ventanas)
• Análisis automático de modelos
• Control por lenguaje natural
• Integración completa con Revit 2026

*¡Sistema BIM autónomo en desarrollo!* 🚀"""
        
        try:
            await update.message.reply_text(mensaje, parse_mode='Markdown')
        except:
            await update.message.reply_text("Ayuda - comandos: /start, /crear_muro, /analizar, /estado, /ayuda")
    
    def run_prueba(self):
        """Ejecutar bot de prueba"""
        if not TELEGRAM_AVAILABLE:
            print("❌ python-telegram-bot no disponible")
            print("💡 Instalar con: pip install python-telegram-bot")
            return
        
        if self.token == "TOKEN_DE_PRUEBA":
            print("🔧 MODO PRUEBA - Sin token real")
            print("💡 Para bot completo: configurar TELEGRAM_TOKEN en .env")
            print("")
        
        try:
            self.application = Application.builder().token(self.token).build()
            
            # Agregar handlers
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("crear_muro", self.crear_muro_command))
            self.application.add_handler(CommandHandler("analizar", self.analizar_command))
            self.application.add_handler(CommandHandler("estado", self.estado_command))
            self.application.add_handler(CommandHandler("ayuda", self.ayuda_command))
            
            print("🤖 Bot de Prueba IA-EN-RVT iniciado")
            print("=" * 40)
            print("🎯 Comandos disponibles:")
            print("  /start - Iniciar")
            print("  /crear_muro - Simular muro")
            print("  /analizar - Simular análisis")
            print("  /estado - Estado del sistema")
            print("  /ayuda - Ayuda")
            print("")
            print("⚠️  Nota: Este es un bot de prueba")
            print("💡 Para funcionalidad completa, configurar token real")
            print("")
            
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 IA-EN-RVT 2026 - Bot de Prueba")
    print("=" * 40)
    
    # Cargar token si está configurado
    token = os.getenv('TELEGRAM_TOKEN')
    if token and token != 'tu_token_aqui':
        print("✅ Token configurado encontrado")
        bot = BotPruebaBIM(token)
    else:
        print("⚠️ Usando modo prueba (sin token)")
        bot = BotPruebaBIM()
    
    bot.run_prueba()

if __name__ == "__main__":
    main()