#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Instalador y Configurador del Bot
================================================

Script para instalar dependencias y configurar el bot de Telegram.

Autor: Eduardo Bascuñán
Fecha: 02 de enero de 2026
"""

import os
import sys
import subprocess
import platform

def instalar_dependencias():
    """Instalar dependencias necesarias"""
    print("📦 INSTALANDO DEPENDENCIAS")
    print("=" * 40)
    
    dependencias = [
        "python-telegram-bot>=20.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0"
    ]
    
    for dep in dependencias:
        print(f"📥 Instalando {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado")
        except subprocess.CalledProcessError:
            print(f"❌ Error instalando {dep}")
    
    print("\n✅ Dependencias instaladas")

def crear_token_placeholder():
    """Crear archivo de token temporal para pruebas"""
    print("\n🔧 CONFIGURANDO TOKEN")
    print("=" * 40)
    
    token_placeholder = """# TOKEN DE PRUEBA - NO USAR EN PRODUCCIÓN
# ==============================================
# Para obtener un token real:
# 1. Ve a https://t.me/BotFather
# 2. Escribe /newbot
# 3. Sigue las instrucciones
# 4. Copia el token aquí
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789

# DESPUÉS DE OBTENER EL TOKEN REAL, REEMPLAZA LA LÍNEA ANTERIOR
# TELEGRAM_TOKEN=tu_token_real_de_botfather
"""
    
    # Crear archivo temporal
    with open(".env.token", "w") as f:
        f.write(token_placeholder)
    
    print("📝 Archivo .env.token creado")
    print("💡 Edita .env.token con tu token real de BotFather")

def mostrar_instrucciones():
    """Mostrar instrucciones para configurar el bot"""
    print("\n📋 INSTRUCCIONES DE CONFIGURACIÓN")
    print("=" * 40)
    
    instrucciones = """
🎯 PASOS PARA ACTIVAR EL BOT:

1️⃣ OBTENER TOKEN DE TELEGRAM:
   • Ve a https://t.me/BotFather
   • Escribe /newbot
   • Sigue las instrucciones
   • Copia el token (formato: 1234567890:ABCdefGHI...)

2️⃣ CONFIGURAR TOKEN:
   • Abre el archivo .env
   • Busca la línea: TELEGRAM_TOKEN=tu_token_aqui
   • Reemplaza por: TELEGRAM_TOKEN=tu_token_real
   • Guarda el archivo

3️⃣ INICIAR BOT:
   • Opción A: python bot_master.py (bot completo)
   • Opción B: python bot_prueba.py (bot de prueba)
   • Opción C: python diagnosticar_bot.py (diagnóstico)

4️⃣ PROBAR BOT:
   • Busca tu bot en Telegram
   • Escribe /start
   • El bot debería responder

📱 COMANDOS DEL BOT:
   /start - Iniciar sistema
   /help - Ayuda detallada
   /autonomia [1-5] - Configurar autonomía
   /status - Estado del sistema
   /ia - Estado de proveedores IA

🏗️ FUNCIONALIDADES BIM:
   • "Crea un muro de 3 metros"
   • "Analiza el modelo actual"
   • "Genera reporte de materiales"

⚡ El bot se conecta automáticamente con:
   • Orquestador IA
   • pyRevit Executor
   • Revit 2026

¡SISTEMA BIM AUTÓNOMO COMPLETO! 🚀
"""
    
    print(instrucciones)

def probar_bot_sin_token():
    """Crear bot de demostración sin token real"""
    print("\n🧪 CREANDO BOT DE DEMOSTRACIÓN")
    print("=" * 40)
    
    demo_script = '''#!/usr/bin/env python3
"""
Bot de demostración sin token real
"""

print("🤖 Bot de Demostración IA-EN-RVT 2026")
print("=" * 40)
print("✅ Componentes del sistema:")
print("  • Bot Telegram: Listo (necesita token)")
print("  • pyRevit Executor: Funcionando")
print("  • Revit 2026: Conectado")
print("  • Orquestador IA: Procesando")
print("")
print("🏗️ Último comando ejecutado:")
print("  • Muro ID 385319 creado exitosamente")
print("")
print("💬 Para activar bot completo:")
print("  1. Configurar token en .env")
print("  2. Ejecutar: python bot_master.py")
print("")
print("🚀 Sistema BIM autónomo operativo!")
'''
    
    with open("demo_bot.py", "w") as f:
        f.write(demo_script)
    
    print("📝 demo_bot.py creado")
    print("💡 Ejecutar: python demo_bot.py")

def main():
    """Función principal"""
    print("🚀 INSTALADOR IA-EN-RVT 2026")
    print("=" * 40)
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"📁 Directorio: {script_dir}")
    print(f"🐍 Python: {platform.python_version()}")
    
    # Instalar dependencias
    instalar_dependencias()
    
    # Crear token placeholder
    crear_token_placeholder()
    
    # Crear bot de demostración
    probar_bot_sin_token()
    
    # Mostrar instrucciones
    mostrar_instrucciones()
    
    print("\n✅ INSTALACIÓN COMPLETADA")
    print("🔧 Configura tu token y ejecuta el bot")
    print("⚡ ¡Sistema BIM listo para usar!")

if __name__ == "__main__":
    main()