#!/usr/bin/env python
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
CONFIG_PATH = r"C:\edbascunan\IA-EN-RVT\backend_ai\config\bot_config.json"
COMMAND_FILE = r"C:\edbascunan\IA-EN-RVT\backend_ai\commands\command_queue.json"
LOG_FILE = r"C:\edbascunan\IA-EN-RVT\backend_ai\logs\pyrevit_execution.log"

def log_message(message):
    """Registrar mensaje en log"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] PYREVIT: {message}\n"
        
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
        bot_script = r"C:\edbascunan\IA-EN-RVT\backend_ai\bot_ia_rvt_inteligente.py"
        
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
    main()