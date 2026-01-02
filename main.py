#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archivo principal que ejecuta el bot_avanzado.py
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar y ejecutar el bot avanzado
from bot_avanzado import AdvancedBot

if __name__ == "__main__":
    print("🚀 EJECUTANDO BOT AVANZADO CON RAG Y MEMORIA...")
    bot = AdvancedBot()
    bot.run()