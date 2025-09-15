# install_dependencies.py
"""
Instalar dependencias para el sistema Tigo RAG
"""

import subprocess
import sys
import os

def install_package(package):
    """Instalar un paquete de Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🔧 Instalando dependencias para Tigo RAG System...")
    print("=" * 50)
    
    # Lista de paquetes críticos
    packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0", 
        "python-multipart==0.0.6",
        "pydantic==2.5.0",
        "requests==2.31.0",
        "numpy==1.24.3",
        "scikit-learn==1.3.0",
        "Pillow==10.1.0",
        "python-json-logger==2.0.7",
        "python-dotenv==1.0.0",
        "typing-extensions==4.8.0"
    ]
    
    installed = 0
    failed = []
    
    for package in packages:
        print(f"📦 Instalando {package.split('==')[0]}...")
        if install_package(package):
            print(f"   ✅ Instalado: {package}")
            installed += 1
        else:
            print(f"   ❌ Error: {package}")
            failed.append(package)
    
    print(f"\n📊 Resultado:")
    print(f"   ✅ Instalados: {installed}/{len(packages)}")
    
    if failed:
        print(f"   ❌ Fallaron: {len(failed)}")
        for pkg in failed:
            print(f"      - {pkg}")
        return False
    else:
        print(f"   🎉 Todas las dependencias instaladas correctamente!")
        return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 Ya puedes ejecutar: python main.py")
    else:
        print("\n⚠️ Algunas dependencias fallaron. Intenta instalar manualmente:")
        print("   pip install -r requirements.txt")
    
    sys.exit(0 if success else 1)