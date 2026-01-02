# 🤖 IA-EN-RVT 2026

## Sistema BIM Autónomo con Inteligencia Artificial para Revit 2026

Control total de Revit mediante **lenguaje natural**, voz, imágenes y automatización.

---

## 🏗️ Arquitectura

```
USUARIO (Telegram/Voz/Texto)
         │
         ▼
    BOT MASTER (Python)
         │
         ▼
    ORCHESTRATOR ◄──► AI PROVIDERS (Claude, GPT, Grok, Minimax...)
         │
         ▼
  BIM COMMAND PROTOCOL (JSON)
         │
         ▼
   REVIT EXECUTOR (pyRevit/IronPython)
         │
         ▼
    MODELO REVIT REAL
```

---

## ✨ Características

- ✅ **Control por lenguaje natural**: "Crea un muro de 3 metros en nivel 1"
- ✅ **Múltiples proveedores IA**: Claude, ChatGPT, Grok, Minimax, DeepSeek, Ollama
- ✅ **Niveles de autonomía**: 1-5 configurables
- ✅ **Protocolo BIM seguro**: JSON firmado con rollback
- ✅ **Ejecución real en Revit**: pyRevit con transacciones seguras
- ✅ **Bot Telegram**: Control remoto completo

---

## 📁 Estructura del Proyecto

```
IA-EN-RVT/
├── backend_ai/
│   ├── bot_master.py          # Bot Telegram principal
│   ├── orchestrator.py        # Orquestador de comandos BIM
│   ├── ai_providers.py        # Gestión de múltiples IAs
│   ├── agents/
│   │   ├── __init__.py
│   │   └── bim_modeler.py     # Agentes BIM especializados
│   ├── shared/
│   │   └── command_out.json   # Comandos para Revit
│   ├── rag/                   # RAG multimodal (futuro)
│   ├── vision/                # Análisis de imágenes (futuro)
│   └── audio/                 # Voz a texto (futuro)
│
├── revit_executor/
│   └── IA_RVT.extension/      # Extensión pyRevit
│       └── IA_RVT.tab/
│           └── Executor.panel/
│               └── RunCommand.pushbutton/
│                   ├── script.py      # Ejecutor en Revit
│                   └── bundle.yaml
│
├── logs/
├── .env                       # Variables de entorno
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/edbascunan/IA-EN-RVT.git
cd IA-EN-RVT
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus API keys
```

### 4. Instalar extensión pyRevit
1. Copiar `revit_executor/IA_RVT.extension/` a tu carpeta de extensiones pyRevit
2. Reiniciar Revit
3. Verificar que aparece la pestaña "IA_RVT"

---

## ⚙️ Configuración (.env)

```env
# Telegram
TELEGRAM_TOKEN=tu_token_de_botfather

# Proveedores de IA (configura al menos uno)
CLAUDE_API_KEY=tu_claude_api_key
CHATGPT_API_KEY=tu_chatgpt_api_key
GROK_API_KEY=tu_grok_api_key
MINIMAX_API_KEY=tu_minimax_api_key
DEEPSEEK_API_KEY=tu_deepseek_api_key

# Proveedor por defecto
AI_PROVIDER_DEFAULT=claude
AI_FALLBACK_ENABLED=true

# Ollama (opcional, local)
OLLAMA_ENABLED=false
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

---

## 📱 Comandos del Bot

| Comando | Descripción |
|---------|-------------|
| `/start` | Iniciar sistema |
| `/help` | Ayuda completa |
| `/autonomia [1-5]` | Configurar nivel de autonomía |
| `/status` | Estado del sistema |
| `/ia` | Estado de proveedores IA |
| `/apis` | Listar proveedores disponibles |
| `/test [proveedor]` | Probar un proveedor |
| `/switch [proveedor]` | Cambiar proveedor principal |
| `/confirmar` | Confirmar comando pendiente |
| `/cancelar` | Cancelar comando pendiente |

---

## 🎚️ Niveles de Autonomía

| Nivel | Descripción | Acciones |
|-------|-------------|----------|
| 1 | Solo confirmar | Requiere `/confirmar` para todo |
| 2 | Ejecutar simple | Solo consultas y análisis |
| 3 | Ejecutar normal | CREATE, MODIFY, QUERY (recomendado) |
| 4 | Ejecutar complejo | Todas las operaciones |
| 5 | Totalmente autónomo | Sin confirmaciones |

---

## 💬 Ejemplos de Comandos en Lenguaje Natural

```
✅ "Crea un muro de 3 metros de altura en nivel 1"
✅ "Añade una puerta en el muro principal"
✅ "Crea una columna de 30x30 en la esquina"
✅ "Analiza el modelo estructural"
✅ "Genera un nivel a 6 metros de altura"
✅ "Elimina las columnas del eje A"
```

---

## 🔄 Flujo de Ejecución

1. **Usuario** envía mensaje por Telegram
2. **Bot Master** recibe y procesa
3. **Orchestrator** interpreta intención BIM
4. **AI Provider** mejora interpretación (si es necesario)
5. **BIM Command** se genera en JSON con firma
6. Se guarda en `shared/command_out.json`
7. Usuario ejecuta **RunCommand** en pyRevit
8. **Revit Executor** lee JSON y ejecuta con transacción
9. Resultado se registra en logs

---

## 🏗️ Protocolo BIM Command

```json
{
  "schema": "IA_RVT_BIM_COMMAND_v1",
  "timestamp": "2026-01-01T23:00:00",
  "accion": "CREATE",
  "elemento": "Wall",
  "payload": {
    "nivel": "Nivel 1",
    "tipo": "Muro Interior - 100mm",
    "altura_m": 3.0,
    "inicio": {"x": 0, "y": 0},
    "fin": {"x": 5, "y": 0}
  },
  "autonomia": 3,
  "rollback": true,
  "estado": "PENDIENTE",
  "firma": "a1b2c3d4e5f6"
}
```

---

## 🔧 Requisitos

- Python 3.11+
- Revit 2026
- pyRevit 4.8+
- Cuenta de Telegram (para el bot)
- Al menos una API key de IA

---

## 📊 Hardware Recomendado

- CPU: Intel Xeon o equivalente
- RAM: 32 GB mínimo
- GPU: NVIDIA Quadro P2000 o superior
- El procesamiento de IA pesado ocurre **fuera de Revit**

---

## 🔒 Seguridad

- ✅ Comandos firmados con hash SHA256
- ✅ Transacciones con rollback automático
- ✅ Logs de auditoría
- ✅ Confirmación humana configurable
- ✅ Revit aislado (sin internet, sin dependencias externas)

---

## 📝 Licencia

MIT License - Eduardo Bascuñán 2026

---

## 🚀 Estado del Proyecto

| Componente | Estado |
|------------|--------|
| Bot Master | ✅ Funcional |
| Orchestrator | ✅ Funcional |
| AI Providers | ✅ 8 proveedores |
| BIM Agents | ✅ Funcional |
| pyRevit Executor | ✅ Funcional |
| Protocolo BIM | ✅ Definido |
| RAG Multimodal | 🔄 En desarrollo |
| Vision Engine | 🔄 En desarrollo |
| Audio Engine | 🔄 En desarrollo |

---

**El humano diseña la intención. La IA decide la acción. Revit ejecuta la realidad.**