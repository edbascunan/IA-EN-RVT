# IA-EN-RVT Bot NLP - README

## 🤖 Bot NLP Autónomo + Extensión pyRevit

Solución real y funcional con bot NLP autónomo usando OpenAI + extensión pyRevit que aparezca correctamente en Revit.

## 🏗️ Arquitectura Implementada

```
Usuario (pyRevit) → Extensión pyRevit → Bot NLP → OpenAI → Respuesta
```

### Componentes Principales

1. **Bot NLP Autónomo** (Backend 24/7)
   - FastAPI + OpenAI SDK ≥ 1.0.0
   - Deploy en Railway
   - Procesamiento de lenguaje natural

2. **Extensión pyRevit** (Frontend)
   - Estructura correcta de pyRevit
   - Botón que aparece en Revit
   - Consume bot NLP externo

## 🚀 Instalación y Deploy

### PASO 1: Deploy Bot NLP en Railway

1. **Ir a Railway**: https://railway.app
2. **Conectar GitHub** y subir carpeta `bot_nlp_autonomo`
3. **Configurar Variables de Entorno**:
   ```
   OPENAI_API_KEY=tu_api_key_aqui
   ```
4. **Deploy automático** - Railway detecta Dockerfile
5. **Obtener URL**: `https://tu-proyecto.up.railway.app`

### PASO 2: Instalar Extensión pyRevit

```bash
# Ejecutar instalador automático
python instalar_extension_final.py
```

### PASO 3: Configurar URL del Bot

Editar `Bot.py` en la extensión:
```python
BOT_NLP_URL = "https://tu-proyecto.up.railway.app/revit-command"
```

### PASO 4: Usar en Revit

1. Abrir Revit 2026
2. PYREVIT > Extensions > Reload
3. Buscar pestaña 'IaEnRvt'
4. Hacer clic en '🤖 IA RVT'

## 📝 Comandos de Ejemplo

- "Crear un muro desde 0,0 hasta 5,0 altura 3.0"
- "Analizar elementos del proyecto"
- "¿Cómo cuantifico elementos en Revit?"
- "Ayuda con modelado BIM"

## 🔧 Estructura de Archivos

### Bot NLP Autónomo (`/bot_nlp_autonomo/`)
- `requirements.txt` - dependencias OpenAI ≥ 1.0.0
- `config.py` - configuración OpenAI SDK
- `nlp_engine.py` - motor NLP con OpenAI
- `schemas.py` - modelos FastAPI
- `main.py` - API endpoints
- `Dockerfile` - contenedor Railway
- `.env.example` - variables entorno

### Extensión pyRevit (`/pyrevit_extension_real/`)
- `IaEnRvt.extension` - configuración principal
- `IaEnRvt.tab/Bot.panel/Bot.panel` - panel
- `Bot.pushbutton/Bot.pushbutton` - configuración botón
- `Bot.py` - script que consume bot externo

## ✅ Verificación

- ✅ Botón '🤖 IA RVT' visible en Revit
- ✅ pyRevit consume servicio externo
- ✅ OpenAI procesa lenguaje natural
- ✅ Respuestas inteligentes en Revit

## 🛠️ Troubleshooting

### Botón no aparece en Revit
1. Verificar PYREVIT instalado
2. PYREVIT > Extensions > Reload
3. Ejecutar instalador nuevamente

### Error de conexión al bot
1. Verificar URL del bot en `Bot.py`
2. Verificar que Railway esté funcionando
3. Verificar OPENAI_API_KEY configurada

### Bot no responde
1. Verificar logs en Railway
2. Verificar OPENAI_API_KEY válida
3. Verificar conectividad a internet

## 🎯 Resultado Final

**Sistema completamente funcional**:
- 🤖 Bot NLP 24/7 con OpenAI
- 🏗️ Extensión pyRevit que aparece correctamente
- 💬 Procesamiento de lenguaje natural real
- ⚡ Respuestas inteligentes en Revit