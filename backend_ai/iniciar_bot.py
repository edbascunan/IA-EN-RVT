#!/usr/bin/env python3
"""
IA-EN-RVT 2026 - Inicio Seguro del Bot
=====================================
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Cargar configuración
load_dotenv()

def main():
    print("🚀 Iniciando Bot IA-EN-RVT 2026...")
    
    token = os.getenv('TELEGRAM_TOKEN')
    if not token or token == 'tu_token_aqui':
        print("❌ Error: Configura TELEGRAM_TOKEN en .env")
        print("📋 Ve a https://t.me/BotFather para crear tu bot")
        return
    
    try:
        # Importar y ejecutar bot
        from bot_master import IARVTBotMaster
        bot = IARVTBotMaster(token)
        bot.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Verifica que todas las dependencias estén instaladas")

if __name__ == "__main__":
    main()
