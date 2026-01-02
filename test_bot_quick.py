#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba rápida del bot IA-EN-RVT
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_bot():
    """Probar que el bot esté funcionando"""
    
    bot_token = os.getenv("TELEGRAM_TOKEN")
    
    if not bot_token:
        print("❌ No se encontró TELEGRAM_TOKEN en .env")
        return
        
    print(f"🤖 Probando bot con token: {bot_token[:20]}...")
    
    # Probar que el bot esté online
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe", timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                bot_data = bot_info['result']
                print(f"✅ Bot '{bot_data['first_name']} (@{bot_data['username']}) está online y funcionando")
                print(f"   ID: {bot_data['id']}")
                print(f"   Soporta inline: {bot_data['supports_inline_queries']}")
                return True
            else:
                print(f"❌ Error del bot: {bot_info}")
        else:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        
    return False

if __name__ == "__main__":
    test_bot()