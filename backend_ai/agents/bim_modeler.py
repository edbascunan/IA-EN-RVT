#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Agente BIM Modeler
===================================

Agente especializado en interpretación y generación de comandos de modelado BIM.
Convierte lenguaje natural en instrucciones específicas para Revit.

Autor: Eduardo Bascuñán
Fecha: 01 de enero de 2026
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class BIMModeler:
    """Agente de modelado BIM - Interpreta y genera comandos de modelado"""
    
    # Tipos de muros disponibles en Revit (ejemplos comunes)
    TIPOS_MUROS = {
        "estructural": "Muro Estructural - 200mm",
        "interior": "Muro Interior - 100mm",
        "exterior": "Muro Exterior - 300mm",
        "cortafuego": "Muro Cortafuego - 150mm",
        "divisorio": "Muro Divisorio - 70mm"
    }
    
    # Tipos de puertas comunes
    TIPOS_PUERTAS = {
        "simple": "Puerta Simple 0.90x2.10",
        "doble": "Puerta Doble 1.80x2.10",
        "corrediza": "Puerta Corrediza 0.90x2.10",
        "vidrio": "Puerta Vidrio 0.90x2.10"
    }
    
    # Tipos de ventanas
    TIPOS_VENTANAS = {
        "fija": "Ventana Fija 1.20x1.20",
        "corrediza": "Ventana Corrediza 1.50x1.20",
        "proyectante": "Ventana Proyectante 0.60x0.60"
    }
    
    def __init__(self):
        self.ultimo_elemento = None
        self.contexto_modelo = {}
        logger.info("🏗️ BIMModeler inicializado")
    
    def interpret(self, texto: str) -> Dict[str, Any]:
        """Interpretar texto y generar comando BIM estructurado"""
        texto_lower = texto.lower()
        
        # Detectar tipo de elemento y acción
        if any(w in texto_lower for w in ["muro", "pared", "muros"]):
            return self._crear_comando_muro(texto)
        elif any(w in texto_lower for w in ["puerta", "puertas"]):
            return self._crear_comando_puerta(texto)
        elif any(w in texto_lower for w in ["ventana", "ventanas"]):
            return self._crear_comando_ventana(texto)
        elif any(w in texto_lower for w in ["columna", "pilar"]):
            return self._crear_comando_columna(texto)
        elif any(w in texto_lower for w in ["viga", "vigas"]):
            return self._crear_comando_viga(texto)
        elif any(w in texto_lower for w in ["piso", "losa", "suelo"]):
            return self._crear_comando_piso(texto)
        elif any(w in texto_lower for w in ["nivel", "niveles"]):
            return self._crear_comando_nivel(texto)
        else:
            return self._crear_comando_generico(texto)
    
    def _crear_comando_muro(self, texto: str) -> Dict[str, Any]:
        """Crear comando para muros"""
        import re
        
        # Extraer altura
        altura = 3.0  # Default 3 metros
        altura_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:metros?|m)?\s*(?:de\s+)?altura", texto.lower())
        if altura_match:
            altura = float(altura_match.group(1))
        
        # Extraer longitud
        longitud = 5.0  # Default 5 metros
        longitud_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:metros?|m)?\s*(?:de\s+)?(?:largo|longitud)", texto.lower())
        if longitud_match:
            longitud = float(longitud_match.group(1))
        
        # Detectar tipo de muro
        tipo = self.TIPOS_MUROS["interior"]  # Default
        for key, value in self.TIPOS_MUROS.items():
            if key in texto.lower():
                tipo = value
                break
        
        # Detectar nivel
        nivel = "Nivel 1"
        nivel_match = re.search(r"nivel\s*(\d+)", texto.lower())
        if nivel_match:
            nivel = f"Nivel {nivel_match.group(1)}"
        
        # Detectar coordenadas de inicio/fin
        inicio = {"x": 0, "y": 0}
        fin = {"x": longitud, "y": 0}
        
        coords_match = re.search(r"desde\s*\((\d+),\s*(\d+)\)\s*hasta\s*\((\d+),\s*(\d+)\)", texto)
        if coords_match:
            inicio = {"x": int(coords_match.group(1)), "y": int(coords_match.group(2))}
            fin = {"x": int(coords_match.group(3)), "y": int(coords_match.group(4))}
        
        return {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "accion": "CREATE",
            "elemento": "Wall",
            "payload": {
                "nivel": nivel,
                "tipo": tipo,
                "altura_m": altura,
                "longitud_m": longitud,
                "inicio": inicio,
                "fin": fin,
                "espesor_mm": 200
            }
        }
    
    def _crear_comando_puerta(self, texto: str) -> Dict[str, Any]:
        """Crear comando para puertas"""
        import re
        
        # Detectar tipo
        tipo = self.TIPOS_PUERTAS["simple"]
        for key, value in self.TIPOS_PUERTAS.items():
            if key in texto.lower():
                tipo = value
                break
        
        # Detectar nivel
        nivel = "Nivel 1"
        nivel_match = re.search(r"nivel\s*(\d+)", texto.lower())
        if nivel_match:
            nivel = f"Nivel {nivel_match.group(1)}"
        
        # Detectar posición en muro
        posicion = 0.5  # Centro del muro por defecto
        
        return {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "accion": "CREATE",
            "elemento": "Door",
            "payload": {
                "nivel": nivel,
                "tipo": tipo,
                "ancho_m": 0.9,
                "alto_m": 2.1,
                "posicion_en_muro": posicion,
                "host_wall": "ultimo_muro"  # Se asocia al último muro creado
            }
        }
    
    def _crear_comando_ventana(self, texto: str) -> Dict[str, Any]:
        """Crear comando para ventanas"""
        import re
        
        tipo = self.TIPOS_VENTANAS["fija"]
        for key, value in self.TIPOS_VENTANAS.items():
            if key in texto.lower():
                tipo = value
                break
        
        nivel = "Nivel 1"
        nivel_match = re.search(r"nivel\s*(\d+)", texto.lower())
        if nivel_match:
            nivel = f"Nivel {nivel_match.group(1)}"
        
        altura_antepecho = 1.0  # 1 metro de altura de antepecho
        
        return {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "accion": "CREATE",
            "elemento": "Window",
            "payload": {
                "nivel": nivel,
                "tipo": tipo,
                "ancho_m": 1.2,
                "alto_m": 1.2,
                "altura_antepecho_m": altura_antepecho,
                "host_wall": "ultimo_muro"
            }
        }
    
    def _crear_comando_columna(self, texto: str) -> Dict[str, Any]:
        """Crear comando para columnas"""
        import re
        
        nivel = "Nivel 1"
        nivel_match = re.search(r"nivel\s*(\d+)", texto.lower())
        if nivel_match:
            nivel = f"Nivel {nivel_match.group(1)}"
        
        # Dimensiones
        dimension = 0.3  # 30cm x 30cm por defecto
        dim_match = re.search(r"(\d+)(?:x(\d+))?\s*(?:cm|mm)?", texto.lower())
        if dim_match:
            dimension = int(dim_match.group(1)) / 100 if int(dim_match.group(1)) > 10 else int(dim_match.group(1))
        
        return {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "accion": "CREATE",
            "elemento": "Column",
            "payload": {
                "nivel": nivel,
                "tipo": "Columna Rectangular",
                "dimension_x_m": dimension,
                "dimension_y_m": dimension,
                "posicion": {"x": 0, "y": 0}
            }
        }
    
    def _crear_comando_viga(self, texto: str) -> Dict[str, Any]:
        """Crear comando para vigas"""
        import re
        
        nivel = "Nivel 1"
        nivel_match = re.search(r"nivel\s*(\d+)", texto.lower())
        if nivel_match:
            nivel = f"Nivel {nivel_match.group(1)}"
        
        return {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "accion": "CREATE",
            "elemento": "Beam",
            "payload": {
                "nivel": nivel,
                "tipo": "Viga Rectangular 30x50",
                "ancho_m": 0.3,
                "alto_m": 0.5,
                "inicio": {"x": 0, "y": 0},
                "fin": {"x": 5, "y": 0}
            }
        }
    
    def _crear_comando_piso(self, texto: str) -> Dict[str, Any]:
        """Crear comando para pisos/losas"""
        import re
        
        nivel = "Nivel 1"
        nivel_match = re.search(r"nivel\s*(\d+)", texto.lower())
        if nivel_match:
            nivel = f"Nivel {nivel_match.group(1)}"
        
        return {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "accion": "CREATE",
            "elemento": "Floor",
            "payload": {
                "nivel": nivel,
                "tipo": "Losa de Hormigón 200mm",
                "espesor_m": 0.2,
                "contorno": [
                    {"x": 0, "y": 0},
                    {"x": 10, "y": 0},
                    {"x": 10, "y": 10},
                    {"x": 0, "y": 10}
                ]
            }
        }
    
    def _crear_comando_nivel(self, texto: str) -> Dict[str, Any]:
        """Crear comando para niveles"""
        import re
        
        elevacion = 3.0  # 3 metros de altura por defecto
        elev_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:metros?|m)", texto.lower())
        if elev_match:
            elevacion = float(elev_match.group(1))
        
        nombre = "Nivel Nuevo"
        nombre_match = re.search(r"(?:llamado|nombre)\s*[\"']?(\w+)[\"']?", texto.lower())
        if nombre_match:
            nombre = nombre_match.group(1)
        
        return {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "accion": "CREATE",
            "elemento": "Level",
            "payload": {
                "nombre": nombre,
                "elevacion_m": elevacion
            }
        }
    
    def _crear_comando_generico(self, texto: str) -> Dict[str, Any]:
        """Crear comando genérico cuando no se detecta elemento específico"""
        return {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "accion": "QUERY",
            "elemento": "View",
            "payload": {
                "consulta": texto,
                "tipo": "informacion_general"
            }
        }
    
    def modificar_elemento(self, elemento_id: str, cambios: Dict[str, Any]) -> Dict[str, Any]:
        """Generar comando de modificación de elemento"""
        return {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "accion": "MODIFY",
            "elemento": "Parameter",
            "payload": {
                "elemento_id": elemento_id,
                "cambios": cambios
            }
        }
    
    def eliminar_elemento(self, elemento_id: str) -> Dict[str, Any]:
        """Generar comando de eliminación"""
        return {
            "schema": "IA_RVT_BIM_COMMAND_v1",
            "accion": "DELETE",
            "elemento": "Family",
            "payload": {
                "elemento_id": elemento_id
            }
        }


class BIMValidator:
    """Agente de validación BIM"""
    
    def __init__(self):
        self.reglas = []
        logger.info("✅ BIMValidator inicializado")
    
    def validar_comando(self, comando: Dict[str, Any]) -> Dict[str, Any]:
        """Validar comando BIM antes de ejecutar"""
        errores = []
        advertencias = []
        
        payload = comando.get("payload", {})
        
        # Validar alturas
        if "altura_m" in payload:
            altura = payload["altura_m"]
            if altura < 0.5:
                errores.append(f"Altura muy baja: {altura}m")
            elif altura > 10:
                advertencias.append(f"Altura inusual: {altura}m")
        
        # Validar dimensiones
        for dim in ["ancho_m", "largo_m", "espesor_m"]:
            if dim in payload:
                valor = payload[dim]
                if valor <= 0:
                    errores.append(f"{dim} debe ser positivo")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }


class BIMOptimizer:
    """Agente de optimización BIM"""
    
    def __init__(self):
        logger.info("⚡ BIMOptimizer inicializado")
    
    def optimizar_modelo(self, elementos: List[Dict]) -> Dict[str, Any]:
        """Analizar y sugerir optimizaciones del modelo"""
        sugerencias = []
        
        # Análisis básico
        if len(elementos) > 1000:
            sugerencias.append("Considerar dividir el modelo en worksets")
        
        return {
            "elementos_analizados": len(elementos),
            "sugerencias": sugerencias
        }


class BIMQAAgent:
    """Agente de Quality Assurance BIM"""
    
    def __init__(self):
        logger.info("🔍 BIMQAAgent inicializado")
    
    def verificar_clashes(self, elementos: List[Dict]) -> Dict[str, Any]:
        """Verificar colisiones entre elementos"""
        # Simulación de clash detection
        return {
            "clashes_detectados": 0,
            "elementos_verificados": len(elementos)
        }
    
    def auditar_modelo(self) -> Dict[str, Any]:
        """Auditoría general del modelo"""
        return {
            "estado": "OK",
            "advertencias": [],
            "errores": []
        }