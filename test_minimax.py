#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba rápida de MINIMAX API
"""

import sys
import os

# Añadir el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_minimax():
    """Probar MINIMAX específicamente"""
    try:
        from backend_ai.ai_providers import AIProviderManager
        
        print("🤖 Probando MINIMAX específicamente...")
        mgr = AIProviderManager()
        
        # Mensaje de prueba simple
        test_message = "Hola, responde solo 'OK'"
        
        print(f"📤 Enviando mensaje: {test_message}")
        
        # Probar con MINIMAX específicamente
        result = mgr.generate_response(test_message, provider_name="minimax")
        
        print(f"\n📥 Respuesta de MINIMAX:")
        if result['success']:
            print(f"   ✅ ÉXITO!")
            print(f"   📝 Mensaje: {result.get('message', 'N/A')}")
            print(f"   🏷️ Modelo: {result.get('model', 'N/A')}")
            print(f"   🔢 Tokens: {result.get('tokens_used', 'N/A')}")
        else:
            print(f"   ❌ ERROR!")
            print(f"   🚫 Error: {result.get('error', 'Error desconocido')}")
            print(f"   📋 Proveedores intentados: {result.get('providers_tried', [])}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_minimax()