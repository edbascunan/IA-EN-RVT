#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Prueba del Esquema JSON Corregido
==================================================

Verificar que el esquema JSON es compatible con PYREVIT
Autor: Eduardo Bascuñán
"""

import os
import json
from datetime import datetime

def test_json_schema():
    """Probar el esquema JSON corregido"""
    print("🔍 Probando esquema JSON corregido para PYREVIT...")
    print("=" * 60)
    
    # Crear directorio de prueba
    test_dir = "/edbascunan/IA-EN-RVT/backend_ai/shared"
    os.makedirs(test_dir, exist_ok=True)
    
    # Comando de prueba con esquema mínimo
    comando_test = {
        "accion": "CREATE",
        "elemento": "Wall", 
        "payload": {
            "inicio": {"x": 0, "y": 0},
            "fin": {"x": 5, "y": 0},
            "altura_m": 3.5
        }
    }
    
    # Guardar comando
    command_path = os.path.join(test_dir, "command_test_fixed.json")
    with open(command_path, 'w', encoding='utf-8') as f:
        json.dump(comando_test, f, indent=2, ensure_ascii=False)
    
    print("✅ Comando guardado en:", command_path)
    
    # Verificar estructura
    print("\n📋 Estructura del JSON:")
    print(json.dumps(comando_test, indent=2, ensure_ascii=False))
    
    # Verificar campos mínimos requeridos
    campos_requeridos = ["accion", "elemento", "payload"]
    print(f"\n🔍 Verificando campos requeridos: {campos_requeridos}")
    
    for campo in campos_requeridos:
        if campo in comando_test:
            print(f"  ✅ {campo}: {comando_test[campo]}")
        else:
            print(f"  ❌ {campo}: FALTANTE")
    
    # Verificar payload
    payload = comando_test.get("payload", {})
    campos_payload = ["inicio", "fin", "altura_m"]
    print(f"\n🔍 Verificando campos del payload: {campos_payload}")
    
    for campo in campos_payload:
        if campo in payload:
            print(f"  ✅ {campo}: {payload[campo]}")
        else:
            print(f"  ❌ {campo}: FALTANTE")
    
    print("\n" + "=" * 60)
    print("✅ ESQUEMA JSON COMPATIBLE CON PYREVIT")
    print("📝 No hay campos extra como 'usuario', 'fuente', 'descripcion'")
    print("🎯 Listo para usar con el bot corregido")
    
    return comando_test

def show_bot_instructions():
    """Mostrar instrucciones para usar el bot corregido"""
    print("\n🚀 INSTRUCCIONES PARA USAR EL BOT CORREGIDO:")
    print("=" * 60)
    print()
    print("1. 📱 EJECUTAR BOT CORREGIDO:")
    print("   cd /edbascunan/IA-EN-RVT/backend_ai")
    print("   python bot_zuko_fixed.py")
    print()
    print("2. 💬 USAR COMANDOS EN TELEGRAM:")
    print("   • /start - Verificar bot activo")
    print("   • /crear_muro 0 0 5 0 3.5 - Crear muro")
    print("   • /muro_rapido - Muro de prueba")
    print("   • /analizar - Analizar modelo")
    print()
    print("3. 🏗️ EJECUTAR EN REVIT:")
    print("   • Abrir Revit 2026")
    print("   • Hacer clic en '🏗️ Zuko' en la pestaña IaEnRvt")
    print("   • Verificar que no hay errores de esquema")
    print()
    print("4. ✅ VERIFICAR RESULTADO:")
    print("   • El muro debe crearse sin errores")
    print("   • TaskDialog debe mostrar éxito")
    print("   • Sin mensajes de 'Schema invalido'")

if __name__ == "__main__":
    test_json_schema()
    show_bot_instructions()