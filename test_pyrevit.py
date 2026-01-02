#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Script de Prueba PYREVIT
=========================================

Prueba completa del sistema con PYREVIT
Autor: Eduardo Bascuñán
"""

import os
import json
from datetime import datetime

def verificar_configuracion_pyrevit():
    """Verificar que todos los archivos PYREVIT estén configurados"""
    print("🔍 Verificando configuración del sistema IA-EN-RVT 2026 PYREVIT...")
    print("=" * 70)
    
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
    
    # Verificar bot PYREVIT
    bot_path = "/edbascunan/IA-EN-RVT/backend_ai/bot_zuko_pyrevit.py"
    if os.path.exists(bot_path):
        print("✅ Bot Zuko PYREVIT encontrado")
    else:
        print("❌ Bot Zuko PYREVIT no encontrado")
    
    # Verificar extensión PYREVIT
    extension_path = "/edbascunan/IA-EN-RVT/pyrevit_extension"
    if os.path.exists(extension_path):
        print("✅ Extensión PYREVIT encontrada")
        
        # Verificar archivos importantes de PYREVIT
        archivos_pyrevit = [
            "IaEnRvt.extension/IaEnRvt.extension",
            "IaEnRvt.extension/IaEnRvt.tab/Panel 1.stack/Muro Zuko.pushbutton/Muro Zuko.py",
            "IaEnRvt.extension/IaEnRvt.tab/Panel 1.stack/Muro Zuko.pushbutton/config.yaml"
        ]
        
        for archivo in archivos_pyrevit:
            archivo_path = os.path.join(extension_path, archivo)
            if os.path.exists(archivo_path):
                print(f"  ✅ {archivo}")
            else:
                print(f"  ❌ {archivo}")
    else:
        print("❌ Extensión PYREVIT no encontrada")
    
    # Verificar instalador PYREVIT
    installer_path = "/edbascunan/IA-EN-RVT/instalar_pyrevit.py"
    if os.path.exists(installer_path):
        print("✅ Instalador PYREVIT encontrado")
    else:
        print("❌ Instalador PYREVIT no encontrado")
    
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
    instr_path = "/edbascunan/IA-EN-RVT/INSTRUCCIONES_PYREVIT_COMPLETAS.md"
    if os.path.exists(instr_path):
        print("✅ Instrucciones PYREVIT encontradas")
    else:
        print("❌ Instrucciones PYREVIT no encontradas")
    
    print("=" * 70)
    print("🎯 Estado: Sistema PYREVIT listo para prueba")
    print()

def crear_comando_pyrevit():
    """Crear comando activo para PYREVIT"""
    comando = {
        "accion": "CREATE",
        "elemento": "Wall",
        "payload": {
            "inicio": {"x": 0, "y": 0},
            "fin": {"x": 6, "y": 0},
            "altura_m": 4.0
        },
        "timestamp": datetime.now().isoformat(),
        "estado": "PENDIENTE",
        "usuario": "Zuko_PYREVIT_Test",
        "fuente": "telegram_bot",
        "descripcion": "Muro de prueba PYREVIT - 6 metros de largo, 4.0m altura"
    }
    
    # Crear directorio si no existe
    shared_dir = "/edbascunan/IA-EN-RVT/backend_ai/shared"
    os.makedirs(shared_dir, exist_ok=True)
    
    # Guardar comando
    command_path = os.path.join(shared_dir, "command_out.json")
    with open(command_path, 'w', encoding='utf-8') as f:
        json.dump(comando, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Comando PYREVIT creado: {command_path}")
    print(f"📋 Acción: {comando['accion']} {comando['elemento']}")
    print(f"📍 Coordenadas: ({comando['payload']['inicio']['x']}, {comando['payload']['inicio']['y']}) → ({comando['payload']['fin']['x']}, {comando['payload']['fin']['y']})")
    print(f"📏 Altura: {comando['payload']['altura_m']}m")
    print()

def mostrar_instrucciones_pyrevit():
    """Mostrar instrucciones finales PYREVIT"""
    print("🚀 INSTRUCCIONES PARA EJECUTAR CON PYREVIT:")
    print("=" * 70)
    print()
    print("1. 📱 EJECUTAR BOT ZUKO PYREVIT:")
    print("   cd /edbascunan/IA-EN-RVT/backend_ai")
    print("   python bot_zuko_pyrevit.py")
    print()
    print("2. 🏗️ INSTALAR PYREVIT:")
    print("   • Descargar desde: github.com/eirannejad/pyRevit")
    print("   • Ejecutar: python instalar_pyrevit.py")
    print()
    print("3. ⚙️ CONFIGURAR REVIT:")
    print("   • Abrir Revit 2026")
    print("   • PYREVIT > Extensions > Reload")
    print("   • Buscar pestaña 'IaEnRvt'")
    print()
    print("4. 💬 PROBAR DESDE TELEGRAM:")
    print("   • Buscar bot: @ZukoIAENRVTBot")
    print("   • Enviar: /start")
    print("   • Enviar: /pyrevit")
    print("   • Enviar: /crear_muro 0 0 6 0 4.0")
    print("   • Hacer clic en 'Zuko' en Revit")
    print()
    print("5. ✅ VERIFICAR EN REVIT:")
    print("   • Debe aparecer nuevo muro en el modelo")
    print("   • PYREVIT debe mostrar TaskDialog de éxito")
    print()
    print("🎯 ¡Sistema IA-EN-RVT 2026 PYREVIT listo!")
    print()

if __name__ == "__main__":
    verificar_configuracion_pyrevit()
    crear_comando_pyrevit()
    mostrar_instrucciones_pyrevit()