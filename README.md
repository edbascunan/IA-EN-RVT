# 🤖 IA_RVT 2026

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
