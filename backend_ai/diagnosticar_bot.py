#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Diagnóstico del Bot de Telegram
===============================================

Script para diagnosticar y resolver problemas del bot.

Autor: Eduardo Bascuñán
Fecha: 02 de enero de 2026
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def verificar_configuracion():
    """Verificar configuración del bot"""
    print("🔍 DIAGNÓSTICO DEL BOT IA-EN-RVT 2026")
    print("=" * 50)
    
    # Verificar token
    token = os.getenv('TELEGRAM_TOKEN')
    print(f"📱 TELEGRAM_TOKEN: {'✅ Configurado' if token and token != 'tu_token_aqui' else '❌ No configurado'}")
    
    if not token:
        print("\n⚠️ PROBLEMA: Token no configurado")
        print("📋 Pasos para configurar:")
        print("1. Ve a https://t.me/BotFather")
        print("2. Crea un bot con /newbot")
        print("3. Copia el token")
        print("4. Edita el archivo .env")
        print("5. Cambia: TELEGRAM_TOKEN=tu_token_aqui")
        print("   Por: TELEGRAM_TOKEN=tu_token_real")
        return False
    
    # Verificar token válido
    if token == 'tu_token_aqui':
        print("\n⚠️ PROBLEMA: Token es placeholder")
        print("📋 Debes obtener un token real de BotFather")
        return False
    
    # Verificar directorios
    dirs_to_check = [
        "shared",
        "logs", 
        "audio",
        "vision",
        "rag"
    ]
    
    print("\n📁 DIRECTORIOS:")
    for dir_name in dirs_to_check:
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        if os.path.exists(dir_path):
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ (crear)")
            os.makedirs(dir_path, exist_ok=True)
    
    # Verificar archivos clave
    archivos_clave = [
        "bot_master.py",
        "orchestrator.py", 
        "ai_providers.py"
    ]
    
    print("\n📄 ARCHIVOS CLAVE:")
    for archivo in archivos_clave:
        if os.path.exists(archivo):
            print(f"  ✅ {archivo}")
        else:
            print(f"  ❌ {archivo} (faltante)")
    
    print("\n🧠 PROVEEDORES DE IA:")
    # Verificar APIs configuradas
    apis = {
        "DEEPSEEK": os.getenv('DEEPSEEK_API_KEY'),
        "GROK": os.getenv('GROK_API_KEY'), 
        "MINIMAX": os.getenv('MINIMAX_API_KEY'),
        "CLAUDE": os.getenv('CLAUDE_API_KEY'),
        "OPENAI": os.getenv('OPENAI_API_KEY')
    }
    
    for nombre, key in apis.items():
        if key and key != f'tu_{nombre.lower()}_key':
            print(f"  ✅ {nombre}")
        else:
            print(f"  ⚠️ {nombre} (no configurado)")
    
    print("\n" + "=" * 50)
    return True

def crear_script_inicio():
    """Crear script de inicio seguro"""
    script_content = '''#!/usr/bin/env python3
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
'''
    
    with open("iniciar_bot.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("📝 Script de inicio creado: iniciar_bot.py")

def main():
    """Función principal"""
    # Cambiar al directorio del bot
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    if verificar_configuracion():
        print("\n✅ CONFIGURACIÓN CORRECTA")
        crear_script_inicio()
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Configura tu token de Telegram en .env")
        print("2. Ejecuta: python iniciar_bot.py")
        print("3. El bot debería responder a comandos")
        print("\n⚡ ¡Listo para usar!")
    else:
        print("\n❌ CONFIGURACIÓN INCOMPLETA")
        print("\n🔧 RESUELVE LOS PROBLEMAS ARRIBA Y VUELVE A EJECUTAR")

if __name__ == "__main__":
    main()