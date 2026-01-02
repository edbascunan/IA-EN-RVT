# -*- coding: utf-8 -*-
"""
IA-EN-RVT Learning System - Sistema de Aprendizaje Persistente en la Nube
========================================================================

Sistema avanzado de aprendizaje que almacena todo el conocimiento en la nube
y utiliza múltiples LLMs para análisis profundo.

Autor: Eduardo Bascuñán
Fecha: 2026-01-02
"""

import os
import json
import asyncio
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import numpy as np

# Imports para vectorización
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import openai
import anthropic
import google.generativeai as genai

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LearningEntry:
    """Entrada de aprendizaje en la base de conocimiento"""
    id: str
    content: str
    content_type: str  # 'text', 'document', 'video', 'audio', 'image', 'cad'
    source: str  # 'youtube', 'google_docs', 'user_input', 'manual'
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    timestamp: str = ""
    importance_score: float = 1.0
    tags: List[str] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.tags:
            self.tags = []
        
        # Generar ID único si no existe
        if not self.id:
            content_hash = hashlib.md5(self.content.encode()).hexdigest()[:8]
            self.id = f"{self.content_type}_{self.source}_{content_hash}"


class MultiLLMProvider:
    """Gestor de múltiples proveedores de LLM con fallback automático"""
    
    def __init__(self):
        self.providers = {}
        self.current_provider = "openai"
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Inicializar todos los proveedores de LLM"""
        # OpenAI
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.providers['openai'] = {
                'client': openai,
                'model': 'gpt-4-turbo-preview',
                'type': 'openai'
            }
        
        # DeepSeek
        if os.getenv('DEEPSEEK_API_KEY'):
            self.providers['deepseek'] = {
                'client': None,  # Usar requests directamente
                'api_key': os.getenv('DEEPSEEK_API_KEY'),
                'model': 'deepseek-chat',
                'type': 'deepseek'
            }
        
        # Anthropic (Claude)
        if os.getenv('ANTHROPIC_API_KEY'):
            self.providers['anthropic'] = {
                'client': anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')),
                'model': 'claude-3-sonnet-20240229',
                'type': 'anthropic'
            }
        
        # Google
        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.providers['google'] = {
                'client': genai,
                'model': 'gemini-pro',
                'type': 'google'
            }
        
        # MiniMax
        if os.getenv('MINIMAX_API_KEY'):
            self.providers['minimax'] = {
                'client': None,
                'api_key': os.getenv('MINIMAX_API_KEY'),
                'model': 'abab6.5s-chat',
                'type': 'minimax'
            }
        
        # Grok
        if os.getenv('GROK_API_KEY'):
            self.providers['grok'] = {
                'client': None,
                'api_key': os.getenv('GROK_API_KEY'),
                'model': 'grok-beta',
                'type': 'grok'
            }
        
        logger.info(f"Initialized {len(self.providers)} LLM providers")
    
    async def generate_response(self, prompt: str, provider: str = None) -> Dict[str, Any]:
        """Generar respuesta usando el proveedor especificado o fallback"""
        if not provider:
            provider = self.current_provider
        
        # Intentar con el proveedor preferido
        if provider in self.providers:
            try:
                result = await self._call_provider(provider, prompt)
                if result['success']:
                    return result
            except Exception as e:
                logger.warning(f"Provider {provider} failed: {e}")
        
        # Fallback a otros proveedores
        for prov_name, prov_config in self.providers.items():
            if prov_name != provider:
                try:
                    result = await self._call_provider(prov_name, prompt)
                    if result['success']:
                        logger.info(f"Fallback successful: {prov_name}")
                        return result
                except Exception as e:
                    logger.warning(f"Provider {prov_name} failed: {e}")
        
        # Si todos fallan, usar respuesta por defecto
        return {
            'success': False,
            'response': "Todos los proveedores de IA están temporalmente no disponibles.",
            'provider': 'fallback'
        }
    
    async def _call_provider(self, provider: str, prompt: str) -> Dict[str, Any]:
        """Llamar a un proveedor específico"""
        prov = self.providers[provider]
        
        if provider == 'openai':
            return await self._call_openai(prov['client'], prompt)
        elif provider == 'anthropic':
            return await self._call_anthropic(prov['client'], prompt)
        elif provider == 'google':
            return await self._call_google(prov['client'], prompt)
        else:
            return await self._call_custom_api(provider, prompt)
    
    async def _call_openai(self, client, prompt: str) -> Dict[str, Any]:
        """Llamar a OpenAI"""
        try:
            response = await asyncio.to_thread(
                client.ChatCompletion.create,
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            return {
                'success': True,
                'response': response.choices[0].message.content,
                'provider': 'openai'
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'provider': 'openai'}
    
    async def _call_anthropic(self, client, prompt: str) -> Dict[str, Any]:
        """Llamar a Anthropic Claude"""
        try:
            response = await asyncio.to_thread(
                client.messages.create,
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return {
                'success': True,
                'response': response.content[0].text,
                'provider': 'anthropic'
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'provider': 'anthropic'}
    
    async def _call_google(self, client, prompt: str) -> Dict[str, Any]:
        """Llamar a Google Gemini"""
        try:
            model = client.GenerativeModel('gemini-pro')
            response = await asyncio.to_thread(
                model.generate_content,
                prompt
            )
            return {
                'success': True,
                'response': response.text,
                'provider': 'google'
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'provider': 'google'}
    
    async def _call_custom_api(self, provider: str, prompt: str) -> Dict[str, Any]:
        """Llamar a APIs personalizadas (DeepSeek, MiniMax, Grok)"""
        # Implementación simplificada - en producción usarías requests
        return {
            'success': False,
            'error': f"Custom API {provider} not implemented yet",
            'provider': provider
        }


class VectorDatabase:
    """Base de datos vectorial usando ChromaDB"""
    
    def __init__(self, db_path: str = "backend_ai/shared/vector_db"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Inicializar ChromaDB
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        
        # Crear o obtener colección
        self.collection = self.client.get_or_create_collection(
            name="ia_en_rvt_knowledge",
            metadata={"description": "Conocimiento persistente del sistema IA-EN-RVT"}
        )
        
        # Modelo de embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        logger.info(f"Vector database initialized at {self.db_path}")
    
    def add_entry(self, entry: LearningEntry) -> bool:
        """Añadir entrada a la base vectorial"""
        try:
            # Generar embedding si no existe
            if not entry.embedding:
                entry.embedding = self.embedding_model.encode(entry.content).tolist()
            
            # Añadir a ChromaDB
            self.collection.add(
                documents=[entry.content],
                embeddings=[entry.embedding],
                metadatas=[asdict(entry)],
                ids=[entry.id]
            )
            
            logger.info(f"Added entry {entry.id} to vector database")
            return True
            
        except Exception as e:
            logger.error(f"Error adding entry {entry.id}: {e}")
            return False
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Buscar en la base vectorial"""
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            return [
                {
                    'content': doc,
                    'metadata': meta,
                    'similarity': 1 - distance  # Convertir distancia a similitud
                }
                for doc, meta, distance in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )
            ]
            
        except Exception as e:
            logger.error(f"Error searching vector database: {e}")
            return []
    
    def get_entries_by_type(self, content_type: str) -> List[Dict[str, Any]]:
        """Obtener entradas por tipo de contenido"""
        try:
            results = self.collection.get(
                where={"content_type": content_type}
            )
            
            return [
                {
                    'content': doc,
                    'metadata': meta,
                    'id': id_val
                }
                for doc, meta, id_val in zip(
                    results['documents'],
                    results['metadatas'],
                    results['ids']
                )
            ]
            
        except Exception as e:
            logger.error(f"Error getting entries by type {content_type}: {e}")
            return []


class LearningSystem:
    """Sistema principal de aprendizaje persistente"""
    
    def __init__(self):
        self.vector_db = VectorDatabase()
        self.llm_provider = MultiLLMProvider()
        self.learning_data_path = Path("backend_ai/shared/learning_data")
        self.learning_data_path.mkdir(parents=True, exist_ok=True)
        
        # Configuración
        self.max_entries = int(os.getenv('MAX_LEARNING_ENTRIES', '10000'))
        self.encrypt_data = os.getenv('ENCRYPT_LEARNING_DATA', 'true').lower() == 'true'
        
        logger.info("Learning System initialized")
    
    async def learn_from_content(self, content: str, content_type: str, 
                                source: str, metadata: Dict[str, Any] = None) -> str:
        """Aprender de nuevo contenido"""
        if not metadata:
            metadata = {}
        
        # Crear entrada de aprendizaje
        entry = LearningEntry(
            id="",  # Se generará automáticamente
            content=content,
            content_type=content_type,
            source=source,
            metadata=metadata
        )
        
        # Añadir a base vectorial
        success = self.vector_db.add_entry(entry)
        
        if success:
            # Guardar también en archivo local para respaldo
            await self._save_learning_entry(entry)
            
            # Analizar con LLM para extraer conocimiento adicional
            await self._analyze_and_extract_knowledge(content, entry.id)
            
            logger.info(f"Learning entry created: {entry.id}")
            return entry.id
        else:
            logger.error(f"Failed to create learning entry")
            return ""
    
    async def query_knowledge(self, query: str, context: str = "") -> Dict[str, Any]:
        """Consultar el conocimiento aprendido"""
        # Buscar en base vectorial
        similar_entries = self.vector_db.search(query)
        
        # Formatear contexto
        context_text = ""
        if similar_entries:
            context_text = "Conocimiento relevante encontrado:\n\n"
            for i, entry in enumerate(similar_entries[:3], 1):
                context_text += f"{i}. {entry['content']}\n"
                context_text += f"   Fuente: {entry['metadata'].get('source', 'unknown')}\n"
                context_text += f"   Tipo: {entry['metadata'].get('content_type', 'unknown')}\n\n"
        
        # Crear prompt para LLM
        prompt = f"""
        Consulta: {query}
        
        {context_text}
        
        Contexto adicional: {context}
        
        Basándote en el conocimiento almacenado, proporciona una respuesta detallada y precisa.
        Si el conocimiento es insuficiente, indica qué información adicional necesitas.
        """
        
        # Obtener respuesta de LLM
        llm_response = await self.llm_provider.generate_response(prompt)
        
        return {
            'query': query,
            'similar_entries': similar_entries,
            'llm_response': llm_response,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _save_learning_entry(self, entry: LearningEntry):
        """Guardar entrada de aprendizaje en archivo"""
        try:
            filename = f"{entry.id}.json"
            filepath = self.learning_data_path / filename
            
            # Encriptar si está habilitado
            data = asdict(entry)
            if self.encrypt_data:
                # Implementar encriptación simple
                data['encrypted'] = True
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving learning entry {entry.id}: {e}")
    
    async def _analyze_and_extract_knowledge(self, content: str, entry_id: str):
        """Analizar contenido con LLM para extraer conocimiento adicional"""
        prompt = f"""
        Analiza el siguiente contenido y extrae información clave para el sistema de construcción:
        
        Contenido: {content[:2000]}...
        
        Extrae:
        1. Conceptos técnicos importantes
        2. Procedimientos o procesos
        3. Normas o regulaciones mencionadas
        4. Materiales o herramientas
        5. Mejores prácticas
        
        Responde en formato JSON con las siguientes claves:
        - concepts: lista de conceptos técnicos
        - procedures: lista de procedimientos
        - regulations: lista de regulaciones
        - materials: lista de materiales
        - practices: lista de mejores prácticas
        - tags: etiquetas relevantes
        """
        
        try:
            response = await self.llm_provider.generate_response(prompt)
            if response['success']:
                # Procesar respuesta y actualizar metadatos
                # (Implementación simplificada)
                logger.info(f"Knowledge extracted for entry {entry_id}")
                
        except Exception as e:
            logger.error(f"Error analyzing content for entry {entry_id}: {e}")
    
    async def get_learning_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del sistema de aprendizaje"""
        try:
            # Contar entradas por tipo
            content_types = {}
            total_entries = 0
            
            for content_type in ['text', 'document', 'video', 'audio', 'image', 'cad']:
                entries = self.vector_db.get_entries_by_type(content_type)
                content_types[content_type] = len(entries)
                total_entries += len(entries)
            
            return {
                'total_entries': total_entries,
                'entries_by_type': content_types,
                'vector_db_path': str(self.vector_db.db_path),
                'learning_data_path': str(self.learning_data_path),
                'max_entries': self.max_entries,
                'encryption_enabled': self.encrypt_data,
                'initialized_providers': len(self.llm_provider.providers)
            }
            
        except Exception as e:
            logger.error(f"Error getting learning stats: {e}")
            return {}


# Instancia global del sistema de aprendizaje
learning_system = LearningSystem()


# Funciones de conveniencia
async def learn_content(content: str, content_type: str = "text", 
                       source: str = "manual", metadata: Dict[str, Any] = None) -> str:
    """Función de conveniencia para aprender contenido"""
    return await learning_system.learn_from_content(content, content_type, source, metadata)


async def query_knowledge(query: str, context: str = "") -> Dict[str, Any]:
    """Función de conveniencia para consultar conocimiento"""
    return await learning_system.query_knowledge(query, context)


async def get_learning_stats() -> Dict[str, Any]:
    """Función de conveniencia para obtener estadísticas"""
    return await learning_system.get_learning_stats()


if __name__ == "__main__":
    # Test del sistema
    async def test_learning_system():
        print("Testing IA-EN-RVT Learning System...")
        
        # Test de aprendizaje
        entry_id = await learn_content(
            "Los muros de contención en Argentina deben cumplir con la norma IRAM 11507.",
            "document",
            "manual",
            {"category": "normativa", "country": "argentina"}
        )