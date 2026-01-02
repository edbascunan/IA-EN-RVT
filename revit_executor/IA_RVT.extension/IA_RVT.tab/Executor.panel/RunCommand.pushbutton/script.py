# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Revit Executor (pyRevit)
==========================================

Ejecutor de comandos BIM en Revit 2026.
Lee comandos JSON generados por el orquestador y los ejecuta en el modelo.

IMPORTANTE: Este script corre en IronPython 2.7 dentro de Revit.
No usa dependencias externas. Solo Revit API.

Autor: Eduardo Bascuñán
Fecha: 01 de enero de 2026
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
# Ajustar esta ruta según tu instalación
COMMAND_PATH = r"C:\IA_RVT\backend_ai\shared\command_out.json"
LOG_PATH = r"C:\IA_RVT\logs\revit_executor.log"

# Alternativa: usar variable de entorno
if os.getenv("IA_RVT_COMMAND_PATH"):
    COMMAND_PATH = os.getenv("IA_RVT_COMMAND_PATH")


def log_message(mensaje):
    """Registrar mensaje en log"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = "[{0}] {1}\n".format(timestamp, mensaje)
        
        # Crear directorio si no existe
        log_dir = os.path.dirname(LOG_PATH)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        with open(LOG_PATH, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print("Error en log: {0}".format(str(e)))


def metros_a_pies(metros):
    """Convertir metros a pies (unidad interna de Revit)"""
    return metros / 0.3048


def pies_a_metros(pies):
    """Convertir pies a metros"""
    return pies * 0.3048


def get_level_by_name(nombre):
    """Obtener nivel por nombre"""
    collector = FilteredElementCollector(doc).OfClass(Level)
    for level in collector:
        if level.Name == nombre:
            return level
    
    # Si no existe, retornar el primer nivel
    levels = list(collector)
    if levels:
        return levels[0]
    return None


def get_wall_type_by_name(nombre):
    """Obtener tipo de muro por nombre"""
    collector = FilteredElementCollector(doc).OfClass(WallType)
    for wt in collector:
        if nombre.lower() in wt.Name.lower():
            return wt
    
    # Retornar primer tipo disponible
    wall_types = list(collector)
    if wall_types:
        return wall_types[0]
    return None


def get_door_type():
    """Obtener tipo de puerta disponible"""
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsElementType()
    door_types = list(collector)
    if door_types:
        return door_types[0]
    return None


def get_window_type():
    """Obtener tipo de ventana disponible"""
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsElementType()
    window_types = list(collector)
    if window_types:
        return window_types[0]
    return None


def get_column_type():
    """Obtener tipo de columna disponible"""
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsElementType()
    column_types = list(collector)
    if column_types:
        return column_types[0]
    return None


def crear_muro(payload):
    """Crear muro en Revit"""
    try:
        # Obtener nivel
        nivel_nombre = payload.get("nivel", "Nivel 1")
        level = get_level_by_name(nivel_nombre)
        if not level:
            return {"exito": False, "error": "Nivel no encontrado: {0}".format(nivel_nombre)}
        
        # Obtener tipo de muro
        tipo_nombre = payload.get("tipo", "")
        wall_type = get_wall_type_by_name(tipo_nombre)
        if not wall_type:
            return {"exito": False, "error": "Tipo de muro no encontrado"}
        
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
        
        # Crear línea base
        punto_inicio = XYZ(x1, y1, 0)
        punto_fin = XYZ(x2, y2, 0)
        linea = Line.CreateBound(punto_inicio, punto_fin)
        
        # Crear muro
        t = Transaction(doc, "IA_RVT - Crear Muro")
        t.Start()
        
        wall = Wall.Create(doc, linea, wall_type.Id, level.Id, altura, 0, False, False)
        
        t.Commit()
        
        log_message("Muro creado: ID={0}".format(wall.Id.IntegerValue))
        
        return {
            "exito": True,
            "elemento_id": wall.Id.IntegerValue,
            "tipo": "Wall",
            "mensaje": "Muro creado exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando muro: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def crear_puerta(payload):
    """Crear puerta en muro"""
    try:
        # Obtener nivel
        nivel_nombre = payload.get("nivel", "Nivel 1")
        level = get_level_by_name(nivel_nombre)
        
        # Obtener tipo de puerta
        door_type = get_door_type()
        if not door_type:
            return {"exito": False, "error": "No hay tipos de puerta disponibles"}
        
        # Buscar muro host (último muro creado o especificado)
        collector = FilteredElementCollector(doc).OfClass(Wall)
        walls = list(collector)
        if not walls:
            return {"exito": False, "error": "No hay muros para insertar puerta"}
        
        host_wall = walls[-1]  # Último muro
        
        # Calcular ubicación en el muro
        location = host_wall.Location
        if isinstance(location, LocationCurve):
            curve = location.Curve
            mid_param = 0.5
            point = curve.Evaluate(mid_param, True)
        else:
            return {"exito": False, "error": "Muro no tiene curva de ubicación"}
        
        t = Transaction(doc, "IA_RVT - Crear Puerta")
        t.Start()
        
        # Crear instancia de puerta
        door = doc.Create.NewFamilyInstance(
            point, 
            door_type, 
            host_wall, 
            level, 
            StructuralType.NonStructural
        )
        
        t.Commit()
        
        log_message("Puerta creada: ID={0}".format(door.Id.IntegerValue))
        
        return {
            "exito": True,
            "elemento_id": door.Id.IntegerValue,
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
        
        window_type = get_window_type()
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
            # Elevar para antepecho
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
        
        log_message("Ventana creada: ID={0}".format(window.Id.IntegerValue))
        
        return {
            "exito": True,
            "elemento_id": window.Id.IntegerValue,
            "tipo": "Window",
            "mensaje": "Ventana creada exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando ventana: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def crear_columna(payload):
    """Crear columna estructural"""
    try:
        nivel_nombre = payload.get("nivel", "Nivel 1")
        level = get_level_by_name(nivel_nombre)
        
        column_type = get_column_type()
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
        
        log_message("Columna creada: ID={0}".format(column.Id.IntegerValue))
        
        return {
            "exito": True,
            "elemento_id": column.Id.IntegerValue,
            "tipo": "Column",
            "mensaje": "Columna creada exitosamente"
        }
        
    except Exception as e:
        log_message("Error creando columna: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def crear_nivel(payload):
    """Crear nuevo nivel"""
    try:
        elevacion = metros_a_pies(payload.get("elevacion_m", 3.0))
        nombre = payload.get("nombre", "Nivel Nuevo")
        
        t = Transaction(doc, "IA_RVT - Crear Nivel")
        t.Start()
        
        level = Level.Create(doc, elevacion)
        level.Name = nombre
        
        t.Commit()
        
        log_message("Nivel creado: {0} a {1}m".format(nombre, payload.get("elevacion_m", 3.0)))
        
        return {
            "exito": True,
            "elemento_id": level.Id.IntegerValue,
            "tipo": "Level",
            "mensaje": "Nivel '{0}' creado exitosamente".format(nombre)
        }
        
    except Exception as e:
        log_message("Error creando nivel: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def modificar_elemento(payload):
    """Modificar parámetros de elemento existente"""
    try:
        elemento_id = payload.get("elemento_id")
        cambios = payload.get("cambios", {})
        
        if not elemento_id:
            return {"exito": False, "error": "ID de elemento requerido"}
        
        element_id = ElementId(int(elemento_id))
        element = doc.GetElement(element_id)
        
        if not element:
            return {"exito": False, "error": "Elemento no encontrado"}
        
        t = Transaction(doc, "IA_RVT - Modificar Elemento")
        t.Start()
        
        for param_name, param_value in cambios.items():
            param = element.LookupParameter(param_name)
            if param and not param.IsReadOnly:
                if param.StorageType == StorageType.Double:
                    param.Set(float(param_value))
                elif param.StorageType == StorageType.Integer:
                    param.Set(int(param_value))
                elif param.StorageType == StorageType.String:
                    param.Set(str(param_value))
        
        t.Commit()
        
        log_message("Elemento modificado: ID={0}".format(elemento_id))
        
        return {
            "exito": True,
            "elemento_id": elemento_id,
            "mensaje": "Elemento modificado exitosamente"
        }
        
    except Exception as e:
        log_message("Error modificando elemento: {0}".format(str(e)))
        return {"exito": False, "error": str(e)}


def eliminar_elemento(payload):
    """Eliminar elemento del modelo"""
    try:
        elemento_id = payload.get("elemento_id")
        
        if not elemento_id:
            return {"exito": False, "error": "ID de elemento requerido"}
        
        element_id = ElementId(int(elemento_id))
        
        t = Transaction(doc, "IA_RVT - Eliminar Elemento")
        t.Start()
        
        doc.Delete(element_id)
        
        t.Commit()
        
        log_message("Elemento eliminado: ID={0}".format(elemento_id))
        
        return {
            "exito": True,
            "mensaje": "Elemento eliminado exitosamente"
        }
        
    except Exception as e:
        log_message("Error eliminando elemento: {0}".format(str(e)))
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
        elif elemento == "Door":
            return crear_puerta(payload)
        elif elemento == "Window":
            return crear_ventana(payload)
        elif elemento == "Column":
            return crear_columna(payload)
        elif elemento == "Level":
            return crear_nivel(payload)
        else:
            return {"exito": False, "error": "Elemento CREATE no soportado: {0}".format(elemento)}
    
    elif accion == "MODIFY":
        return modificar_elemento(payload)
    
    elif accion == "DELETE":
        return eliminar_elemento(payload)
    
    elif accion == "ANALYZE":
        return analizar_modelo(payload)
    
    elif accion == "QUERY":
        return analizar_modelo(payload)
    
    else:
        return {"exito": False, "error": "Acción no soportada: {0}".format(accion)}


def main():
    """Función principal - Lee y ejecuta comando"""
    
    print("=" * 50)
    print("IA-EN-RVT 2026 - Revit Executor")
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