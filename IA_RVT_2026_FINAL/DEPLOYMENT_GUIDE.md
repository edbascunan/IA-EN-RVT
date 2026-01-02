# 🚀 Guía de Deployment - IA-EN-RVT 2026

## 📋 PASOS PARA DESPLEGAR EN RAILWAY

### 1. Preparar el Repositorio
```bash
# Subir código a GitHub
git init
git add .
git commit -m "Initial commit: IA-EN-RVT 2026 System"
git remote add origin https://github.com/edbascunan/IA-EN-RVT.git
git push -u origin main
```

### 2. Configurar Railway
1. Ir a [railway.app](https://railway.app)
2. Crear cuenta/login
3. Click "New Project"
4. Seleccionar "Deploy from GitHub repo"
5. Seleccionar tu repositorio `IA-EN-RVT`
6. Railway detectará automáticamente el proyecto

### 3. Configurar Variables de Entorno en Railway
En Railway dashboard, ir a Variables y añadir:

```
TELEGRAM_TOKEN_ZUKO=tu_token_telegram_zuko
TELEGRAM_TOKEN_DATA=tu_token_telegram_data  
OPENAI_API_KEY=tu_openai_key
ZUKO_URL=http://localhost:8000
DATA_BOT_URL=http://localhost:8001
COMMAND_PATH=backend_ai/shared/command_out.json
DEBUG=False
ENVIRONMENT=production
```

### 4. Deployment Automático
Railway automáticamente:
- Detectará `requirements.txt`
- Instalará dependencias
- Ejecutará `main_bot_system.py` (definido en Procfile)
- Asignará URL pública

### 5. Verificar Deployment
```bash
# El sistema estará disponible en la URL de Railway
# URL ejemplo: https://ia-rvt-2026-production.up.railway.app
```

## 🔧 PROBLEMAS POTENCIALES Y SOLUCIONES

### Problema 1: "Module not found"
**Si ves error de importación de módulos:**

**Instrucción para Claude:**
```
El proyecto IA-EN-RVT tiene errores de importación en Railway. 

Problema: Los imports fallan al ejecutar en Railway:
- from bots.zuko_bot import ZukoBot
- from bots.data_bot import DataBot

Por favor corrige el archivo main_bot_system.py para que maneje correctamente los imports en Railway. 

Asegúrate de que:
1. Los imports usen rutas relativas correctas
2. Se manejen excepciones de importación
3. El sistema funcione tanto local como en Railway

El archivo actual está en: IA_RVT_2026_FINAL/main_bot_system.py
```

### Problema 2: "AsyncIO runtime error"
**Si Railway da error de AsyncIO:**

**Instrucción para Claude:**
```
Railway da error: "RuntimeError: asyncio.run() cannot be called from a running event loop"

El archivo main_bot_system.py usa asyncio.run() que no funciona en Railway.

Por favor corrige el main_bot_system.py para:
1. Usar el método correcto para ejecutar asyncio en Railway
2. Manejar la ejecución asíncrona apropiadamente
3. Asegurar que ambos bots se ejecuten correctamente

Archivo: IA_RVT_2026_FINAL/main_bot_system.py
```

### Problema 3: "Database file not found"
**Si hay errores de base de datos:**

**Instrucción para Claude:**
```
Los bots no pueden acceder a las bases de datos SQLite en Railway.

Error: "database file not found" o "Permission denied"

Por favor modifica los archivos para:
1. Crear directorios de datos si no existen
2. Usar rutas de base de datos apropiadas para Railway
3. Manejar errores de permisos de archivos

Archivos a corregir:
- bots/zuko_bot.py (shared_knowledge_db)
- bots/data_bot.py (learning_db)
- backend_ai/memory_manager.py (memory_db_path)
```

### Problema 4: "Environment variables not set"
**Si faltan variables de entorno:**

**Instrucción para Claude:**
```
Railway no puede leer las variables de entorno correctamente.

Error: "Token not configured" o variables undefined

Por favor crea un script mejorado que:
1. Valide todas las variables de entorno requeridas
2. Proporcione mensajes de error claros
3. Permita ejecución con variables mínimas
4. Maneje fallbacks para variables opcionales

Mejorar: main_bot_system.py y todos los archivos de bots
```

## 📊 MONITOREO DEL DEPLOYMENT

### Logs en Railway
1. En Railway dashboard, ir a "Deployments"
2. Click en el deployment activo
3. Ver logs en tiempo real

### URLs de Bots
Una vez desplegado, tendrás:
- URL principal del sistema
- Bot ZUKO: Configurar webhook a la URL de Railway
- Bot de Datos: Configurar webhook a la URL de Railway

### Verificación de Funcionamiento
```bash
# En Railway logs, deberías ver:
✅ ZUKO Bot iniciado exitosamente
✅ Bot de Datos iniciado exitosamente  
🎉 Sistema de Bots iniciado completamente
```

## 🔄 ACTUALIZACIONES

### Para actualizar el código:
```bash
git add .
git commit -m "Update: descripción del cambio"
git push
# Railway detectará automáticamente y redeployará
```

## 🆘 SOPORTE

Si hay problemas adicionales:

1. **Revisar logs** en Railway dashboard
2. **Verificar variables** de entorno están configuradas
3. **Comprobar imports** y dependencias
4. **Contactar Claude** con el error específico

## ✅ CHECKLIST FINAL

- [ ] Repositorio subido a GitHub
- [ ] Proyecto conectado a Railway
- [ ] Variables de entorno configuradas
- [ ] Deployment exitoso
- [ ] Ambos bots funcionando
- [ ] Logs sin errores críticos
- [ ] URLs de bots configuradas
- [ ] Sistema respondiendo a comandos

**Una vez completado este checklist, el sistema IA-EN-RVT estará completamente desplegado y funcionando en Railway.**