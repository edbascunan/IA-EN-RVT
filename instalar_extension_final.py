#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Instalador Automático Final
============================================

Instala la extensión pyRevit real que consume bot NLP externo
Sigue la arquitectura correcta: pyRevit consume servicio externo

Autor: Eduardo Bascuñán
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

def log_instalacion(mensaje):
    """Log del proceso de instalación"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] INSTALADOR: {mensaje}")

def encontrar_pyrevit_path():
    """Encontrar ruta de instalación de PYREVIT"""
    username = os.getenv('USERNAME', '')
    posibles_paths = [
        rf"C:\Users\{username}\AppData\Roaming\pyRevit\Extensions",
        r"C:\ProgramData\pyRevit\Extensions",
        r"C:\pyRevit\Extensions"
    ]
    
    for path in posibles_paths:
        if os.path.exists(path):
            return path
    
    return None

def instalar_extension_real():
    """Instalar extensión IA-EN-RVT real en PYREVIT"""
    print("🏗️ IA-EN-RVT 2026 - Instalador Automático Final")
    print("=" * 60)
    
    # Rutas
    extension_source = os.path.abspath(r"pyrevit_extension_real")
    pyrevit_extensions_path = encontrar_pyrevit_path()
    
    if not pyrevit_extensions_path:
        print("❌ No se encontró PYREVIT instalado")
        print("📥 Descarga e instala PYREVIT desde: https://github.com/eirannejad/pyRevit/releases")
        return False
    
    print(f"📁 PYREVIT Extensions Path: {pyrevit_extensions_path}")
    
    # Ruta de destino
    extension_dest = os.path.join(pyrevit_extensions_path, "IaEnRvt.extension")
    
    try:
        # Limpiar instalación anterior si existe
        if os.path.exists(extension_dest):
            print("🧹 Limpiando instalación anterior...")
            shutil.rmtree(extension_dest)
        
        # Crear directorio si no existe
        os.makedirs(extension_dest, exist_ok=True)
        
        # Verificar archivos fuente
        if not os.path.exists(extension_source):
            print(f"❌ No se encontró la carpeta de extensión: {extension_source}")
            return False
        
        print(f"📋 Instalando extensión desde: {extension_source}")
        print(f"📋 Hacia: {extension_dest}")
        
        # Copiar archivos
        archivos_copiados = 0
        for root, dirs, files in os.walk(extension_source):
            for file in files:
                src = os.path.join(root, file)
                rel_path = os.path.relpath(src, extension_source)
                dest = os.path.join(extension_dest, rel_path)
                
                # Crear directorio si no existe
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                
                # Copiar archivo
                shutil.copy2(src, dest)
                print(f"  ✅ {rel_path}")
                archivos_copiados += 1
        
        print(f"\n✅ Extensión IA-EN-RVT instalada correctamente")
        print(f"📊 Archivos copiados: {archivos_copiados}")
        print(f"🤖 Botón disponible: '🤖 IA RVT' en pestaña 'IaEnRvt'")
        print(f"🌐 Consume bot NLP externo (OpenAI)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error instalando extensión: {str(e)}")
        return False

def verificar_instalacion_real():
    """Verificar que la instalación real fue exitosa"""
    print("\n🔍 Verificando instalación real...")
    
    pyrevit_extensions_path = encontrar_pyrevit_path()
    if not pyrevit_extensions_path:
        return False
    
    extension_path = os.path.join(pyrevit_extensions_path, "IaEnRvt.extension")
    
    if os.path.exists(extension_path):
        print("✅ Extensión encontrada")
        
        # Verificar archivos importantes
        archivos_importantes = [
            "IaEnRvt.extension",
            "IaEnRvt.tab/Bot.panel/Bot.panel",
            "IaEnRvt.tab/Bot.panel/Bot.pushbutton/Bot.pushbutton",
            "IaEnRvt.tab/Bot.panel/Bot.pushbutton/Bot.py"
        ]
        
        todos_presentes = True
        for archivo in archivos_importantes:
            archivo_path = os.path.join(extension_path, archivo)
            if os.path.exists(archivo_path):
                print(f"  ✅ {archivo}")
            else:
                print(f"  ❌ {archivo}")
                todos_presentes = False
        
        if todos_presentes:
            print("\n🎉 INSTALACIÓN EXITOSA")
            print("🤖 El botón '🤖 IA RVT' aparecerá en la pestaña 'IaEnRvt'")
            print("🧠 Bot NLP consume servicio externo con OpenAI")
            print("🌐 Arquitectura correcta: pyRevit → Bot → OpenAI")
            return True
        else:
            print("\n❌ Instalación incompleta")
            return False
    else:
        print("❌ Extensión no encontrada")
        return False

def mostrar_instrucciones_finales():
    """Mostrar instrucciones finales de uso"""
    print("\n🚀 INSTRUCCIONES FINALES - ARQUITECTURA CORRECTA:")
    print("=" * 60)
    print()
    print("1. 🤖 BOT NLP AUTÓNOMO (DEPLOY EN RAILWAY):")
    print("   cd bot_nlp_autonomo")
    print("   # Configurar OPENAI_API_KEY en .env")
    print("   # Deploy con Railway: railway.app")
    print()
    print("2. 🏗️ USAR EN REVIT:")
    print("   • Abrir Revit 2026")
    print("   • PYREVIT > Extensions > Reload")
    print("   • Buscar pestaña 'IaEnRvt'")
    print("   • Hacer clic en botón '🤖 IA RVT'")
    print()
    print("3. 💬 FUNCIONALIDAD:")
    print("   • Escribir comandos en lenguaje natural")
    print("   • pyRevit envía comando a bot NLP externo")
    print("   • Bot procesa con OpenAI GPT-4")
    print("   • Respuesta mostrada en Revit")
    print()
    print("4. 📝 EJEMPLOS DE COMANDOS:")
    print("   • 'Crear un muro desde 0,0 hasta 5,0 altura 3.0'")
    print("   • 'Analizar elementos del proyecto'")
    print("   • '¿Cómo cuantifico elementos en Revit?'")
    print("   • 'Ayuda con modelado BIM'")
    print()
    print("5. ✅ VERIFICAR ARQUITECTURA:")
    print("   • Botón '🤖 IA RVT' visible en Revit")
    print("   • pyRevit consume servicio externo")
    print("   • OpenAI procesa lenguaje natural")
    print("   • Respuestas inteligentes en Revit")

if __name__ == "__main__":
    if instalar_extension_real():
        if verificar_instalacion_real():
            mostrar_instrucciones_finales()
            print("\n🎉 ¡INSTALACIÓN COMPLETADA CON ÉXITO!")
            print("\n✅ ARQUITECTURA CORRECTA IMPLEMENTADA:")
            print("   pyRevit → Bot NLP → OpenAI → Respuesta")
        else:
            print("❌ Verificación falló")
    else:
        print("❌ Instalación falló")
        
    print("\nPresiona Enter para salir...")
    try:
        input()
    except:
        pass