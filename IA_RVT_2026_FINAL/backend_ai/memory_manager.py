# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Gestor de Memoria Ilimitada
============================================

Sistema de memoria con RAG (Retrieval-Augmented Generation)
Basado en embeddings y búsqueda vectorial para memoria ilimitada
Autor: Eduardo Bascuñán
"""

import os
import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import hashlib

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from config import ConfigClass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryManager:
    """Gestor de memoria con RAG para IA_RVT"""
    
    def __init__(self, config=None):
        """Inicializar gestor de memoria"""
        self.config = config or ConfigClass
        self.embedding_config = self.config.get_embedding_config()
        
        # Inicializar embeddings
        self.embeddings_model = OpenAIEmbeddings(
            api_key=self.config.OPENAI_API_KEY,
            model="text-embedding-ada-002"
        )
        
        # Alternativa: modelo local
        self.local_model = SentenceTransformer(self.embedding_config['model_name'])
        
        # Inicializar vector store
        self.vector_store_path = self.embedding_config['vector_store_path']
        self.memory_db_path = self.embedding_config['memory_db_path']
        
        self._init_storage()
    
    def _init_storage(self):
        """Inicializar almacenamiento de memoria"""
        # Crear directorios si no existen
        os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.memory_db_path), exist_ok=True)
        
        # Inicializar base de datos SQLite
        self._init_database()
        
        # Inicializar vector store
        self._init_vector_store()
    
    def _init_database(self):
        """Inicializar base de datos SQLite"""
        conn = sqlite3.connect(self.memory_db_path)
        cursor = conn.cursor()
        
        # Tabla de conversaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                message TEXT NOT NULL,
                response TEXT,
                context TEXT,
                embedding_id TEXT,
                metadata TEXT
            )
        ''')
        
        # Tabla de embeddings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                vector BLOB,
                metadata TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de conocimiento BIM
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bim_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                relevance_score REAL DEFAULT 1.0,
                usage_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Base de datos de memoria inicializada")
    
    def _init_vector_store(self):
        """Inicializar vector store FAISS"""
        try:
            if os.path.exists(f"{self.vector_store_path}/index.faiss"):
                # Cargar vector store existente
                self.vector_store = FAISS.load_local(
                    self.vector_store_path,
                    self.embeddings_model,
                    "memory_store"
                )
                logger.info("Vector store cargado desde disco")
            else:
                # Crear nuevo vector store
                self.vector_store = FAISS.from_texts(
                    ["Memoria inicializada"],
                    self.embeddings_model
                )
                self.vector_store.save_local(self.vector_store_path, "memory_store")
                logger.info("Nuevo vector store creado")
        except Exception as e:
            logger.error(f"Error inicializando vector store: {e}")
            # Crear vector store básico como fallback
            self.vector_store = FAISS.from_texts(
                ["Memoria inicializada"],
                self.embeddings_model
            )
    
    def store_conversation(self, session_id: str, user_id: str, 
                          message: str, response: str, 
                          context: Dict[str, Any] = None) -> str:
        """Almacenar conversación en memoria"""
        try:
            # Generar ID único
            content_hash = hashlib.md5(f"{message}{response}".encode()).hexdigest()
            embedding_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{content_hash[:8]}"
            
            # Combinar mensaje y respuesta para embedding
            combined_content = f"Mensaje: {message}\nRespuesta: {response}"
            
            # Generar embedding
            embedding = self.embeddings_model.embed_query(combined_content)
            
            # Almacenar en vector store
            self.vector_store.add_texts([combined_content], 
                                      metadatas=[{
                                          'id': embedding_id,
                                          'session_id': session_id,
                                          'user_id': user_id,
                                          'type': 'conversation',
                                          'timestamp': datetime.now().isoformat()
                                      }])
            
            # Guardar vector store
            self.vector_store.save_local(self.vector_store_path, "memory_store")
            
            # Almacenar en SQLite
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conversations 
                (session_id, user_id, message, response, context, embedding_id, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (session_id, user_id, message, response, 
                  json.dumps(context) if context else None,
                  embedding_id, json.dumps(context) if context else None))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Conversación almacenada: {embedding_id}")
            return embedding_id
            
        except Exception as e:
            logger.error(f"Error almacenando conversación: {e}")
            return None
    
    def retrieve_relevant_memory(self, query: str, session_id: str = None, 
                               limit: int = 5) -> List[Dict[str, Any]]:
        """Recuperar memoria relevante usando RAG"""
        try:
            # Buscar en vector store
            docs_and_scores = self.vector_store.similarity_search_with_score(
                query, k=limit, filter={'session_id': session_id} if session_id else None
            )
            
            results = []
            for doc, score in docs_and_scores:
                if score > 0.3:  # Umbral de relevancia
                    results.append({
                        'content': doc.page_content,
                        'metadata': doc.metadata,
                        'score': score,
                        'relevance': 'Alta' if score > 0.7 else 'Media' if score > 0.5 else 'Baja'
                    })
            
            # Si no hay resultados suficientes, buscar en toda la memoria
            if len(results) < 2:
                all_docs = self.vector_store.similarity_search(query, k=limit)
                for doc in all_docs:
                    results.append({
                        'content': doc.page_content,
                        'metadata': doc.metadata,
                        'score': 0.5,
                        'relevance': 'General'
                    })
            
            logger.info(f"Memoria recuperada: {len(results)} resultados")
            return results
            
        except Exception as e:
            logger.error(f"Error recuperando memoria: {e}")
            return []
    
    def add_bim_knowledge(self, category: str, topic: str, 
                         content: str, source: str = None) -> bool:
        """Añadir conocimiento específico de BIM"""
        try:
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO bim_knowledge 
                (category, topic, content, source)
                VALUES (?, ?, ?, ?)
            ''', (category, topic, content, source))
            
            conn.commit()
            conn.close()
            
            # Añadir al vector store para búsqueda
            self.vector_store.add_texts([f"Categoría: {category}\nTema: {topic}\n{content}"],
                                      metadatas=[{
                                          'type': 'bim_knowledge',
                                          'category': category,
                                          'topic': topic,
                                          'source': source
                                      }])
            
            logger.info(f"Conocimiento BIM añadido: {category} - {topic}")
            return True
            
        except Exception as e:
            logger.error(f"Error añadiendo conocimiento BIM: {e}")
            return False
    
    def search_bim_knowledge(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """Buscar conocimiento específico de BIM"""
        try:
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()
            
            base_query = '''
                SELECT category, topic, content, source, relevance_score, usage_count
                FROM bim_knowledge
                WHERE (topic LIKE ? OR content LIKE ?)
            '''
            params = [f"%{query}%", f"%{query}%"]
            
            if category:
                base_query += " AND category = ?"
                params.append(category)
            
            base_query += " ORDER BY relevance_score DESC, usage_count DESC"
            
            cursor.execute(base_query, params)
            results = cursor.fetchall()
            
            conn.close()
            
            knowledge = []
            for row in results:
                knowledge.append({
                    'category': row[0],
                    'topic': row[1],
                    'content': row[2],
                    'source': row[3],
                    'relevance_score': row[4],
                    'usage_count': row[5]
                })
            
            # Incrementar contador de uso
            self._increment_knowledge_usage(query)
            
            return knowledge
            
        except Exception as e:
            logger.error(f"Error buscando conocimiento BIM: {e}")
            return []
    
    def _increment_knowledge_usage(self, query: str):
        """Incrementar contador de uso del conocimiento"""
        try:
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE bim_knowledge
                SET usage_count = usage_count + 1
                WHERE topic LIKE ? OR content LIKE ?
            ''', (f"%{query}%", f"%{query}%"))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error incrementando uso: {e}")
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener historial de conversación"""
        try:
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT message, response, context, timestamp
                FROM conversations
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (session_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            history = []
            for row in reversed(results):  # Orden cronológico
                history.append({
                    'message': row[0],
                    'response': row[1],
                    'context': json.loads(row[2]) if row[2] else None,
                    'timestamp': row[3]
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error obteniendo historial: {e}")
            return []
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de memoria"""
        try:
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()
            
            # Contar conversaciones
            cursor.execute('SELECT COUNT(*) FROM conversations')
            conversations = cursor.fetchone()[0]
            
            # Contar conocimiento BIM
            cursor.execute('SELECT COUNT(*) FROM bim_knowledge')
            knowledge_items = cursor.fetchone()[0]
            
            # Categorías de conocimiento
            cursor.execute('''
                SELECT category, COUNT(*) 
                FROM bim_knowledge 
                GROUP BY category
            ''')
            categories = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'total_conversations': conversations,
                'knowledge_items': knowledge_items,
                'categories': categories,
                'vector_store_size': len(self.vector_store.index_to_docstore_id),
                'memory_usage': 'Activa'
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
    
    def export_memory(self, file_path: str) -> bool:
        """Exportar memoria completa"""
        try:
            conn = sqlite3.connect(self.memory_db_path)
            
            # Exportar conversaciones
            conversations = pd.read_sql_query('SELECT * FROM conversations', conn)
            conversations.to_csv(f"{file_path}_conversations.csv", index=False)
            
            # Exportar conocimiento BIM
            knowledge = pd.read_sql_query('SELECT * FROM bim_knowledge', conn)
            knowledge.to_csv(f"{file_path}_knowledge.csv", index=False)
            
            conn.close()
            
            logger.info(f"Memoria exportada a: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exportando memoria: {e}")
            return False