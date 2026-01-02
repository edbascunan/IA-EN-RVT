#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de APIs de IA para verificar configuración
"""

import asyncio
import sys
import os

# Añadir el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_ai_apis():
    """Probar todas las APIs de IA configuradas"""
    try:
        from backend_ai.ai_providers import AIProviderManager
        
        print("🤖 Probando configuración de APIs de IA...")
        mgr = AIProviderManager()
        
        # Obtener estado de proveedores
        status = mgr.get_status()
        print(f"\n📊 Estado del sistema:")
        print(f"   Proveedor por defecto: {status['default_provider']}")
        print(f"   Fallback habilitado: {status['fallback_enabled']}")
        print(f"   Proveedores configurados: {len(status['providers'])}")
        
        # Probar cada proveedor disponible
        test_message = "Hola, responde solo 'OK' si puedes leer esto correctamente."
        
        for provider_name in status['providers'].keys():
            try:
                print(f"\n📡 Probando {provider_name.upper()}...")
                provider_info = status['providers'][provider_name]
                print(f"   Tipo: {provider_info['type']}")
                print(f"   Modelo: {provider_info.get('model', 'N/A')}")
                
                # Test rápido de API usando generate_response
                result = mgr.generate_response(test_message, provider_name=provider_name)
                
                if result['success']:
                    print(f"   ✅ {provider_name.upper()}: API funcionando correctamente")
                    print(f"   📝 Respuesta: {result.get('message', 'N/A')[:50]}...")
                    print(f"   🏷️ Modelo usado: {result.get('model', 'N/A')}")
                else:
                    print(f"   ❌ {provider_name.upper()}: {result.get('error', 'Error desconocido')}")
                        
            except Exception as e:
                print(f"   ❌ {provider_name.upper()}: Error - {str(e)}")
                
        # Probar sistema de fallback con un mensaje
        print(f"\n🔄 Probando sistema de fallback...")
        fallback_result = mgr.generate_response("Responde 'FALLBACK OK' si el sistema funciona.")
        
        if fallback_result['success']:
            print(f"✅ Sistema de fallback funciona con: {fallback_result.get('provider', 'N/A').upper()}")
        else:
            print(f"❌ Sistema de fallback falló: {fallback_result.get('error', 'Error desconocido')}")
        
        print("\n🏁 Prueba completada.")
        
    except ImportError as e:
        print(f"❌ Error importando ai_providers: {e}")
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_apis())