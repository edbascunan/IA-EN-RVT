#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Instalador Automático Completo
===============================================

Instala TODO automáticamente:
1. PYREVIT
2. Extensión IA-EN-RVT
3. Bot NLP Real
4. Configuración completa

Autor: Eduardo Bascuñán
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

def print_header():
    """Mostrar header del instalador"""
    print("🏗️" + "=" * 60)
    print("    IA-EN-RVT 2026 - INSTALADOR AUTOMÁTICO COMPLETO")
    print("    Bot NLP Real con OpenAI + PYREVIT + Railway")
    print("=" * 70)
    print()

def verificar_python():
    """Verificar versión de Python"""
    print("🔍 Verificando Python...")
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def verificar_pyrevit():
    """Verificar si PYREVIT está instalado"""
    print("\n🔍 Verificando PYREVIT...")
    
    posibles_paths = [
        r"C:\Users\%s\AppData\Roaming\pyRevit\Extensions" % os.getenv('USERNAME', ''),
        r"C:\ProgramData\pyRevit\Extensions",
        r"C:\pyRevit\Extensions"
    ]
    
    for path in posibles_paths:
        if os.path.exists(path):
            print(f"✅ PYREVIT encontrado en: {path}")
            return path
    
    print("❌ PYREVIT no encontrado")
    return None

def instalar_pyrevit():
    """Instalar PYREVIT si no está presente"""
    print("\n📥 Instalando PYREVIT...")
    
    # URL de descarga
    pyrevit_url = "https://github.com/eirannejad/pyRevit/releases/download/v4.8.18/pyRevit_4.8.18.exe"
    
    print("📋 Para instalar PYREVIT:")
    print(f"   1. Descargar desde: {pyrevit_url}")
    print("   2. Ejecutar el instalador como administrador")
    print("   3. Reiniciar el sistema")
    print("   4. Ejecutar este instalador nuevamente")
    
    respuesta = input("\n❓ ¿Has instalado PYREVIT y reiniciado? (s/n): ").lower()
    return respuesta in ['s', 'si', 'sí', 'y', 'yes']

def instalar_extension_pyrevit():
    """Instalar extensión IA-EN-RVT en PYREVIT"""
    print("\n🏗️ Instalando extensión IA-EN-RVT...")
    
    pyrevit_path = verificar_pyrevit()
    if not pyrevit_path:
        print("❌ No se puede instalar extensión sin PYREVIT")
        return False
    
    # Rutas
    extension_source = os.path.join(os.getcwd(), "pyrevit_extension")
    extension_dest = os.path.join(pyrevit_path, "IaEnRvt.extension")
    
    try:
        # Limpiar instalación anterior
        if os.path.exists(extension_dest):
            print("🧹 Limpiando instalación anterior...")
            shutil.rmtree(extension_dest)
        
        # Copiar archivos
        print(f"📋 Copiando extensión...")
        os.makedirs(extension_dest, exist_ok=True)
        
        archivos_copiados = 0
        for root, dirs, files in os.walk(extension_source):
            for file in files:
                src = os.path.join(root, file)
                rel_path = os.path.relpath(src, extension_source)
                dest = os.path.join(extension_dest, rel_path)
                
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src, dest)
                print(f"  ✅ {rel_path}")
                archivos_copiados += 1
        
        print(f"\n✅ Extensión instalada: {archivos_copiados} archivos")
        return True
        
    except Exception as e:
        print(f"❌ Error instalando extensión: {e}")
        return False

def instalar_dependencias():
    """Instalar dependencias de Python"""
    print("\n📦 Instalando dependencias...")
    
    try:
        # Actualizar pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Instalar dependencias
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def configurar_bot_nlp():
    """Configurar bot con NLP real"""
    print("\n🤖 Configurando bot NLP Real...")
    
    # Verificar que el bot existe
    bot_path = "bot_nlp_real.py"
    if not os.path.exists(bot_path):
        print("❌ Bot NLP Real no encontrado")
        return False
    
    # Verificar archivo .env
    env_path = ".env"
    if not os.path.exists(env_path):
        print("📋 Creando archivo .env...")
        env_content = """# IA-EN-RVT 2026 - Variables de Entorno
# =====================================

# Bot Principal Telegram (Zuko NLP)
TELEGRAM_TOKEN=7537372382:AAF58awLAyaQ4fFpZfdhn88dP555zW9JAGI

# OpenAI API para NLP Real
OPENAI_API_KEY=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

# Configuración adicional
DEBUG=True
LOG_LEVEL=INFO

# Rutas de trabajo
COMMAND_PATH=backend_ai/shared/command_out.json
        """
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
    else:
        print("✅ Archivo .env ya existe")
    
    return True

def probar_instalacion():
    """Probar que todo esté instalado correctamente"""
    print("\n🧪 Probando instalación...")
    
    # Probar PYREVIT
    pyrevit_path = verificar_pyrevit()
    if pyrevit_path:
        extension_path = os.path.join(pyrevit_path, "IaEnRvt.extension")
        if os.path.exists(extension_path):
            print("✅ Extensión PYREVIT OK")
        else:
            print("❌ Extensión PYREVIT no encontrada")
    
    # Probar bot
    if os.path.exists("bot_nlp_real.py"):
        print("✅ Bot NLP Real OK")
    else:
        print("❌ Bot NLP Real no encontrado")
    
    # Probar dependencias
    try:
        import openai
        import telegram
        print("✅ Dependencias Python OK")
    except ImportError as e:
        print(f"❌ Error importando dependencias: {e}")
    
    return True

def mostrar_instrucciones_finales():
    """Mostrar instrucciones finales de uso"""
    print("\n🎉" + "=" * 60)
    print("    INSTALACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print()
    print("🚀 PASOS SIGUIENTES:")
    print()
    print("1. 🏗️ CONFIGURAR REVIT:")
    print("   • Abrir Revit 2026")
    print("   • PYREVIT > Extensions > Reload")
    print("   • Buscar pestaña 'IaEnRvt'")
    print("   • Verificar botón '🤖 IA RVT'")
    print()
    print("2. 🤖 EJECUTAR BOT NLP REAL:")
    print("   cd /edbascunan/IA-EN-RVT")
    print("   python bot_nlp_real.py")
    print()
    print("3. 💬 USAR LENGUAJE NATURAL:")
    print("   • 'Quiero crear un muro de 6 metros'")
    print("   • 'Analiza mi proyecto completo'")
    print("   • 'Ayúdame a organizar el modelo'")
    print("   • '¿Qué problemas ves en mi diseño?'")
    print()
    print("4. 🌐 DESPLIEGUE EN RAILWAY:")
    print("   • El bot está listo para Railway")
    print("   • Usar railway.json para despliegue")
    print("   • Variables ya configuradas")
    print()
    print("🎯 ¡SISTEMA COMPLETO INSTALADO Y LISTO!")
    print()

def main():
    """Función principal del instalador"""
    print_header()
    
    # Verificaciones iniciales
    if not verificar_python():
        return
    
    # Instalar PYREVIT si es necesario
    if not verificar_pyrevit():
        if not instalar_pyrevit():
            print("❌ No se puede continuar sin PYREVIT")
            return
    
    # Instalaciones
    if not instalar_extension_pyrevit():
        print("⚠️ Advertencia: Error instalando extensión PYREVIT")
    
    if not instalar_dependencias():
        print("❌ Error instalando dependencias")
        return
    
    if not configurar_bot_nlp():
        print("❌ Error configurando bot")
        return
    
    # Prueba final
    probar_instalacion()
    
    # Instrucciones finales
    mostrar_instrucciones_finales()

if __name__ == "__main__":
    main()