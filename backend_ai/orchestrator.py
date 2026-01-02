#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Orquestador Principal
======================================

Sistema de orquestación multi-agente para control autónomo de Revit.
Interpreta comandos en lenguaje natural y genera acciones BIM.

Autor: Eduardo Bascuñán
Fecha: 01 de enero de 2026
"""

import os
import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta de salida para comandos BIM
COMMAND_OUTPUT_PATH = Path(__file__).parent / "shared" / "command_out.json"
COMMAND_HISTORY_PATH = Path(__file__).parent / "shared" / "command_history.json"

class BIMCommandProtocol:
    """Protocolo de comandos BIM - Contrato entre IA y Revit"""
    
    SCHEMA_VERSION = "IA_RVT_BIM_COMMAND_v1"
    
    ACCIONES_VALIDAS = [
        "CREATE", "MODIFY", "DELETE", "ANALYZE", 
        "QUERY", "EXPORT", "VALIDATE", "OPTIMIZE"
    ]
    
    ELEMENTOS_VALIDOS = [
        "Wall", "Door", "Window", "Floor", "Ceiling", "Roof",
        "Column", "Beam", "Family", "View", "Sheet", "Level",
        "Grid", "Room", "Area", "Parameter", "Material", "Schedule"
    ]
    
    @staticmethod
    def crear_comando(
        accion: str,
        elemento: str,
        payload: Dict[str, Any],
        autonomia: int = 3,
        rollback: bool = True
    ) -> Dict[str, Any]:
        """Crear comando BIM con firma de seguridad"""
        
        timestamp = datetime.now().isoformat()
        comando = {
            "schema": BIMCommandProtocol.SCHEMA_VERSION,
            "timestamp": timestamp,
            "accion": accion.upper(),
            "elemento": elemento,
            "payload": payload,
            "autonomia": autonomia,
            "rollback": rollback,
            "estado": "PENDIENTE"
        }
        
        # Generar firma hash para seguridad
        firma_data = f"{accion}{elemento}{json.dumps(payload)}{timestamp}"
        comando["firma"] = hashlib.sha256(firma_data.encode()).hexdigest()[:16]
        
        return comando
    
    @staticmethod
    def validar_comando(comando: Dict[str, Any]) -> tuple:
        """Validar que el comando cumpla el protocolo"""
        errores = []
        
        if comando.get("schema") != BIMCommandProtocol.SCHEMA_VERSION:
            errores.append("Schema inválido")
            
        if comando.get("accion") not in BIMCommandProtocol.ACCIONES_VALIDAS:
            errores.append(f"Acción inválida: {comando.get('accion')}")
            
        if comando.get("elemento") not in BIMCommandProtocol.ELEMENTOS_VALIDOS:
            errores.append(f"Elemento inválido: {comando.get('elemento')}")
            
        if not isinstance(comando.get("autonomia"), int) or not 1 <= comando.get("autonomia", 0) <= 5:
            errores.append("Autonomía debe ser entre 1 y 5")
            
        return len(errores) == 0, errores


class IntentParser:
    """Parser de intenciones - Interpreta lenguaje natural"""
    
    # Mapeo de palabras clave a acciones BIM
    KEYWORDS_ACCIONES = {
        "crear": "CREATE", "crea": "CREATE", "agregar": "CREATE", "añadir": "CREATE",
        "nuevo": "CREATE", "nueva": "CREATE", "generar": "CREATE", "dibujar": "CREATE",
        "modificar": "MODIFY", "cambiar": "MODIFY", "editar": "MODIFY", "ajustar": "MODIFY",
        "mover": "MODIFY", "rotar": "MODIFY", "escalar": "MODIFY", "actualizar": "MODIFY",
        "eliminar": "DELETE", "borrar": "DELETE", "quitar": "DELETE", "remover": "DELETE",
        "analizar": "ANALYZE", "revisar": "ANALYZE", "verificar": "ANALYZE", "evaluar": "ANALYZE",
        "consultar": "QUERY", "buscar": "QUERY", "encontrar": "QUERY", "listar": "QUERY",
        "exportar": "EXPORT", "guardar": "EXPORT", "generar reporte": "EXPORT",
        "validar": "VALIDATE", "comprobar": "VALIDATE", "chequear": "VALIDATE",
        "optimizar": "OPTIMIZE", "mejorar": "OPTIMIZE", "simplificar": "OPTIMIZE"
    }
    
    KEYWORDS_ELEMENTOS = {
        "muro": "Wall", "muros": "Wall", "pared": "Wall", "paredes": "Wall",
        "puerta": "Door", "puertas": "Door", "ventana": "Window", "ventanas": "Window",
        "piso": "Floor", "pisos": "Floor", "suelo": "Floor", "losa": "Floor",
        "techo": "Ceiling", "cielo": "Ceiling", "cubierta": "Roof", "tejado": "Roof",
        "columna": "Column", "columnas": "Column", "pilar": "Column",
        "viga": "Beam", "vigas": "Beam", "familia": "Family", "familias": "Family",
        "vista": "View", "vistas": "View", "plano": "Sheet", "lámina": "Sheet",
        "nivel": "Level", "niveles": "Level", "piso": "Level",
        "eje": "Grid", "ejes": "Grid", "grilla": "Grid",
        "habitación": "Room", "cuarto": "Room", "espacio": "Room",
        "área": "Area", "áreas": "Area", "parámetro": "Parameter",
        "material": "Material", "materiales": "Material"
    }
    
    # Patrones para extraer valores numéricos
    PATRONES_VALORES = {
        "altura": r"(\d+(?:\.\d+)?)\s*(?:metros?|m|mm)?.*altura",
        "ancho": r"(\d+(?:\.\d+)?)\s*(?:metros?|m|mm)?.*ancho",
        "largo": r"(\d+(?:\.\d+)?)\s*(?:metros?|m|mm)?.*largo",
        "espesor": r"(\d+(?:\.\d+)?)\s*(?:metros?|m|mm)?.*espesor",
    }
    
    def __init__(self):
        import re
        self.re = re
    
    def parsear_intencion(self, texto: str) -> Dict[str, Any]:
        """Analizar texto y extraer intención BIM"""
        texto_lower = texto.lower()
        
        # Detectar acción
        accion = None
        for keyword, acc in self.KEYWORDS_ACCIONES.items():
            if keyword in texto_lower:
                accion = acc
                break
        
        # Detectar elemento
        elemento = None
        for keyword, elem in self.KEYWORDS_ELEMENTOS.items():
            if keyword in texto_lower:
                elemento = elem
                break
        
        # Extraer parámetros numéricos
        payload = self._extraer_parametros(texto)
        
        # Detectar nivel/piso
        nivel_match = self.re.search(r"nivel\s*(\d+)", texto_lower)
        if nivel_match:
            payload["nivel"] = f"Nivel {nivel_match.group(1)}"
        
        return {
            "accion": accion or "QUERY",
            "elemento": elemento or "View",
            "payload": payload,
            "texto_original": texto,
            "confianza": self._calcular_confianza(accion, elemento)
        }
    
    def _extraer_parametros(self, texto: str) -> Dict[str, Any]:
        """Extraer parámetros numéricos del texto"""
        payload = {}
        
        # Buscar patrones de medidas
        metros_match = self.re.search(r"(\d+(?:\.\d+)?)\s*(?:metros?|m)\b", texto.lower())
        if metros_match:
            payload["medida_m"] = float(metros_match.group(1))
        
        # Buscar altura específica
        altura_match = self.re.search(r"(\d+(?:\.\d+)?)\s*(?:metros?|m)?(?:\s+de\s+)?altura", texto.lower())
        if altura_match:
            payload["altura_m"] = float(altura_match.group(1))
        
        # Buscar coordenadas
        coords_match = self.re.search(r"\((\d+),\s*(\d+)\)", texto)
        if coords_match:
            payload["inicio"] = {"x": int(coords_match.group(1)), "y": int(coords_match.group(2))}
        
        return payload
    
    def _calcular_confianza(self, accion: Optional[str], elemento: Optional[str]) -> float:
        """Calcular nivel de confianza de la interpretación"""
        confianza = 0.0
        if accion:
            confianza += 0.5
        if elemento:
            confianza += 0.5
        return confianza


class Orchestrator:
    """Orquestador principal del sistema IA-EN-RVT"""
    
    def __init__(self):
        self.autonomia = 3  # Nivel por defecto
        self.parser = IntentParser()
        self.protocol = BIMCommandProtocol()
        self.historial: List[Dict[str, Any]] = []
        self.ai_provider = None  # Se conecta con ai_providers
        
        # Asegurar que existe el directorio shared
        COMMAND_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info("🧠 Orquestador IA-EN-RVT inicializado")
    
    def set_autonomy(self, nivel: int) -> bool:
        """Configurar nivel de autonomía (1-5)"""
        if 1 <= nivel <= 5:
            self.autonomia = nivel
            logger.info(f"🎚️ Autonomía establecida en {nivel}")
            return True
        return False
    
    def set_ai_provider(self, provider):
        """Conectar proveedor de IA para procesamiento avanzado"""
        self.ai_provider = provider
        logger.info("🔗 Proveedor de IA conectado al orquestador")
    
    def process(self, texto: str, usar_ia: bool = True) -> Dict[str, Any]:
        """Procesar comando en lenguaje natural y generar comando BIM"""
        
        logger.info(f"📝 Procesando: {texto[:50]}...")
        
        # 1. Parsear intención básica
        intencion = self.parser.parsear_intencion(texto)
        
        # 2. Si hay IA disponible y confianza baja, usar IA para mejor interpretación
        if usar_ia and self.ai_provider and intencion["confianza"] < 0.8:
            intencion = self._mejorar_con_ia(texto, intencion)
        
        # 3. Crear comando BIM según protocolo
        comando = self.protocol.crear_comando(
            accion=intencion["accion"],
            elemento=intencion["elemento"],
            payload=intencion["payload"],
            autonomia=self.autonomia,
            rollback=True
        )
        
        # 4. Validar comando
        es_valido, errores = self.protocol.validar_comando(comando)
        
        if not es_valido:
            return {
                "exito": False,
                "mensaje": f"Comando inválido: {', '.join(errores)}",
                "comando": comando
            }
        
        # 5. Verificar nivel de autonomía
        resultado = self._ejecutar_segun_autonomia(comando, intencion)
        
        # 6. Guardar en historial
        self.historial.append({
            "texto": texto,
            "comando": comando,
            "resultado": resultado,
            "timestamp": datetime.now().isoformat()
        })
        
        return resultado
    
    def _mejorar_con_ia(self, texto: str, intencion: Dict[str, Any]) -> Dict[str, Any]:
        """Usar IA para mejorar la interpretación del comando"""
        
        prompt = f"""Analiza este comando BIM y extrae:
- accion: CREATE/MODIFY/DELETE/ANALYZE/QUERY/EXPORT/VALIDATE/OPTIMIZE
- elemento: Wall/Door/Window/Floor/Column/Beam/Level/Grid/Room/View
- payload: diccionario con parámetros (altura_m, nivel, tipo, etc.)

Comando: "{texto}"

Responde SOLO en JSON válido."""
        
        try:
            resultado = self.ai_provider.generate_response(
                message=prompt,
                system_prompt="Eres un parser de comandos BIM. Responde solo JSON válido."
            )
            
            if resultado.get("success"):
                import json
                # Intentar parsear la respuesta como JSON
                respuesta = resultado["message"]
                # Buscar JSON en la respuesta
                import re
                json_match = re.search(r'\{.*\}', respuesta, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    intencion.update(parsed)
                    intencion["confianza"] = 0.9
                    logger.info("✨ Interpretación mejorada con IA")
        except Exception as e:
            logger.warning(f"⚠️ Error usando IA para interpretar: {e}")
        
        return intencion
    
    def _ejecutar_segun_autonomia(self, comando: Dict[str, Any], intencion: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar comando según nivel de autonomía"""
        
        nivel = self.autonomia
        accion = comando["accion"]
        
        # Nivel 1: Solo confirmar, no ejecutar nada
        if nivel == 1:
            return {
                "exito": True,
                "estado": "REQUIERE_CONFIRMACION",
                "mensaje": f"⚠️ Comando preparado. Requiere confirmación manual.",
                "comando": comando,
                "accion_pendiente": True
            }
        
        # Nivel 2: Solo operaciones de consulta/análisis
        if nivel == 2 and accion not in ["QUERY", "ANALYZE"]:
            return {
                "exito": True,
                "estado": "REQUIERE_CONFIRMACION",
                "mensaje": f"⚠️ Acción {accion} requiere autonomía 3+",
                "comando": comando,
                "accion_pendiente": True
            }
        
        # Nivel 3-5: Ejecutar según tipo de acción
        if nivel >= 3:
            # Escribir comando para Revit
            self._guardar_comando_para_revit(comando)
            
            return {
                "exito": True,
                "estado": "ENVIADO_A_REVIT",
                "mensaje": f"✅ Comando BIM generado y listo para ejecutar en Revit",
                "comando": comando,
                "archivo_salida": str(COMMAND_OUTPUT_PATH),
                "instruccion": "Ejecuta RunCommand en pyRevit para aplicar"
            }
        
        return {
            "exito": False,
            "mensaje": "Nivel de autonomía no reconocido",
            "comando": comando
        }
    
    def _guardar_comando_para_revit(self, comando: Dict[str, Any]):
        """Guardar comando en archivo JSON para que pyRevit lo lea"""
        
        try:
            with open(COMMAND_OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(comando, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Comando guardado en {COMMAND_OUTPUT_PATH}")
            
            # También agregar al historial
            self._agregar_a_historial(comando)
            
        except Exception as e:
            logger.error(f"❌ Error guardando comando: {e}")
    
    def _agregar_a_historial(self, comando: Dict[str, Any]):
        """Agregar comando al historial para auditoría"""
        try:
            historial = []
            if COMMAND_HISTORY_PATH.exists():
                with open(COMMAND_HISTORY_PATH, "r", encoding="utf-8") as f:
                    historial = json.load(f)
            
            historial.append(comando)
            
            # Mantener solo últimos 100 comandos
            if len(historial) > 100:
                historial = historial[-100:]
            
            with open(COMMAND_HISTORY_PATH, "w", encoding="utf-8") as f:
                json.dump(historial, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.warning(f"⚠️ Error en historial: {e}")
    
    def get_ultimo_comando(self) -> Optional[Dict[str, Any]]:
        """Obtener último comando generado"""
        if COMMAND_OUTPUT_PATH.exists():
            with open(COMMAND_OUTPUT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
    
    def confirmar_comando(self) -> Dict[str, Any]:
        """Confirmar y ejecutar comando pendiente"""
        comando = self.get_ultimo_comando()
        if comando and comando.get("estado") == "PENDIENTE":
            comando["estado"] = "CONFIRMADO"
            self._guardar_comando_para_revit(comando)
            return {
                "exito": True,
                "mensaje": "✅ Comando confirmado y enviado a Revit",
                "comando": comando
            }
        return {
            "exito": False,
            "mensaje": "No hay comando pendiente para confirmar"
        }
    
    def cancelar_comando(self) -> Dict[str, Any]:
        """Cancelar comando pendiente"""
        comando = self.get_ultimo_comando()
        if comando:
            comando["estado"] = "CANCELADO"
            with open(COMMAND_OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(comando, f, indent=2, ensure_ascii=False)
            return {
                "exito": True,
                "mensaje": "❌ Comando cancelado"
            }
        return {
            "exito": False,
            "mensaje": "No hay comando para cancelar"
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obtener estado del orquestador"""
        return {
            "autonomia": self.autonomia,
            "ia_conectada": self.ai_provider is not None,
            "comandos_en_historial": len(self.historial),
            "ultimo_comando": self.get_ultimo_comando()
        }


# Instancia global del orquestador
orchestrator = Orchestrator()


if __name__ == "__main__":
    # Prueba del orquestador
    orc = Orchestrator()
    orc.set_autonomy(3)
    
    # Probar comandos
    pruebas = [
        "Crea un muro de 3 metros de altura en nivel 1",
        "Añade una puerta en el muro principal",
        "Analiza el modelo estructural",
        "Elimina las columnas del eje A"
    ]
    
    for prueba in pruebas:
        print(f"\n📝 Entrada: {prueba}")
        resultado = orc.process(prueba, usar_ia=False)
        print(f"✅ Resultado: {resultado['mensaje']}")
        if resultado.get("comando"):
            print(f"   Acción: {resultado['comando']['accion']}")
            print(f"   Elemento: {resultado['comando']['elemento']}")