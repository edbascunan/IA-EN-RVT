#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Ejecutor del Bot Telegram con NLP Real
====================================================

Script para ejecutar el bot de Telegram con NLP funcional
Incluye verificación de configuración y modo de prueba

Autor: Eduardo Bascuñán
Fecha: 01 de febrero de 2026
"""

import os
import sys
import subprocess
from pathlib import Path

def verificar_dependencias():
    """Verificar que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    dependencias = [
        ('python-telegram-bot', 'python-telegram-bot'),
        ('openai', 'openai'),
        ('python-dotenv', 'python-dotenv')
    ]
    
    faltantes = []
    
    for nombre_pip, nombre_python in dependencias:
        try:
            __import__(nombre_python)
            print(f"✅ {nombre_pip} instalado")
        except ImportError:
            print(f"❌ {nombre_pip} NO instalado")
            faltantes.append(nombre_pip)
    
    if faltantes:
        print(f"\n💡 Para instalar las dependencias faltantes:")
        print(f"pip install {' '.join(faltantes)}")
        return False
    
    return True

def verificar_configuracion():
    """Verificar configuración del bot"""
    print("\n🔧 Verificando configuración...")
    
    # Variables de entorno que se pueden configurar
    variables = {
        'TELEGRAM_TOKEN': 'Token del bot de Telegram',
        'OPENAI_API_KEY': 'API Key de OpenAI (opcional)',
        'COMMAND_PATH': 'Ruta del archivo de comandos JSON'
    }
    
    configurado = False
    
    for var, descripcion in variables.items():
        valor = os.getenv(var)
        if valor:
            # Mostrar parcialmente por seguridad
            valor_seguro = valor[:10] + "..." if len(valor) > 10 else valor
            print(f"✅ {var}: {valor_seguro}")
            configurado = True
        else:
            print(f"⚠️ {var}: No configurado (usando valor por defecto)")
    
    return configurado

def crear_archivo_env():
    """Crear archivo .env de ejemplo"""
    print("\n📝 Creando archivo .env de ejemplo...")
    
    env_content = """# IA-EN-RVT Bot Telegram - Configuración
# Copia este archivo a .env y completa con tus valores

# Token del bot de Telegram (OBLIGATORIO)
# Obtener en: https://t.me/BotFather
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# API Key de OpenAI (OPCIONAL - para NLP real)
# Obtener en: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-1234567890abcdef

# Ruta del archivo de comandos JSON
COMMAND_PATH=C:\\edbascunan\\IA-EN-RVT\\backend_ai\\command_out.json
"""
    
    try:
        with open('.env.example', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env.example creado")
        return True
    except Exception as e:
        print(f"❌ Error creando .env.example: {e}")
        return False

def ejecutar_bot():
    """Ejecutar el bot de Telegram"""
    print("\n🚀 Ejecutando bot de Telegram...")
    
    bot_file = 'bot_telegram_nlp_funcional.py'
    
    if not os.path.exists(bot_file):
        print(f"❌ No se encuentra el archivo: {bot_file}")
        return False
    
    try:
        # Ejecutar el bot
        print("💬 Iniciando bot de Telegram...")
        print("📱 Busca tu bot en Telegram y envía /start")
        print("🧪 Usa /test para probar comandos NLP")
        print("⏹️  Presiona Ctrl+C para detener")
        print("-" * 50)
        
        subprocess.run([sys.executable, bot_file])
        
    except KeyboardInterrupt:
        print("\n⏹️ Bot detenido por el usuario")
        return True
    except Exception as e:
        print(f"❌ Error ejecutando bot: {e}")
        return False

def mostrar_comandos_prueba():
    """Mostrar comandos de prueba"""
    print("\n🧪 COMANDOS DE PRUEBA:")
    print("1. Abre tu bot en Telegram")
    print("2. Envía /start - Ver mensaje de bienvenida")
    print("3. Envía /help - Ver manual completo")
    print("4. Envía /status - Ver estado del sistema")
    print("5. Envía /test - Ver comandos de prueba")
    print("6. Prueba estos comandos en lenguaje natural:")
    print("   • 'quiero crear un muro'")
    print("   • 'analiza mi proyecto'")
    print("   • 'cuántos muros hay'")
    print("   • 'ayúdame con BIM'")

def main():
    """Función principal"""
    print("🤖 EJECUTOR DEL BOT TELEGRAM IA-EN-RVT")
    print("=" * 50)
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n❌ Dependencias faltantes. Instálalas antes de continuar.")
        return
    
    # Verificar configuración
    configurar = verificar_configuracion()
    
    if not configurar:
        print("\n💡 CONFIGURACIÓN OPCIONAL:")
        print("Para mejor funcionamiento, crea un archivo .env:")
        crear_archivo_env()
        print("Edita .env con tus valores reales y vuelve a ejecutar.")
    
    # Mostrar comandos de prueba
    mostrar_comandos_prueba()
    
    # Preguntar si ejecutar
    print("\n" + "=" * 50)
    respuesta = input("¿Quieres ejecutar el bot ahora? (s/n): ").lower().strip()
    
    if respuesta in ['s', 'sí', 'si', 'y', 'yes']:
        ejecutar_bot()
    else:
        print("💡 Para ejecutar más tarde: python ejecutar_bot_telegram.py")

if __name__ == "__main__":
    main()