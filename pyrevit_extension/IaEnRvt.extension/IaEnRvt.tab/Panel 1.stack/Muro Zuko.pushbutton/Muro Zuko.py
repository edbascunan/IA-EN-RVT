# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Bot Zuko PYREVIT Script
========================================

Script para ejecutar comandos del Bot Zuko en Revit usando PYREVIT
Autor: Eduardo Bascuñán
"""

import clr
import os
import json
import sys
from datetime import datetime

# Referencias a Revit API
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.Exceptions import *

# Configuración
SCRIPT_DIR = os.path.dirname(__file__)
COMMAND_PATH = r"C:\edbascunan\IA-EN-RVT\backend_ai\shared\command_out.json"

# Obtener documento activo
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

def metros_a_pies(metros):
    """Convertir metros a pies"""
    return metros / 0.3048

def get_level():
    """Obtener primer nivel disponible"""
    collector = FilteredElementCollector(doc).OfClass(Level)
    levels = list(collector)
    if levels:
        return levels[0]
    return None

def get_wall_type():
    """Obtener primer tipo de muro disponible"""
    collector = FilteredElementCollector(doc).OfClass(WallType)
    wall_types = list(collector)
    for wt in wall_types:
        if wt.Kind == WallKind.Basic:
            return wt
    return wall_types[0] if wall_types else None

def crear_muro(payload):
    """Crear muro en Revit"""
    level = get_level()
    wall_type = get_wall_type()
    
    if not level:
        TaskDialog.Show("IA-EN-RVT", "ERROR: No hay niveles en el modelo")
        return None
    
    if not wall_type:
        TaskDialog.Show("IA-EN-RVT", "ERROR: No hay tipos de muro")
        return None
    
    # Coordenadas
    inicio = payload.get("inicio", {"x": 0, "y": 0})
    fin = payload.get("fin", {"x": 5, "y": 0})
    
    x1 = metros_a_pies(inicio.get("x", 0))
    y1 = metros_a_pies(inicio.get("y", 0))
    x2 = metros_a_pies(fin.get("x", 5))
    y2 = metros_a_pies(fin.get("y", 0))
    
    altura = metros_a_pies(payload.get("altura_m", 3.0))
    
    # Crear línea
    punto_inicio = XYZ(x1, y1, 0)
    punto_fin = XYZ(x2, y2, 0)
    linea = Line.CreateBound(punto_inicio, punto_fin)
    
    # Crear muro con transacción
    try:
        t = Transaction(doc, "IA_RVT - Crear Muro Zuko")
        t.Start()
        
        wall = Wall.Create(doc, linea, wall_type.Id, level.Id, altura, 0, False, False)
        
        t.Commit()
        
        # Mostrar resultado
        TaskDialog.Show(
            "IA-EN-RVT", 
            f"✅ MURO CREADO EXITOSAMENTE\n\n"
            f"ID del muro: {wall.Id}\n"
            f"Coordenadas: ({inicio['x']}, {inicio['y']}) → ({fin['x']}, {fin['y']})\n"
            f"Altura: {payload.get('altura_m', 3.0)}m\n"
            f"Tipo: {wall_type.Name}"
        )
        
        return wall
        
    except Exception as e:
        t.RollBack()
        TaskDialog.Show("IA-EN-RVT", f"ERROR creando muro: {str(e)}")
        return None

def analizar_modelo():
    """Analizar modelo actual"""
    try:
        muros = FilteredElementCollector(doc).OfClass(Wall).GetElementCount()
        niveles = FilteredElementCollector(doc).OfClass(Level).GetElementCount()
        puertas = FilteredElementCollector(doc).OfClass(FamilyInstance).Where(lambda x: x.Category.Name == "Puertas").GetElementCount()
        ventanas = FilteredElementCollector(doc).OfClass(FamilyInstance).Where(lambda x: x.Category.Name == "Ventanas").GetElementCount()
        
        resultado = f"""🔍 ANÁLISIS DEL MODELO REVIT

📊 ELEMENTOS ENCONTRADOS:
• Muros: {muros}
• Niveles: {niveles}
• Puertas: {puertas}
• Ventanas: {ventanas}

🤖 Sistema: IA-EN-RVT 2026
📅 Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """
        
        TaskDialog.Show("IA-EN-RVT - Análisis", resultado)
        
    except Exception as e:
        TaskDialog.Show("IA-EN-RVT", f"ERROR en análisis: {str(e)}")

def ejecutar_comando():
    """Ejecutar comando desde archivo JSON"""
    try:
        if not os.path.exists(COMMAND_PATH):
            TaskDialog.Show("IA-EN-RVT", "No hay comando pendiente.\nRuta: " + COMMAND_PATH)
            return
        
        # Leer comando
        with open(COMMAND_PATH, "r", encoding='utf-8') as f:
            comando = json.load(f)
        
        accion = comando.get("accion", "")
        elemento = comando.get("elemento", "")
        payload = comando.get("payload", {})
        
        TaskDialog.Show("IA-EN-RVT", f"Procesando comando:\n\nAcción: {accion}\nElemento: {elemento}\nPayload: {str(payload)}")
        
        # Ejecutar según acción
        if accion == "CREATE" and elemento == "Wall":
            crear_muro(payload)
        elif accion in ["ANALYZE", "QUERY"]:
            analizar_modelo()
        else:
            TaskDialog.Show("IA-EN-RVT", f"Acción no soportada: {accion}")
        
        # Marcar como ejecutado
        comando["estado"] = "EJECUTADO"
        comando["ejecutado_en"] = datetime.now().isoformat()
        
        with open(COMMAND_PATH, "w", encoding='utf-8') as f:
            json.dump(comando, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        TaskDialog.Show("IA-EN-RVT", f"ERROR ejecutando comando: {str(e)}")

def crear_muro_rapido():
    """Crear muro rápido como prueba"""
    payload = {
        "inicio": {"x": 0, "y": 0},
        "fin": {"x": 4, "y": 0},
        "altura_m": 3.2
    }
    
    wall = crear_muro(payload)
    if wall:
        TaskDialog.Show("IA-EN-RVT", f"✅ Muro rápido creado con ID: {wall.Id}")

# ========== EJECUCIÓN PRINCIPAL ==========

def main():
    """Función principal"""
    TaskDialog.Show("IA-EN-RVT 2026", """
🤖 IA-EN-RVT 2026 - Bot Zuko en PYREVIT

Opciones disponibles:
• Ejecutar comando del bot
• Crear muro rápido
• Analizar modelo

El sistema está conectado y listo.
    """)
    
    # Por defecto ejecutar comando pendiente
    ejecutar_comando()

# Ejecutar script
main()