#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Script de Prueba Integral
==========================================

Prueba TODOS los componentes del sistema:
1. Estructura de pyRevit
2. Bot NLP
3. Funcionalidad completa

Autor: Eduardo Bascuñán
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

def log_prueba(mensaje):
    """Log de prueba"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] PRUEBA: {mensaje}")

def probar_estructura_pyrevit():
    """Probar la estructura de pyRevit"""
    log_prueba("=== PROBANDO ESTRUCTURA PYREVIT ===")
    
    extension_path = r"C:\Users\56968\AppData\Roaming\pyRevit\Extensions\IaEnRvt.extension"
    
    if not os.path.exists(extension_path):
        log_prueba("❌ Extensión NO instalada en pyRevit")
        return False
    
    log_prueba(f"✅ Extensión encontrada: {extension_path}")
    
    # Verificar archivos críticos
    archivos_criticos = [
        "IaEnRvt.extension",
        "IaEnRvt.tab/Panel Bot IA/Panel Bot IA.panel",
        "IaEnRvt.tab/Panel Bot IA/Bot IA.pushbutton/Bot IA.pushbutton",
        "IaEnRvt.tab/Panel Bot IA/Bot IA.pushbutton/Bot IA.py"
    ]
    
    todos_ok = True
    for archivo in archivos_criticos:
        archivo_path = os.path.join(extension_path, archivo)
        if os.path.exists(archivo_path):
            log_prueba(f"✅ {archivo}")
        else:
            log_prueba(f"❌ {archivo} - NO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def probar_bot_nlp():
    """Probar el bot NLP"""
    log_prueba("=== PROBANDO BOT NLP ===")
    
    # Cambiar al directorio del bot
    bot_dir = r"C:\edbascunan\IA-EN-RVT\backend_ai"
    if not os.path.exists(bot_dir):
        log_prueba("❌ Directorio del bot NO encontrado")
        return False
    
    log_prueba(f"✅ Directorio del bot: {bot_dir}")
    
    # Probar importaciones
    try:
        sys.path.append(bot_dir)
        
        # Verificar archivos del bot
        bot_files = [
            "bot_ia_rvt_inteligente.py",
            "config/bot_config.json"
        ]
        
        for file in bot_files:
            file_path = os.path.join(bot_dir, file)
            if os.path.exists(file_path):
                log_prueba(f"✅ {file}")
            else:
                log_prueba(f"❌ {file} - NO ENCONTRADO")
                return False
        
        # Probar carga del módulo principal
        log_prueba("🔍 Probando carga del bot...")
        result = subprocess.run([
            sys.executable, "-c", 
            "import sys; sys.path.append(r'C:\\edbascunan\\IA-EN-RVT\\backend_ai'); import bot_ia_rvt_inteligente; print('Bot loaded')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            log_prueba("✅ Bot se carga correctamente")
            return True
        else:
            log_prueba(f"❌ Error cargando bot: {result.stderr}")
            return False
            
    except Exception as e:
        log_prueba(f"❌ Error probando bot: {str(e)}")
        return False

def probar_sistema_completo():
    """Probar el sistema completo"""
    log_prueba("=== PROBANDO SISTEMA COMPLETO ===")
    
    # Probar estructura pyRevit
    pyrevit_ok = probar_estructura_pyrevit()
    
    # Probar bot NLP
    bot_ok = probar_bot_nlp()
    
    log_prueba("=== RESUMEN DE PRUEBAS ===")
    log_prueba(f"PyRevit: {'✅ OK' if pyrevit_ok else '❌ FALLO'}")
    log_prueba(f"Bot NLP: {'✅ OK' if bot_ok else '❌ FALLO'}")
    
    if pyrevit_ok and bot_ok:
        log_prueba("🎉 SISTEMA COMPLETO FUNCIONANDO")
        return True
    else:
        log_prueba("❌ SISTEMA TIENE PROBLEMAS")
        return False

def mostrar_instrucciones():
    """Mostrar instrucciones de uso"""
    log_prueba("=== INSTRUCCIONES DE USO ===")
    print("""
🚀 INSTRUCCIONES PARA USAR EL BOT:

1. 📱 EJECUTAR BOT BACKEND:
   cd C:\\edbascunan\\IA-EN-RVT\\backend_ai
   python bot_ia_rvt_inteligente.py

2. 🏗️ USAR EN REVIT:
   • Abrir Revit 2026
   • PYREVIT > Extensions > Reload (si es necesario)
   • Buscar pestaña 'IaEnRvt'
   • Hacer clic en botón '🤖 IA RVT'

3. 💬 COMANDOS DE EJEMPLO:
   • "Crear muro desde 0,0 hasta 5,0 altura 3.5"
   • "Analizar elementos del proyecto"
   • "Mostrar estadísticas del modelo"

4. 🔧 SOLUCIÓN DE PROBLEMAS:
   • Si no aparece el botón: Reinstalar extensión
   • Si bot no responde: Verificar que esté ejecutándose
   • Verificar logs en: C:\\edbascunan\\IA-EN-RVT\\backend_ai\\logs
""")

if __name__ == "__main__":
    print("🔬 IA-EN-RVT 2026 - SCRIPT DE PRUEBA INTEGRAL")
    print("=" * 60)
    
    # Ejecutar pruebas
    sistema_ok = probar_sistema_completo()
    
    # Mostrar instrucciones
    mostrar_instrucciones()
    
    if sistema_ok:
        print("\n🎉 ¡SISTEMA LISTO PARA USAR!")
    else:
        print("\n❌ SISTEMA REQUIERE CORRECCIONES")
    
    print("\nPresiona Enter para salir...")
    input()