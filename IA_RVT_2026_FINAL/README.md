# IA-EN-RVT 2026 - Sistema BIM Autónomo con IA

## 🏗️ Descripción
Sistema completo de automatización BIM que permite controlar Revit 2026 mediante:
- **Procesamiento de Lenguaje Natural (NLP)**
- **Memoria Ilimitada con RAG**
- **Procesamiento Multimodal** (texto, imagen, video, audio)
- **Aprendizaje Continuo**
- **Integración Telegram + PYREVIT**

## 📁 Estructura del Proyecto

```
IA-EN-RVT-2026/
├── README.md
├── requirements.txt
├── .env
├── backend_ai/                    # Motor de IA
│   ├── bot_master.py             # Bot Master Principal
│   ├── orchestrator.py           # Orquestador
│   ├── memory_manager.py         # Gestión de memoria
│   ├── rag_system.py            # Sistema RAG
│   ├── youtube_processor.py      # Procesador YouTube
│   ├── document_processor.py     # Procesador documentos
│   ├── vision_engine.py          # Motor de visión
│   ├── audio_engine.py           # Motor de audio
│   ├── config.py                 # Configuración
│   └── shared/                   # Archivos compartidos
│       └── command_out.json      # Comandos para Revit
├── chatbots/                      # 3 Propuestas de Chatbot
│   ├── propuesta_1_basico/       # Chatbot Básico NLP
│   ├── propuesta_2_avanzado/     # Chatbot Avanzado RAG+Memoria
│   └── propuesta_3_empresarial/  # Chatbot Empresarial Multimodal
├── pyrevit_extension/             # Extensión PYREVIT
│   └── IA_RVT.extension/
├── instaladores/                  # Scripts de instalación
├── docs/                         # Documentación
└── tests/                        # Tests
```

## 🚀 Inicio Rápido

1. **Instalar dependencias**: `pip install -r requirements.txt`
2. **Configurar variables**: Copiar `.env.example` a `.env`
3. **Ejecutar bot**: `python backend_ai/bot_master.py`
4. **Usar en Telegram**: Escribir comandos en lenguaje natural

## 📋 3 Propuestas de Chatbot

### 🤖 Propuesta 1: Chatbot Básico NLP
- **Características**: NLP básico con OpenAI
- **Memoria**: Contexto de conversación
- **Uso**: Comandos simples de Revit

### 🧠 Propuesta 2: Chatbot Avanzado RAG+Memoria  
- **Características**: RAG + Memoria vectorial
- **Memoria**: Historial completo con embeddings
- **Uso**: Análisis complejos y aprendizaje

### 🏢 Propuesta 3: Chatbot Empresarial Multimodal
- **Características**: Procesamiento multimodal completo
- **Memoria**: Memoria gráfica de proyectos BIM
- **Uso**: Automatización empresarial completa

## 🛠️ Tecnologías
- **Python 3.11+**
- **OpenAI API** (GPT-4)
- **LangChain** (RAG y memoria)
- **FAISS** (Búsqueda vectorial)
- **Telegram Bot API**
- **PYREVIT** (Integración Revit)
- **Railway** (Despliegue)

## 📖 Documentación
Ver carpeta `docs/` para documentación completa.

---
**Autor**: Eduardo Bascuñán  
**Versión**: 2026.01.01  
**Estado**: ✅ Completo y Funcional