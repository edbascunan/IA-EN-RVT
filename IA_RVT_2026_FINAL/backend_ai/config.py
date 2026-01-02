# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Configuración del Sistema
==========================================

Configuración centralizada del sistema BIM autónomo
Autor: Eduardo Bascuñán
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración principal del sistema"""
    
    # Bot Telegram
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = "gpt-4"
    OPENAI_TEMPERATURE = 0.7
    OPENAI_MAX_TOKENS = 500
    
    # Memoria y RAG
    VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH', 'backend_ai/data/vector_store')
    MEMORY_DB_PATH = os.getenv('MEMORY_DB_PATH', 'backend_ai/data/memory.db')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    
    # Documentos
    DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH', 'backend_ai/data/documents')
    YOUTUBE_CACHE_PATH = os.getenv('YOUTUBE_CACHE_PATH', 'backend_ai/data/youtube_cache')
    
    # PYREVIT
    PYREVIT_COMMAND_PATH = os.getenv('PYREVIT_COMMAND_PATH', 'backend_ai/shared/command_out.json')
    
    # Redis (opcional)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Seguridad
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    
    # Despliegue
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    @classmethod
    def validate(cls):
        """Validar configuración requerida"""
        required_vars = [
            'TELEGRAM_TOKEN',
            'OPENAI_API_KEY'
        ]
        
        missing = []
        for var in required_vars:
            if not getattr(cls, var):
                missing.append(var)
        
        if missing:
            raise ValueError(f"Variables de entorno requeridas faltantes: {missing}")
        
        return True
    
    @classmethod
    def get_embedding_config(cls):
        """Obtener configuración de embeddings"""
        return {
            "model_name": cls.EMBEDDING_MODEL,
            "vector_store_path": cls.VECTOR_STORE_PATH,
            "memory_db_path": cls.MEMORY_DB_PATH
        }
    
    @classmethod
    def get_openai_config(cls):
        """Obtener configuración de OpenAI"""
        return {
            "api_key": cls.OPENAI_API_KEY,
            "model": cls.OPENAI_MODEL,
            "temperature": cls.OPENAI_TEMPERATURE,
            "max_tokens": cls.OPENAI_MAX_TOKENS
        }
    
    @classmethod
    def get_bot_config(cls):
        """Obtener configuración del bot"""
        return {
            "token": cls.TELEGRAM_TOKEN,
            "command_path": cls.PYREVIT_COMMAND_PATH,
            "debug": cls.DEBUG
        }

# Configuración específica para diferentes ambientes
class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'INFO'
    
    @classmethod
    def validate(cls):
        super().validate()
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'default-secret-key':
            raise ValueError("SECRET_KEY requerida en producción")

# Seleccionar configuración según ambiente
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': Config
}

# Configuración activa
ConfigClass = config_map.get(os.getenv('ENVIRONMENT', 'default'), Config)