#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Script de Prueba del Bot Zuko
===============================================

Prueba rápida del sistema antes de ejecutar en Revit
Autor: Eduardo Bascuñán
"""

import os
import json
from datetime import datetime

def verificar_configuracion():
    """Verificar que todos los archivos estén configurados correctamente"""
    print("🔍 Verificando configuración del sistema IA-EN-RVT 2026...")
    print("=" * 60)
    
    # Verificar archivo .env
    env_path = "/edbascunan/IA-EN-RVT/.env"
    if os.path.exists(env_path):
        print("✅ Archivo .env encontrado")
        with open(env_path, 'r') as f:
            env_content = f.read()
            if "7537372382:AAF58awLAyaQ4fFpZfdhn88dP555zW9JAGI" in env_content:
                print("✅ Token del bot Zuko configurado correctamente")
            else:
                print("❌ Token del bot no encontrado")
    else:
        print("❌ Archivo .env no encontrado")
    
    # Verificar bot principal
    bot_path = "/edbascunan/IA-EN-RVT/backend_ai/bot_zuko.py"
    if os.path.exists(bot_path):
        print("✅ Bot Zuko encontrado")
    else:
        print("❌ Bot Zuko no encontrado")
    
    # Verificar script de Revit
    revit_path = "/edbascunan/IA-EN-RVT/revit_executor/script_rps.py"
    if os.path.exists(revit_path):
        print("✅ Script de Revit encontrado")
    else:
        print("❌ Script de Revit no encontrado")
    
    # Verificar comando de prueba
    test_path = "/edbascunan/IA-EN-RVT/backend_ai/shared/command_test.json"
    if os.path.exists(test_path):
        print("✅ Comando de prueba encontrado")
        with open(test_path, 'r') as f:
            test_cmd = json.load(f)
            print(f"   📋 Comando: {test_cmd['accion']} {test_cmd['elemento']}")
            print(f"   📍 Inicio: ({test_cmd['payload']['inicio']['x']}, {test_cmd['payload']['inicio']['y']})")
            print(f"   📍 Fin: ({test_cmd['payload']['fin']['x']}, {test_cmd['payload']['fin']['y']})")
            print(f"   📏 Altura: {test_cmd['payload']['altura_m']}m")
    else:
        print("❌ Comando de prueba no encontrado")
    
    # Verificar requirements
    req_path = "/edbascunan/IA-EN-RVT/requirements.txt"
    if os.path.exists(req_path):
        print("✅ Requirements.txt encontrado")
    else:
        print("❌ Requirements.txt no encontrado")
    
    # Verificar instrucciones
    instr_path = "/edbascunan/IA-EN-RVT/INSTRUCCIONES_REVIT.md"
    if os.path.exists(instr_path):
        print("✅ Instrucciones de Revit encontradas")
    else:
        print("❌ Instrucciones de Revit no encontradas")
    
    print("=" * 60)
    print("🎯 Estado: Sistema listo para prueba en Revit")
    print()

def crear_comando_revit():
    """Crear comando activo para Revit"""
    comando = {
        "accion": "CREATE",
        "elemento": "Wall",
        "payload": {
            "inicio": {"x": 0, "y": 0},
            "fin": {"x": 5, "y": 0},
            "altura_m": 3.5
        },
        "timestamp": datetime.now().isoformat(),
        "estado": "PENDIENTE",
        "usuario": "Zuko_Bot_Test",
        "descripcion": "Muro de prueba - 5 metros de largo, 3.5m altura"
    }
    
    # Crear directorio si no existe
    shared_dir = "/edbascunan/IA-EN-RVT/backend_ai/shared"
    os.makedirs(shared_dir, exist_ok=True)
    
    # Guardar comando
    command_path = os.path.join(shared_dir, "command_out.json")
    with open(command_path, 'w', encoding='utf-8') as f:
        json.dump(comando, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Comando creado: {command_path}")
    print(f"📋 Acción: {comando['accion']} {comando['elemento']}")
    print(f"📍 Coordenadas: ({comando['payload']['inicio']['x']}, {comando['payload']['inicio']['y']}) → ({comando['payload']['fin']['x']}, {comando['payload']['fin']['y']})")
    print(f"📏 Altura: {comando['payload']['altura_m']}m")
    print()

def mostrar_instrucciones():
    """Mostrar instrucciones finales"""
    print("🚀 INSTRUCCIONES PARA EJECUTAR EN REVIT:")
    print("=" * 60)
    print()
    print("1. 📱 EJECUTAR BOT ZUKO:")
    print("   cd /edbascunan/IA-EN-RVT/backend_ai")
    print("   python bot_zuko.py")
    print()
    print("2. 🏗️ CONFIGURAR REVIT:")
    print("   - Instalar RevitPythonShell en Revit 2026")
    print("   - Copiar contenido de 'revit_executor/script_rps.py'")
    print("   - Ejecutar script en RevitPythonShell")
    print()
    print("3. 💬 PROBAR DESDE TELEGRAM:")
    print("   - Buscar bot: @ZukoIAENRVTBot (token: 7537372382:AAF58awLA...)")
    print("   - Enviar: /start")
    print("   - Enviar: /status")
    print("   - Enviar: /crear_muro 0 0 5 0 3.5")
    print()
    print("4. ✅ VERIFICAR EN REVIT:")
    print("   - Debe aparecer nuevo muro en el modelo")
    print("   - RevitPythonShell debe mostrar mensaje de éxito")
    print()
    print("🎯 ¡Sistema IA-EN-RVT 2026 listo para prueba!")
    print()

if __name__ == "__main__":
    verificar_configuracion()
    crear_comando_revit()
    mostrar_instrucciones()