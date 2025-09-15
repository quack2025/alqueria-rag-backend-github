#!/usr/bin/env python3
"""
Script para verificar el estado de las dependencias del sistema Tigo RAG
"""

import sys
import subprocess

def check_package(package_name):
    """Verificar si un paquete está instalado"""
    try:
        __import__(package_name)
        print(f"✅ {package_name}: INSTALADO")
        return True
    except ImportError:
        print(f"❌ {package_name}: NO ENCONTRADO")
        return False

def install_package(package):
    """Instalar paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🔍 Verificando dependencias del sistema Tigo RAG...")
    print("=" * 60)
    
    # Lista de paquetes críticos para el funcionamiento básico
    critical_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("requests", "requests"),
        ("pydantic", "pydantic")
    ]
    
    # Lista de paquetes opcionales (ML y visualización)
    optional_packages = [
        ("numpy", "numpy"),
        ("sklearn", "scikit-learn"),
        ("PIL", "Pillow")
    ]
    
    print("\n📦 DEPENDENCIAS CRÍTICAS:")
    critical_missing = []
    for display_name, import_name in critical_packages:
        if not check_package(import_name):
            critical_missing.append(display_name)
    
    print("\n📊 DEPENDENCIAS OPCIONALES:")
    optional_missing = []
    for display_name, import_name in optional_packages:
        if not check_package(import_name):
            optional_missing.append(display_name)
    
    print("\n" + "=" * 60)
    
    if critical_missing:
        print("❌ DEPENDENCIAS CRÍTICAS FALTANTES:")
        for pkg in critical_missing:
            print(f"   - {pkg}")
        print("\n🔧 Intentando instalar dependencias críticas...")
        
        for pkg in critical_missing:
            print(f"   Instalando {pkg}...")
            if install_package(pkg):
                print(f"   ✅ {pkg} instalado")
            else:
                print(f"   ❌ Error instalando {pkg}")
    else:
        print("✅ TODAS LAS DEPENDENCIAS CRÍTICAS ESTÁN DISPONIBLES")
    
    if optional_missing:
        print(f"\n⚠️  DEPENDENCIAS OPCIONALES FALTANTES: {len(optional_missing)}")
        print("   (El sistema puede funcionar sin estas dependencias)")
        for pkg in optional_missing:
            print(f"   - {pkg}")
    else:
        print("✅ TODAS LAS DEPENDENCIAS OPCIONALES ESTÁN DISPONIBLES")
    
    # Verificar configuración
    print("\n🔧 VERIFICANDO CONFIGURACIÓN...")
    try:
        import json
        with open("config/tigo_config.json", 'r') as f:
            config = json.load(f)
        print("✅ Archivo de configuración encontrado")
        
        # Verificar Azure OpenAI
        if config.get("azure_openai", {}).get("api_key"):
            print("✅ API Key de Azure OpenAI configurada")
        else:
            print("⚠️  API Key de Azure OpenAI no configurada")
            
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
    
    print("\n🚀 SIGUIENTE PASO:")
    if not critical_missing:
        print("   ✅ El sistema puede iniciarse!")
        print("   💻 Ejecuta: python main.py")
        print("   🧪 O prueba: python test_system.py")
    else:
        print("   ❌ Instala las dependencias críticas faltantes primero")
        print("   📝 O ejecuta manualmente: pip install <paquete>")
    
    return len(critical_missing) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)