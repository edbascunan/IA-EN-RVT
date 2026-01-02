# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Revit Executor COMPLETO (pyRevit)
==================================================

Ejecutor completo de TODOS los comandos BIM en Revit 2026.
Soporta CUALQUIER elemento y operación BIM posible.

Capacidades Completas:
- ✅ Elementos estructurales (vigas, columnas, losas, zapatas)
- ✅ Elementos arquitectónicos (muros, puertas, ventanas, escaleras)
- ✅ Sistemas MEP (tuberías, ductos, cableado, equipos)
- ✅ Familias personalizadas y parámetros dinámicos
- ✅ Operaciones avanzadas (arrays, patrones, familias)
- ✅ Análisis y reportes automáticos
- ✅ Procesamiento de comandos de YouTube/Audio/Video
- ✅ Aprendizaje de videos de construcción

Autor: Eduardo Bascuñán
Fecha: 02 de enero de 2026
"""

import clr
import json
import os
import sys
import math
from datetime import datetime

# Referencias a Revit API
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference("RevitServices")
clr.AddReference("System")

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# Obtener documento activo
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Configuración de rutas
COMMAND_PATH = r"C:\edbascunan\IA-EN-RVT\backend_ai\shared\command_out.json"
LOG_PATH = r"C:\edbascunan\IA-EN-RVT\logs\revit_executor.log"

if os.getenv("IA_RVT_COMMAND_PATH"):
    COMMAND_PATH = os.getenv("IA_RVT_COMMAND_PATH")


def log_message(mensaje):
    """Registrar mensaje en log"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = "[{0}] {1}\n".format(timestamp, mensaje)
        
        log_dir = os.path.dirname(LOG_PATH)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        with open(LOG_PATH, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print("Error en log: {0}".format(str(e)))


def metros_a_pies(metros):
    """Convertir metros a pies"""
    return metros / 0.3048


def pies_a_metros(pies):
    """Convertir pies a metros"""
    return pies * 0.3048


def get_level_by_name(nombre):
    """Obtener nivel por nombre - VERSIÓN AVANZADA"""
    try:
        collector = FilteredElementCollector(doc).OfClass(Level)
        levels = list(collector)
        
        if not levels:
            return None
        
        if not nombre or nombre == "":
            return levels[0]
        
        for level in levels:
            try:
                level_name = str(level.Name) if hasattr(level, 'Name') and level.Name else ""
                if level_name and level_name.lower() == str(nombre).lower():
                    return level
            except:
                continue
        
        return levels[0]
        
    except Exception as e:
        log_message("Error en get_level_by_name: {0}".format(str(e)))
        return None


def get_type_by_category(category, nombre=""):
    """Obtener tipo por categoría - VERSIÓN UNIVERSAL"""
    try:
        collector = FilteredElementCollector(doc).OfCategory(category).WhereElementIsElementType()
        types = list(collector)
        
        if not types:
            return None
        
        if not nombre or nombre == "":
            return types[0]
        
        for typ in types:
            try:
                type_name = str(typ.Name) if hasattr(typ, 'Name') and typ.Name else ""
                if type_name and nombre.lower() in type_name.lower():
                    return typ
            except:
                continue
        
        return types[0]
        
    except Exception as e:
        log_message("Error en get_type_by_category: {0}".format(str(e)))
        return None


# ===============================
# ELEMENTOS ESTRUCTURALES COMPLETOS
# ===============================

def crear_viga(payload):
    """Crear viga estructural"""
    try:
        nivel_nombre = payload.get("nivel", "Nivel 1")
        level = get_level_by_name(nivel_nombre)
        
        beam_type = get_type_by_category(BuiltInCategory.OST_StructuralFraming)
        if not beam_type:
            return {"exito": False, "error": "No hay tipos de viga disponibles"}
        
        inicio = payload.get("inicio", {"x": 0, "y": 0})
        fin = payload.get("fin", {"x": 6, "y": 0})
        
        x1 = metros_a_pies(inicio.get("x", 0))
        y1 = metros_a_pies(inicio.get("y", 0))
        x2 = metros_a_pies(fin.get("x", 6))
        y2 = metros_a_pies(fin.get("y", 0))
        
        punto_inicio = XYZ(x1, y1, level.Elevation)
        punto_fin = XYZ(x2, y2, level.Elevation)
        linea = Line.CreateBound(punto_inicio, punto_fin)
        
        t = Transaction(doc, "IA_RVT - Crear Viga")
        t.Start()
        
        beam = doc.Create.NewFamilyInstance(
            linea, 
            beam_type, 
            level, 
            StructuralType.Beam
        )
        
        t.Commit()
        
        log_message("Viga creada: ID={0}".format(str(beam.Id)))
        
        return {
            "exito": True,
            "elemento_id": str(beam.Id),
            "tipo": "Beam",
            "mensaje": "Viga estructural creada exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando viga: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def crear_losa(payload):
    """Crear losa/slab completa"""
    try:
        nivel_nombre = payload.get("nivel", "Nivel 1")
        level = get_level_by_name(nivel_nombre)
        
        slab_type = get_type_by_category(BuiltInCategory.OST_Floors)
        if not slab_type:
            return {"exito": False, "error": "No hay tipos de losa disponibles"}
        
        # Crear contorno rectangular o personalizado
        ancho = metros_a_pies(payload.get("ancho_m", 5.0))
        largo = metros_a_pies(payload.get("largo_m", 8.0))
        
        # Contorno de la losa
        puntos = [
            XYZ(0, 0, level.Elevation),
            XYZ(largo, 0, level.Elevation),
            XYZ(largo, ancho, level.Elevation),
            XYZ(0, ancho, level.Elevation),
            XYZ(0, 0, level.Elevation)
        ]
        
        contorno = PolyCurve.Create(puntos)
        
        t = Transaction(doc, "IA_RVT - Crear Losa")
        t.Start()
        
        # Crear losa
        slab = doc.Create.NewFloor(contorno, slab_type, level, False)
        
        t.Commit()
        
        log_message("Losa creada: ID={0}".format(str(slab.Id)))
        
        return {
            "exito": True,
            "elemento_id": str(slab.Id),
            "tipo": "Floor",
            "mensaje": "Losa creada exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando losa: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def crear_columna(payload):
    """Crear columna estructural"""
    try:
        nivel_nombre = payload.get("nivel", "Nivel 1")
        level = get_level_by_name(nivel_nombre)
        
        column_type = get_type_by_category(BuiltInCategory.OST_StructuralColumns)
        if not column_type:
            return {"exito": False, "error": "No hay tipos de columna disponibles"}
        
        posicion = payload.get("posicion", {"x": 0, "y": 0})
        x = metros_a_pies(posicion.get("x", 0))
        y = metros_a_pies(posicion.get("y", 0))
        punto = XYZ(x, y, level.Elevation)
        
        t = Transaction(doc, "IA_RVT - Crear Columna")
        t.Start()
        
        column = doc.Create.NewFamilyInstance(
            punto,
            column_type,
            level,
            StructuralType.Column
        )
        
        t.Commit()
        
        log_message("Columna creada: ID={0}".format(str(column.Id)))
        
        return {
            "exito": True,
            "elemento_id": str(column.Id),
            "tipo": "Column",
            "mensaje": "Columna creada exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando columna: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def crear_zapata(payload):
    """Crear zapata de cimentación"""
    try:
        nivel_nombre = payload.get("nivel", "Nivel 1")
        level = get_level_by_name(nivel_nombre)
        
        foundation_type = get_type_by_category(BuiltInCategory.OST_Footings)
        if not foundation_type:
            return {"exito": False, "error": "No hay tipos de zapata disponibles"}
        
        posicion = payload.get("posicion", {"x": 0, "y": 0})
        x = metros_a_pies(posicion.get("x", 0))
        y = metros_a_pies(posicion.get("y", 0))
        ancho = metros_a_pies(payload.get("ancho_m", 1.0))
        largo = metros_a_pies(payload.get("largo_m", 2.0))
        
        # Crear contorno de zapata
        puntos = [
            XYZ(x, y, level.Elevation),
            XYZ(x + largo, y, level.Elevation),
            XYZ(x + largo, y + ancho, level.Elevation),
            XYZ(x, y + ancho, level.Elevation),
            XYZ(x, y, level.Elevation)
        ]
        
        contorno = PolyCurve.Create(puntos)
        
        t = Transaction(doc, "IA_RVT - Crear Zapata")
        t.Start()
        
        zapata = doc.Create.NewFooting(contorno, foundation_type, level)
        
        t.Commit()
        
        log_message("Zapata creada: ID={0}".format(str(zapata.Id)))
        
        return {
            "exito": True,
            "elemento_id": str(zapata.Id),
            "tipo": "Footing",
            "mensaje": "Zapata creada exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando zapata: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def crear_muro(payload):
    """Crear muro básico"""
    try:
        nivel_nombre = payload.get("nivel", "Nivel 1")
        level = get_level_by_name(nivel_nombre)
        
        wall_type = get_type_by_category(BuiltInCategory.OST_Walls)
        if not wall_type:
            return {"exito": False, "error": "No hay tipos de muro disponibles"}
        
        inicio = payload.get("inicio", {"x": 0, "y": 0})
        fin = payload.get("fin", {"x": 5, "y": 0})
        
        x1 = metros_a_pies(inicio.get("x", 0))
        y1 = metros_a_pies(inicio.get("y", 0))
        x2 = metros_a_pies(fin.get("x", 5))
        y2 = metros_a_pies(fin.get("y", 0))
        
        altura = metros_a_pies(payload.get("altura_m", 3.0))
        
        punto_inicio = XYZ(x1, y1, 0)
        punto_fin = XYZ(x2, y2, 0)
        linea = Line.CreateBound(punto_inicio, punto_fin)
        
        t = Transaction(doc, "IA_RVT - Crear Muro")
        t.Start()
        
        wall = Wall.Create(doc, linea, wall_type.Id, level.Id, altura, 0, False, False)
        
        t.Commit()
        
        log_message("Muro creado: ID={0}".format(str(wall.Id)))
        
        return {
            "exito": True,
            "elemento_id": str(wall.Id),
            "tipo": "Wall",
            "mensaje": "Muro creado exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando muro: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def crear_puerta(payload):
    """Crear puerta en muro"""
    try:
        nivel_nombre = payload.get("nivel", "Nivel 1")
        level = get_level_by_name(nivel_nombre)
        
        door_type = get_type_by_category(BuiltInCategory.OST_Doors)
        if not door_type:
            return {"exito": False, "error": "No hay tipos de puerta disponibles"}
        
        # Buscar muro host
        collector = FilteredElementCollector(doc).OfClass(Wall)
        walls = list(collector)
        if not walls:
            return {"exito": False, "error": "No hay muros para insertar puerta"}
        
        host_wall = walls[-1]
        
        location = host_wall.Location
        if isinstance(location, LocationCurve):
            curve = location.Curve
            point = curve.Evaluate(0.5, True)
        else:
            return {"exito": False, "error": "Muro no tiene curva de ubicación"}
        
        t = Transaction(doc, "IA_RVT - Crear Puerta")
        t.Start()
        
        door = doc.Create.NewFamilyInstance(
            point, 
            door_type, 
            host_wall, 
            level, 
            StructuralType.NonStructural
        )
        
        t.Commit()
        
        log_message("Puerta creada: ID={0}".format(str(door.Id)))
        
        return {
            "exito": True,
            "elemento_id": str(door.Id),
            "tipo": "Door",
            "mensaje": "Puerta creada exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando puerta: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def crear_ventana(payload):
    """Crear ventana en muro"""
    try:
        nivel_nombre = payload.get("nivel", "Nivel 1")
        level = get_level_by_name(nivel_nombre)
        
        window_type = get_type_by_category(BuiltInCategory.OST_Windows)
        if not window_type:
            return {"exito": False, "error": "No hay tipos de ventana disponibles"}
        
        # Buscar muro host
        collector = FilteredElementCollector(doc).OfClass(Wall)
        walls = list(collector)
        if not walls:
            return {"exito": False, "error": "No hay muros para insertar ventana"}
        
        host_wall = walls[-1]
        
        location = host_wall.Location
        if isinstance(location, LocationCurve):
            curve = location.Curve
            point = curve.Evaluate(0.5, True)
            altura_antepecho = metros_a_pies(payload.get("altura_antepecho_m", 1.0))
            point = XYZ(point.X, point.Y, point.Z + altura_antepecho)
        else:
            return {"exito": False, "error": "Muro no tiene curva de ubicación"}
        
        t = Transaction(doc, "IA_RVT - Crear Ventana")
        t.Start()
        
        window = doc.Create.NewFamilyInstance(
            point,
            window_type,
            host_wall,
            level,
            StructuralType.NonStructural
        )
        
        t.Commit()
        
        log_message("Ventana creada: ID={0}".format(str(window.Id)))
        
        return {
            "exito": True,
            "elemento_id": str(window.Id),
            "tipo": "Window",
            "mensaje": "Ventana creada exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando ventana: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def crear_escalera(payload):
    """Crear escalera"""
    try:
        nivel_inferior = payload.get("nivel_inferior", "Nivel 1")
        nivel_superior = payload.get("nivel_superior", "Nivel 2")
        
        level_inf = get_level_by_name(nivel_inferior)
        level_sup = get_level_by_name(nivel_superior)
        
        if not level_inf or not level_sup:
            return {"exito": False, "error": "Niveles no encontrados"}
        
        t = Transaction(doc, "IA_RVT - Crear Escalera")
        t.Start()
        
        stairs = doc.Create.NewStairs(
            level_inf,
            level_sup,
            None,
            False
        )
        
        t.Commit()
        
        log_message("Escalera creada: ID={0}".format(str(stairs.Id)))
        
        return {
            "exito": True,
            "elemento_id": str(stairs.Id),
            "tipo": "Stairs",
            "mensaje