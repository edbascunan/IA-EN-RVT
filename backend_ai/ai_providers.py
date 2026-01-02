#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Múltiples Proveedores de IA
=============================================

Sistema de gestión de múltiples APIs de IA

Autor: Eduardo Bascuñán
Fecha: 01 de enero de 2026
Versión: 2.0.1 - CORREGIDO Y FUNCIONAL
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
    """Proveedor MINIMAX - API china gratuita"""
    
    def __init__(self, api_key: str, group_id: str = None):
        self.api_key = api_key
        self.group_id = group_id or os.getenv("MINIMAX_GROUP_ID", "")
        self.base_url = "https://api.minimax.chat/v1"
        self.model = "abab5.5-chat"
        
    def generate_response(self, message: str, system_prompt: str = None) -> Dict[str, Any]:
        """Generar respuesta usando MINIMAX"""
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
                return {
                    "success": True,
                    "provider": "minimax",
                    "message": result["choices"][0]["text"],
                    "model": self.model,
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0)
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
                timeout=180
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
            try:
                self.providers["claude"] = ClaudeProvider(claude_key)
                print("  ✅ CLAUDE configurado (Prioridad: ALTA)")
            except Exception as e:
                print(f"  ⚠️ CLAUDE error: {e}")
            
        # 2. ChatGPT (OpenAI) - PRIORIDAD ALTA
        chatgpt_key = os.getenv("CHATGPT_API_KEY")
        if chatgpt_key and chatgpt_key not in ["", "tu_chatgpt_api_key_aqui"]:
            try:
                self.providers["chatgpt"] = ChatGPTProvider(chatgpt_key)
                print("  ✅ ChatGPT configurado (Prioridad: ALTA)")
            except Exception as e:
                print(f"  ⚠️ ChatGPT error: {e}")
            
        # 3. GROK (x.ai) - PRIORIDAD MEDIA (Gratuito)
        grok_key = os.getenv("GROK_API_KEY")
        if grok_key and grok_key not in ["", "tu_grok_api_key_aqui"]:
            try:
                self.providers["grok"] = GrokProvider(grok_key)
                print("  ✅ GROK configurado (Prioridad: MEDIA - Gratuito)")
            except Exception as e:
                print(f"  ⚠️ GROK error: {e}")
            
        # 4. MINIMAX - PRIORIDAD MEDIA (Gratuito)
        minimax_key = os.getenv("MINIMAX_API_KEY")
        if minimax_key and minimax_key not in ["", "tu_minimax_api_key_aqui"]:
            try:
                self.providers["minimax"] = MinimaxProvider(minimax_key)
                print("  ✅ MINIMAX configurado (Prioridad: MEDIA - Gratuito)")
            except Exception as e:
                print(f"  ⚠️ MINIMAX error: {e}")
            
        # 5. DEEPSEEK - PRIORIDAD BAJA (Sin saldo actualmente)
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key and deepseek_key not in ["", "tu_deepseek_api_key_aqui"]:
            try:
                self.providers["deepseek"] = DeepSeekProvider(deepseek_key)
                print("  ⚠️ DEEPSEEK configurado (Prioridad: BAJA - Sin saldo)")
            except Exception as e:
                print(f"  ⚠️ DEEPSEEK error: {e}")
            
        # 6. OpenAI (fallback)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key not in ["", "tu_openai_api_key_aqui"]:
            try:
                self.providers["openai"] = OpenAIProvider(openai_key)
                print("  ✅ OpenAI configurado (Fallback)")
            except Exception as e:
                print(f"  ⚠️ OpenAI error: {e}")
            
        # 7. Anthropic (fallback)
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key and anthropic_key not in ["", "tu_anthropic_api_key_aqui"]:
            try:
                self.providers["anthropic"] = AnthropicProvider(anthropic_key)
                print("  ✅ Anthropic configurado (Fallback)")
            except Exception as e:
                print(f"  ⚠️ Anthropic error: {e}")
                
        # 8. OLLAMA (local)
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "llama2")
        ollama_enabled = os.getenv("OLLAMA_ENABLED", "false").lower() == "true"
        
        if ollama_enabled:
            try:
                self.providers["ollama"] = OllamaProvider(ollama_host, ollama_model)
                print("  ✅ OLLAMA configurado (Local)")
            except Exception as e:
                print(f"  ⚠️ OLLAMA error: {e}")
        
        print(f"\n✅ Total de proveedores configurados: {len(self.providers)}")
        if len(self.providers) == 0:
            print("❌ ADVERTENCIA: No hay proveedores de IA disponibles!")
    
    def set_default_provider(self, provider_name: str) -> bool:
        """Cambiar proveedor por defecto"""
        if provider_name in self.providers:
            self.default_provider = provider_name
            os.environ["AI_PROVIDER_DEFAULT"] = provider_name
            return True
        return False
        
    def get_provider(self, name: str = None) -> Optional[Any]:
        """Obtener proveedor por nombre"""
        if name and name in self.providers:
            return self.providers[name]
            
        if self.default_provider in self.providers:
            return self.providers[self.default_provider]
            
        if self.providers:
            return list(self.providers.values())[0]
            
        return None
        
    def generate_response(self, message: str, provider_name: str = None, system_prompt: str = None) -> Dict[str, Any]:
        """Generar respuesta usando el proveedor especificado con fallback mejorado"""
        
        # Orden de fallback optimizado (proveedores que funcionan primero)
        fallback_order = [
            'claude',      # 1. Claude (mejor calidad, configurado)
            'chatgpt',     # 2. ChatGPT (rápido, configurado)
            'grok',        # 3. Grok (gratuito, configurado)
            'minimax',     # 4. Minimax (gratuito, configurado)
            'openai',      # 5. OpenAI (fallback premium)
            'anthropic',   # 6. Anthropic (fallback premium)
            'deepseek',    # 7. DeepSeek (sin saldo actualmente)
            'ollama'       # 8. Ollama (local, puede no estar activo)
        ]
        
        # Si se especificó un proveedor, intentar con ese primero
        if provider_name and provider_name in self.providers:
            provider = self.providers[provider_name]
            result = provider.generate_response(message, system_prompt)
            
            if result["success"]:
                return result
            
            # Si falló y fallback está habilitado, continuar con otros
            print(f"⚠️ {provider_name.upper()} falló: {result.get('error', 'Unknown')}")
            
            if not self.fallback_enabled:
                return result
        
        # Intentar con proveedor por defecto si no se especificó uno
        if not provider_name and self.default_provider in self.providers:
            provider = self.providers[self.default_provider]
            result = provider.generate_response(message, system_prompt)
            
            if result["success"]:
                return result
            
            print(f"⚠️ {self.default_provider.upper()} falló: {result.get('error', 'Unknown')}")
        
        # Fallback: intentar con todos los proveedores en orden
        if self.fallback_enabled:
            print("🔄 Activando sistema de fallback...")
            
            for fallback_name in fallback_order:
                # Saltar si ya intentamos con este proveedor
                if fallback_name == provider_name or fallback_name == self.default_provider:
                    continue
                    
                if fallback_name in self.providers:
                    print(f"   Intentando con {fallback_name.upper()}...")
                    fallback_provider = self.providers[fallback_name]
                    fallback_result = fallback_provider.generate_response(message, system_prompt)
                    
                    if fallback_result["success"]:
                        print(f"✅ {fallback_name.upper()} respondió exitosamente")
                        return fallback_result
                    else:
                        print(f"   ❌ {fallback_name.upper()} falló: {fallback_result.get('error', 'Unknown')}")
        
        # Si llegamos aquí, todos fallaron
        return {
            "success": False,
            "error": "Todos los proveedores de IA fallaron",
            "providers_tried": list(self.providers.keys()),
            "fallback_enabled": self.fallback_enabled
        }
        
    def check_ollama_connection(self) -> Dict[str, Any]:
        """Verificar estado de conexión de OLLAMA"""
        if "ollama" in self.providers:
            ollama = self.providers["ollama"]
            is_connected = ollama.check_connection()
            
            return {
                "connected": is_connected,
                "host": ollama.host,
                "model": ollama.model,
                "status": "🟢 Conectado" if is_connected else "🔴 Desconectado"
            }
        else:
            return {
                "connected": False,
                "host": "No configurado",
                "model": "No configurado",
                "status": "❌ No configurado"
            }
            
    def get_status(self) -> Dict[str, Any]:
        """Obtener estado de todos los proveedores"""
        status = {
            "default_provider": self.default_provider,
            "fallback_enabled": self.fallback_enabled,
            "providers": {},
            "ollama": self.check_ollama_connection()
        }
        
        for name, provider in self.providers.items():
            if hasattr(provider, 'api_key'):
                status["providers"][name] = {
                    "configured": True,
                    "type": "API",
                    "model": getattr(provider, 'model', 'unknown'),
                    "available": True
                }
            elif hasattr(provider, 'host'):
                status["providers"][name] = {
                    "configured": True,
                    "type": "Local",
                    "host": provider.host,
                    "model": provider.model,
                    "available": provider.check_connection()
                }
            else:
                status["providers"][name] = {
                    "configured": True,
                    "type": "Unknown",
                    "available": False
                }
                
        return status

# Instancia global del gestor
ai_manager = AIProviderManager()