#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Instalador Definitivo CORREGIDO
================================================

Instala la extensión IaEnRvt en pyRevit con estructura correcta
Resuelve problemas de permisos y estructura

Autor: Eduardo Bascuñán
"""

import os
import shutil
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def log_instalacion(mensaje):
    """Log del proceso de instalación"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] INSTALADOR: {mensaje}")

def crear_estructura_pyrevit():
    """Crear estructura correcta de pyRevit"""
    log_instalacion("Creando estructura de pyRevit...")
    
    # Rutas base
    base_path = Path(r"C:\Users\56968\AppData\Roaming\pyRevit\Extensions\IaEnRvt.extension")
    
    try:
        # Crear directorios CORRECTOS de pyRevit
        directorios = [
            base_path,  # Directorio principal
            base_path / "IaEnRvt.tab",  # Tab
            base_path / "IaEnRvt.tab" / "Bot IA.panel",  # Panel (DIRECTORIO)
            base_path / "IaEnRvt.tab" / "Bot IA.pushbutton",  # PushButton (DIRECTORIO)
        ]
        
        for directorio in directorios:
            directorio.mkdir(parents=True, exist_ok=True)
            log_instalacion(f"✅ Creado directorio: {directorio.name}")
        
        # Crear archivos de configuración
        # 1. Archivo .extension (en directorio raíz)
        extension_content = """# IA-EN-RVT Extension
# ====================

# Name of the tab in pyRevit
name: IA-EN-RVT

# Description
description: "Bot inteligente para automatización en Revit con IA"

# Author
author: Eduardo Bascuñán

# Version
version: 1.0.0

# Minimum pyRevit version
min_pyrevit_version: 4.8.0

# Help URL
help_url: https://github.com/edbascunan/IA-EN-RVT"""
        
        extension_file = base_path / "IaEnRvt.extension"
        with open(extension_file, 'w', encoding='utf-8') as f:
            f.write(extension_content)
        log_instalacion("✅ Creado archivo: IaEnRvt.extension")
        
        # 2. Archivo .panel (dentro del directorio del panel)
        panel_content = """# Panel Configuration
# ===================

# Name of the panel
name: Bot IA

# Description
description: "Bot inteligente para automatización en Revit"

# Visibility
visibility: true"""
        
        panel_file = base_path / "IaEnRvt.tab" / "Bot IA.panel" / "Bot IA.panel"
        with open(panel_file, 'w', encoding='utf-8') as f:
            f.write(panel_content)
        log_instalacion("✅ Creado archivo: Bot IA.panel (dentro del directorio)")
        
        # 3. Archivo .pushbutton (dentro del directorio del pushbutton)
        pushbutton_content = """# Bot IA PushButton Configuration
# ===============================

# Name of the button
name: 🤖 IA RVT

# Description
description: "Bot inteligente para automatización en Revit"

# Tooltip
tooltip: "Iniciar bot de IA para automatización de Revit"

# Author
author: Eduardo Bascuñán

# Min version
min_revit_version: 2024

# Execution type
execution_type: Manual"""
        
        pushbutton_file = base_path / "IaEnRvt.tab" / "Bot IA.pushbutton" / "Bot IA.pushbutton"
        with open(pushbutton_file, 'w', encoding='utf-8') as f:
            f.write(pushbutton_content)
        log_instalacion("✅ Creado archivo: Bot IA.pushbutton (dentro del directorio)")
        
        log_instalacion("🎉 Estructura de pyRevit creada exitosamente")
        return True
        
    except Exception as e:
        log_instalacion(f"❌ Error creando estructura: {str(e)}")
        return False

def verificar_instalacion():
    """Verificar que la instalación es correcta"""
    log_instalacion("Verificando instalación...")
    
    base_path = Path(r"C:\Users\56968\AppData\Roaming\pyRevit\Extensions\IaEnRvt.extension")
    
    # Verificar que la estructura es correcta
    estructura_esperada = [
        (base_path / "IaEnRvt.extension", "archivo"),
        (base_path / "IaEnRvt.tab", "directorio"),
        (base_path / "IaEnRvt.tab" / "Bot IA.panel", "directorio"),
        (base_path / "IaEnRvt.tab" / "Bot IA.panel" / "Bot IA.panel", "archivo"),
        (base_path / "IaEnRvt.tab" / "Bot IA.pushbutton", "directorio"),
        (base_path / "IaEnRvt.tab" / "Bot IA.pushbutton" / "Bot IA.pushbutton", "archivo"),
    ]
    
    todos_ok = True
    for ruta, tipo in estructura_esperada:
        if tipo == "directorio":
            if ruta.is_dir():
                log_instalacion(f"✅ Directorio: {ruta.name}")
            else:
                log_instalacion(f"❌ Directorio faltante: {ruta.name}")
                todos_ok = False
        else:  # archivo
            if ruta.is_file():
                log_instalacion(f"✅ Archivo: {ruta.name}")
            else:
                log_instalacion(f"❌ Archivo faltante: {ruta.name}")
                todos_ok = False
    
    return todos_ok

def main():
    """Función principal"""
    print("🏗️ IA-EN-RVT 2026 - Instalador Definitivo CORREGIDO")
    print("=" * 60)
    
    # Crear estructura de pyRevit
    if crear_estructura_pyrevit():
        # Verificar instalación
        if verificar_instalacion():
            print("\n🎉 ¡INSTALACIÓN EXITOSA!")
            print("\n✅ Botón '🤖 IA RVT' aparecerá en pestaña 'IaEnRvt'")
            print("\n🚀 SIGUIENTE PASO:")
            print("1. Abrir Revit 2026")
            print("2. PYREVIT > Extensions > Reload")
            print("3. Buscar pestaña 'IaEnRvt'")
            print("4. Hacer clic en '🤖 IA RVT'")
            
            # Ahora ejecutar prueba final
            print("\n🔍 EJECUTANDO PRUEBA FINAL...")
            os.system("python probar_sistema_completo.py")
        else:
            print("\n❌ Verificación falló")
    else:
        print("\n❌ Instalación falló")

if __name__ == "__main__":
    main()