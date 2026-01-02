# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Sistema RAG Multimodal
=======================================

Sistema RAG (Retrieval-Augmented Generation) para procesamiento multimodal:
- Texto (documentos, PDFs, normas)
- Imágenes (planos, screenshots)
- Video (YouTube, MP4)
- Audio (transcripciones)

Autor: Eduardo Bascuñán
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    Docx2txtLoader,
    CSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

from config import ConfigClass
from memory_manager import MemoryManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGSystem:
    """Sistema RAG Multimodal para IA_RVT"""
    
    def __init__(self, config=None):
        """Inicializar sistema RAG"""
        self.config = config or ConfigClass
        self.embedding_config = self.config.get_embedding_config()
        
        # Inicializar componentes
        self.memory_manager = MemoryManager(self.config)
        self.embeddings_model = OpenAIEmbeddings(
            api_key=self.config.OPENAI_API_KEY,
            model="text-embedding-ada-002"
        )
        
        # Inicializar vector store multimodal
        self.vector_store_path = os.path.join(
            self.embedding_config['vector_store_path'], 'multimodal'
        )
        self._init_multimodal_store()
        
        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def _init_multimodal_store(self):
        """Inicializar vector store multimodal"""
        os.makedirs(self.vector_store_path, exist_ok=True)
        
        try:
            if os.path.exists(os.path.join(self.vector_store_path, "index.faiss")):
                self.vector_store = FAISS.load_local(
                    self.vector_store_path,
                    self.embeddings_model,
                    "multimodal_store"
                )
                logger.info("Vector store multimodal cargado")
            else:
                self.vector_store = FAISS.from_texts(
                    ["Sistema RAG multimodal inicializado"],
                    self.embeddings_model
                )
                self.vector_store.save_local(self.vector_store_path, "multimodal_store")
                logger.info("Nuevo vector store multimodal creado")
        except Exception as e:
            logger.error(f"Error inicializando vector store multimodal: {e}")
            self.vector_store = FAISS.from_texts(
                ["Sistema RAG multimodal inicializado"],
                self.embeddings_model
            )
    
    def process_document(self, file_path: str, doc_type: str = "general") -> Dict[str, Any]:
        """Procesar documento y añadir al vector store"""
        try:
            # Determinar loader según tipo de archivo
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension == '.docx':
                loader = Docx2txtLoader(file_path)
            elif file_extension == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
            elif file_extension == '.csv':
                loader = CSVLoader(file_path)
            else:
                logger.warning(f"Tipo de archivo no soportado: {file_extension}")
                return {"success": False, "error": "Tipo de archivo no soportado"}
            
            # Cargar documentos
            documents = loader.load()
            
            # Dividir en chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Añadir metadatos
            for chunk in chunks:
                chunk.metadata.update({
                    'source': file_path,
                    'type': 'document',
                    'doc_type': doc_type,
                    'processed_at': datetime.now().isoformat()
                })
            
            # Añadir al vector store
            self.vector_store.add_documents(chunks)
            self.vector_store.save_local(self.vector_store_path, "multimodal_store")
            
            # Añadir conocimiento a memoria
            self.memory_manager.add_bim_knowledge(
                category=f"documentos_{doc_type}",
                topic=f"Documento: {os.path.basename(file_path)}",
                content=f"Procesado desde {file_path}",
                source=file_path
            )
            
            logger.info(f"Documento procesado: {file_path} ({len(chunks)} chunks)")
            return {
                "success": True,
                "chunks": len(chunks),
                "source": file_path,
                "type": doc_type
            }
            
        except Exception as e:
            logger.error(f"Error procesando documento: {e}")
            return {"success": False, "error": str(e)}
    
    def process_image(self, image_path: str, description: str = None) -> Dict[str, Any]:
        """Procesar imagen (plano, screenshot)"""
        try:
            # Por ahora, almacenar metadata de imagen
            # En implementación completa, usar CLIP para embeddings de imagen
            
            image_info = {
                'path': image_path,
                'description': description or f"Imagen: {os.path.basename(image_path)}",
                'processed_at': datetime.now().isoformat(),
                'type': 'image'
            }
            
            # Añadir descripción al vector store como texto
            self.vector_store.add_texts([
                f"IMAGEN: {image_info['description']}\nArchivo: {image_path}"
            ], metadatas=[{
                'source': image_path,
                'type': 'image',
                'file_path': image_path
            }])
            
            self.vector_store.save_local(self.vector_store_path, "multimodal_store")
            
            logger.info(f"Imagen procesada: {image_path}")
            return {"success": True, "path": image_path}
            
        except Exception as e:
            logger.error(f"Error procesando imagen: {e}")
            return {"success": False, "error": str(e)}
    
    def process_video_youtube(self, url: str, transcript: str = None) -> Dict[str, Any]:
        """Procesar video de YouTube"""
        try:
            # Extraer ID del video de YouTube
            video_id = self._extract_youtube_id(url)
            if not video_id:
                return {"success": False, "error": "URL de YouTube inválida"}
            
            # Simular procesamiento de transcripción
            # En implementación completa, usar YouTube API y Whisper
            
            video_info = {
                'url': url,
                'video_id': video_id,
                'transcript': transcript or f"Transcripción del video {video_id}",
                'processed_at': datetime.now().isoformat(),
                'type': 'video'
            }
            
            # Dividir transcripción en chunks
            transcript_chunks = self.text_splitter.split_text(video_info['transcript'])
            
            # Añadir al vector store
            self.vector_store.add_texts(transcript_chunks, metadatas=[{
                'source': url,
                'type': 'video',
                'video_id': video_id,
                'content_type': 'transcript'
            }])
            
            self.vector_store.save_local(self.vector_store_path, "multimodal_store")
            
            # Añadir conocimiento a memoria
            self.memory_manager.add_bim_knowledge(
                category="videos_youtube",
                topic=f"Video: {video_id}",
                content=f"Video procesado desde {url}",
                source=url
            )
            
            logger.info(f"Video de YouTube procesado: {video_id}")
            return {
                "success": True,
                "video_id": video_id,
                "url": url,
                "chunks": len(transcript_chunks)
            }
            
        except Exception as e:
            logger.error(f"Error procesando video: {e}")
            return {"success": False, "error": str(e)}
    
    def process_audio_transcript(self, audio_path: str, transcript: str) -> Dict[str, Any]:
        """Procesar transcripción de audio"""
        try:
            # Dividir transcripción en chunks
            audio_chunks = self.text_splitter.split_text(transcript)
            
            # Añadir al vector store
            self.vector_store.add_texts(audio_chunks, metadatas=[{
                'source': audio_path,
                'type': 'audio',
                'content_type': 'transcript'
            }])
            
            self.vector_store.save_local(self.vector_store_path, "multimodal_store")
            
            logger.info(f"Audio procesado: {audio_path}")
            return {
                "success": True,
                "path": audio_path,
                "chunks": len(audio_chunks)
            }
            
        except Exception as e:
            logger.error(f"Error procesando audio: {e}")
            return {"success": False, "error": str(e)}
    
    def _extract_youtube_id(self, url: str) -> Optional[str]:
        """Extraer ID de video de YouTube"""
        import re
        
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)',
            r'youtube\.com/embed/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def query_multimodal(self, query: str, filter_type: str = None) -> Dict[str, Any]:
        """Consultar en la base de conocimiento multimodal"""
        try:
            # Buscar en vector store
            search_kwargs = {"k": 5}
            
            if filter_type:
                search_kwargs["filter"] = {"type": filter_type}
            
            docs = self.vector_store.similarity_search(query, **search_kwargs)
            
            # Formatear resultados
            results = []
            for doc in docs:
                results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'source': doc.metadata.get('source', 'Desconocido'),
                    'type': doc.metadata.get('type', 'general')
                })
            
            # Buscar en memoria adicional
            memory_results = self.memory_manager.search_bim_knowledge(query)
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "memory_results": memory_results,
                "total_results": len(results) + len(memory_results)
            }
            
        except Exception as e:
            logger.error(f"Error en consulta multimodal: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_contextual_response(self, query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generar respuesta contextual usando RAG"""
        try:
            # Consultar base de conocimiento
            rag_results = self.query_multimodal(query)
            
            # Obtener memoria relevante
            memory_results = self.memory_manager.retrieve_relevant_memory(
                query, 
                session_id=user_context.get('session_id') if user_context else None
            )
            
            # Preparar contexto para OpenAI
            context_text = ""
            
            # Añadir resultados RAG
            if rag_results["success"] and rag_results["results"]:
                context_text += "CONTEXTO DE BASE DE CONOCIMIENTO:\n"
                for result in rag_results["results"][:3]:  # Top 3
                    context_text += f"- {result['content']}\n"
            
            # Añadir memoria relevante
            if memory_results:
                context_text += "\nMEMORIA RELEVANTE:\n"
                for mem in memory_results[:2]:  # Top 2
                    context_text += f"- {mem['content']}\n"
            
            # Generar respuesta con OpenAI
            from openai import OpenAI as OpenAIClient
            client = OpenAIClient(api_key=self.config.OPENAI_API_KEY)
            
            system_prompt = """
Eres un asistente experto en Revit y BIM. Tu trabajo es:
1. ENTENDER la consulta del usuario
2. USAR el contexto proporcionado para dar respuestas precisas
3. GENERAR comandos específicos para Revit cuando sea necesario
4. MANTENER un enfoque técnico y práctico

Si el contexto no es suficiente, usa tu conocimiento general de BIM y Revit.
            """
            
            user_prompt = f"""
CONSULTA: {query}

CONTEXTO DISPONIBLE:
{context_text}

USUARIO: {user_context.get('user_name', 'Usuario')} en sesión {user_context.get('session_id', 'N/A')}

Proporciona una respuesta útil y técnica.
            """
            
            response = client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Almacenar en memoria
            if user_context and user_context.get('session_id'):
                self.memory_manager.store_conversation(
                    session_id=user_context['session_id'],
                    user_id=user_context.get('user_id', 'unknown'),
                    message=query,
                    response=ai_response,
                    context=user_context
                )
            
            return {
                "success": True,
                "query": query,
                "response": ai_response,
                "context_used": len(rag_results["results"]) + len(memory_results),
                "sources": [r['source'] for r in rag_results["results"] if 'source' in r]
            }
            
        except Exception as e:
            logger.error(f"Error generando respuesta contextual: {e}")
            return {"success": False, "error": str(e)}
    
    def get_multimodal_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del sistema multimodal"""
        try:
            # Estadísticas del vector store
            vector_stats = {
                "vector_store_size": len(self.vector_store.index_to_docstore_id),
                "vector_store_path": self.vector_store_path
            }
            
            # Estadísticas de memoria
            memory_stats = self.memory_manager.get_memory_stats()
            
            return {
                "vector_store": vector_stats,
                "memory": memory_stats,
                "status": "Activo",
                "last_update": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {"error": str(e)}