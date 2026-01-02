# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Sistema Principal de Bots
==========================================

Sistema principal que ejecuta ambos bots:
1. ZUKO (Bot Principal) - RAG + Memoria ilimitada
2. Bot de Datos - Multimodal empresarial

Incluye sistema de comunicación entre bots para compartir conocimiento.

Autor: Eduardo Bascuñán
"""

import os
import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any, List

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BotSystem:
    """Sistema principal de bots IA_RVT"""
    
    def __init__(self):
        """Inicializar sistema de bots"""
        self.bots = {}
        self.is_running = False
        self.shared_knowledge_db = 'backend_ai/data/shared_knowledge.db'
        
        logger.info("🏗️ Sistema de Bots IA_RVT inicializado")
    
    async def start_zuko_bot(self):
        """Iniciar Bot Principal ZUKO"""
        try:
            # Importar e iniciar ZUKO
            from bots.zuko_bot import ZukoBot
            
            logger.info("🐲 Iniciando Bot Principal ZUKO...")
            self.bots['zuko'] = ZukoBot()
            
            # Iniciar en modo asíncrono
            await self.bots['zuko'].app.initialize()
            await self.bots['zuko'].app.start()
            
            logger.info("✅ ZUKO Bot iniciado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error iniciando ZUKO: {e}")
            return False
    
    async def start_data_bot(self):
        """Iniciar Bot de Datos"""
        try:
            # Importar e iniciar Bot de Datos
            from bots.data_bot import DataBot
            
            logger.info("📊 Iniciando Bot de Datos...")
            self.bots['data'] = DataBot()
            
            # Iniciar en modo asíncrono
            await self.bots['data'].app.initialize()
            await self.bots['data'].app.start()
            
            logger.info("✅ Bot de Datos iniciado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error iniciando Bot de Datos: {e}")
            return False
    
    async def start_all_bots(self):
        """Iniciar todos los bots"""
        logger.info("🚀 Iniciando Sistema Completo de Bots...")
        
        # Iniciar ZUKO primero (bot principal)
        zuko_success = await self.start_zuko_bot()
        
        # Iniciar Bot de Datos
        data_success = await self.start_data_bot()
        
        if zuko_success and data_success:
            self.is_running = True
            logger.info("🎉 Sistema de Bots iniciado completamente")
            logger.info("🐲 ZUKO: Bot Principal activo")
            logger.info("📊 Bot de Datos: Multimodal activo")
            logger.info("🔗 Comunicación entre bots: Habilitada")
            return True
        else:
            logger.error("❌ Error iniciando sistema completo")
            return False
    
    async def share_knowledge_data_to_zuko(self, knowledge_items: List[Dict[str, Any]]):
        """Compartir conocimiento del bot de datos con ZUKO"""
        try:
            if 'zuko' not in self.bots:
                logger.warning("ZUKO no está disponible para compartir conocimiento")
                return False
            
            # Añadir a base de conocimiento compartido
            self._add_to_shared_knowledge("data_bot", knowledge_items)
            
            # Notificar a ZUKO que hay nuevo conocimiento
            if hasattr(self.bots['zuko'], 'knowledge_shared'):
                self.bots['zuko'].knowledge_shared += len(knowledge_items)
            
            logger.info(f"✅ {len(knowledge_items)} elementos compartidos con ZUKO")
            return True
            
        except Exception as e:
            logger.error(f"Error compartiendo conocimiento: {e}")
            return False
    
    def _add_to_shared_knowledge(self, source: str, knowledge_items: List[Dict[str, Any]]):
        """Añadir conocimiento a la base compartida"""
        try:
            import sqlite3
            
            conn = sqlite3.connect(self.shared_knowledge_db)
            cursor = conn.cursor()
            
            for item in knowledge_items:
                cursor.execute('''
                    INSERT INTO shared_knowledge 
                    (source_bot, category, topic, content, metadata)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    source,
                    item.get('category', 'general'),
                    item.get('topic', 'Sin título'),
                    item.get('content', ''),
                    json.dumps(item.get('metadata', {}))
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error añadiendo conocimiento compartido: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtener estado del sistema"""
        status = {
            "system_running": self.is_running,
            "bots_active": list(self.bots.keys()),
            "timestamp": datetime.now().isoformat(),
            "bots": {}
        }
        
        # Estado de cada bot
        if 'zuko' in self.bots:
            zuko = self.bots['zuko']
            status["bots"]["zuko"] = {
                "active": True,
                "query_count": getattr(zuko, 'query_count', 0),
                "knowledge_shared": getattr(zuko, 'knowledge_shared', 0),
                "data_integration": getattr(zuko, 'data_learning_active', False)
            }
        
        if 'data' in self.bots:
            data = self.bots['data']
            status["bots"]["data"] = {
                "active": True,
                "documents": getattr(data, 'document_count', 0),
                "videos": getattr(data, 'video_count', 0),
                "images": getattr(data, 'image_count', 0),
                "knowledge_learned": getattr(data, 'knowledge_learned', 0),
                "automation_level": data.enterprise_metrics.get('automation_level', 0)
            }
        
        return status
    
    async def stop_system(self):
        """Detener sistema"""
        logger.info("🛑 Deteniendo Sistema de Bots...")
        
        for bot_name, bot in self.bots.items():
            try:
                await bot.app.stop()
                logger.info(f"✅ {bot_name} detenido")
            except Exception as e:
                logger.error(f"❌ Error deteniendo {bot_name}: {e}")
        
        self.bots.clear()
        self.is_running = False
        logger.info("🔴 Sistema de Bots detenido")

async def main():
    """Función principal"""
    print("""
🏗️ IA-EN-RVT 2026 - Sistema de Bots
===================================

🐲 ZUKO: Bot Principal (RAG + Memoria ilimitada)
📊 Bot de Datos: Multimodal Empresarial
🔗 Comunicación: Compartición automática de conocimiento

Iniciando sistema...
    """)
    
    # Crear sistema
    bot_system = BotSystem()
    
    try:
        # Iniciar sistema completo
        success = await bot_system.start_all_bots()
        
        if success:
            print("✅ Sistema iniciado correctamente")
            print("🐲 ZUKO: Esperando comandos...")
            print("📊 Bot de Datos: Procesando datos...")
            print("🔗 Comunicación: Activa")
            
            # Mantener el sistema corriendo
            try:
                while bot_system.is_running:
                    # Verificar estado cada 30 segundos
                    await asyncio.sleep(30)
                    status = bot_system.get_system_status()
                    logger.info(f"Estado del sistema: {len(status['bots_active'])} bots activos")
                    
            except KeyboardInterrupt:
                print("\n🛑 Deteniendo sistema...")
                
        else:
            print("❌ Error iniciando el sistema")
            
    except Exception as e:
        logger.error(f"Error en sistema principal: {e}")
        print(f"❌ Error: {e}")
        
    finally:
        await bot_system.stop_system()
        print("🔴 Sistema detenido")

if __name__ == "__main__":
    # Configurar variables de entorno necesarias
    if not os.getenv('TELEGRAM_TOKEN'):
        print("⚠️ TELEGRAM_TOKEN no configurado")
        print("Configura las variables de entorno en .env")
    
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️ OPENAI_API_KEY no configurado")
        print("Configura las variables de entorno en .env")
    
    # Ejecutar sistema
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Sistema interrumpido por usuario")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        logger.error(f"Error fatal: {e}")

# Funciones de utilidad para el sistema
def create_env_file():
    """Crear archivo .env con configuración necesaria"""
    env_content = """# IA-EN-RVT 2026 - Configuración de Bots
# =====================================

# Bot Principal ZUKO
TELEGRAM_TOKEN_ZUKO=tu_token_zuko_aqui

# Bot de Datos
TELEGRAM_TOKEN_DATA=tu_token_data_aqui
# (Usar el mismo token si es un solo bot)

# OpenAI API (común para ambos bots)
OPENAI_API_KEY=tu_openai_key_aqui

# URLs de comunicación entre bots
ZUKO_URL=http://localhost:8000
DATA_BOT_URL=http://localhost:8001

# Configuración común
COMMAND_PATH=backend_ai/shared/command_out.json
DEBUG=False
ENVIRONMENT=production
    """
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado con configuración de ejemplo")

def check_dependencies():
    """Verificar dependencias del sistema"""
    required_modules = [
        'telegram',
        'openai', 
        'langchain',
        'sqlite3',
        'asyncio'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Dependencias faltantes: {missing}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    else:
        print("✅ Todas las dependencias están instaladas")
        return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "setup":
            create_env_file()
        elif sys.argv[1] == "check":
            check_dependencies()
        elif sys.argv[1] == "help":
            print("""
IA-EN-RVT 2026 - Comandos disponibles:

python main_bot_system.py         # Ejecutar sistema completo
python main_bot_system.py setup   # Crear archivo .env
python main_bot_system.py check   # Verificar dependencias
python main_bot_system.py help    # Mostrar esta ayuda
            """)
    else:
        # Ejecutar sistema por defecto
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n👋 Sistema interrumpido")
        except Exception as e:
            print(f"❌ Error: {e}")