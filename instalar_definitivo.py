#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Instalador Definitivo
======================================

Instala la extensión IaEnRvt en pyRevit con permisos correctos
Resuelve TODOS los problemas identificados en las pruebas

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

def ejecutar_como_admin(comando):
    """Ejecutar comando con permisos administrativos"""
    try:
        result = subprocess.run(['runas', '/user:Administrator', comando], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def crear_estructura_pyrevit():
    """Crear estructura correcta de pyRevit"""
    log_instalacion("Creando estructura de pyRevit...")
    
    # Rutas base
    base_path = Path(r"C:\Users\56968\AppData\Roaming\pyRevit\Extensions\IaEnRvt.extension")
    estructura_base = Path(r"C:\edbascunan\IA-EN-RVT\pyrevit_extension\IaEnRvt.extension")
    
    try:
        # Crear directorios
        directorios = [
            base_path,
            base_path / "IaEnRvt.tab",
            base_path / "IaEnRvt.tab" / "Bot IA.panel",
            base_path / "IaEnRvt.tab" / "Bot IA.pushbutton"
        ]
        
        for directorio in directorios:
            directorio.mkdir(parents=True, exist_ok=True)
            log_instalacion(f"✅ Creado: {directorio}")
        
        # Crear archivo .extension
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
        
        with open(base_path / "IaEnRvt.extension", 'w', encoding='utf-8') as f:
            f.write(extension_content)
        log_instalacion("✅ Creado: IaEnRvt.extension")
        
        # Crear archivo .panel
        panel_content = """# Panel Configuration
# ===================

# Name of the panel
name: Bot IA

# Description
description: "Bot inteligente para automatización en Revit"

# Visibility
visibility: true"""
        
        with open(base_path / "IaEnRvt.tab" / "Bot IA.panel", 'w', encoding='utf-8') as f:
            f.write(panel_content)
        log_instalacion("✅ Creado: Bot IA.panel")
        
        # Crear archivo .pushbutton
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
        
        with open(base_path / "IaEnRvt.tab" / "Bot IA.pushbutton" / "Bot IA.pushbutton", 'w', encoding='utf-8') as f:
            f.write(pushbutton_content)
        log_instalacion("✅ Creado: Bot IA.pushbutton")
        
        # Crear script .py
        script_content = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Script del Bot para pyRevit
============================================

Script principal que ejecuta el bot inteligente desde pyRevit
Se conecta con el backend para procesar comandos de IA
Autor: Eduardo Bascuñán
"""

import clr
import sys
import os
import json
import subprocess
from datetime import datetime

# Importar librerías de Revit
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# Configuración del bot
CONFIG_PATH = r"C:\\edbascunan\\IA-EN-RVT\\backend_ai\\config\\bot_config.json"
COMMAND_FILE = r"C:\\edbascunan\\IA-EN-RVT\\backend_ai\\commands\\command_queue.json"
LOG_FILE = r"C:\\edbascunan\\IA-EN-RVT\\backend_ai\\logs\\pyrevit_execution.log"

def log_message(message):
    """Registrar mensaje en log"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] PYREVIT: {message}\\n"
        
        # Crear directorio de logs si no existe
        log_dir = os.path.dirname(LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except:
        pass  # No fallar si no se puede escribir log

def execute_bot_command():
    """Ejecutar comando del bot desde pyRevit"""
    try:
        log_message("Iniciando ejecución del bot IA desde pyRevit")
        
        # Verificar archivos de configuración
        if not os.path.exists(CONFIG_PATH):
            log_message(f"Error: No se encontró configuración en {CONFIG_PATH}")
            return False
            
        # Leer configuración
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Determinar el comando a ejecutar
        bot_script = r"C:\\edbascunan\\IA-EN-RVT\\backend_ai\\bot_ia_rvt_inteligente.py"
        
        if not os.path.exists(bot_script):
            log_message(f"Error: No se encontró el bot en {bot_script}")
            return False
        
        # Ejecutar bot
        log_message(f"Ejecutando: {bot_script}")
        result = subprocess.run([sys.executable, bot_script], 
                              capture_output=True, 
                              text=True, 
                              timeout=30)
        
        if result.returncode == 0:
            log_message("Bot ejecutado exitosamente")
            if result.stdout:
                log_message(f"Salida: {result.stdout[:200]}...")
            return True
        else:
            log_message(f"Error ejecutando bot: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        log_message("Error: Timeout ejecutando bot")
        return False
    except Exception as e:
        log_message(f"Error inesperado: {str(e)}")
        return False

def show_notification(message, title="Bot IA RVT"):
    """Mostrar notificación en Revit"""
    try:
        TaskDialog.Show(title, message)
    except:
        print(f"{title}: {message}")

def main():
    """Función principal del script"""
    try:
        # Obtener documento actual
        doc = __revit__.ActiveUIDocument.Document
        ui_doc = __revit__.ActiveUIDocument
        
        # Verificar que hay un documento abierto
        if doc.IsEmpty:
            show_notification("Por favor, abre un proyecto de Revit antes de usar el bot.", 
                            "Bot IA RVT")
            return
        
        log_message(f"Documento actual: {doc.Title}")
        
        # Ejecutar bot
        success = execute_bot_command()
        
        if success:
            message = """🤖 Bot IA RVT iniciado exitosamente

✅ El bot está procesando comandos
📱 Usa Telegram para enviar instrucciones
🧠 IA procesa lenguaje natural automáticamente

Ejemplos de comandos:
• "Crear muro desde 0,0 hasta 5,0 altura 3.5"
• "Analizar elementos del proyecto"
• "Mostrar estadísticas del modelo"
"""
            show_notification(message, "Bot IA RVT")
        else:
            error_message = """❌ Error iniciando Bot IA RVT

Verificar:
1. Bot backend está ejecutándose
2. Archivos de configuración existen
3. Permisos de acceso a archivos

Revisar logs para más detalles."""
            show_notification(error_message, "Bot IA RVT - Error")
            
    except Exception as e:
        log_message(f"Error en función main: {str(e)}")
        show_notification(f"Error ejecutando bot: {str(e)}", "Bot IA RVT - Error")

# Ejecutar script
if __name__ == "__main__":
    main()'''
        
        with open(base_path / "IaEnRvt.tab" / "Bot IA.pushbutton" / "Bot IA.py", 'w', encoding='utf-8') as f:
            f.write(script_content)
        log_instalacion("✅ Creado: Bot IA.py")
        
        log_instalacion("🎉 Estructura de pyRevit creada exitosamente")
        return True
        
    except Exception as e:
        log_instalacion(f"❌ Error creando estructura: {str(e)}")
        return False

def verificar_instalacion():
    """Verificar que la instalación es correcta"""
    log_instalacion("Verificando instalación...")
    
    base_path = Path(r"C:\Users\56968\AppData\Roaming\pyRevit\Extensions\IaEnRvt.extension")
    
    archivos_requeridos = [
        "IaEnRvt.extension",
        "IaEnRvt.tab/Bot IA.panel",
        "IaEnRvt.tab/Bot IA.pushbutton/Bot IA.pushbutton",
        "IaEnRvt.tab/Bot IA.pushbutton/Bot IA.py"
    ]
    
    todos_ok = True
    for archivo in archivos_requeridos:
        archivo_path = base_path / archivo
        if archivo_path.exists():
            log_instalacion(f"✅ {archivo}")
        else:
            log_instalacion(f"❌ {archivo} - NO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def main():
    """Función principal"""
    print("🏗️ IA-EN-RVT 2026 - Instalador Definitivo")
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
        else:
            print("\n❌ Verificación falló")
    else:
        print("\n❌ Instalación falló")

if __name__ == "__main__":
    main()