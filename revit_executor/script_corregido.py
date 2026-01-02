# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Revit Executor (pyRevit) - VERSIÓN CORREGIDA
===============================================================

Ejecutor de comandos BIM en Revit 2026.
Versión corregida para manejar errores de "Name" en IronPython.

Autor: Eduardo Bascuñán
Fecha: 02 de enero de 2026
"""

import clr
import json
import os
import sys
from datetime import datetime

# Referencias a Revit API
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference("RevitServices")

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


def get_level_by_name(nombre):
    """Obtener nivel por nombre - VERSIÓN CORREGIDA"""
    try:
        collector = FilteredElementCollector(doc).OfClass(Level)
        levels = list(collector)
        
        if not levels:
            return None
        
        # Si no se especifica nombre, retornar el primer nivel
        if not nombre or nombre == "":
            return levels[0]
        
        # Buscar nivel exacto
        for level in levels:
            try:
                level_name = str(level.Name) if hasattr(level, 'Name') and level.Name else ""
                if level_name and level_name.lower() == str(nombre).lower():
                    return level
            except:
                continue
        
        # Si no se encuentra exacto, retornar el primer nivel
        return levels[0]
        
    except Exception as e:
        log_message("Error en get_level_by_name: {0}".format(str(e)))
        return None


def get_wall_type_by_name(nombre):
    """Obtener tipo de muro por nombre - VERSIÓN CORREGIDA"""
    try:
        collector = FilteredElementCollector(doc).OfClass(WallType)
        wall_types = list(collector)
        
        if not wall_types:
            return None
        
        # Si no se especifica nombre, retornar el primer tipo
        if not nombre or nombre == "":
            return wall_types[0]
        
        # Buscar tipo que contenga el nombre
        for wt in wall_types:
            try:
                wt_name = str(wt.Name) if hasattr(wt, 'Name') and wt.Name else ""
                if wt_name and nombre.lower() in wt_name.lower():
                    return wt
            except:
                continue
        
        # Si no se encuentra, retornar el primer tipo
        return wall_types[0]
        
    except Exception as e:
        log_message("Error en get_wall_type_by_name: {0}".format(str(e)))
        return None


def get_door_type():
    """Obtener tipo de puerta disponible"""
    try:
        collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsElementType()
        door_types = list(collector)
        if door_types:
            return door_types[0]
        return None
    except Exception as e:
        log_message("Error en get_door_type: {0}".format(str(e)))
        return None


def get_window_type():
    """Obtener tipo de ventana disponible"""
    try:
        collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsElementType()
        window_types = list(collector)
        if window_types:
            return window_types[0]
        return None
    except Exception as e:
        log_message("Error en get_window_type: {0}".format(str(e)))
        return None


def get_column_type():
    """Obtener tipo de columna disponible"""
    try:
        collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsElementType()
        column_types = list(collector)
        if column_types:
            return column_types[0]
        return None
    except Exception as e:
        log_message("Error en get_column_type: {0}".format(str(e)))
        return None


def crear_muro(payload):
    """Crear muro en Revit - VERSIÓN CORREGIDA"""
    try:
        log_message("Iniciando creación de muro")
        
        # Obtener nivel
        nivel_nombre = payload.get("nivel", "")
        level = get_level_by_name(nivel_nombre)
        if not level:
            return {"exito": False, "error": "No se pudo obtener nivel"}
        
        log_message("Nivel obtenido: {0}".format(str(level.Name) if hasattr(level, 'Name') else "Nivel"))
        
        # Obtener tipo de muro
        tipo_nombre = payload.get("tipo", "")
        wall_type = get_wall_type_by_name(tipo_nombre)
        if not wall_type:
            return {"exito": False, "error": "No se pudo obtener tipo de muro"}
        
        log_message("Tipo de muro obtenido: {0}".format(str(wall_type.Name) if hasattr(wall_type, 'Name') else "Tipo"))
        
        # Obtener coordenadas
        inicio = payload.get("inicio", {"x": 0, "y": 0})
        fin = payload.get("fin", {"x": 5, "y": 0})
        
        # Convertir a pies
        x1 = metros_a_pies(inicio.get("x", 0))
        y1 = metros_a_pies(inicio.get("y", 0))
        x2 = metros_a_pies(fin.get("x", 5))
        y2 = metros_a_pies(fin.get("y", 0))
        
        # Altura en pies
        altura = metros_a_pies(payload.get("altura_m", 3.0))
        
        log_message("Coordenadas: ({0}, {1}) a ({2}, {3}), altura: {4}m".format(inicio.get("x", 0), inicio.get("y", 0), fin.get("x", 5), fin.get("y", 0), payload.get("altura_m", 3.0)))
        
        # Crear línea base
        punto_inicio = XYZ(x1, y1, 0)
        punto_fin = XYZ(x2, y2, 0)
        linea = Line.CreateBound(punto_inicio, punto_fin)
        
        # Crear muro
        t = Transaction(doc, "IA_RVT - Crear Muro")
        t.Start()
        
        wall = Wall.Create(doc, linea, wall_type.Id, level.Id, altura, 0, False, False)
        
        t.Commit()
        
        log_message("Muro creado exitosamente: ID={0}".format(str(wall.Id)))
        
        return {
            "exito": True,
            "elemento_id": str(wall.Id),
            "tipo": "Wall",
            "mensaje": "Muro creado exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando muro: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def analizar_modelo(payload):
    """Analizar modelo y retornar estadísticas"""
    try:
        stats = {
            "muros": FilteredElementCollector(doc).OfClass(Wall).GetElementCount(),
            "puertas": FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().GetElementCount(),
            "ventanas": FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().GetElementCount(),
            "niveles": FilteredElementCollector(doc).OfClass(Level).GetElementCount(),
            "columnas": FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().GetElementCount()
        }
        
        log_message("Análisis de modelo completado")
        
        return {
            "exito": True,
            "estadisticas": stats,
            "mensaje": "Análisis completado"
        }
        
    except Exception as e:
        log_message("Error en análisis: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def ejecutar_comando(comando):
    """Ejecutar comando BIM según el schema"""
    
    accion = comando.get("accion", "").upper()
    elemento = comando.get("elemento", "")
    payload = comando.get("payload", {})
    
    log_message("Ejecutando: {0} {1}".format(accion, elemento))
    
    # Router de acciones
    if accion == "CREATE":
        if elemento == "Wall":
            return crear_muro(payload)
        else:
            return {"exito": False, "error": "Elemento CREATE no soportado: {0}".format(elemento)}
    
    elif accion == "ANALYZE":
        return analizar_modelo(payload)
    
    elif accion == "QUERY":
        return analizar_modelo(payload)
    
    else:
        return {"exito": False, "error": "Acción no soportada: {0}".format(accion)}


def main():
    """Función principal - Lee y ejecuta comando"""
    
    print("=" * 50)
    print("IA-EN-RVT 2026 - Revit Executor (CORREGIDO)")
    print("=" * 50)
    
    # Verificar archivo de comando
    if not os.path.exists(COMMAND_PATH):
        print("No hay comando pendiente en: {0}".format(COMMAND_PATH))
        log_message("No hay comando pendiente")
        return
    
    try:
        # Leer comando
        with open(COMMAND_PATH, "r") as f:
            comando = json.load(f)
        
        print("Comando leido:")
        print("  Accion: {0}".format(comando.get("accion")))
        print("  Elemento: {0}".format(comando.get("elemento")))
        print("  Autonomia: {0}".format(comando.get("autonomia")))
        
        # Verificar schema
        if comando.get("schema") != "IA_RVT_BIM_COMMAND_v1":
            print("ERROR: Schema invalido")
            return
        
        # Verificar estado
        if comando.get("estado") == "CANCELADO":
            print("Comando cancelado por el usuario")
            return
        
        # Ejecutar
        resultado = ejecutar_comando(comando)
        
        # Mostrar resultado
        if resultado.get("exito"):
            print("\n✅ EXITO: {0}".format(resultado.get("mensaje")))
            if resultado.get("elemento_id"):
                print("   ID: {0}".format(resultado.get("elemento_id")))
        else:
            print("\n❌ ERROR: {0}".format(resultado.get("error")))
        
        # Actualizar estado del comando
        comando["estado"] = "EJECUTADO" if resultado.get("exito") else "ERROR"
        comando["resultado"] = resultado
        
        with open(COMMAND_PATH, "w") as f:
            json.dump(comando, f, indent=2)
        
    except Exception as e:
        print("Error critico: {0}".format(str(e)))
        log_message("Error critico: {0}".format(str(e)))


# Ejecutar
if __name__ == "__main__":
    main()
else:
    main()