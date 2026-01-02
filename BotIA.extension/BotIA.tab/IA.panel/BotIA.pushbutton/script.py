# -*- coding: utf-8 -*-
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
            result = "✓ Encontrados {} muros en el proyecto".format(count)
            return result
            
        elif accion == "analizar_proyecto":
            # Análisis básico del proyecto
            walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()
            floors = FilteredElementCollector(doc).OfClass(Floor).ToElements()
            result = "✓ Análisis completado:\n- Muros: {}\n- Losas: {}".format(len(walls), len(floors))
            return result
            
        elif accion == "mostrar_ayuda":
            return "📋 Comandos disponibles:\n- crear muro\n- contar muros\n- analizar proyecto"
            
        else:
            return "⚠️ Comando '{}' no implementado".format(accion)
            
    except Exception as e:
        return "❌ Error ejecutando acción: {}".format(str(e))

def main():
    """Función principal del bot"""
    
    # Mostrar interfaz de usuario
    forms.alert("🤖 Bot IA para pyRevit\n\nEscribe tu comando en lenguaje natural:", 
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
    forms.alert("Comando: {}\n\nResultado:\n{}".format(comando, respuesta), 
                title="Bot IA - Respuesta")

# Ejecutar bot cuando se presiona el botón
if __name__ == "__main__":
    main()