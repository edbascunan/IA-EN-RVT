#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bot NLP Simple para IA-EN-RVT
=============================

Bot básico que funciona con procesamiento de lenguaje natural
"""

import re
import json
from datetime import datetime

class BotNLP:
    def __init__(self):
        self.comandos = {
            'crear.*muro': self.crear_muro,
            'analizar.*proyecto': self.analizar_proyecto,
            'ayuda': self.mostrar_ayuda,
            'estadísticas': self.mostrar_estadisticas
        }
    
    def procesar_comando(self, texto):
        """Procesar comando en lenguaje natural"""
        texto = texto.lower().strip()
        
        for patron, funcion in self.comandos.items():
            if re.search(patron, texto):
                return funcion()
        
        return "No entendí el comando. Escribe 'ayuda' para ver comandos disponibles."
    
    def crear_muro(self):
        return "Muro creado desde (0,0) hasta (5,0) altura 3.0"
    
    def analizar_proyecto(self):
        return "Análisis: 15 muros, 8 ventanas, 4 puertas, 3 niveles"
    
    def mostrar_ayuda(self):
        return """Comandos disponibles:
- 'crear muro'
- 'analizar proyecto'  
- 'estadísticas'
- 'ayuda'"""
    
    def mostrar_estadisticas(self):
        return "Estadísticas: Proyecto con 25 elementos totales"

if __name__ == "__main__":
    bot = BotNLP()
    
    # Prueba simple
    comando = input("Escribe tu comando: ")
    respuesta = bot.procesar_comando(comando)
    print(f"Bot: {respuesta}")