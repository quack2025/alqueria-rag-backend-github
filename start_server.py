# start_server.py  
"""
Script de inicio para el servidor Tigo RAG con verificación de dependencias
"""

import sys
import os
import subprocess

def check_dependencies():
    """Verificar que las dependencias críticas estén instaladas"""
    critical_packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('requests', 'Requests'),
        ('numpy', 'NumPy'),
        ('sklearn', 'Scikit-learn'),
        ('PIL', 'Pillow')
    ]
    
    missing = []
    
    for package, name in critical_packages:
        try:
            __import__(package)
            print(f"✅ {name} disponible")
        except ImportError:
            print(f"❌ {name} faltante")
            missing.append(package)
    
    return missing

def install_missing_packages(missing):
    """Instalar paquetes faltantes"""
    if not missing:
        return True
    
    print(f"\n🔧 Instalando {len(missing)} paquetes faltantes...")
    
    package_map = {
        'sklearn': 'scikit-learn==1.3.0',
        'PIL': 'Pillow==10.1.0',
        'fastapi': 'fastapi==0.104.1',
        'uvicorn': 'uvicorn[standard]==0.24.0',
        'requests': 'requests==2.31.0',
        'numpy': 'numpy==1.24.3'
    }
    
    for package in missing:
        install_name = package_map.get(package, package)
        try:
            print(f"   📦 Instalando {install_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
            print(f"   ✅ {install_name} instalado")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error instalando {install_name}: {e}")
            return False
    
    return True

def start_server():
    """Iniciar el servidor Tigo RAG"""
    print("\n🚀 Iniciando Tigo RAG Server...")
    print("=" * 50)
    
    try:
        # Verificar que main.py existe
        if not os.path.exists("main.py"):
            print("❌ main.py no encontrado")
            return False
        
        # Importar y ejecutar main
        import main
        print("✅ Servidor iniciado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        return False

def main():
    """Función principal"""
    print("Tigo Honduras RAG System - Iniciador")
    print("=" * 40)
    
    # Verificar dependencias
    print("🔍 Verificando dependencias...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️ Faltan {len(missing)} dependencias críticas")
        install = input("¿Instalar automáticamente? (s/n): ").lower().strip()
        
        if install == 's' or install == 'si' or install == 'y' or install == 'yes':
            if not install_missing_packages(missing):
                print("❌ Error instalando dependencias")
                return 1
        else:
            print("❌ No se pueden continuar sin las dependencias")
            print("   Ejecuta: pip install -r requirements.txt")
            return 1
    
    # Iniciar servidor
    if start_server():
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main())