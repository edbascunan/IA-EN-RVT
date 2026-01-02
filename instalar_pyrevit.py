#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Instalador PYREVIT
===================================

Script para instalar la extensión IA-EN-RVT en PYREVIT
Autor: Eduardo Bascuñán
"""

import os
import shutil
import sys
from pathlib import Path

def encontrar_pyrevit_path():
    """Encontrar ruta de instalación de PYREVIT"""
    posibles_paths = [
        r"C:\Users\%s\AppData\Roaming\pyRevit\Extensions" % os.getenv('USERNAME', ''),
        r"C:\ProgramData\pyRevit\Extensions",
        r"C:\pyRevit\Extensions"
    ]
    
    for path in posibles_paths:
        if os.path.exists(path):
            return path
    
    return None

def instalar_extension():
    """Instalar extensión IA-EN-RVT en PYREVIT"""
    print("🏗️ IA-EN-RVT 2026 - Instalador PYREVIT")
    print("=" * 50)
    
    # Ruta de la extensión
    extension_source = r"C:\edbascunan\IA-EN-RVT\pyrevit_extension"
    pyrevit_extensions_path = encontrar_pyrevit_path()
    
    if not pyrevit_extensions_path:
        print("❌ No se encontró PYREVIT instalado")
        print("📥 Descarga e instala PYREVIT desde: https://github.com/eirannejad/pyRevit/releases")
        return False
    
    print(f"📁 PYREVIT Extensions Path: {pyrevit_extensions_path}")
    
    # Ruta de destino
    extension_dest = os.path.join(pyrevit_extensions_path, "IaEnRvt.extension")
    
    try:
        # Crear directorio si no existe
        os.makedirs(extension_dest, exist_ok=True)
        
        # Copiar archivos
        if os.path.exists(extension_source):
            print(f"📋 Copiando extensión desde: {extension_source}")
            print(f"📋 Hacia: {extension_dest}")
            
            # Copiar todos los archivos
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
            
            print("\n✅ Extensión IA-EN-RVT instalada correctamente en PYREVIT")
            return True
        else:
            print(f"❌ No se encontró la carpeta de extensión: {extension_source}")
            return False
            
    except Exception as e:
        print(f"❌ Error instalando extensión: {str(e)}")
        return False

def verificar_instalacion():
    """Verificar que la instalación fue exitosa"""
    print("\n🔍 Verificando instalación...")
    
    pyrevit_extensions_path = encontrar_pyrevit_path()
    if not pyrevit_extensions_path:
        return False
    
    extension_path = os.path.join(pyrevit_extensions_path, "IaEnRvt.extension")
    
    if os.path.exists(extension_path):
        print("✅ Extensión encontrada")
        
        # Verificar archivos importantes
        archivos_importantes = [
            "IaEnRvt.extension",
            "IaEnRvt.tab/Panel 1.stack/Muro Zuko.pushbutton/Muro Zuko.py",
            "IaEnRvt.tab/Panel 1.stack/Muro Zuko.pushbutton/config.yaml"
        ]
        
        for archivo in archivos_importantes:
            archivo_path = os.path.join(extension_path, archivo)
            if os.path.exists(archivo_path):
                print(f"  ✅ {archivo}")
            else:
                print(f"  ❌ {archivo}")
        
        return True
    else:
        print("❌ Extensión no encontrada")
        return False

def mostrar_instrucciones():
    """Mostrar instrucciones de uso"""
    print("\n🚀 INSTRUCCIONES DE USO:")
    print("=" * 50)
    print("1. 📂 Abrir Revit 2026")
    print("2. 🔄 Recargar extensiones PYREVIT (pyRevit > Extensions > Reload)")
    print("3. 🏗️ Buscar la pestaña 'IaEnRvt' en la cinta de Revit")
    print("4. 🤖 Hacer clic en 'Zuko' para ejecutar comandos del bot")
    print("5. 💬 Usar comandos de Telegram para enviar tareas a Revit")
    print("\n💡 Comandos útiles:")
    print("   • /start - Iniciar bot")
    print("   • /crear_muro 0 0 5 0 3.5 - Crear muro")
    print("   • /analizar - Analizar modelo")
    print("   • /status - Ver estado del sistema")

if __name__ == "__main__":
    if instalar_extension():
        if verificar_instalacion():
            mostrar_instrucciones()
        else:
            print("❌ Verificación falló")
    else:
        print("❌ Instalación falló")