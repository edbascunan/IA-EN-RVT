# 🏗️ IA-EN-RVT 2026 - Instrucciones para Prueba en Revit

## 📋 Resumen del Sistema

El **Bot Zuko** es un asistente de IA avanzado para Revit que permite:
- Crear elementos mediante comandos de Telegram
- Analizar modelos de Revit
- Procesamiento con múltiples LLMs
- Integración completa con el ecosistema IA-EN-RVT

## 🚀 Pasos para la Prueba

### 1. Configuración Inicial

#### A. Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### B. Verificar Configuración
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Token configurado:', os.getenv('TELEGRAM_TOKEN', 'NO CONFIGURADO')[:20] + '...')"
```

### 2. Ejecutar Bot Zuko

#### Iniciar el Bot
```bash
cd /edbascunan/IA-EN-RVT/backend_ai
python bot_zuko.py
```

#### Verificar Conexión
- El bot debe mostrar: "🤖 Iniciando Bot Zuko..."
- Token configurado: `7537372382:AAF58awLA...`
- Comando path: `C:\edbascunan\IA-EN-RVT\backend_ai\shared\command_out.json`

### 3. Configurar Revit

#### A. Instalar RevitPythonShell
1. Descargar desde: https://github.com/architecture-building-systems/revitpythonshell
2. Instalar en Revit 2026

#### B. Copiar Script en RevitPythonShell
1. Abrir RevitPythonShell
2. Copiar el contenido completo de `revit_executor/script_rps.py`
3. Pegar en la consola de RevitPythonShell

#### C. Ejecutar Script
- El script se ejecutará automáticamente
- Buscará comandos en: `command_out.json`
- Ejecutará las acciones en Revit

### 4. Realizar Prueba Completa

#### A. Enviar Comando desde Telegram

**Comando 1: Estado del Sistema**
```
/status
```

**Comando 2: Crear Muro Simple**
```
/crear_muro 0 0 4 0 3.2
```

**Comando 3: Analizar Modelo**
```
/analizar
```

#### B. Verificar en Revit
1. **RevitPythonShell debe mostrar:**
   ```
   IA-EN-RVT 2026 - RevitPythonShell
   Accion: CREATE
   Elemento: Wall
   EXITO: Muro creado con ID: [numero]
   ```

2. **Revit debe mostrar:**
   - Nuevo muro creado desde (0,0) hasta (4,0)
   - Altura: 3.2 metros

### 5. Comandos Adicionales de Prueba

#### Crear Muro con Parámetros Personalizados
```
/crear_muro 2 1 6 3 4.5
```

#### Comando Personalizado
```
/revit
```

#### Mensaje de IA
```
Hola Zuko, ¿puedes ayudarme con este proyecto?
```

### 6. Verificación de Funcionalidades

#### ✅ Bot Activo
- Bot responde a `/start`, `/help`, `/status`
- Respuestas en español con emojis

#### ✅ Comando a Revit
- Comando se guarda en `command_out.json`
- RevitPythonShell lee y ejecuta el comando
- Elemento se crea correctamente en Revit

#### ✅ Análisis de Modelo
- Comando `/analizar` funciona
- Muestra cantidad de muros y niveles

#### ✅ Persistencia
- Comando se marca como "EJECUTADO" después de procesar
- Timestamp se actualiza correctamente

## 🔧 Solución de Problemas

### Error: "Token inválido"
- Verificar que `.env` existe y tiene el token correcto
- Reiniciar el bot después de cambios en `.env`

### Error: "No hay comando pendiente"
- Verificar que el path en `COMMAND_PATH` sea correcto
- Asegurar que el directorio `shared/` existe

### Error en RevitPythonShell
- Verificar que Revit 2026 está instalado
- Asegurar que RevitPythonShell está instalado
- Revisar que el script no tenga errores de sintaxis

### Bot no responde
- Verificar conexión a internet
- Comprobar que el token está activo en @BotFather
- Revisar logs del bot para errores

## 📁 Archivos Importantes

- **`.env`** - Configuración de tokens y APIs
- **`bot_zuko.py`** - Bot principal de Telegram
- **`revit_executor/script_rps.py`** - Script para RevitPythonShell
- **`backend_ai/shared/command_out.json`** - Archivo de comandos
- **`requirements.txt`** - Dependencias del sistema

## 🎯 Resultado Esperado

Al completar la prueba exitosamente:
1. ✅ Bot Zuko responde en Telegram
2. ✅ Comando se envía desde Telegram
3. ✅ RevitPythonShell ejecuta el comando
4. ✅ Muro se crea en el modelo de Revit
5. ✅ Sistema completo funciona integrado

---

**¡Sistema IA-EN-RVT 2026 listo para prueba en Revit!** 🚀