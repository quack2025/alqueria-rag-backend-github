@echo off
echo Tigo RAG System - Setup
echo =======================

echo Instalando dependencias criticas...
pip install scikit-learn==1.3.0
pip install fastapi==0.104.1  
pip install uvicorn[standard]==0.24.0
pip install python-multipart==0.0.6
pip install pydantic>=2.5.0
pip install requests==2.31.0
pip install numpy==1.24.3
pip install pandas==2.1.3
pip install Pillow==10.1.0
pip install python-json-logger==2.0.7
pip install python-dotenv==1.0.0
pip install typing-extensions>=4.9.0

echo.
echo ✅ Dependencias instaladas
echo.
echo Para iniciar el servidor ejecuta:
echo   python main.py
echo.
echo O usa el instalador Python:
echo   python install_dependencies.py
echo.
pause