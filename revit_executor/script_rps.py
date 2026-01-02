# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Script para RevitPythonShell
==============================================

Copia este script completo en RevitPythonShell y ejecútalo.
Lee comandos JSON de command_out.json y los ejecuta en Revit.

Autor: Eduardo Bascuñán
"""

import clr
import json
import os

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# IMPORTANTE: Cambia esta ruta si es diferente
COMMAND_PATH = r"C:\edbascunan\IA-EN-RVT\backend_ai\shared\command_out.json"

# Obtener documento activo
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def metros_a_pies(metros):
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
    for wt in collector:
        if wt.Kind == WallKind.Basic:
            return wt
    wall_types = list(collector)
    if wall_types:
        return wall_types[0]
    return None

def crear_muro(payload):
    """Crear muro en Revit"""
    level = get_level()
    wall_type = get_wall_type()
    
    if not level:
        print("ERROR: No hay niveles en el modelo")
        return
    
    if not wall_type:
        print("ERROR: No hay tipos de muro")
        return
    
    # Coordenadas
    inicio = payload.get("inicio", {"x": 0, "y": 0})
    fin = payload.get("fin", {"x": 5, "y": 0})
    
    x1 = metros_a_pies(inicio.get("x", 0))
    y1 = metros_a_pies(inicio.get("y", 0))
    x2 = metros_a_pies(fin.get("x", 5))
    y2 = metros_a_pies(fin.get("y", 0))
    
    altura = metros_a_pies(payload.get("altura_m", 3.0))
    
    # Crear linea
    punto_inicio = XYZ(x1, y1, 0)
    punto_fin = XYZ(x2, y2, 0)
    linea = Line.CreateBound(punto_inicio, punto_fin)
    
    # Crear muro con transaccion
    t = Transaction(doc, "IA_RVT - Crear Muro")
    t.Start()
    
    wall = Wall.Create(doc, linea, wall_type.Id, level.Id, altura, 0, False, False)
    
    t.Commit()
    
    print("EXITO: Muro creado con ID: " + str(wall.Id))
    return wall

def analizar_modelo():
    """Analizar modelo"""
    muros = FilteredElementCollector(doc).OfClass(Wall).GetElementCount()
    niveles = FilteredElementCollector(doc).OfClass(Level).GetElementCount()
    
    print("=== ANALISIS DEL MODELO ===")
    print("Muros: " + str(muros))
    print("Niveles: " + str(niveles))

# ========== EJECUCION PRINCIPAL ==========

print("=" * 50)
print("IA-EN-RVT 2026 - RevitPythonShell")
print("=" * 50)

# Verificar archivo
if not os.path.exists(COMMAND_PATH):
    print("No hay comando pendiente")
    print("Ruta: " + COMMAND_PATH)
else:
    # Leer comando
    with open(COMMAND_PATH, "r") as f:
        comando = json.load(f)
    
    accion = comando.get("accion", "")
    elemento = comando.get("elemento", "")
    payload = comando.get("payload", {})
    
    print("Accion: " + accion)
    print("Elemento: " + elemento)
    print("Payload: " + str(payload))
    
    # Ejecutar segun accion
    if accion == "CREATE" and elemento == "Wall":
        crear_muro(payload)
    elif accion in ["ANALYZE", "QUERY"]:
        analizar_modelo()
    else:
        print("Accion no soportada: " + accion)
    
    # Marcar como ejecutado
    comando["estado"] = "EJECUTADO"
    with open(COMMAND_PATH, "w") as f:
        json.dump(comando, f, indent=2)

print("=" * 50)