# IA-EN-RVT Bot NLP - Documentación

## Arquitectura Implementada
- **Bot NLP**: FastAPI + OpenAI SDK ≥ 1.0.0 (24/7 en Railway)
- **Extensión pyRevit**: Estructura correcta que consuma el bot como servicio
- **Integración**: pyRevit llama al bot externo, no ejecuta IA directamente

## Componentes Creados

### 1. Bot NLP Autónomo (`/bot_nlp_autonomo/`)
- ✅ `requirements.txt` - dependencias con OpenAI ≥ 1.0.0
- ✅ `config.py` - configuración OpenAI SDK
- ✅ `nlp_engine.py` - motor NLP con OpenAI
- ✅ `schemas.py` - modelos FastAPI
- ✅ `main.py` - API con endpoints `/ask` y `/revit-command`
- ✅ `Dockerfile` - contenedor para Railway
- ✅ `.env.example` - variables de entorno

### 2. Extensión pyRevit (`/pyrevit_extension_real/`)
- ✅ `IaEnRvt.extension` - configuración principal
- ✅ `IaEnRvt.tab/Bot.panel/Bot.panel` - panel del bot
- ✅ `Bot.pushbutton/Bot.pushbutton` - configuración botón
- ✅ `Bot.py` - script que consume bot NLP externo

## Estado Actual
- Bot NLP autónomo: ✅ IMPLEMENTADO
- Extensión pyRevit: ✅ IMPLEMENTADO
- Instalador automático: ✅ IMPLEMENTADO
- Deploy Railway: 🔄 PENDIENTE

## Próximos Pasos
1. Deploy del bot en Railway
2. Configurar OPENAI_API_KEY
3. Testing de integración completa