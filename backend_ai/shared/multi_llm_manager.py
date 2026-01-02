# -*- coding: utf-8 -*-
"""
IA-EN-RVT Multi-LLM Manager
===========================

Gestor avanzado para múltiples proveedores de LLM con fallback automático,
balanceador de carga y aprendizaje continuo.

Autor: Eduardo Bascuñán
Fecha: 2026-01-02
"""

import os
import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import logging

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Enumeración de proveedores de LLM disponibles"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    MINIMAX = "minimax"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GROK = "grok"
    OLLAMA = "ollama"


@dataclass
class LLMRequest:
    """Solicitud a un LLM"""
    prompt: str
    provider: LLMProvider = None
    model: str = ""
    max_tokens: int = 2000
    temperature: float = 0.7
    system_message: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if not self.metadata:
            self.metadata = {}


@dataclass
class LLMResponse:
    """Respuesta de un LLM"""
    success: bool
    content: str = ""
    provider: LLMProvider = None
    model: str = ""
    tokens_used: int = 0
    cost: float = 0.0
    response_time: float = 0.0
    error: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if not self.metadata:
            self.metadata = {}


@dataclass
class LLMStats:
    """Estadísticas de un proveedor LLM"""
    provider: LLMProvider
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time: float = 0.0
    avg_tokens_per_request: float = 0.0
    total_cost: float = 0.0
    last_used: datetime = None
    is_available: bool = True
    rate_limit_remaining: int = 1000
    rate_limit_reset: datetime = None


class MultiLLMManager:
    """Gestor principal de múltiples LLMs"""
    
    def __init__(self):
        self.providers = {}
        self.stats = {}
        self.rate_limits = {}
        self.fallback_chain = [
            LLMProvider.OPENAI,
            LLMProvider.ANTHROPIC,
            LLMProvider.GOOGLE,
            LLMProvider.DEEPSEEK,
            LLMProvider.MINIMAX,
            LLMProvider.GROK,
            LLMProvider.OLLAMA
        ]
        
        # Configuración desde variables de entorno
        self.config = {
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
            'google_api_key': os.getenv('GOOGLE_API_KEY'),
            'deepseek_api_key': os.getenv('DEEPSEEK_API_KEY'),
            'minimax_api_key': os.getenv('MINIMAX_API_KEY'),
            'grok_api_key': os.getenv('GROK_API_KEY'),
            'ollama_base_url': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        }
        
        self._initialize_providers()
        self._load_learning_data()
    
    def _initialize_providers(self):
        """Inicializar todos los proveedores disponibles"""
        # OpenAI
        if self.config['openai_api_key']:
            self.providers[LLMProvider.OPENAI] = OpenAIProvider(
                self.config['openai_api_key']
            )
            self.stats[LLMProvider.OPENAI] = LLMStats(provider=LLMProvider.OPENAI)
        
        # Anthropic (Claude)
        if self.config['anthropic_api_key']:
            self.providers[LLMProvider.ANTHROPIC] = AnthropicProvider(
                self.config['anthropic_api_key']
            )
            self.stats[LLMProvider.ANTHROPIC] = LLMStats(provider=LLMProvider.ANTHROPIC)
        
        # Google (Gemini)
        if self.config['google_api_key']:
            self.providers[LLMProvider.GOOGLE] = GoogleProvider(
                self.config['google_api_key']
            )
            self.stats[LLMProvider.GOOGLE] = LLMStats(provider=LLMProvider.GOOGLE)
        
        # DeepSeek
        if self.config['deepseek_api_key']:
            self.providers[LLMProvider.DEEPSEEK] = DeepSeekProvider(
                self.config['deepseek_api_key']
            )
            self.stats[LLMProvider.DEEPSEEK] = LLMStats(provider=LLMProvider.DEEPSEEK)
        
        # MiniMax
        if self.config['minimax_api_key']:
            self.providers[LLMProvider.MINIMAX] = MiniMaxProvider(
                self.config['minimax_api_key']
            )
            self.stats[LLMProvider.MINIMAX] = LLMStats(provider=LLMProvider.MINIMAX)
        
        # Grok
        if self.config['grok_api_key']:
            self.providers[LLMProvider.GROK] = GrokProvider(
                self.config['grok_api_key']
            )
            self.stats[LLMProvider.GROK] = LLMStats(provider=LLMProvider.GROK)
        
        # Ollama (Local)
        self.providers[LLMProvider.OLLAMA] = OllamaProvider(
            self.config['ollama_base_url']
        )
        self.stats[LLMProvider.OLLAMA] = LLMStats(provider=LLMProvider.OLLAMA)
        
        logger.info(f"Initialized {len(self.providers)} LLM providers")
    
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Generar respuesta usando el proveedor especificado o fallback automático"""
        start_time = time.time()
        
        # Determinar orden de proveedores a probar
        providers_to_try = self._get_provider_priority(request.provider)
        
        last_error = ""
        for provider in providers_to_try:
            if provider not in self.providers:
                continue
            
            # Verificar disponibilidad del proveedor
            if not self._is_provider_available(provider):
                continue
            
            try:
                response = await self._call_provider(provider, request)
                
                if response.success:
                    # Actualizar estadísticas
                    self._update_stats(provider, response, time.time() - start_time)
                    
                    # Guardar en aprendizaje
                    await self._save_interaction(request, response)
                    
                    logger.info(f"Response generated by {provider.value}")
                    return response
                else:
                    last_error = response.error
                    logger.warning(f"Provider {provider.value} failed: {response.error}")
                    
            except Exception as e:
                last_error = str(e)
                logger.error(f"Error calling provider {provider.value}: {e}")
        
        # Si todos fallan, devolver respuesta de error
        return LLMResponse(
            success=False,
            error=f"All providers failed. Last error: {last_error}",
            provider=LLMProvider.OPENAI  # Default fallback
        )
    
    def _get_provider_priority(self, preferred_provider: LLMProvider = None) -> List[LLMProvider]:
        """Obtener orden de proveedores según prioridad y disponibilidad"""
        if preferred_provider and preferred_provider in self.providers:
            # Mover el proveedor preferido al inicio
            providers = [p for p in self.fallback_chain if p in self.providers]
            providers.remove(preferred_provider)
            providers.insert(0, preferred_provider)
            return providers
        
        # Ordenar por estadísticas de rendimiento
        return sorted(
            [p for p in self.fallback_chain if p in self.providers],
            key=lambda p: self._get_provider_score(p),
            reverse=True
        )
    
    def _get_provider_score(self, provider: LLMProvider) -> float:
        """Calcular puntuación de rendimiento del proveedor"""
        if provider not in self.stats:
            return 0.0
        
        stats = self.stats[provider]
        
        # Factores de puntuación
        success_rate = stats.successful_requests / max(stats.total_requests, 1)
        speed_score = 1.0 / max(stats.avg_response_time, 0.1)  # Más rápido = mayor puntuación
        availability_score = 1.0 if stats.is_available else 0.0
        
        # Puntuación combinada
        score = (success_rate * 0.4 + min(speed_score, 10.0) * 0.3 + availability_score * 0.3)
        
        return score
    
    def _is_provider_available(self, provider: LLMProvider) -> bool:
        """Verificar si un proveedor está disponible"""
        if provider not in self.stats:
            return False
        
        stats = self.stats[provider]
        
        # Verificar disponibilidad básica
        if not stats.is_available:
            return False
        
        # Verificar rate limits
        if stats.rate_limit_remaining <= 0:
            if stats.rate_limit_reset and datetime.now() < stats.rate_limit_reset:
                return False
            else:
                # Reset rate limit
                stats.rate_limit_remaining = 1000
                stats.rate_limit_reset = None
        
        return True
    
    async def _call_provider(self, provider: LLMRequest, request: LLMRequest) -> LLMResponse:
        """Llamar a un proveedor específico"""
        prov = self.providers[provider]
        return await prov.generate_response(request)
    
    def _update_stats(self, provider: LLMProvider, response: LLMResponse, response_time: float):
        """Actualizar estadísticas del proveedor"""
        if provider not in self.stats:
            return
        
        stats = self.stats[provider]
        
        # Actualizar contadores
        stats.total_requests += 1
        if response.success:
            stats.successful_requests += 1
        else:
            stats.failed_requests += 1
        
        # Actualizar tiempos promedio
        stats.avg_response_time = (
            (stats.avg_response_time * (stats.total_requests - 1) + response_time) / 
            stats.total_requests
        )
        
        # Actualizar tokens promedio
        if response.tokens_used > 0:
            stats.avg_tokens_per_request = (
                (stats.avg_tokens_per_request * (stats.total_requests - 1) + response.tokens_used) /
                stats.total_requests
            )
        
        # Actualizar costo total
        stats.total_cost += response.cost
        
        # Actualizar último uso
        stats.last_used = datetime.now()
        
        # Actualizar rate limits
        stats.rate_limit_remaining -= 1
    
    async def _save_interaction(self, request: LLMRequest, response: LLMResponse):
        """Guardar interacción para aprendizaje futuro"""
        try:
            interaction_data = {
                'timestamp': datetime.now().isoformat(),
                'provider': response.provider.value,
                'request': {
                    'prompt': request.prompt,
                    'model': request.model,
                    'max_tokens': request.max_tokens,
                    'temperature': request.temperature
                },
                'response': {
                    'success': response.success,
                    'content': response.content,
                    'tokens_used': response.tokens_used,
                    'cost': response.cost,
                    'response_time': response.response_time
                },
                'success': response.success,
                'error': response.error
            }
            
            # Guardar en archivo de interacciones
            interactions_file = Path("backend_ai/shared/learning_data/llm_interactions.json")
            interactions_file.parent.mkdir(parents=True, exist_ok=True)
            
            interactions = []
            if interactions_file.exists():
                with open(interactions_file, 'r', encoding='utf-8') as f:
                    interactions = json.load(f)
            
            interactions.append(interaction_data)
            
            # Mantener solo las últimas 1000 interacciones
            if len(interactions) > 1000:
                interactions = interactions[-1000:]
            
            with open(interactions_file, 'w', encoding='utf-8') as f:
                json.dump(interactions, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving interaction: {e}")
    
    def _load_learning_data(self):
        """Cargar datos de aprendizaje para mejorar el balanceador"""
        try:
            interactions_file = Path("backend_ai/shared/learning_data/llm_interactions.json")
            if interactions_file.exists():
                with open(interactions_file, 'r', encoding='utf-8') as f:
                    interactions = json.load(f)
                
                # Analizar interacciones pasadas para optimizar el balanceador
                for interaction in interactions[-100:]:  # Últimas 100 interacciones
                    if interaction['success']:
                        provider = LLMProvider(interaction['provider'])
                        if provider in self.stats:
                            # Ajustar estadísticas basadas en datos históricos
                            self.stats[provider].successful_requests += 1
                            self.stats[provider].total_requests += 1
                            self.stats[provider].avg_response_time = (
                                (self.stats[provider].avg_response_time * 0.8) +
                                (interaction['response']['response_time'] * 0.2)
                            )
                
                logger.info(f"Loaded {len(interactions)} historical interactions")
                
        except Exception as e:
            logger.error(f"Error loading learning data: {e}")
    
    def get_provider_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de todos los proveedores"""
        stats_data = {}
        for provider, stats in self.stats.items():
            stats_data[provider.value] = asdict(stats)
            # Convertir datetime a string para JSON
            if stats.last_used:
                stats_data[provider.value]['last_used'] = stats.last_used.isoformat()
            if stats.rate_limit_reset:
                stats_data[provider.value]['rate_limit_reset'] = stats.rate_limit_reset.isoformat()
        
        return stats_data
    
    def set_provider_availability(self, provider: LLMProvider, available: bool):
        """Configurar disponibilidad de un proveedor"""
        if provider in self.stats:
            self.stats[provider].is_available = available
            logger.info(f"Provider {provider.value} availability set to {available}")
    
    def get_best_provider(self) -> Optional[LLMProvider]:
        """Obtener el mejor proveedor disponible"""
        available_providers = [
            p for p in self.fallback_chain 
            if p in self.providers and self._is_provider_available(p)
        ]
        
        if not available_providers:
            return None
        
        return max(available_providers, key=lambda p: self._get_provider_score(p))


# Clases de proveedores específicos
class OpenAIProvider:
    """Proveedor de OpenAI"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
    
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Generar respuesta usando OpenAI"""
        try:
            import openai
            openai.api_key = self.api_key
            
            messages = []
            if request.system_message:
                messages.append({"role": "system", "content": request.system_message})
            messages.append({"role": "user", "content": request.prompt})
            
            response = await asyncio.to_thread(
                openai.ChatCompletion.create,
                model=request.model or "gpt-4-turbo-preview",
                messages=messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            return LLMResponse(
                success=True,
                content=response.choices[0].message.content,
                provider=LLMProvider.OPENAI,
                model=request.model or "gpt-4-turbo-preview",
                tokens_used=response.usage.total_tokens if hasattr(response, 'usage') else 0,
                cost=0.02  # Estimación aproximada
            )
            
        except Exception as e:
            return LLMResponse(
                success=False,
                error=str(e),
                provider=LLMProvider.OPENAI
            )


class AnthropicProvider:
    """Proveedor de Anthropic (Claude)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com"
    
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Generar respuesta usando Anthropic Claude"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = await asyncio.to_thread(
                client.messages.create,
                model=request.model or "claude-3-sonnet-20240229",
                max_tokens=request.max_tokens,
                messages=[{"role": "user", "content": request.prompt}]
            )
            
            return LLMResponse(
                success=True,
                content=response.content[0