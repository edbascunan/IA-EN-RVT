#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA_RVT Setup Script - Versión Funcional
======================================
Script para generar la estructura completa del proyecto IA_RVT

Uso:
    python ebf.py

Autor: Eduardo Bascuñán
Fecha: 2026-01-01
"""

import os
import sys
from pathlib import Path


def create_directory_structure():
    """Crear estructura de directorios del proyecto"""
    directories = [
        'backend_ai/agents',
        'backend_ai/rag',
        'backend_ai/vision',
        'backend_ai/audio',
        'backend_ai/automation',
        'backend_ai/protocol',
        'backend_ai/shared',
        'revit_executor/IA_RVT.extension/IA_RVT.tab/Executor.panel/RunCommand.pushbutton',
        'docs',
        'tests',
        'logs'
    ]
    
    print("📁 Creando estructura de directorios...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    print("\n✅ Estructura de directorios creada\n")


def create_file(filepath, content):
    """Crear archivo con contenido"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✅ {filepath}")


def create_all_files():
    """Crear todos los archivos del proyecto"""
    print("📝 Creando archivos del proyecto...\n")
    
    # README.md
    create_file('README.md', '''# 🤖 IA_RVT 2026

**Sistema BIM Autónomo con Inteligencia Artificial para Revit 2026**

IA_RVT es un sistema revolucionario que permite controlar Revit 2026 mediante comandos de lenguaje natural, voz, imágenes y videos.

## ✨ Características Principales

- 🤖 Bot Master de Telegram
- 🧠 Sistema Multi-Agente
- 🔐 Seguridad Industrial
- 📱 Control desde móvil
- 🏗️ Modelado BIM automático

## 🚀 Instalación Rápida

1. Clonar repositorio: `git clone https://github.com/edbascunan/IA_RVT.git`
2. Crear entorno virtual: `python -m venv venv`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Configurar token: `cp .env.example .env` (añadir TELEGRAM_TOKEN)
5. Ejecutar bot: `python backend_ai/bot_master.py`

## 📱 Uso

Comandos de Telegram:
- `/start` - Iniciar bot
- `/autonomia [1-5]` - Configurar nivel de autonomía
- `/status` - Estado del sistema
- `/help` - Ayuda detallada

Ejemplos:
- "Crea un muro de 3 metros en nivel 1"
- "Analiza el modelo actual"
- "Genera reporte de materiales"

## 🎚️ Niveles de Autonomía

1. Solo confirmar
2. Ejecutar simple
3. Ejecutar normal (recomendado)
4. Ejecutar complejo
5. Totalmente autónomo

## 📁 Estructura

```
IA_RVT/
├── backend_ai/              # Backend IA
│   ├── bot_master.py       # Bot Telegram
│   ├── orchestrator.py     # Orquestador
│   ├── agents/             # Agentes especializados
│   ├── rag/                # Sistema RAG
│   ├── vision/             # Análisis de imágenes
│   ├── audio/              # Speech-to-Text
│   └── protocol/           # Protocolo BIM
├── revit_executor/         # Executor Revit
│   └── IA_RVT.extension/   # Extensión pyRevit
├── tests/                  # Tests
├── docs/                   # Documentación
└── logs/                   # Logs
```

## 👨‍💻 Autor

**Eduardo Bascuñán**
- GitHub: [@edbascunan](https://github.com/edbascunan)
- Email: contacto@edbascunan.com

> "El humano diseña la intención. La IA decide la acción. Revit ejecuta la realidad."

*Última actualización: 01 de enero de 2026*
''')

    # .gitignore
    create_file('.gitignore', '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg-info/
dist/
build/

# Entorno
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/*.log

# Revit
*.rvt.backup*

# Sistema
Thumbs.db

# Datos temporales
backend_ai/shared/*.json
!backend_ai/shared/.gitkeep
''')

    # .env.example
    create_file('.env.example', '''# IA_RVT - Variables de Entorno
# Configura estas variables en un archivo .env

# OBLIGATORIO: Token de Bot de Telegram
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# OPCIONAL: OpenAI API Key
# OPENAI_API_KEY=sk-...

# OPCIONAL: Anthropic API Key
# ANTHROPIC_API_KEY=sk-ant-...

# Configuración del sistema
LOG_LEVEL=INFO
MAX_COMMANDS_PER_HOUR=100
''')

    # requirements.txt
    create_file('requirements.txt', '''# IA_RVT - Dependencias Python

# Bot de Telegram
python-telegram-bot==20.7

# Procesamiento de texto
openai==1.6.1
anthropic==0.8.1

# RAG y embeddings
sentence-transformers==2.2.2
faiss-cpu==1.7.4
chromadb==0.4.22

# Procesamiento de archivos
PyPDF2==3.0.1
python-docx==1.1.0
openpyxl==3.1.2

# Visión
Pillow==10.1.0
opencv-python==4.8.1.78

# Audio
openai-whisper==20231117
soundfile==0.12.1

# Video
yt-dlp==2023.12.30
moviepy==1.0.3

# Automatización
requests==2.31.0
python-dotenv==1.0.0

# Utilidades
pydantic==2.5.3
numpy==1.24.3
pandas==2.1.4

# Desarrollo
pytest==7.4.3
black==23.12.1
flake8==7.0.0
''')

    # LICENSE
    create_file('LICENSE', '''MIT License

Copyright (c) 2026 Eduardo Bascuñán

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''')

    # __init__.py files
    init_files = [
        'backend_ai/__init__.py',
        'backend_ai/agents/__init__.py',
        'backend_ai/rag/__init__.py',
        'backend_ai/vision/__init__.py',
        'backend_ai/audio/__init__.py',
        'backend_ai/automation/__init__.py',
        'backend_ai/protocol/__init__.py',
        'tests/__init__.py'
    ]
    
    for init_file in init_files:
        create_file(init_file, '# -*- coding: utf-8 -*-\n"""Package initialization"""\n')

    # .gitkeep files
    create_file('backend_ai/shared/.gitkeep', '')
    create_file('logs/.gitkeep', '')

    print("\n✅ Todos los archivos principales creados!\n")


def display_final_instructions():
    """Mostrar instrucciones finales"""
    instructions = """
╔════════════════════════════════════════════════════════════════╗
║                  ✅ SETUP COMPLETADO                          ║
╚════════════════════════════════════════════════════════════════╝

📁 Estructura completa creada
📝 Todos los archivos principales generados
🚀 Proyecto listo para GitHub

═══════════════════════════════════════════════════════════════════
 PRÓXIMOS PASOS:
═══════════════════════════════════════════════════════════════════

1️⃣  CONFIGURAR TOKEN DE TELEGRAM:
   
   cp .env.example .env
   # Edita .env y añade tu TELEGRAM_TOKEN

2️⃣  INICIALIZAR GIT (si no lo has hecho):
   
   git init
   git add .
   git commit -m "🚀 Implementación completa IA_RVT 2026"

3️⃣  CONECTAR CON GITHUB:
   
   git remote add origin https://github.com/edbascunan/IA_RVT.git
   git branch -M main
   git push -u origin main

4️⃣  PROBAR LOCALMENTE:
   
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   pip install -r requirements.txt
   python backend_ai/bot_master.py

═══════════════════════════════════════════════════════════════════
 🎉 ¡PROYECTO LISTO!
═══════════════════════════════════════════════════════════════════

El sistema IA_RVT está completamente configurado y listo para usar.

Para comenzar:
1. Configura tu token de Telegram en .env
2. Ejecuta: python backend_ai/bot_master.py
3. Envía comandos desde Telegram

¡Gracias por usar IA_RVT! 🚀
    """
    
    print(instructions)


def main():
    """Función principal del script de setup"""
    print("\n" + "="*70)
    print("  🤖 IA_RVT SETUP SCRIPT - Configuración Completa del Proyecto")
    print("="*70 + "\n")
    
    try:
        # Crear estructura de directorios
        create_directory_structure()
        
        # Crear todos los archivos principales
        create_all_files()
        
        # Mostrar instrucciones finales
        display_final_instructions()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error durante el setup: {e}")
        print("\nPor favor, revisa el error y vuelve a ejecutar el script.")
        return 1


if __name__ == "__main__":
    sys.exit(main())