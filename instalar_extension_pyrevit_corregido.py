#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instalador Corregido de Extensión pyRevit - IaEnRvt
==================================================

Versión mejorada que maneja problemas de acceso a archivos y permisos
e instala la extensión del bot NLP de manera robusta.

Autor: Eduardo Bascuñán
"""

import os
import sys
import shutil
import platform
import time
import tempfile
from pathlib import Path
import stat

class InstaladorExtensionPyRevitRobusto:
    def __init__(self):
        self.sistema = platform.system()
        self.home_dir = os.path.expanduser("~")
        self.proyecto_dir = os.path.dirname(os.path.abspath(__file__))
        self.extension_origen = os.path.join(self.proyecto_dir, "pyrevit_extension_simple")
        self.bot_origen = os.path.join(self.proyecto_dir, "bot_nlp_funcional.py")
        
    def remover_archivo_solo_lectura(self, ruta):
        """Remover atributo de solo lectura y eliminar archivo"""
        try:
            if os.path.exists(ruta):
                # Cambiar permisos si es necesario
                if os.name == 'nt':  # Windows
                    os.chmod(ruta, stat.S_IWRITE)
                else:
                    os.chmod(ruta, 0o755)
                return True
        except Exception as e:
            print(f"⚠️ No se pudo cambiar permisos de {ruta}: {e}")
        return False
    
    def esperar_y_reintentar(self, funcion, max_intentos=3, delay=1):
        """Reintentar función con delays para manejar archivos bloqueados"""
        for intento in range(max_intentos):
            try:
                return funcion()
            except Exception as e:
                if "WinError 32" in str(e) or "being used by another process" in str(e):
                    print(f"⚠️ Intento {intento + 1}: Archivo en uso, esperando {delay} segundos...")
                    time.sleep(delay)
                    delay *= 2  # Aumentar delay exponencialmente
                else:
                    print(f"❌ Error: {e}")
                    raise e
        raise Exception(f"Fallo después de {max_intentos} intentos")
    
    def obtener_directorio_pyrevit(self):
        """Obtener directorio de extensiones de pyRevit según el sistema operativo"""
        if self.sistema == "Windows":
            # Windows: buscar en AppData de pyRevit
            posibles_rutas = [
                os.path.join(self.home_dir, "AppData", "Roaming", "pyRevit", "Extensions"),
                os.path.join(self.home_dir, "Documents", "pyRevit", "Extensions"),
                os.path.join("C:\\Program Files", "pyRevit", "Extensions"),
                os.path.join(self.home_dir, "pyRevit", "Extensions")
            ]
        else:
            # Linux/Mac
            posibles_rutas = [
                os.path.join(self.home_dir, ".pyRevit", "Extensions"),
                os.path.join("/usr/local", "pyRevit", "Extensions")
            ]
        
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                return ruta
        
        # Si no existe, crear en AppData
        if self.sistema == "Windows":
            extensiones_dir = os.path.join(self.home_dir, "AppData", "Roaming", "pyRevit", "Extensions")
        else:
            extensiones_dir = os.path.join(self.home_dir, ".pyRevit", "Extensions")
        
        return extensiones_dir
    
    def crear_directorio_extensions(self, extensiones_dir):
        """Crear directorio de extensiones si no existe"""
        def crear_dir():
            if not os.path.exists(extensiones_dir):
                os.makedirs(extensiones_dir, exist_ok=True)
                print(f"✅ Directorio creado: {extensiones_dir}")
            else:
                print(f"✅ Directorio encontrado: {extensiones_dir}")
            return True
        
        return self.esperar_y_reintentar(crear_dir)
    
    def eliminar_extension_anterior(self, extension_destino):
        """Eliminar extensión anterior con manejo de errores robusto"""
        def eliminar():
            if os.path.exists(extension_destino):
                # Eliminar directorio completo
                shutil.rmtree(extension_destino, onerror=self.eliminar_archivo_con_permisos)
                print("🗑️ Extensión anterior eliminada")
            return True
        
        return self.esperar_y_reintentar(eliminar)
    
    def eliminar_archivo_con_permisos(self, func, path, exc_info):
        """Manejar errores de permisos al eliminar archivos"""
        try:
            print(f"⚠️ Cambiando permisos de {path}")
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception as e:
            print(f"⚠️ No se pudo eliminar {path}: {e}")
    
    def copiar_con_reintentos(self, origen, destino):
        """Copiar archivo/directorio con reintentos"""
        def copiar():
            if os.path.isdir(origen):
                shutil.copytree(origen, destino)
            else:
                shutil.copy2(origen, destino)
            return True
        
        return self.esperar_y_reintentar(copiar)
    
    def instalar_extension(self):
        """Instalar la extensión copiando archivos con manejo robusto"""
        try:
            extensiones_dir = self.obtener_directorio_pyrevit()
            if not self.crear_directorio_extensions(extensiones_dir):
                return False
            
            # Directorio destino de la extensión
            extension_destino = os.path.join(extensiones_dir, "IaEnRvt.extension")
            
            # Eliminar extensión anterior si existe
            self.eliminar_extension_anterior(extension_destino)
            
            # Copiar extensión completa
            print(f"📋 Copiando extensión de {self.extension_origen} a {extension_destino}")
            self.copiar_con_reintentos(self.extension_origen, extension_destino)
            print(f"✅ Extensión copiada a: {extension_destino}")
            
            # Copiar bot NLP al directorio del proyecto
            bot_destino = os.path.join(self.proyecto_dir, "bot_nlp_funcional.py")
            if os.path.exists(self.bot_origen):
                print(f"📋 Copiando bot NLP de {self.bot_origen} a {bot_destino}")
                self.copiar_con_reintentos(self.bot_origen, bot_destino)
                print(f"✅ Bot NLP copiado a: {bot_destino}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error instalando extensión: {e}")
            return False
    
    def verificar_instalacion(self):
        """Verificar que la instalación fue correcta"""
        try:
            extensiones_dir = self.obtener_directorio_pyrevit()
            extension_destino = os.path.join(extensiones_dir, "IaEnRvt.extension")
            
            # Verificar archivos clave
            archivos_requeridos = [
                os.path.join(extension_destino, "IaEnRvt.extension"),
                os.path.join(extension_destino, "IaEnRvt.tab", "IaEnRvt.tab"),
                os.path.join(extension_destino, "IaEnRvt.tab", "Bot.panel", "Bot.panel"),
                os.path.join(extension_destino, "IaEnRvt.tab", "Bot.panel", "Script.pushbutton", "Script.pushbutton"),
                os.path.join(extension_destino, "IaEnRvt.tab", "Bot.panel", "Script.pushbutton", "Script.py"),
                os.path.join(self.proyecto_dir, "bot_nlp_funcional.py")
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
        print("3. Debería aparecer 'IaEnRvt' en la pestaña")
        print("4. Haz clic en 'Bot IA NLP' para ejecutar el bot")
        print("5. El bot procesará comandos en lenguaje natural")
        
        print("\n🔧 CONFIGURACIÓN ADICIONAL:")
        print("• Si no aparece la extensión, reinicia Revit completamente")
        print("• Si sigue sin aparecer, verifica que pyRevit esté instalado")
        print("• Ejecuta 'pyrevit extensions reload' en la consola de pyRevit")
        print("• Cierra todos los procesos de Revit antes de instalar")
        
        print("\n🤖 COMANDOS DISPONIBLES EN EL BOT:")
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
        print("\n💡 CONSEJO: Asegúrate de que Revit esté CERRADO durante la instalación")
    
    def ejecutar(self):
        """Ejecutar instalación completa"""
        print("🚀 INSTALADOR ROBUSTO DE EXTENSIÓN PYREVIT - IaEnRvt")
        print("="*60)
        
        print("\n🔍 Verificando archivos de origen...")
        if not os.path.exists(self.extension_origen):
            print(f"❌ No se encuentra la extensión en: {self.extension_origen}")
            return False
        
        if not os.path.exists(self.bot_origen):
            print(f"❌ No se encuentra el bot en: {self.bot_origen}")
            return False
        
        print("✅ Archivos de origen encontrados")
        
        print("\n💡 IMPORTANTE: Asegúrate de que Revit esté CERRADO durante la instalación")
        print("📋 Si Revit está abierto, ciérralo antes de continuar...")
        
        print("\n📦 Instalando extensión...")
        if not self.instalar_extension():
            print("\n❌ LA INSTALACIÓN FALLÓ")
            print("💡 Posibles soluciones:")
            print("   • Cierra todos los procesos de Revit")
            print("   • Reinicia el computador")
            print("   • Ejecuta como administrador")
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
        instalador = InstaladorExtensionPyRevitRobusto()
        exito = instalador.ejecutar()
        
        if exito:
            print("\n🎉 ¡INSTALACIÓN COMPLETADA CON ÉXITO!")
            print("La extensión del bot NLP está lista para usar en Revit.")
            print("\n💡 Próximo paso: Abre Revit y verifica que aparezca la pestaña 'IaEnRvt'")
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