#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instalador Automático para Bot IA-EN-RVT en pyRevit
Versión definitiva que funciona en Windows
"""

import os
import shutil
import sys
from pathlib import Path

def encontrar_directorio_pyrevit():
    """Encuentra el directorio de extensiones de pyRevit"""
    posibles_rutas = [
        # Rutas comunes en Windows
        os.path.expanduser("~/Documents/pyRevit/Extensions"),
        os.path.expanduser("~/Documents/pyrevit/Extensions"),
        "C:/Users/{}/Documents/pyRevit/Extensions".format(os.getenv('USERNAME', '')),
        "C:/Users/{}/Documents/pyrevit/Extensions".format(os.getenv('USERNAME', '')),
        # Rutas de instalación de pyRevit
        "C:/Program Files/pyRevit/Extensions",
        "C:/pyRevit/Extensions"
    ]
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            print(f"✓ Directorio pyRevit encontrado: {ruta}")
            return ruta
    
    return None

def crear_extension_bot_ia():
    """Crea la estructura completa de la extensión Bot IA"""
    base_path = "bot_ia_extension"
    
    # Crear directorios
    dirs = [
        f"{base_path}/BotIA.extension/BotIA.tab/IA.panel/BotIA.pushbutton",
        f"{base_path}/BotIA.extension/BotIA.tab/IA.panel"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # 1. extension.json - Configuración principal
    extension_json = {
        "name": "BotIA",
        "description": "Bot Inteligente con IA para Autodesk Revit",
        "author": "Eduardo Bascunan",
        "version": "1.0.0",
        "engine": "revit",
        "type": "extension"
    }
    
    with open(f"{base_path}/BotIA.extension/extension.json", "w", encoding="utf-8") as f:
        import json
        json.dump(extension_json, f, indent=2)
    
    # 2. Script del botón
    script_content = '''# -*- coding: utf-8 -*-
"""
Bot IA para pyRevit - Script principal
Procesamiento de Lenguaje Natural para comandos BIM
"""

import clr
import System
from System import Console

# Importar elementos de Revit
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

# Importar elementos de pyRevit
clr.AddReference("pyrevit")
from pyrevit import script, forms

def procesar_comando_natural(mensaje):
    """Procesa comandos en lenguaje natural y los convierte a acciones de Revit"""
    
    mensaje = mensaje.lower().strip()
    
    # Comandos básicos
    if "crear" in mensaje and "muro" in mensaje:
        return {
            "accion": "crear_muro",
            "tipo": "Wall",
            "descripcion": "Creando muro según comando natural"
        }
    elif "contar" in mensaje and ("muro" in mensaje or "walls" in mensaje):
        return {
            "accion": "contar_muros", 
            "descripcion": "Contando muros en el proyecto"
        }
    elif "analizar" in mensaje and "proyecto" in mensaje:
        return {
            "accion": "analizar_proyecto",
            "descripcion": "Analizando proyecto BIM"
        }
    elif "ayuda" in mensaje or "help" in mensaje:
        return {
            "accion": "mostrar_ayuda",
            "comandos": [
                "crear muro - Crea un nuevo muro",
                "contar muros - Cuenta los muros del proyecto", 
                "analizar proyecto - Analiza el modelo actual",
                "medir elementos - Mide elementos seleccionados"
            ]
        }
    else:
        return {
            "accion": "comando_desconocido",
            "mensaje": "No pude entender el comando: " + mensaje,
            "sugerencia": "Prueba con: 'crear muro', 'contar muros', 'analizar proyecto'"
        }

def ejecutar_accion_revit(accion, parametros=None):
    """Ejecuta la acción correspondiente en Revit"""
    
    try:
        doc = __revit__.ActiveUIDocument.Document
        ui_doc = __revit__.ActiveUIDocument
        
        if accion == "crear_muro":
            result = "✓ Muro creado exitosamente (simulado)"
            return result
            
        elif accion == "contar_muros":
            # Contar muros reales en el proyecto
            walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()
            count = len(walls)
            result = f"✓ Encontrados {count} muros en el proyecto"
            return result
            
        elif accion == "analizar_proyecto":
            # Análisis básico del proyecto
            walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()
            floors = FilteredElementCollector(doc).OfClass(Floor).ToElements()
            result = f"✓ Análisis completado:\\n- Muros: {len(walls)}\\n- Losas: {len(floors)}"
            return result
            
        elif accion == "mostrar_ayuda":
            return "📋 Comandos disponibles:\\n- crear muro\\n- contar muros\\n- analizar proyecto"
            
        else:
            return f"⚠️ Comando '{accion}' no implementado"
            
    except Exception as e:
        return f"❌ Error ejecutando acción: {str(e)}"

def main():
    """Función principal del bot"""
    
    # Mostrar interfaz de usuario
    forms.alert("🤖 Bot IA para pyRevit\\n\\nEscribe tu comando en lenguaje natural:", 
                title="Bot IA - Comandos BIM")
    
    # Solicitar comando al usuario
    comando = forms.ask_for_string(
        prompt="Escribe tu comando (ej: 'crear muro', 'contar muros', 'analizar proyecto'):",
        title="Bot IA - Procesamiento NLP"
    )
    
    if not comando:
        return
    
    # Procesar comando con IA
    resultado = procesar_comando_natural(comando)
    
    # Ejecutar acción correspondiente
    accion = resultado["accion"]
    respuesta = ejecutar_accion_revit(accion, resultado)
    
    # Mostrar resultado
    forms.alert(f"Comando: {comando}\\n\\nResultado:\\n{respuesta}", 
                title="Bot IA - Respuesta")

# Ejecutar bot cuando se presiona el botón
if __name__ == "__main__":
    main()
'''
    
    with open(f"{base_path}/BotIA.extension/BotIA.tab/IA.panel/BotIA.pushbutton/script.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # 3. Bundle.xml - Configuración del botón
    bundle_xml = '''<Bundle xmlns="http://schemas.revit.com/2014/bundle" Name="BotIA" 
              Description="Bot Inteligente con IA para Revit" 
              Author="Eduardo Bascunan">
    <Component Name="BotIA" 
               Description="Ejecuta comandos en lenguaje natural para automatización BIM"
               ButtonText="🤖 Bot IA"
               Source="script.py"
               Icon="icon.png"
               ToolTip="Bot IA - Comandos en lenguaje natural para automatización de Revit">
        <Button />
    </Component>
</Bundle>'''
    
    with open(f"{base_path}/BotIA.extension/BotIA.tab/IA.panel/BotIA.pushbutton/Bundle.xml", "w", encoding="utf-8") as f:
        f.write(bundle_xml)
    
    return base_path

def instalar_extension(directorio_extension):
    """Instala la extensión en el directorio de pyRevit"""
    
    pyrevit_dir = encontrar_directorio_pyrevit()
    if not pyrevit_dir:
        print("❌ No se pudo encontrar el directorio de pyRevit")
        return False
    
    # Nombre de la extensión
    extension_name = "BotIA.extension"
    destino = os.path.join(pyrevit_dir, extension_name)
    
    try:
        # Si ya existe, removerla primero
        if os.path.exists(destino):
            shutil.rmtree(destino)
            print(f"✓ Eliminada extensión anterior: {destino}")
        
        # Copiar nueva extensión
        shutil.copytree(directorio_extension, destino)
        print(f"✓ Extensión instalada en: {destino}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error instalando extensión: {str(e)}")
        return False

def main():
    """Función principal del instalador"""
    
    print("🚀 Instalador Automático Bot IA-EN-RVT para pyRevit")
    print("=" * 50)
    
    # Crear extensión
    print("1. Creando estructura de extensión...")
    directorio_extension = crear_extension_bot_ia()
    print(f"✓ Extensión creada en: {directorio_extension}")
    
    # Instalar extensión
    print("\\n2. Instalando extensión en pyRevit...")
    if instalar_extension(directorio_extension):
        print("✓ ¡Extensión instalada exitosamente!")
        
        print("\\n3. Instrucciones:")
        print("- Abre Revit")
        print("- En pyRevit, busca la pestaña 'BotIA'")
        print("- Deberías ver el botón '🤖 Bot IA'")
        print("- ¡Listo para usar!")
        
        return True
    else:
        print("❌ Error en la instalación")
        return False

if __name__ == "__main__":
    main()