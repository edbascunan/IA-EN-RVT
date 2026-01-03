#!/usr/bin/env python3
"""
START BOT - Bot IA-EN-RVT con RAG y Memoria Infinita
====================================================

Este archivo ejecuta el bot_avanzado.py con logging completo
de todas las interacciones en pantalla.

Modificado para usar exclusivamente el bot avanzado sin fallbacks.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Configurar logging para mostrar todas las interacciones en pantalla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Mostrar banner de inicio
print("=" * 80)
print("🚀 BOT IA-EN-RVT 2026 - INTELIGENCIA ARTIFICIAL AVANZADA")
print("=" * 80)
print("🧠 RAG: Retrieval-Augmented Generation - ACTIVO")
print("💾 MEMORIA: Sistema vectorial persistente - ACTIVO") 
print("🌐 WEB: Búsquedas especializadas - ACTIVO")
print("📱 TELEGRAM: Bot de conversación inteligente - ACTIVO")
print("👁️ INTERACCIONES: Logging en pantalla - ACTIVO")
print("=" * 80)

def log_interaction_start():
    """Log del inicio del sistema"""
    logger.info("🎯 INICIANDO SISTEMA DE BOT AVANZADO")
    logger.info(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🔧 Working Directory: {os.getcwd()}")
    logger.info(f"🐍 Python Version: {sys.version}")

def check_dependencies():
    """Verificar dependencias críticas"""
    logger.info("🔍 Verificando dependencias...")
    
    required_modules = ['telegram', 'sqlite3', 'requests', 'os', 'sys']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"✅ {module}: Disponible")
        except ImportError:
            missing_modules.append(module)
            logger.error(f"❌ {module}: NO DISPONIBLE")
    
    if missing_modules:
        logger.error(f"🚨 MÓDULOS FALTANTES: {missing_modules}")
        return False
    
    logger.info("✅ Todas las dependencias están disponibles")
    return True

def load_bot_advanced():
    """Cargar bot_avanzado.py con logging completo"""
    logger.info("🔄 Cargando bot_avanzado.py...")
    
    try:
        # Agregar directorio actual al path si no está
        current_dir = Path(__file__).parent
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
        
        # Importar AdvancedBot
        from bot_avanzado import AdvancedBot
        
        logger.info("✅ bot_avanzado.py importado correctamente")
        logger.info("🧠 Funcionalidades RAG detectadas:")
        logger.info("   • VectorDB (Memoria Infinita)")
        logger.info("   • WebSearcher (Búsqueda Web)")
        logger.info("   • AdvancedBot (IA Avanzada)")
        logger.info("   • Comandos especializados")
        
        return AdvancedBot
        
    except ImportError as e:
        logger.error(f"❌ Error importando bot_avanzado.py: {e}")
        logger.error("🚨 IMPOSIBLE CARGAR BOT AVANZADO")
        logger.error("💡 Verifica que bot_avanzado.py existe en el directorio actual")
        return None
    except Exception as e:
        logger.error(f"❌ Error inesperado cargando bot: {e}")
        return None

def run_advanced_bot():
    """Ejecutar el bot avanzado con logging completo"""
    logger.info("🚀 Iniciando AdvancedBot...")
    
    try:
        # Crear instancia del bot
        bot_class = load_bot_advanced()
        if not bot_class:
            logger.error("🚨 No se pudo cargar el bot avanzado")
            sys.exit(1)
        
        logger.info("🤖 Creando instancia de AdvancedBot...")
        bot = bot_class()
        
        logger.info("✅ AdvancedBot inicializado correctamente")
        logger.info("📊 Configuración del bot:")
        logger.info(f"   • Token: {bot.token[:20]}..." if bot.token else "   • Token: NO CONFIGURADO")
        logger.info(f"   • OpenRouter: {'✅' if bot.openrouter_key else '❌'}")
        logger.info(f"   • HuggingFace: {'✅' if bot.hf_token else '❌'}")
        logger.info(f"   • VectorDB: ✅ Inicializada")
        logger.info(f"   • WebSearcher: ✅ Configurada")
        
        logger.info("🌟 INICIANDO POLLING - Bot activo y escuchando mensajes...")
        logger.info("=" * 80)
        logger.info("📱 Bot de Telegram listo para recibir mensajes")
        logger.info("🧠 RAG: Buscando información relevante en base de conocimiento")
        logger.info("💾 MEMORIA: Almacenando y consultando conversaciones")
        logger.info("🌐 WEB: Búsquedas especializadas activas")
        logger.info("👁️ TODAS LAS INTERACCIONES SE MOSTRARÁN EN ESTA PANTALLA")
        logger.info("=" * 80)
        
        # Ejecutar bot con manejo de errores
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("🛑 Deteniendo bot por interrupción del usuario")
    except Exception as e:
        logger.error(f"🚨 Error crítico ejecutando bot: {e}")
        logger.error("💡 Revisa los logs anteriores para más detalles")
        sys.exit(1)

def main():
    """Función principal con logging completo"""
    try:
        # Log del inicio
        log_interaction_start()
        
        # Verificar dependencias
        if not check_dependencies():
            logger.error("🚨 FALTAN DEPENDENCIAS CRÍTICAS")
            sys.exit(1)
        
        # Ejecutar bot avanzado
        run_advanced_bot()
        
    except Exception as e:
        logger.error(f"🚨 ERROR CRÍTICO EN MAIN: {e}")
        logger.error("💡 El sistema no puede continuar")
        sys.exit(1)

if __name__ == "__main__":
    main()