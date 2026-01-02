#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Múltiples Proveedores de IA (CORREGIDO)
========================================================

Sistema de gestión de múltiples APIs de IA
VERSIÓN CORREGIDA: Manejo mejorado de respuestas de MINIMAX

Autor: Eduardo Bascuñán
Fecha: 01 de enero de 2026
Versión: 2.0.2 - CORREGIDO PARA MINIMAX
"""

import os
import requests
import json
from typing import Dict, Optional, Any
from dotenv import load_dotenv

load_dotenv()

class GrokProvider:
    """Proveedor GROK (x.ai) - API gratuita"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-beta"
        
    def generate_response(self, message: str, system_prompt: str = None) -> Dict[str, Any]:
        """Generar respuesta usando GROK"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": message})
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": float(os.getenv("TEMPERATURE", "0.7")),
                "max_tokens": int(os.getenv("MAX_TOKENS", "4096"))
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "provider": "grok",
                    "message": result["choices"][0]["message"]["content"],
                    "model": self.model,
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0)
                }
            else:
                return {
                    "success": False,
                    "provider": "grok",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "provider": "grok",
                "error": str(e)
            }

class MinimaxProvider:
    """Proveedor MINIMAX - API china gratuita (CORREGIDO)"""
    
    def __init__(self, api_key: str, group_id: str = None):
        self.api_key = api_key
        self.group_id = group_id or os.getenv("MINIMAX_GROUP_ID", "")
        self.base_url = "https://api.minimax.chat/v1"
        self.model = "abab5.5-chat"
        
    def generate_response(self, message: str, system_prompt: str = None) -> Dict[str, Any]:
        """Generar respuesta usando MINIMAX (FORMATO CORREGIDO)"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if system_prompt:
                messages.append({"sender_type": "SYSTEM", "text": system_prompt})
            messages.append({"sender_type": "USER", "text": message})
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": float(os.getenv("TEMPERATURE", "0.7")),
                "max_tokens": int(os.getenv("MAX_TOKENS", "4096"))
            }
            
            if self.group_id:
                data["group_id"] = self.group_id
            
            response = requests.post(
                f"{self.base_url}/text/chatcompletion_v2",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # MANEJO MEJORADO DE RESPUESTAS DE MINIMAX
                message = ""
                tokens_used = 0
                
                # Intentar diferentes formatos de respuesta que puede devolver MINIMAX
                if "choices" in result and isinstance(result["choices"], list) and len(result["choices"]) > 0:
                    choice = result["choices"][0]
                    if "text" in choice:
                        message = choice["text"]
                    elif "message" in choice and "content" in choice["message"]:
                        message = choice["message"]["content"]
                elif "reply" in result:
                    message = result["reply"]
                elif "output" in result:
                    message = result["output"]
                elif "response" in result:
                    message = result["response"]
                elif "content" in result:
                    message = result["content"]
                elif "result" in result:
                    message = result["result"]
                else:
                    # Si no encontramos ningún formato esperado, devolver el resultado completo
                    message = str(result)
                
                # Obtener tokens si están disponibles
                if "usage" in result:
                    tokens_used = result["usage"].get("total_tokens", 0)
                elif "prompt_tokens" in result and "completion_tokens" in result:
                    tokens_used = result["prompt_tokens"] + result["completion_tokens"]
                elif "input_tokens" in result and "output_tokens" in result:
                    tokens_used = result["input_tokens"] + result["output_tokens"]
                
                return {
                    "success": True,
                    "provider": "minimax",
                    "message": message,
                    "model": self.model,
                    "tokens_used": tokens_used
                }
            else:
                return {
                    "success": False,
                    "provider": "minimax",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "provider": "minimax",
                "error": str(e)
            }

class ClaudeProvider:
    """Proveedor CLAUDE (Anthropic) - Configuración mejorada"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
        self.model = "claude-3-5-sonnet-20241022"
        self.anthropic_version = "2023-06-01"
        
    def generate_response(self, message: str, system_prompt: str = None) -> Dict[str, Any]:
        """Generar respuesta usando CLAUDE"""
        try:
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": self.anthropic_version,
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "max_tokens": int(os.getenv("MAX_TOKENS", "4096")),
                "temperature": float(os.getenv("TEMPERATURE", "0.7")),
                "messages": [
                    {"role": "user", "content": message}
                ]
            }
            
            if system_prompt:
                data["system"] = system_prompt
            
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "provider": "claude",
                    "message": result["content"][0]["text"],
                    "model": self.model,
                    "tokens_used": result.get("usage", {}).get("input_tokens", 0) + result.get("usage", {}).get("output_tokens", 0)
                }
            else:
                return {
                    "success": False,
                    "provider": "claude",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "provider": "claude",
                "error": str(e)
            }

class ChatGPTProvider:
    """Proveedor ChatGPT (OpenAI) - Gestión mejorada"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.model = os.getenv("CHATGPT_MODEL", "gpt-4o-mini")
        
    def generate_response(self, message: str, system_prompt: str = None) -> Dict[str, Any]:
        """Generar respuesta usando ChatGPT"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": message})
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": float(os.getenv("TEMPERATURE", "0.7")),
                "max_tokens": int(os.getenv("MAX_TOKENS", "4096"))
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "provider": "chatgpt",
                    "message": result["choices"][0]["message"]["content"],
                    "model": self.model,
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0)
                }
            else:
                return {
                    "success": False,
                    "provider": "chatgpt",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "provider": "chatgpt",
                "error": str(e)
            }

class DeepSeekProvider:
    """Proveedor DEEPSEEK API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com"
        self.model = "deepseek-chat"
        
    def generate_response(self, message: str, system_prompt: str = None) -> Dict[str, Any]:
        """Generar respuesta usando DEEPSEEK"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": message})
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": float(os.getenv("TEMPERATURE", "0.7")),
                "max_tokens": int(os.getenv("MAX_TOKENS", "4096"))
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "provider": "deepseek",
                    "message": result["choices"][0]["message"]["content"],
                    "model": self.model,
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0)
                }
            else:
                return {
                    "success": False,
                    "provider": "deepseek",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "provider": "deepseek",
                "error": str(e)
            }

class OllamaProvider:
    """Proveedor OLLAMA (API local gratuita)"""
    
    def __init__(self, host: str, model: str):
        self.host = host.rstrip('/')
        self.model = model
        
    def generate_response(self, message: str, system_prompt: str = None) -> Dict[str, Any]:
        """Generar respuesta usando OLLAMA"""
        try:
            data = {
                "model": self.model,
                "prompt": f"{system_prompt}\n\n{message}" if system_prompt else message,
                "stream": False,
                "options": {
                    "temperature": float(os.getenv("TEMPERATURE", "0.7")),
                    "num_predict": int(os.getenv("MAX_TOKENS", "4096"))
                }
            }
            
            response = requests.post(
                f"{self.host}/api/generate",
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "provider": "ollama",
                    "message": result.get("response", ""),
                    "model": self.model,
                    "tokens_used": result.get("eval_count", 0)
                }
            else:
                return {
                    "success": False,
                    "provider": "ollama",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "provider": "ollama",
                "error": str(e)
            }
            
    def check_connection(self) -> bool:
        """Verificar conexión con OLLAMA"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

class OpenAIProvider:
    """Proveedor OpenAI (fallback adicional)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "gpt-3.5-turbo"
        
    def generate_response(self, message: str, system_prompt: str = None) -> Dict[str, Any]:
        """Generar respuesta usando OpenAI"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": message})
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=float(os.getenv("TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("MAX_TOKENS", "4096"))
            )
            
            return {
                "success": True,
                "provider": "openai",
                "message": response.choices[0].message.content,
                "model": self.model,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "provider": "openai",
                "error": str(e)
            }

class AnthropicProvider:
    """Proveedor Anthropic (fallback adicional)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
        self.model = "claude-3-haiku-20240307"
        self.anthropic_version = "2023-06-01"
        
    def generate_response(self, message: str, system_prompt: str = None) -> Dict[str, Any]:
        """Generar respuesta usando Anthropic"""
        try:
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": self.anthropic_version,
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "max_tokens": int(os.getenv("MAX_TOKENS", "4096")),
                "messages": [
                    {"role": "user", "content": message}
                ]
            }
            
            if system_prompt:
                data["system"] = system_prompt
            
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "provider": "anthropic",
                    "message": result["content"][0]["text"],
                    "model": self.model,
                    "tokens_used": result.get("usage", {}).get("input_tokens", 0) + result.get("usage", {}).get("output_tokens", 0)
                }
            else:
                return {
                    "success": False,
                    "provider": "anthropic",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "provider": "anthropic",
                "error": str(e)
            }

class AIProviderManager:
    """Gestor principal de proveedores de IA"""
    
    def __init__(self):
        self.providers = {}
        self.default_provider = os.getenv("AI_PROVIDER_DEFAULT", "minimax")
        self.fallback_enabled = os.getenv("AI_FALLBACK_ENABLED", "true").lower() == "true"
        self._initialize_providers()
        
    def _initialize_providers(self):
        """Inicializar todos los proveedores (8 proveedores) - ORDEN OPTIMIZADO"""
        
        print("\n🔧 Inicializando proveedores de IA...")
        
        # 1. CLAUDE (Anthropic Premium) - PRIORIDAD ALTA
        claude_key = os.getenv("CLAUDE_API_KEY")
        if claude_key and claude_key not in ["", "tu_claude_api_key_aqui"]:
            try