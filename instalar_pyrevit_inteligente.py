#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IA-EN-RVT 2026 - Instalador PYREVIT Inteligente
================================================

Instala la extensión IA-EN-RVT con bot inteligente en PYREVIT
Asegura que el botón "🤖 IA RVT" aparezca correctamente
Autor: Eduardo Bascuñán
"""

import os
import shutil
import sys
from pathlib import Path

def encontrar_pyrevit_path():
    """Encontrar ruta de instalación de PYREVIT"""
    posibles_paths = [
        r"C:\Users\%s\AppData\Roaming\pyRevit\Extensions" % os.getenv('USERNAME', ''),
        r"C:\ProgramData\pyRevit\Extensions",
        r"C:\pyRevit\Extensions"
    ]
    
    for path in posibles_paths:
        if os.path.exists(path):
            return path
    
    return None

def instalar_extension_inteligente():
    """Instalar extensión IA-EN-RVT inteligente en PYREVIT"""
    print("🏗️ IA-EN-RVT 2026 - Instalador PYREVIT Inteligente")
    print("=" * 60)
    
    # Ruta de la extensión
    extension_source = r"C:\edbascunan\IA-EN-RVT\pyrevit_extension"
    pyrevit_extensions_path = encontrar_pyrevit_path()
    
    if not pyrevit_extensions_path:
        print("❌ No se encontró PYREVIT instalado")
        print("📥 Descarga e instala PYREVIT desde: https://github.com/eirannejad/pyRevit/releases")
        return False
    
    print(f"📁 PYREVIT Extensions Path: {pyrevit_extensions_path}")
    
    # Ruta de destino
    extension_dest = os.path.join(pyrevit_extensions_path, "IaEnRvt.extension")
    
    try:
        # Limpiar instalación anterior si existe
        if os.path.exists(extension_dest):
            print("🧹 Limpiando instalación anterior...")
            shutil.rmtree(extension_dest)
        
        # Crear directorio si no existe
        os.makedirs(extension_dest, exist_ok=True)
        
        # Verificar archivos fuente
        if not os.path.exists(extension_source):
            print(f"❌ No se encontró la carpeta de extensión: {extension_source}")
            return False
        
        print(f"📋 Instalando extensión desde: {extension_source}")
        print(f"📋 Hacia: {extension_dest}")
        
        # Copiar archivos
        archivos_copiados = 0
        for root, dirs, files in os.walk(extension_source):
            for file in files:
                src = os.path.join(root, file)
                rel_path = os.path.relpath(src, extension_source)
                dest = os.path.join(extension_dest, rel_path)
                
                # Crear directorio si no existe
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                
                # Copiar archivo
                shutil.copy2(src, dest)
                print(f"  ✅ {rel_path}")
                archivos_copiados += 1
        
        print(f"\n✅ Extensión IA-EN-RVT instalada correctamente")
        print(f"📊 Archivos copiados: {archivos_copiados}")
        print(f"🎯 Botón disponible: '🤖 IA RVT' en pestaña 'IaEnRvt'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error instalando extensión: {str(e)}")
        return False

def verificar_instalacion_inteligente():
    """Verificar que la instalación inteligente fue exitosa"""
    print("\n🔍 Verificando instalación inteligente...")
    
    pyrevit_extensions_path = encontrar_pyrevit_path()
    if not pyrevit_extensions_path:
        return False
    
    extension_path = os.path.join(pyrevit_extensions_path, "IaEnRvt.extension")
    
    if os.path.exists(extension_path):
        print("✅ Extensión encontrada")
        
        # Verificar archivos importantes
        archivos_importantes = [
            "IaEnRvt.extension",
            "IaEnRvt.tab/Panel 1.stack/IA RVT.pushbutton/IA RVT.py",
            "IaEnRvt.tab/Panel 1.stack/IA RVT.pushbutton/config.yaml"
        ]
        
        todos_presentes = True
        for archivo in archivos_importantes:
            archivo_path = os.path.join(extension_path, archivo)
            if os.path.exists(archivo_path):
                print(f"  ✅ {archivo}")
            else:
                print(f"  ❌ {archivo}")
                todos_presentes = False
        
        if todos_presentes:
            print("\n🎉 INSTALACIÓN EXITOSA")
            print("🤖 El botón '🤖 IA RVT' aparecerá en la pestaña 'IaEnRvt'")
            print("🧠 Bot inteligente con procesamiento de lenguaje natural")
            print("📚 Sistema de aprendizaje continuo activo")
            return True
        else:
            print("\n❌ Instalación incompleta")
            return False
    else:
        print("❌ Extensión no encontrada")
        return False

def mostrar_instrucciones_inteligentes():
    """Mostrar instrucciones de uso del sistema inteligente"""
    print("\n🚀 INSTRUCCIONES DE USO - SISTEMA INTELIGENTE:")
    print("=" * 60)
    print()
    print("1. 📱 EJECUTAR BOT INTELIGENTE:")
    print("   cd /edbascunan/IA-EN-RVT/backend_ai")
    print("   python bot_ia_rvt_inteligente.py")
    print()
    print("2. 🏗️ CONFIGURAR REVIT:")
    print("   • Abrir Revit 2026")
    print("   • PYREVIT > Extensions > Reload")
    print("   • Buscar pestaña 'IaEnRvt'")
    print("   • Verificar botón '🤖 IA RVT'")
    print()
    print("3. 💬 USAR LENGUAJE NATURAL EN TELEGRAM:")
    print("   • 'Crear muro desde 0,0 hasta 5,0 altura 3.5'")
    print("   • 'Necesito un muro de 6 metros'")
    print("   • 'Analizar el modelo completo'")
    print("   • '¿Cuántos muros hay?'")
    print("   • 'Mostrar estadísticas del proyecto'")
    print()
    print("4. 🧠 SISTEMA INTELIGENTE:")
    print("   • Procesa instrucciones en lenguaje natural")
    print("   • Aprende de cada interacción")
    print("   • Sin ejemplos fijos - todo es dinámico")
    print("   • Ejecución automática en Revit")
    print()
    print("5. ✅ VERIFICAR FUNCIONAMIENTO:")
    print("   • Botón '🤖 IA RVT' visible en Revit")
    print("   • Comandos procesados por IA")
    print("   • Elementos creados automáticamente")
    print("   • Sin errores de esquema")

def mostrar_resolucion_problemas():
    """Mostrar soluciones a problemas comunes"""
    print("\n🔧 SOLUCIÓN DE PROBLEMAS:")
    print("=" * 60)
    print()
    print("❓ *PROBLEMA: No aparece el botón '🤖 IA RVT'*")
    print("✅ *SOLUCIÓN:*")
    print("   1. Reiniciar Revit completamente")
    print("   2. PYREVIT > Extensions > Reload")
    print("   3. Verificar que PYREVIT esté instalado")
    print("   4. Ejecutar instalador nuevamente")
    print()
    print("❓ *PROBLEMA: Error de esquema JSON*")
    print("✅ *SOLUCIÓN:*")
    print("   1. Usar bot_ia_rvt_inteligente.py (esquema corregido)")
    print("   2. Verificar que el comando se guarda correctamente")
    print("   3. Reiniciar bot y Revit")
    print()
    print("❓ *PROBLEMA: Bot no entiende comandos*")
    print("✅ *SOLUCIÓN:*")
    print("   1. Usar lenguaje natural más específico")
    print("   2. Incluir coordenadas cuando sea necesario")
    print("   3. Usar palabras clave como 'crear', 'analizar'")
    print()
    print("❓ *PROBLEMA: PYREVIT no encontrado*")
    print("✅ *SOLUCIÓN:*")
    print("   1. Descargar desde: github.com/eirannejad/pyRevit")
    print("   2. Instalar en el sistema")
    print("   3. Reiniciar el sistema")
    print("   4. Ejecutar instalador nuevamente")

if __name__ == "__main__":
    if instalar_extension_inteligente():
        if verificar_instalacion_inteligente():
            mostrar_instrucciones_inteligentes()
            mostrar_resolucion_problemas()
        else:
            print("❌ Verificación falló")
    else:
        print("❌ Instalación falló")