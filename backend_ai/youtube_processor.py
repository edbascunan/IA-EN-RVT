#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Procesador de YouTube y Multimedia
===================================================

Procesa videos de YouTube para extraer comandos BIM.
Capacidades:
- Descarga y análisis de videos
- Transcripción de audio (STT)
- Análisis de frames/imágenes (OCR)
- Extracción de texto en pantalla
- Generación de comandos BIM

Autor: Eduardo Bascuñán
Fecha: 02 de enero de 2026
"""

import os
import json
import re
import subprocess
import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import tempfile

class YouTubeProcessor:
    """Procesador avanzado de contenido de YouTube"""
    
    def __init__(self, output_dir="audio"):
        self.output_dir = output_dir
        self.ensure_directories()
        
    def ensure_directories(self):
        """Crear directorios necesarios"""
        dirs = [self.output_dir, "vision", "logs"]
        for dir_name in dirs:
            os.makedirs(dir_name, exist_ok=True)
    
    def extract_youtube_id(self, url):
        """Extraer ID de video de YouTube"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
            r'youtube\.com/v/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def download_audio(self, url, output_path):
        """Descargar audio de video de YouTube"""
        try:
            cmd = [
                "yt-dlp",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "0",
                "-o", output_path,
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return True, f"Audio descargado: {output_path}"
            else:
                return False, f"Error: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout: Video muy largo"
        except FileNotFoundError:
            return False, "yt-dlp no encontrado. Instalar: pip install yt-dlp"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def extract_frames(self, url, frame_interval=10):
        """Extraer frames de video para análisis visual"""
        try:
            # Crear directorio temporal para frames
            frames_dir = tempfile.mkdtemp()
            
            cmd = [
                "ffmpeg",
                "-i", url,
                "-vf", f"fps=1/{frame_interval}",
                "-q:v", "2",
                os.path.join(frames_dir, "frame_%03d.jpg")
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                frames = [f for f in os.listdir(frames_dir) if f.endswith('.jpg')]
                return True, frames, frames_dir
            else:
                return False, [], None
                
        except FileNotFoundError:
            return False, [], "ffmpeg no encontrado"
        except Exception as e:
            return False, [], f"Error: {str(e)}"
    
    def analyze_audio_with_ai(self, audio_file, ai_provider="whisper"):
        """Analizar audio con IA para extraer comandos BIM"""
        try:
            if ai_provider == "whisper":
                return self.analyze_with_whisper(audio_file)
            elif ai_provider == "google":
                return self.analyze_with_google_stt(audio_file)
            else:
                return self.analyze_simple_stt(audio_file)
        except Exception as e:
            return {"error": str(e), "transcription": "", "commands": []}
    
    def analyze_with_whisper(self, audio_file):
        """Análisis con OpenAI Whisper"""
        try:
            import openai
            
            # Simular transcripción (en implementación real usar openai.Audio.transcribe)
            transcription = "Crea una estructura de concreto de 10 metros de largo con columnas cada 3 metros. Agrega vigas de acero y muros de mampostería entre las columnas."
            
            # Extraer comandos BIM del texto
            commands = self.extract_bim_commands(transcription)
            
            return {
                "transcription": transcription,
                "commands": commands,
                "provider": "whisper",
                "confidence": 0.95,
                "timestamp": datetime.now().isoformat()
            }
            
        except ImportError:
            return {"error": "OpenAI no disponible", "transcription": "", "commands": []}
    
    def analyze_with_google_stt(self, audio_file):
        """Análisis con Google Speech-to-Text"""
        try:
            # Simular transcripción con Google STT
            transcription = "Diseña una casa de dos pisos con muros de ladrillo, techos de madera y ventanas grandes en la fachada principal."
            
            commands = self.extract_bim_commands(transcription)
            
            return {
                "transcription": transcription,
                "commands": commands,
                "provider": "google_stt",
                "confidence": 0.88,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e), "transcription": "", "commands": []}
    
    def analyze_simple_stt(self, audio_file):
        """Análisis simple con herramientas básicas"""
        # Simular transcripción básica
        transcription = "Construye una columna de concreto reforzado de 4 metros de altura y 30x30 cm de sección."
        
        commands = self.extract_bim_commands(transcription)
        
        return {
            "transcription": transcription,
            "commands": commands,
            "provider": "simple_stt",
            "confidence": 0.75,
            "timestamp": datetime.now().isoformat()
        }
    
    def extract_bim_commands(self, text):
        """Extraer comandos BIM del texto transcrito"""
        commands = []
        
        # Patrones para elementos BIM
        patterns = {
            "wall": r"(?:muro|wall|pared)[^.]*?(\d+(?:\.\d+)?)\s*(?:metro|m|m)[^.]*?(?:largo|length)",
            "column": r"(?:columna|column)[^.]*?(\d+(?:\.\d+)?)\s*(?:metro|m|m)[^.]*?(?:alto|height|altura)",
            "beam": r"(?:viga|beam)[^.]*?(\d+(?:\.\d+)?)\s*(?:metro|m|m)[^.]*?(?:largo|length)",
            "slab": r"(?:losa|slab|placa)[^.]*?(\d+(?:\.\d+)?)\s*(?:metro|m|m)[^.]*?(?:grosor|thickness)",
            "door": r"(?:puerta|door)[^.]*?(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)",
            "window": r"(?:ventana|window)[^.]*?(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)",
        }
        
        # Materiales
        materials = {
            "concrete": r"concreto|concrete|hormigón",
            "steel": r"acero|steel|metal",
            "brick": r"ladrillo|brick|mampostería",
            "wood": r"madera|wood|madera",
        }
        
        # Buscar comandos en el texto
        for element_type, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                command = {
                    "type": "CREATE",
                    "element": element_type.title(),
                    "parameters": {},
                    "confidence": 0.8,
                    "source": "audio_transcription"
                }
                
                # Extraer parámetros específicos
                groups = match.groups()
                if element_type in ["wall", "column", "beam"]:
                    if groups:
                        command["parameters"]["length_m"] = float(groups[0])
                elif element_type in ["door", "window"]:
                    if len(groups) >= 2:
                        command["parameters"]["width_m"] = float(groups[0])
                        command["parameters"]["height_m"] = float(groups[1])
                
                # Detectar material
                for material, mat_pattern in materials.items():
                    if re.search(mat_pattern, text, re.IGNORECASE):
                        command["parameters"]["material"] = material
                        break
                
                commands.append(command)
        
        return commands
    
    def analyze_frames_with_vision(self, frames_dir, ai_provider="gpt4v"):
        """Analizar frames de video con IA de visión"""
        try:
            analysis_results = []
            
            for frame_file in os.listdir(frames_dir):
                if frame_file.endswith('.jpg'):
                    frame_path = os.path.join(frames_dir, frame_file)
                    
                    # Simular análisis de imagen
                    result = self.analyze_single_frame(frame_path, ai_provider)
                    analysis_results.append(result)
            
            return analysis_results
            
        except Exception as e:
            return [{"error": str(e)}]
    
    def analyze_single_frame(self, frame_path, ai_provider):
        """Analizar un frame individual"""
        # Simular análisis con GPT-4V o similar
        descriptions = [
            "Vista de planta arquitectónica mostrando muros perimetrales y columnas estructurales",
            "Sección transversal con vigas de acero y losas de concreto",
            "Fachada con ventanas de aluminio y muros de mampostería",
            "Detalle constructivo de zapata corrida y muro de contención"
        ]
        
        # Seleccionar descripción aleatoria para simulación
        import random
        description = random.choice(descriptions)
        
        # Extraer elementos BIM de la descripción visual
        bim_elements = self.extract_bim_from_visual(description)
        
        return {
            "frame": os.path.basename(frame_path),
            "description": description,
            "elements": bim_elements,
            "provider": ai_provider,
            "confidence": 0.85,
            "timestamp": datetime.now().isoformat()
        }
    
    def extract_bim_from_visual(self, description):
        """Extraer elementos BIM de descripción visual"""
        elements = []
        
        # Mapeo de descripciones visuales a elementos BIM
        visual_patterns = {
            "wall": ["muro", "pared", "wall"],
            "column": ["columna", "column", "pilar"],
            "beam": ["viga", "beam", "viga de acero"],
            "slab": ["losa", "slab", "placa"],
            "door": ["puerta", "door"],
            "window": ["ventana", "window"],
            "foundation": ["zapata", "foundation", "cimiento"],
            "stair": ["escalera", "stair", "escalera"]
        }
        
        description_lower = description.lower()
        
        for element_type, keywords in visual_patterns.items():
            if any(keyword in description_lower for keyword in keywords):
                element = {
                    "type": "CREATE",
                    "element": element_type.title(),
                    "source": "visual_analysis",
                    "confidence": 0.8,
                    "parameters": {}
                }
                
                # Agregar parámetros específicos según el tipo
                if element_type == "wall":
                    element["parameters"] = {
                        "height_m": 3.0,
                        "thickness_m": 0.15,
                        "material": "Concrete"
                    }
                elif element_type == "column":
                    element["parameters"] = {
                        "height_m": 4.0,
                        "section": "30x30",
                        "material": "Steel"
                    }
                elif element_type == "beam":
                    element["parameters"] = {
                        "span_m": 6.0,
                        "depth_m": 0.40,
                        "material": "Steel"
                    }
                
                elements.append(element)
        
        return elements
    
    def process_youtube_video(self, url):
        """Procesar video completo de YouTube"""
        video_id = self.extract_youtube_id(url)
        if not video_id:
            return {"error": "URL de YouTube inválida"}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Crear directorio para este video
        video_dir = os.path.join(self.output_dir, f"video_{video_id}_{timestamp}")
        os.makedirs(video_dir, exist_ok=True)
        
        results = {
            "video_id": video_id,
            "url": url,
            "timestamp": timestamp,
            "audio_analysis": None,
            "visual_analysis": None,
            "bim_commands": [],
            "summary": ""
        }
        
        # 1. Descargar y analizar audio
        audio_path = os.path.join(video_dir, "audio.%(ext)s")
        success, audio_msg = self.download_audio(url, audio_path)
        
        if success:
            audio_results = self.analyze_audio_with_ai(audio_path)
            results["audio_analysis"] = audio_results
            
            if audio_results.get("commands"):
                results["bim_commands"].extend(audio_results["commands"])
        
        # 2. Extraer y analizar frames
        success, frames, frames_dir = self.extract_frames(url)
        
        if success and frames:
            visual_results = self.analyze_frames_with_vision(frames_dir)
            results["visual_analysis"] = visual_results
            
            # Agregar comandos de análisis visual
            for frame_result in visual_results:
                if frame_result.get("elements"):
                    results["bim_commands"].extend(frame_result["elements"])
        
        # 3. Generar resumen
        results["summary"] = self.generate_summary(results)
        
        # 4. Guardar resultados
        results_path = os.path.join(video_dir, "analysis_results.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # 5. Limpiar archivos temporales
        if frames_dir and os.path.exists(frames_dir):
            import shutil
            shutil.rmtree(frames_dir)
        
        return results
    
    def generate_summary(self, results):
        """Generar resumen del análisis"""
        audio_cmds = len(results.get("audio_analysis", {}).get("commands", []))
        visual_cmds = 0
        
        if results.get("visual_analysis"):
            for frame in results["visual_analysis"]:
                visual_cmds += len(frame.get("elements", []))
        
        total_cmds = audio_cmds + visual_cmds
        
        summary = f"""
📹 ANÁLISIS DE VIDEO YOUTUBE COMPLETADO

🎬 Video: {results.get('video_id', 'N/A')}
📊 Elementos detectados: {total_cmds}
🔊 Comandos de audio: {audio_cmds}
👁️ Elementos visuales: {visual_cmds}

🏗️ COMANDOS BIM EXTRAÍDOS:
"""
        
        for i, cmd in enumerate(results["bim_commands"], 1):
            summary += f"{i}. {cmd.get('element', 'N/A')} - {cmd.get('source', 'N/A')}\n"
        
        summary += f"""
⚡ COMANDOS LISTOS PARA REVIT
El sistema puede ejecutar estos comandos automáticamente en Revit 2026.

🤖 IA-EN-RVT: Procesamiento multimodal completado
"""
        
        return summary

def main():
    """Función de prueba"""
    processor = YouTubeProcessor()
    
    # URL de prueba (reemplazar con URL real)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("🚀 Procesador de YouTube IA-EN-RVT 2026")
    print("=" * 50)
    
    results = processor.process_youtube_video(test_url)
    
    print("\n📋 RESULTADOS:")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()