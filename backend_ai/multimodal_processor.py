#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Sistema Multimodal Completo
============================================

Sistema completo de procesamiento multimodal para BIM:
- Videos de YouTube (audio + frames)
- Detección de audio (STT)
- Análisis de texto (OCR)
- Procesamiento de imágenes (CV)
- Generación de CUALQUIER comando BIM
- Aprendizaje de contenido de construcción

Autor: Eduardo Bascuñán
Fecha: 02 de enero de 2026
"""

import os
import json
import re
import subprocess
import requests
import tempfile
import shutil
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import sqlite3
import hashlib

class BIMMultimodalProcessor:
    """Procesador multimodal completo para BIM"""
    
    def __init__(self, output_dir="multimodal"):
        self.output_dir = output_dir
        self.db_path = os.path.join(output_dir, "bim_knowledge.db")
        self.ensure_directories()
        self.init_database()
        
    def ensure_directories(self):
        """Crear directorios necesarios"""
        dirs = [
            self.output_dir, 
            os.path.join(self.output_dir, "youtube"),
            os.path.join(self.output_dir, "audio"),
            os.path.join(self.output_dir, "frames"),
            os.path.join(self.output_dir, "images"),
            os.path.join(self.output_dir, "commands"),
            os.path.join(self.output_dir, "learning"),
            "logs"
        ]
        for dir_name in dirs:
            os.makedirs(dir_name, exist_ok=True)
    
    def init_database(self):
        """Inicializar base de conocimiento BIM"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de elementos BIM aprendidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bim_elements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                element_type TEXT NOT NULL,
                description TEXT,
                parameters TEXT,  -- JSON
                source_type TEXT, -- 'youtube', 'audio', 'image', 'text'
                source_content TEXT,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usage_count INTEGER DEFAULT 0
            )
        ''')
        
        # Tabla de comandos ejecutados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS executed_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT,  -- JSON
                element_type TEXT,
                success BOOLEAN,
                execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                revit_element_id TEXT,
                feedback TEXT
            )
        ''')
        
        # Tabla de patrones aprendidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT NOT NULL,
                action TEXT NOT NULL,
                element_type TEXT,
                confidence REAL,
                examples TEXT,  -- JSON array
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def extract_youtube_content(self, url):
        """Extraer contenido completo de YouTube"""
        video_id = self.extract_youtube_id(url)
        if not video_id:
            return {"error": "URL de YouTube inválida"}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_dir = os.path.join(self.output_dir, "youtube", f"{video_id}_{timestamp}")
        os.makedirs(video_dir, exist_ok=True)
        
        results = {
            "video_id": video_id,
            "url": url,
            "timestamp": timestamp,
            "audio_transcription": None,
            "visual_analysis": [],
            "text_ocr": [],
            "bim_commands": [],
            "learning_results": {}
        }
        
        # 1. Descargar y procesar audio
        audio_path = os.path.join(video_dir, "audio.%(ext)s")
        success, audio_msg = self.download_youtube_audio(url, audio_path)
        
        if success:
            # Transcribir audio
            transcription = self.transcribe_audio(audio_path)
            results["audio_transcription"] = transcription
            
            # Extraer comandos del audio
            audio_commands = self.extract_bim_commands_from_text(transcription)
            results["bim_commands"].extend(audio_commands)
            
            # Aprender del contenido de audio
            self.learn_from_audio(transcription, url)
        
        # 2. Extraer y analizar frames
        frames_success, frames, frames_dir = self.extract_video_frames(url, video_dir)
        
        if frames_success and frames:
            # Analizar cada frame
            for frame_file in frames:
                frame_path = os.path.join(frames_dir, frame_file)
                
                # OCR para texto en pantalla
                ocr_text = self.extract_text_from_image(frame_path)
                if ocr_text:
                    results["text_ocr"].append({
                        "frame": frame_file,
                        "text": ocr_text,
                        "confidence": 0.9
                    })
                    
                    # Extraer comandos del texto OCR
                    ocr_commands = self.extract_bim_commands_from_text(ocr_text)
                    results["bim_commands"].extend(ocr_commands)
                
                # Análisis visual de construcción
                visual_analysis = self.analyze_construction_frame(frame_path)
                if visual_analysis:
                    results["visual_analysis"].append(visual_analysis)
                    
                    # Extraer elementos BIM de análisis visual
                    visual_commands = self.extract_bim_from_visual_description(visual_analysis)
                    results["bim_commands"].extend(visual_commands)
                    
                    # Aprender del contenido visual
                    self.learn_from_visual(visual_analysis, url)
        
        # 3. Generar comandos BIM avanzados
        advanced_commands = self.generate_advanced_bim_commands(results)
        results["bim_commands"].extend(advanced_commands)
        
        # 4. Guardar y aprender
        self.save_learning_results(results)
        
        # 5. Limpiar archivos temporales
        if frames_dir and os.path.exists(frames_dir):
            shutil.rmtree(frames_dir)
        
        return results
    
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
    
    def download_youtube_audio(self, url, output_path):
        """Descargar audio de YouTube"""
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
    
    def extract_video_frames(self, url, output_dir):
        """Extraer frames del video"""
        try:
            frames_dir = os.path.join(output_dir, "frames")
            os.makedirs(frames_dir, exist_ok=True)
            
            # Extraer frames cada 10 segundos
            cmd = [
                "ffmpeg",
                "-i", url,
                "-vf", "fps=1/10",
                "-q:v", "2",
                os.path.join(frames_dir, "frame_%04d.jpg")
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
    
    def transcribe_audio(self, audio_file):
        """Transcribir audio a texto"""
        try:
            # Simulación de transcripción avanzada
            # En implementación real usar: OpenAI Whisper, Google STT, etc.
            
            transcriptions = [
                "Crea una estructura de concreto de 10 metros de largo con columnas cada 3 metros. Agrega vigas de acero y muros de mampostería entre las columnas.",
                "Diseña una casa de dos pisos con muros de ladrillo, techos de madera y ventanas grandes en la fachada principal.",
                "Construye una columna de concreto reforzado de 4 metros de altura y 30x30 cm de sección transversal.",
                "Instala un sistema de tuberías de PVC de 4 pulgadas para agua potable y otro de 6 pulgadas para aguas residuales.",
                "Crea una escalera de concreto de 3 metros de ancho con 15 escalones y contrahuella de 18 centímetros.",
                "Diseña una zapata corrida de concreto de 80 cm de ancho por 1.2 metros de profundidad para muro de contención.",
                "Instala ductos rectangulares de HVAC de 40x20 cm para sistema de climatización del edificio.",
                "Crea una losa de entrepiso de concreto reforzado de 15 cm de espesor con malla electrosoldada.",
                "Construye un pórtico de acero con viga principal de 8 metros de luz y columnas de perfil IPE 300.",
                "Diseña un muro cortina de aluminio y vidrio de 20 metros de largo por 4 metros de alto."
            ]
            
            import random
            return random.choice(transcriptions)
            
        except Exception as e:
            return f"Error en transcripción: {str(e)}"
    
    def extract_text_from_image(self, image_path):
        """Extraer texto de imagen (OCR)"""
        try:
            # Simulación de OCR
            # En implementación real usar: Tesseract, Google Vision, etc.
            
            ocr_texts = [
                "Planta Arquitectónica - Primer Piso",
                "Sección A-A: Vigas de Concreto Reforzado",
                "Detalles Constructivos - Zapata Corrida",
                "Esquema Hidráulico - Sistema de Agua Potable",
                "Plan de Instalaciones Eléctricas",
                "Cortes y Elevaciones - Fachada Principal",
                "Detalles de Acabados - Pisos y Revestimientos",
                "Plano de Estructuras - Pórticos de Acero",
                "Sistema HVAC - Distribución de Ductos",
                "Detalles de Ventanas y Puertas"
            ]
            
            import random
            return random.choice(ocr_texts)
            
        except Exception as e:
            return f"Error en OCR: {str(e)}"
    
    def analyze_construction_frame(self, image_path):
        """Analizar frame de construcción con IA"""
        try:
            # Simulación de análisis visual avanzado
            # En implementación real usar: GPT-4V, Claude Vision, etc.
            
            analyses = [
                {
                    "description": "Vista de planta arquitectónica mostrando muros perimetrales de ladrillo y columnas estructurales de concreto cada 4 metros",
                    "elements_detected": ["Wall_Brick", "Column_Concrete", "Slab_Concrete"],
                    "materials": ["Brick", "Concrete", "Steel"],
                    "dimensions": {"span": "12m", "height": "3.5m", "thickness": "0.20m"},
                    "construction_phase": "Structure"
                },
                {
                    "description": "Sección transversal con vigas de acero IPE 300 y losa de concreto de 15 cm de espesor",
                    "elements_detected": ["Beam_Steel", "Slab_Concrete", "Column_Steel"],
                    "materials": ["Steel", "Concrete"],
                    "dimensions": {"span": "8m", "depth": "0.30m", "slab_thickness": "0.15m"},
                    "construction_phase": "Structure"
                },
                {
                    "description": "Fachada con muro cortina de aluminio y vidrio, ventanas de 2x1.5 metros",
                    "elements_detected": ["CurtainWall", "Window", "Door"],
                    "materials": ["Aluminum", "Glass", "Steel"],
                    "dimensions": {"window_width": "2.0m", "window_height": "1.5m"},
                    "construction_phase": "Envelope"
                },
                {
                    "description": "Sistema MEP con tuberías de PVC y ductos rectangulares de HVAC",
                    "elements_detected": ["Pipe_PVC", "Duct_Rectangular", "Equipment_HVAC"],
                    "materials": ["PVC", "Steel", "Insulation"],
                    "dimensions": {"pipe_diameter": "0.10m", "duct_size": "0.40x0.20m"},
                    "construction_phase": "MEP"
                },
                {
                    "description": "Cimentación con zapatas aisladas de concreto reforzado y vigas de cimentación",
                    "elements_detected": ["Footing", "Grade_Beam", "Rebar"],
                    "materials": ["Concrete", "Rebar"],
                    "dimensions": {"footing_size": "1.5x1.5m", "beam_width": "0.40m"},
                    "construction_phase": "Foundation"
                }
            ]
            
            import random
            return random.choice(analyses)
            
        except Exception as e:
            return {"error": str(e)}
    
    def extract_bim_commands_from_text(self, text):
        """Extraer comandos BIM de texto transcrito"""
        commands = []
        
        # Patrones avanzados para elementos BIM
        patterns = {
            "Wall": {
                "patterns": [
                    r"muro[s]?\s+de\s+([a-zA-Z]+)\s+de\s+(\d+(?:\.\d+)?)\s*(?:metro|m)s?\s+de\s+largo",
                    r"(?:wall|pared)\s+([a-zA-Z]+)\s+(\d+(?:\.\d+)?)\s*(?:m|metro)s?\s*de\s*largo",
                    r"construye\s+un\s+muro\s+de\s+([a-zA-Z]+)\s+de\s+(\d+(?:\.\d+)?)\s*metros"
                ],
                "materials": ["ladrillo", "concreto", "acero", "madera", "bloque"]
            },
            "Column": {
                "patterns": [
                    r"columna[s]?\s+de\s+([a-zA-Z]+)\s+de\s+(\d+(?:\.\d+)?)\s*(?:metro|m)s?\s+de\s+alto",
                    r"(?:column|pilar)\s+([a-zA-Z]+)\s+(\d+(?:\.\d+)?)\s*(?:m|metro)s?\s*de\s*alto",
                    r"construye\s+una\s+columna\s+de\s+([a-zA-Z]+)\s+de\s+(\d+(?:\.\d+)?)\s*metros\s+de\s*alto"
                ],
                "materials": ["concreto", "acero", "hierro"]
            },
            "Beam": {
                "patterns": [
                    r"viga[s]?\s+de\s+([a-zA-Z]+)\s+de\s+(\d+(?:\.\d+)?)\s*(?:metro|m)s?\s+de\s+largo",
                    r"(?:beam|viga)\s+([a-zA-Z]+)\s+(\d+(?:\.\d+)?)\s*(?:m|metro)s?\s*de\s*largo",
                    r"instala\s+una\s+viga\s+de\s+([a-zA-Z]+)\s+de\s+(\d+(?:\.\d+)?)\s*metros\s*de\s*luz"
                ],
                "materials": ["acero", "concreto", "madera"]
            },
            "Floor": {
                "patterns": [
                    r"losa[s]?\s+de\s+([a-zA-Z]+)\s+de\s+(\d+(?:\.\d+)?)\s*(?:metro|m)s?\s+de\s+grosor",
                    r"(?:slab|floor|placa)\s+([a-zA-Z]+)\s+(\d+(?:\.\d+)?)\s*(?:cm|centímetro)s?\s*de\s*espesor",
                    r"crea\s+una\s+losa\s+de\s+([a-zA-Z]+)\s+de\s+(\d+(?:\.\d+)?)\s*centímetros"
                ],
                "materials": ["concreto", "acero", "madera"]
            },
            "Pipe": {
                "patterns": [
                    r"tubería[s]?\s+de\s+([a-zA-Z]+)\s+de\s+(\d+(?:\.\d+)?)\s*(?:pulgada|inch|cm)",
                    r"(?:pipe|tubo)\s+([a-zA-Z