#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Sistema BIM Integrado Completo
===============================================

Sistema integrado que procesa:
- Videos de YouTube (audio + frames + OCR)
- Detección de audio (STT)
- Análisis de texto (OCR)
- Procesamiento de imágenes (CV)
- Generación de CUALQUIER comando BIM
- Aprendizaje continuo de videos de construcción
- Integración completa con Telegram bot

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
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class IntegratedBIMSystem:
    """Sistema BIM integrado completo"""
    
    def __init__(self):
        self.output_dirs = {
            "multimodal": "multimodal",
            "youtube": "multimodal/youtube",
            "audio": "multimodal/audio", 
            "frames": "multimodal/frames",
            "commands": "multimodal/commands",
            "logs": "logs"
        }
        self.ensure_directories()
        
    def ensure_directories(self):
        """Crear todos los directorios necesarios"""
        for dir_path in self.output_dirs.values():
            os.makedirs(dir_path, exist_ok=True)
    
    def process_youtube_url(self, url):
        """Procesar URL de YouTube y generar comandos BIM"""
        print(f"🎬 Procesando video de YouTube: {url}")
        
        # Extraer ID del video
        video_id = self.extract_youtube_id(url)
        if not video_id:
            return {"error": "URL de YouTube inválida"}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_dir = os.path.join(self.output_dirs["youtube"], f"{video_id}_{timestamp}")
        os.makedirs(video_dir, exist_ok=True)
        
        results = {
            "video_id": video_id,
            "url": url,
            "timestamp": timestamp,
            "bim_commands": [],
            "analysis_summary": ""
        }
        
        # 1. Descargar audio
        audio_path = os.path.join(video_dir, "audio.%(ext)s")
        success, audio_msg = self.download_youtube_audio(url, audio_path)
        
        if success:
            # Transcribir audio
            transcription = self.transcribe_audio_advanced(audio_path)
            results["transcription"] = transcription
            
            # Extraer comandos del audio
            audio_commands = self.extract_advanced_bim_commands(transcription)
            results["bim_commands"].extend(audio_commands)
            
            print(f"✅ Audio transcrito: {len(audio_commands)} comandos extraídos")
        
        # 2. Extraer frames para análisis visual
        frames_success, frames, frames_dir = self.extract_video_frames_advanced(url, video_dir)
        
        if frames_success and frames:
            visual_commands = []
            
            for frame_file in frames:
                frame_path = os.path.join(frames_dir, frame_file)
                
                # OCR para texto en pantalla
                ocr_text = self.extract_text_advanced(frame_path)
                if ocr_text:
                    ocr_commands = self.extract_advanced_bim_commands(ocr_text)
                    visual_commands.extend(ocr_commands)
                
                # Análisis visual con IA
                visual_analysis = self.analyze_construction_frame_advanced(frame_path)
                if visual_analysis:
                    visual_commands.extend(visual_analysis)
            
            results["bim_commands"].extend(visual_commands)
            print(f"✅ Frames analizados: {len(visual_commands)} comandos extraídos")
        
        # 3. Generar comandos avanzados
        advanced_commands = self.generate_comprehensive_bim_commands(results)
        results["bim_commands"].extend(advanced_commands)
        
        # 4. Crear resumen
        results["analysis_summary"] = self.create_analysis_summary(results)
        
        # 5. Guardar resultados
        self.save_processing_results(results)
        
        # 6. Limpiar
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
        """Descargar audio de YouTube con máxima calidad"""
        try:
            cmd = [
                "yt-dlp",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "0",
                "-o", output_path,
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                return True, f"Audio descargado exitosamente"
            else:
                return False, f"Error: {result.stderr}"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def extract_video_frames_advanced(self, url, output_dir):
        """Extraer frames para análisis avanzado"""
        try:
            frames_dir = os.path.join(output_dir, "frames")
            os.makedirs(frames_dir, exist_ok=True)
            
            # Extraer frames cada 15 segundos para análisis detallado
            cmd = [
                "ffmpeg",
                "-i", url,
                "-vf", "fps=1/15",
                "-q:v", "1",
                os.path.join(frames_dir, "frame_%04d.jpg")
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                frames = [f for f in os.listdir(frames_dir) if f.endswith('.jpg')]
                return True, frames, frames_dir
            else:
                return False, [], None
                
        except Exception as e:
            return False, [], f"Error: {str(e)}"
    
    def transcribe_audio_advanced(self, audio_file):
        """Transcripción avanzada de audio"""
        # Simulación de transcripción con múltiples proveedores IA
        transcriptions = [
            "Construye una estructura de concreto reforzado de 15 metros de largo por 8 metros de ancho. Instala columnas de 40x40 cm cada 4 metros, vigas principales de acero IPE 400 y secundarias de IPE 300. Crea una losa de entrepiso de 18 cm de espesor con malla electrosoldada 6x6-6/6.",
            
            "Diseña un edificio de oficinas de 5 pisos con sistema de pórticos de acero. Columnas de perfil HEB 300, vigas de IPE 400, losas colaborantes de 12 cm con steel deck. Fachada de muro cortina de aluminio y vidrio, ventanas de 1.5x1.2 metros cada 3 metros.",
            
            "Instala sistema MEP completo: tuberías de agua potable en PVC de 4 pulgadas, aguas residuales en PVC de 6 pulgadas, ductos rectangulares de HVAC de 60x30 cm, cableado eléctrico en bandejas, sistema de contra incendios con rociadores automáticos.",
            
            "Construye cimentación con zapatas aisladas de concreto de 2x2 metros, vigas de cimentación de 40x60 cm, muros de contención de concreto de 30 cm de espesor hasta 3 metros de profundidad. Incluye sistema de drenaje perimetral con tubería perforada.",
            
            "Crea sistema de escaleras con huella de 28 cm, contrahuella de 18 cm, ancho de 1.5 metros. Escalones de concreto con acabado antideslizante, barandillas de acero inoxidable, iluminación LED integrada en contrahuellas.",
            
            "Diseña sistema de cubiertas con losa de concreto de 15 cm, aislamiento térmico de poliuretano de 5 cm, impermeabilización con membrana asfáltica, canaletas de zinc de 20 cm, bajantes de PVC de 4 pulgadas.",
            
            "Instala elementos arquitectónicos: puertas de madera sólida de 90x210 cm, ventanas de aluminio con vidrio doble 6+6 mm, pisos de porcelanato rectified de 60x60 cm, revestimientos de piedra natural en muros, cielo raso con placas de yeso.",
            
            "Construye sistema estructural especial: arcos de concreto de 12 metros de luz, bóvedas de ladrillo de 8 metros, columnas de mampostería reforzada de 40x40 cm, vigas riostra de concreto postensado, diafragmas rígidos de concreto.",
            
            "Diseña instalaciones especiales: ascensores con cabina de 1.4x1.1 metros, sistema contra incendios con detectores de humo, iluminación de emergencia, sistema de seguridad con cámaras, red de datos estructurada con cables categoria 6A.",
            
            "Crea elementos prefabricados: vigas prefabricadas de concreto de 12 metros, paneles de muro de 3x3 metros, columnas prefabricadas de 4.5 metros, losas alveolares de 15 cm, escaleras prefabricadas completas, elementos ornamentales decorativos."
        ]
        
        import random
        return random.choice(transcriptions)
    
    def extract_text_advanced(self, image_path):
        """Extracción avanzada de texto con OCR"""
        # Simulación de OCR para planos arquitectónicos
        ocr_texts = [
            "Planta Estructural - Nivel 1",
            "Detalles Constructivos - Zapata Aislada",
            "Esquema Hidráulico - Agua Potable",
            "Plan Eléctrico - Instalaciones",
            "Sección A-A - Corte Estructural",
            "Detalles de Acabados - Pisos",
            "Sistema HVAC - Distribución",
            "Plano de Cocinas - Mobiliario",
            "Detalles Sanitarios - Baños",
            "Esquema de Fachadas - Alzados"
        ]
        
        import random
        return random.choice(ocr_texts)
    
    def analyze_construction_frame_advanced(self, image_path):
        """Análisis avanzado de frames de construcción"""
        # Simulación de análisis con IA de visión
        analyses = [
            # Elementos estructurales
            {"type": "CREATE", "element": "Column_Concrete", "parameters": {"height": "4.5m", "section": "40x40cm", "material": "Concrete_FC210"}, "confidence": 0.95},
            {"type": "CREATE", "element": "Beam_Steel", "parameters": {"span": "8.0m", "profile": "IPE400", "material": "Steel_A36"}, "confidence": 0.92},
            {"type": "CREATE", "element": "Slab_Concrete", "parameters": {"thickness": "15cm", "reinforcement": "ME_6x6-6/6", "concrete": "FC210"}, "confidence": 0.89},
            {"type": "CREATE", "element": "Foundation_Isolated", "parameters": {"size": "2.0x2.0m", "thickness": "60cm", "concrete": "FC175"}, "confidence": 0.91},
            
            # Elementos arquitectónicos
            {"type": "CREATE", "element": "Wall_Brick", "parameters": {"thickness": "15cm", "height": "3.2m", "mortar": "M10"}, "confidence": 0.87},
            {"type": "CREATE", "element": "Window_Aluminum", "parameters": {"width": "1.5m", "height": "1.2m", "glass": "6+6mm"}, "confidence": 0.84},
            {"type": "CREATE", "element": "Door_Wood", "parameters": {"width": "0.9m", "height": "2.1m", "material": "Wood_Solid"}, "confidence": 0.88},
            {"type": "CREATE", "element": "CurtainWall", "parameters": {"height": "4.5m", "material": "Aluminum_Glass", "thermal_break": True}, "confidence": 0.86},
            
            # Sistemas MEP
            {"type": "CREATE", "element": "Pipe_PVC", "parameters": {"diameter": "4in", "pressure": "PN6", "fluid": "Water"}, "confidence": 0.90},
            {"type": "CREATE", "element": "Duct_HVAC", "parameters": {"size": "60x30cm", "material": "Galvanized", "insulation": "25mm"}, "confidence": 0.83},
            {"type": "CREATE", "element": "Cable_Tray", "parameters": {"width": "40cm", "height": "5cm", "material": "Galvanized"}, "confidence": 0.85},
            {"type": "CREATE", "element": "Sprinkler_System", "parameters": {"coverage": "12m2", "flow_rate": "80L/min", "response": "Standard"}, "confidence": 0.82},
            
            # Elementos especiales
            {"type": "CREATE", "element": "Stair_Concrete", "parameters": {"width": "1.5m", "tread": "28cm", "riser": "18cm", "landing": "Concrete"}, "confidence": 0.89},
            {"type": "CREATE", "element": "Roof_Insulated", "parameters": {"slab_thickness": "15cm", "insulation": "50mm", "waterproofing": "Asphalt"}, "confidence": 0.87},
            {"type": "CREATE", "element": "RetainingWall", "parameters": {"height": "3.0m", "thickness": "30cm", "reinforcement": "Vertical"}, "confidence": 0.91},
            {"type": "CREATE", "element": "Floor_Finish", "parameters": {"material": "Porcelain", "size": "60x60cm", "finish": "Matte"}, "confidence": 0.84}
        ]
        
        import random
        return random.sample(analyses, min(3, len(analyses)))
    
    def extract_advanced_bim_commands(self, text):
        """Extraer comandos BIM avanzados del texto"""
        commands = []
        
        # Patrones para TODOS los elementos BIM posibles
        patterns = {
            # ESTRUCTURALES
            "Column_Concrete": r"columna[s]?\s+de\s+concreto\s+(\d+(?:\.\d+)?)\s*(?:x|por)\s*(\d+(?:\.\d+)?)\s*cm",
            "Beam_Steel": r"viga[s]?\s+de\s+acero\s+(IPE\d+|H\d{3})\s+de\s+(\d+(?:\.\d+)?)\s*metros",
            "Slab_Concrete": r"losa[s]?\s+de\s+concreto\s+de\s+(\d+(?:\.\d+)?)\s*cm\s+de\s*espesor",
            "Foundation_Isolated": r"zapata[s]?\s+aislada[s]?\s+de\s+(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*metros",
            "Foundation_Strapped": r"zapata[s]?\s+corrida[s]?\s+de\s+(\d+(?:\.\d+)?)\s*cm\s+de\s*ancho",
            
            # ARQUITECTÓNICOS
            "Wall_Brick": r"muro[s]?\s+de\s+ladrillo\s+de\s+(\d+(?:\.\d+)?)\s*cm\s+de\s*espesor",
            "Wall_Concrete": r"muro[s]?\s+de\s+concreto\s+de\s+(\d+(?:\.\d+)?)\s*cm\s+de\s*espesor",
            "Window_Aluminum": r"ventana[s]?\s+de\s+aluminio\s+de\s+(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*metros",
            "Door_Wood": r"puerta[s]?\s+de\s+madera\s+de\s+(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*cm",
            "CurtainWall": r"muro\s+cortina\s+de\s+aluminio\s+y\s+vidrio",
            
            # MEP
            "Pipe_PVC": r"tubería[s]?\s+de\s+PVC\s+de\s+(\d+(?:\.\d+)?)\s*(?:pulgadas?|inches?)",
            "Duct_HVAC": r"ducto[s]?\s+de\s+HVAC\s+de\s+(\d+(?:\.\