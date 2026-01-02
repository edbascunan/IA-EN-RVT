# 🏗️ IA-EN-RVT 2026 - INSTRUCCIONES COMPLETAS PYREVIT

## 🚀 SISTEMA COMPLETO CON PYREVIT

El sistema **IA-EN-RVT 2026** ahora utiliza **PYREVIT** para una integración nativa y poderosa con Revit.

### 📋 Ventajas de PYREVIT vs RevitPythonShell

| Característica | RevitPythonShell | **PYREVIT** |
|---|---|---|
| Integración | Básica | **Nativa** |
| UI | Consola | **Cinta de herramientas** |
| Distribución | Manual | **Instalador automático** |
| Mantenimiento | Manual | **Extensiones** |
| Estabilidad | Básica | **Profesional** |

## 🛠️ INSTALACIÓN PASO A PASO

### Paso 1: Instalar PYREVIT

1. **Descargar PYREVIT:**
   - Ir a: https://github.com/eirannejad/pyRevit/releases
   - Descargar la última versión estable
   - Ejecutar el instalador

2. **Verificar instalación:**
   - PYREVIT debe aparecer en el menú de Windows
   - Icono de PYREVIT en la barra de tareas

### Paso 2: Instalar Extensión IA-EN-RVT

#### Opción A: Instalador Automático
```bash
cd /edbascunan/IA-EN-RVT
python instalar_pyrevit.py
```

#### Opción B: Instalación Manual
1. Copiar carpeta: `pyrevit_extension` a:
   - `%APPDATA%\pyRevit\Extensions\` (usuario)
   - `C:\ProgramData\pyRevit\Extensions` (sistema)

### Paso 3: Configurar Revit

1. **Abrir Revit 2026**
2. **Recargar extensiones PYREVIT:**
   - PYREVIT > Extensions > Reload
3. **Buscar nueva pestaña:**
   - Debe aparecer "IaEnRvt" en la cinta
   - Botón "🏗️ Zuko" visible

## 🤖 BOT ZUKO PARA PYREVIT

### Ejecutar Bot
```bash
cd /edbascunan/IA-EN-RVT/backend_ai
python bot_zuko_pyrevit.py
```

### Comandos Disponibles

#### 🔧 Comandos PYREVIT
- `/pyrevit` - Verificar conexión PYREVIT
- `/crear_muro x1 y1 x2 y2 [altura]` - Crear muro personalizado
- `/muro_rapido` - Muro de prueba (4m x 3.2m)
- `/analizar` - Analizar elementos del modelo

#### 📱 Comandos del Bot
- `/start` - Iniciar bot
- `/help` - Mostrar ayuda completa
- `/status` - Estado del sistema y PYREVIT
- `/instalar` - Instrucciones de instalación

### Ejemplos de Uso

#### Crear Muro Personalizado
```
/crear_muro 0 0 5 0 3.5
```
Resultado: Muro de 5m x 3.5m desde origen

#### Muro de Prueba Rápida
```
/muro_rapido
```
Resultado: Muro de 4m x 3.2m desde origen

#### Analizar Modelo
```
/analizar
```
Resultado: Estadísticas del modelo actual

## 🔄 FLUJO DE TRABAJO COMPLETO

### 1. Enviar Comando desde Telegram
```
Usuario envía: /crear_muro 0 0 5 0 3.5
```

### 2. Bot Procesa y Guarda
```
Bot crea: command_out.json
{
  "accion": "CREATE",
  "elemento": "Wall",
  "payload": {
    "inicio": {"x": 0, "y": 0},
    "fin": {"x": 5, "y": 0},
    "altura_m": 3.5
  }
}
```

### 3. Ejecutar en Revit
```
Usuario hace clic en "Zuko" en Revit
PYREVIT lee command_out.json
Crea muro automáticamente
Marca comando como "EJECUTADO"
```

### 4. Confirmación
```
Revit muestra: "✅ MURO CREADO EXITOSAMENTE"
Bot confirma en Telegram
```

## 📁 ESTRUCTURA DE ARCHIVOS

```
/edbascunan/IA-EN-RVT/
├── .env                          # Configuración de tokens
├── bot_zuko_pyrevit.py           # Bot optimizado para PYREVIT
├── instalar_pyrevit.py           # Instalador automático
├── requirements.txt              # Dependencias
├── INSTRUCCIONES_PYREVIT_COMPLETAS.md
├── pyrevit_extension/            # Extensión PYREVIT
│   └── IaEnRvt.extension/
│       ├── IaEnRvt.extension     # Manifest de extensión
│       └── IaEnRvt.tab/
│           └── Panel 1.stack/
│               └── Muro Zuko.pushbutton/
│                   ├── Muro Zuko.py      # Script principal
│                   └── config.yaml       # Configuración UI
└── backend_ai/
    └── shared/
        └── command_out.json      # Comandos para Revit
```

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "PYREVIT no encontrado"
1. Verificar PYREVIT instalado
2. Reiniciar el sistema
3. Ejecutar instalador nuevamente

### Error: "Extensión no aparece"
1. PYREVIT > Extensions > Reload
2. Verificar permisos de carpeta
3. Revisar logs de PYREVIT

### Error: "Bot no conecta"
1. Verificar token en .env
2. Comprobar conexión a internet
3. Revisar `/status` del bot

### Error: "Comando no ejecuta"
1. Verificar archivo command_out.json existe
2. Comprobar permisos de lectura
3. Revisar formato JSON

## 🎯 COMANDOS DE PRUEBA

### Prueba Básica
1. `/start` - Verificar bot activo
2. `/pyrevit` - Verificar PYREVIT conectado
3. `/muro_rapido` - Crear muro de prueba
4. Hacer clic en "Zuko" en Revit
5. Verificar muro creado

### Prueba Avanzada
1. `/crear_muro 2 1 8 4 4.5` - Muro personalizado
2. `/analizar` - Analizar modelo
3. Verificar resultados en ambos lados

## 🚀 BENEFICIOS DEL SISTEMA PYREVIT

### Para el Usuario
- ✅ Interfaz visual intuitiva
- ✅ Botón directo en la cinta
- ✅ Integración nativa con Revit
- ✅ Distribución fácil

### Para el Desarrollador
- ✅ Estructura modular
- ✅ Instalación automatizada
- ✅ Configuración declarativa
- ✅ Mantenimiento simplificado

### Para el Sistema
- ✅ Rendimiento optimizado
- ✅ Estabilidad mejorada
- ✅ Compatibilidad total
- ✅ Escalabilidad

## 🎉 RESULTADO FINAL

Al completar la instalación:

1. **Bot Zuko** responde en Telegram
2. **Comandos** se envían automáticamente
3. **PYREVIT** ejecuta en Revit
4. **Elementos** se crean en el modelo
5. **Sistema** funciona integrado end-to-end

---

**🚀 ¡SISTEMA IA-EN-RVT 2026 CON PYREVIT COMPLETAMENTE OPERATIVO!**

*Autor: Eduardo Bascuñán*  
*Fecha: 2026-01-02*  
*Versión: IA-EN-RVT 2026 PYREVIT*