# -*- coding: utf-8 -*-
"""
IA-EN-RVT Google Documents Processor
===================================

Procesador avanzado para documentos de Google (Sheets, XLS, DOC, PDF, CAD)
con integración completa del sistema de aprendizaje persistente.

Autor: Eduardo Bascuñán
Fecha: 2026-01-02
"""

import os
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json

# Google Services
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gspread
from google.auth.transport.requests import Request

# Document Processing
import pandas as pd
import PyPDF2
import pdfplumber
import openpyxl
import mammoth
from docx import Document
import ezdxf

# Learning System Integration
from learning_system import learn_content, query_knowledge

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Scopes para Google APIs
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/presentations.readonly'
]


class GoogleDocsProcessor:
    """Procesador principal de documentos de Google"""
    
    def __init__(self):
        self.credentials = None
        self.service = None
        self.gspread_client = None
        self._initialize_google_services()
    
    def _initialize_google_services(self):
        """Inicializar servicios de Google"""
        try:
            # Configurar credenciales OAuth2
            self._setup_credentials()
            
            # Inicializar Google Drive/Docs API
            self.service = build('drive', 'v3', credentials=self.credentials)
            
            # Inicializar gspread para Google Sheets
            self.gspread_client = gspread.authorize(self.credentials)
            
            logger.info("Google services initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google services: {e}")
            raise
    
    def _setup_credentials(self):
        """Configurar credenciales OAuth2"""
        try:
            # Verificar si ya tenemos credenciales guardadas
            token_path = Path("backend_ai/shared/google_docs/token.json")
            
            if token_path.exists():
                self.credentials = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            
            # Si las credenciales no son válidas o no existen, solicitar nuevo token
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    # En un entorno real, esto abriría un navegador para autenticación
                    # Para este ejemplo, usaremos credenciales de API key cuando sea posible
                    logger.warning("OAuth2 authentication required - using API key fallback")
                    self._setup_api_key_auth()
        
        except Exception as e:
            logger.error(f"Error setting up credentials: {e}")
            self._setup_api_key_auth()
    
    def _setup_api_key_auth(self):
        """Configurar autenticación con API Key"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Configurar servicio con API key
        from googleapiclient.discovery import build
        self.service = build('drive', 'v3', developerKey=api_key)
    
    async def process_google_sheet(self, spreadsheet_id: str, sheet_name: str = None) -> Dict[str, Any]:
        """Procesar Google Sheet"""
        try:
            logger.info(f"Processing Google Sheet: {spreadsheet_id}")
            
            # Abrir el spreadsheet
            spreadsheet = self.gspread_client.open_by_key(spreadsheet_id)
            
            # Obtener todas las hojas si no se especifica una
            if sheet_name:
                worksheet = spreadsheet.worksheet(sheet_name)
            else:
                worksheet = spreadsheet.get_worksheet(0)
            
            # Obtener todos los datos
            data = worksheet.get_all_records()
            
            if not data:
                return {'success': False, 'error': 'No data found in sheet'}
            
            # Convertir a DataFrame para análisis
            df = pd.DataFrame(data)
            
            # Analizar estructura del documento
            analysis = {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'columns': list(df.columns),
                'data_types': df.dtypes.to_dict(),
                'sample_data': df.head().to_dict('records')
            }
            
            # Extraer contenido textual relevante
            content_parts = []
            content_parts.append(f"Google Sheet: {spreadsheet.title}")
            content_parts.append(f"Hoja: {worksheet.title}")
            content_parts.append(f"Dimensiones: {analysis['total_rows']} filas x {analysis['total_columns']} columnas")
            content_parts.append(f"Columnas: {', '.join(analysis['columns'])}")
            
            # Añadir datos significativos (primeras filas)
            for i, row in df.head(10).iterrows():
                row_data = {k: v for k, v in row.items() if pd.notna(v)}
                if row_data:
                    content_parts.append(f"Fila {i+1}: {json.dumps(row_data, ensure_ascii=False)}")
            
            content = "\n".join(content_parts)
            
            # Aprender del contenido
            learning_id = await learn_content(
                content=content,
                content_type="document",
                source="google_sheet",
                metadata={
                    'spreadsheet_id': spreadsheet_id,
                    'sheet_name': worksheet.title,
                    'analysis': analysis,
                    'processed_at': datetime.now().isoformat()
                }
            )
            
            logger.info(f"Successfully processed Google Sheet, learning ID: {learning_id}")
            
            return {
                'success': True,
                'learning_id': learning_id,
                'analysis': analysis,
                'content_preview': content[:500] + "..." if len(content) > 500 else content
            }
            
        except Exception as e:
            logger.error(f"Error processing Google Sheet: {e}")
            return {'success': False, 'error': str(e)}
    
    async def process_google_document(self, document_id: str) -> Dict[str, Any]:
        """Procesar Google Document"""
        try:
            logger.info(f"Processing Google Document: {document_id}")
            
            # Obtener el documento
            document = self.service.files().get(fileId=document_id, fields='*').execute()
            
            # Verificar que es un documento de Google
            if document.get('mimeType') != 'application/vnd.google-apps.document':
                return {'success': False, 'error': 'File is not a Google Document'}
            
            # Descargar como HTML
            request = self.service.files().export_media(
                fileId=document_id,
                mimeType='text/html'
            )
            
            content = await asyncio.to_thread(request.execute)
            html_content = content.decode('utf-8')
            
            # Extraer texto del HTML
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text(separator=' ', strip=True)
            
            # Analizar estructura del documento
            analysis = {
                'title': document.get('name', 'Sin título'),
                'mime_type': document.get('mimeType'),
                'created_time': document.get('createdTime'),
                'modified_time': document.get('modifiedTime'),
                'size': document.get('size'),
                'word_count': len(text_content.split())
            }
            
            # Aprender del contenido
            learning_id = await learn_content(
                content=text_content,
                content_type="document",
                source="google_doc",
                metadata={
                    'document_id': document_id,
                    'title': analysis['title'],
                    'analysis': analysis,
                    'processed_at': datetime.now().isoformat()
                }
            )
            
            logger.info(f"Successfully processed Google Document, learning ID: {learning_id}")
            
            return {
                'success': True,
                'learning_id': learning_id,
                'analysis': analysis,
                'content_preview': text_content[:500] + "..." if len(text_content) > 500 else text_content
            }
            
        except HttpError as e:
            logger.error(f"HTTP error processing Google Document: {e}")
            return {'success': False, 'error': f'HTTP error: {e}'}
        except Exception as e:
            logger.error(f"Error processing Google Document: {e}")
            return {'success': False, 'error': str(e)}
    
    async def process_local_file(self, file_path: str, file_type: str = None) -> Dict[str, Any]:
        """Procesar archivo local (XLS, DOC, PDF, CAD)"""
        try:
            logger.info(f"Processing local file: {file_path}")
            
            file_path = Path(file_path)
            if not file_path.exists():
                return {'success': False, 'error': 'File not found'}
            
            # Determinar tipo de archivo si no se especifica
            if not file_type:
                file_type = file_path.suffix.lower()
            
            content = ""
            analysis = {}
            
            if file_type in ['.xls', '.xlsx', '.csv']:
                # Procesar archivo Excel
                content, analysis = await self._process_excel_file(file_path)
                
            elif file_type in ['.doc', '.docx']:
                # Procesar archivo Word
                content, analysis = await self._process_word_file(file_path)
                
            elif file_type == '.pdf':
                # Procesar archivo PDF
                content, analysis = await self._process_pdf_file(file_path)
                
            elif file_type in ['.dwg', '.dxf']:
                # Procesar archivo CAD
                content, analysis = await self._process_cad_file(file_path)
                
            else:
                return {'success': False, 'error': f'Unsupported file type: {file_type}'}
            
            if not content:
                return {'success': False, 'error': 'No content extracted from file'}
            
            # Aprender del contenido
            learning_id = await learn_content(
                content=content,
                content_type="document",
                source="local_file",
                metadata={
                    'file_path': str(file_path),
                    'file_type': file_type,
                    'analysis': analysis,
                    'processed_at': datetime.now().isoformat()
                }
            )
            
            logger.info(f"Successfully processed local file, learning ID: {learning_id}")
            
            return {
                'success': True,
                'learning_id': learning_id,
                'analysis': analysis,
                'content_preview': content[:500] + "..." if len(content) > 500 else content
            }
            
        except Exception as e:
            logger.error(f"Error processing local file: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _process_excel_file(self, file_path: Path) -> tuple:
        """Procesar archivo Excel"""
        try:
            # Leer con pandas
            df = pd.read_excel(file_path)
            
            analysis = {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'columns': list(df.columns),
                'data_types': df.dtypes.to_dict(),
                'missing_values': df.isnull().sum().to_dict()
            }
            
            # Extraer contenido textual
            content_parts = []
            content_parts.append(f"Archivo Excel: {file_path.name}")
            content_parts.append(f"Dimensiones: {analysis['total_rows']} filas x {analysis['total_columns']} columnas")
            content_parts.append(f"Columnas: {', '.join(analysis['columns'])}")
            
            # Añadir datos de muestra
            for i, row in df.head(20).iterrows():
                row_data = {k: v for k, v in row.items() if pd.notna(v)}
                if row_data:
                    content_parts.append(f"Fila {i+1}: {json.dumps(row_data, ensure_ascii=False)}")
            
            content = "\n".join(content_parts)
            
            return content, analysis
            
        except Exception as e:
            logger.error(f"Error processing Excel file: {e}")
            return "", {}
    
    async def _process_word_file(self, file_path: Path) -> tuple:
        """Procesar archivo Word"""
        try:
            if file_path.suffix.lower() == '.docx':
                # Procesar .docx con python-docx
                doc = Document(file_path)
                
                content_parts = []
                content_parts.append(f"Documento Word: {file_path.name}")
                
                paragraphs = []
                for paragraph in doc.paragraphs:
                    if paragraph.text.strip():
                        paragraphs.append(paragraph.text.strip())
                
                content = "\n".join(paragraphs)
                
                analysis = {
                    'total_paragraphs': len(paragraphs),
                    'total_characters': len(content),
                    'word_count': len(content.split())
                }
                
                return content, analysis
                
            else:
                # Para .doc, usar mammoth (requiere conversión)
                with open(file_path, "rb") as docx_file:
                    result = mammoth.extract_raw_text(docx_file)
                    content = result.value
                
                analysis = {
                    'total_characters': len(content),
                    'word_count': len(content.split())
                }
                
                return content, analysis
                
        except Exception as e:
            logger.error(f"Error processing Word file: {e}")
            return "", {}
    
    async def _process_pdf_file(self, file_path: Path) -> tuple:
        """Procesar archivo PDF"""
        try:
            content_parts = []
            analysis = {
                'total_pages': 0,
                'total_characters': 0,
                'word_count': 0
            }
            
            # Intentar con pdfplumber primero (mejor para tablas)
            try:
                with pdfplumber.open(file_path) as pdf:
                    analysis['total_pages'] = len(pdf.pages)
                    
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            content_parts.append(f"Página {page_num + 1}:\n{text}")
                        
                        # Extraer tablas si las hay
                        tables = page.extract_tables()
                        if tables:
                            for table_num, table in enumerate(tables):
                                content_parts.append(f"Tabla {table_num + 1} (Página {page_num + 1}):")
                                for row in table:
                                    if row:
                                        content_parts.append(" | ".join([str(cell) if cell else "" for cell in row]))
            
            except Exception as e:
                logger.warning(f"pdfplumber failed, trying PyPDF2: {e}")
                
                # Fallback a PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    analysis['total_pages'] = len(pdf_reader.pages)
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        text = page.extract_text()
                        if text:
                            content_parts.append(f"Página {page_num + 1}:\n{text}")
            
            content = "\n".join(content_parts)
            analysis['total_characters'] = len(content)
            analysis['word_count'] = len(content.split())
            
            return content, analysis
            
        except Exception as e:
            logger.error(f"Error processing PDF file: {e}")
            return "", {}
    
    async def _process_cad_file(self, file_path: Path) -> tuple:
        """Procesar archivo CAD (DWG, DXF)"""
        try:
            content_parts = []
            analysis = {
                'file_type': file_path.suffix.lower(),
                'total_entities': 0,
                'layers': [],
                'blocks': [],
                'dimensions': {}
            }
            
            if file_path.suffix.lower() == '.dxf':
                # Procesar DXF con ezdxf
                doc = ezdxf.readfile(file_path)
                analysis['dxf_version'] = doc.dxfversion
                
                # Contar entidades por tipo
                entity_counts = {}
                layers = set()
                blocks = set()
                
                for layout in doc.layouts:
                    for entity in layout:
                        entity_type = entity.dxftype()
                        entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
                        
                        # Recopilar capas
                        if hasattr(entity, 'dxf') and hasattr(entity.dxf, 'layer'):
                            layers.add(entity.dxf.layer)
                        
                        # Recopilar bloques
                        if entity_type == 'INSERT':
                            if hasattr(entity.dxf, 'name'):
                                blocks.add(entity.dxf.name)
                
                analysis['total_entities'] = sum(entity_counts.values())
                analysis['entity_counts'] = entity_counts
                analysis['layers'] = list(layers)
                analysis['blocks'] = list(blocks)
                
                # Crear descripción textual del contenido
                content_parts.append(f"Archivo CAD: {file_path.name}")
                content_parts.append(f"Tipo: DXF")
                content_parts.append(f"Versión DXF: {doc.dxfversion}")
                content_parts.append(f"Total de entidades: {analysis['total_entities']}")
                content_parts.append(f"Capas encontradas: {', '.join(layers) if layers else 'Ninguna'}")
                content_parts.append(f"Bloques encontrados: {', '.join(blocks) if blocks else 'Ninguno'}")
                
                # Añadir estadísticas de entidades
                for entity_type, count in entity_counts.items():
                    content_parts.append(f"Entidades {entity_type}: {count}")
                
                content = "\n".join(content_parts)
                
                return content, analysis
                
            else:
                # Para DWG, usar dwgread (si está disponible)
                try:
                    import dwgread
                    doc = dwgread.read(file_path)
                    # Procesar contenido DWG...
                    content = f"Archivo DWG: {file_path.name} - Procesado con dwgread"
                    analysis['processed_with'] = 'dwgread'
                    return content, analysis
                except ImportError:
                    logger.warning("dwgread not available for DWG processing")
                    content = f"Archivo DWG: {file_path.name} - Requiere dwgread para procesamiento completo"
                    analysis['processed_with'] = 'basic'
                    return content, analysis
                    
        except