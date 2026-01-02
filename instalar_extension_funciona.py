#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instalador de Extensión pyRevit que SÍ Funciona - IA_RVT
======================================================

Este instalador crea la extensión siguiendo exactamente la estructura
que funciona en pyRevit (basado en IA_RVT.extension)

Autor: Eduardo Bascuñán
"""

import os
import sys
import shutil
import platform
from pathlib import Path

class InstaladorExtensionPyRevitFunciona:
    def __init__(self):
        self.sistema = platform.system()
        self.home_dir = os.path.expanduser("~")
        self.proyecto_dir = os.path.dirname(os.path.abspath(__file__))
        self.extension_origen = os.path.join(self.proyecto_dir, "pyrevit_extension_funciona")
        
    def obtener_directorio_pyrevit(self):
        """Obtener directorio de extensiones de pyRevit"""
        if self.sistema == "Windows":
            extensiones_dir = os.path.join(self.home_dir, "AppData", "Roaming", "pyRevit", "Extensions")
        else:
            extensiones_dir = os.path.join(self.home_dir, ".pyRevit", "Extensions")
        
        return extensiones_dir
    
    def crear_directorio_extensions(self, extensiones_dir):
        """Crear directorio de extensiones si no existe"""
        try:
            if not os.path.exists(extensiones_dir):
                os.makedirs(extensiones_dir, exist_ok=True)
                print(f"✅ Directorio creado: {extensiones_dir}")
            else:
                print(f"✅ Directorio encontrado: {extensiones_dir}")
            return True
        except Exception as e:
            print(f"❌ Error creando directorio {extensiones_dir}: {e}")
            return False
    
    def eliminar_extension_anterior(self, extension_destino):
        """Eliminar extensión anterior"""
        try:
            if os.path.exists(extension_destino):
                shutil.rmtree(extension_destino)
                print("🗑️ Extensión anterior eliminada")
            return True
        except Exception as e:
            print(f"⚠️ No se pudo eliminar extensión anterior: {e}")
            return True
    
    def instalar_extension(self):
        """Instalar la extensión"""
        try:
            extensiones_dir = self.obtener_directorio_pyrevit()
            if not self.crear_directorio_extensions(extensiones_dir):
                return False
            
            # Directorio destino de la extensión
            extension_destino = os.path.join(extensiones_dir, "IA_RVT.extension")
            
            # Eliminar extensión anterior
            self.eliminar_extension_anterior(extension_destino)
            
            # Copiar extensión completa
            shutil.copytree(self.extension_origen, extension_destino)
            print(f"✅ Extensión instalada en: {extension_destino}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error instalando extensión: {e}")
            return False
    
    def verificar_instalacion(self):
        """Verificar que la instalación fue correcta"""
        try:
            extensiones_dir = self.obtener_directorio_pyrevit()
            extension_destino = os.path.join(extensiones_dir, "IA_RVT.extension")
            
            # Verificar archivos clave (estructura que funciona)
            archivos_requeridos = [
                os.path.join(extension_destino, "extension.json"),
                os.path.join(extension_destino, "IA_RVT.tab", "IA_RVT.tab"),
                os.path.join(extension_destino, "IA_RVT.tab", "Executor.panel", "Executor.panel"),
                os.path.join(extension_destino, "IA_RVT.tab", "Executor.panel", "BotNLP.pushbutton", "BotNLP.pushbutton"),
                os.path.join(extension_destino, "IA_RVT.tab", "Executor.panel", "BotNLP.pushbutton", "bundle.yaml"),
                os.path.join(extension_destino, "IA_RVT.tab", "Executor.panel", "BotNLP.pushbutton", "script.py")
            ]
            
            archivos_faltantes = []
            for archivo in archivos_requeridos:
                if os.path.exists(archivo):
                    print(f"✅ Archivo verificado: {os.path.basename(archivo)}")
                else:
                    print(f"❌ Archivo faltante: {os.path.basename(archivo)}")
                    archivos_faltantes.append(archivo)
            
            if archivos_faltantes:
                print(f"⚠️ Archivos faltantes: {len(archivos_faltantes)}")
                return False
            
            print("✅ Todos los archivos verificados correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error verificando instalación: {e}")
            return False
    
    def mostrar_instrucciones(self):
        """Mostrar instrucciones finales al usuario"""
        print("\n" + "="*60)
        print("🎉 INSTALACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        print("\n📋 PASOS PARA USAR EN REVIT:")
        print("1. Abre Autodesk Revit")
        print("2. Ve a Add-Ins → External Tools")
        print("3. Debería aparecer la pestaña 'IA_RVT'")
        print("4. En el panel 'Executor', haz clic en 'Bot IA NLP'")
        print("5. El bot procesará comandos en lenguaje natural")
        
        print("\n🔧 CONFIGURACIÓN ADICIONAL:")
        print("• Si no aparece la extensión, reinicia Revit completamente")
        print("• Si sigue sin aparecer, verifica que pyRevit esté instalado")
        print("• Ejecuta 'pyrevit extensions reload' en la consola de pyRevit")
        
        print("\n🤖 COMANDOS NLP DISPONIBLES EN EL BOT:")
        print("• 'crear muro' - Crear nuevo muro")
        print("• 'analizar proyecto' - Analizar elementos")
        print("• 'contar muros' - Contar muros existentes")
        print("• 'medir elementos' - Medir todos los elementos")
        print("• 'revisar modelo' - Revisar estado del modelo")
        print("• 'cuantificar' - Cuantificar elementos BIM")
        print("• 'estadísticas' - Ver estadísticas del proyecto")
        print("• 'ayuda' - Mostrar todos los comandos")
        
        print(f"\n📁 UBICACIÓN DE LA EXTENSIÓN:")
        print(f"   {self.obtener_directorio_pyrevit()}")
        
        print("\n✅ EXTENSIÓN LISTA PARA USAR EN REVIT")
        print("   Esta extensión sigue la estructura EXACTA que funciona")
    
    def ejecutar(self):
        """Ejecutar instalación completa"""
        print("🚀 INSTALADOR DE EXTENSIÓN PYREVIT QUE SÍ FUNCIONA")
        print("="*60)
        print("Basado en IA_RVT.extension que aparece en Revit")
        
        print("\n🔍 Verificando archivos de origen...")
        if not os.path.exists(self.extension_origen):
            print(f"❌ No se encuentra la extensión en: {self.extension_origen}")
            return False
        
        print("✅ Archivos de origen encontrados")
        
        print("\n📦 Instalando extensión...")
        if not self.instalar_extension():
            return False
        
        print("\n🔍 Verificando instalación...")
        if not self.verificar_instalacion():
            print("\n❌ LA VERIFICACIÓN FALLÓ")
            print("Algunos archivos no se instalaron correctamente")
            return False
        
        self.mostrar_instrucciones()
        return True

def main():
    """Función principal"""
    try:
        instalador = InstaladorExtensionPyRevitFunciona()
        exito = instalador.ejecutar()
        
        if exito:
            print("\n🎉 ¡INSTALACIÓN COMPLETADA CON ÉXITO!")
            print("La extensión del bot NLP está lista para usar en Revit.")
            print("Esta extensión sigue la estructura EXACTA que funciona.")
            print("\n💡 Próximo paso: Abre Revit y verifica que aparezca la pestaña 'IA_RVT'")
        else:
            print("\n❌ LA INSTALACIÓN FALLÓ")
            print("Revisa los errores anteriores e intenta nuevamente.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Instalación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor, contacta al soporte técnico.")

if __name__ == "__main__":
    main()