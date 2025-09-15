@echo off
echo ========================================
echo  TIGO RAG ENHANCED SYSTEM - SETUP
echo  Academic-Grade Persona System
echo ========================================
echo.

echo Checking if Claude-Code environment is active...
if "%VIRTUAL_ENV%"=="" (
    echo ERROR: No virtual environment detected!
    echo Please run: ..\activate_claude_code.bat first
    pause
    exit /b 1
)

if not "%VIRTUAL_ENV%"=="C:\Users\jorge\proyectos_python\Claude-Code" (
    echo WARNING: Different environment active: %VIRTUAL_ENV%
    echo Expected: C:\Users\jorge\proyectos_python\Claude-Code
    echo.
    echo Continue anyway? (y/n)
    set /p choice=
    if /i not "%choice%"=="y" exit /b 1
)

echo.
echo ✅ Claude-Code environment detected
echo.
echo Installing enhanced dependencies...
echo ========================================

REM Core FastAPI dependencies
echo [1/10] Installing FastAPI and server...
pip install fastapi>=0.104.1
pip install uvicorn[standard]>=0.24.0
pip install python-multipart>=0.0.6

REM Fixed compatibility versions
echo [2/10] Installing compatible core packages...
pip install "typing-extensions>=4.9.0"
pip install "pydantic>=2.5.0"

REM Scientific computing
echo [3/10] Installing scientific packages...
pip install "numpy>=1.24.3"
pip install "pandas>=2.1.3"
pip install "scikit-learn>=1.3.0"

REM HTTP and utilities
echo [4/10] Installing utilities...
pip install "requests>=2.31.0"
pip install "python-json-logger>=2.0.7"
pip install "python-dotenv>=1.0.0"

REM Image processing
echo [5/10] Installing image processing...
pip install "Pillow>=10.1.0"

REM Optional: Additional packages for enhanced functionality
echo [6/10] Installing enhanced functionality packages...
pip install "matplotlib>=3.7.0" --quiet
pip install "seaborn>=0.12.0" --quiet

echo [7/10] Verifying critical imports...
python -c "from typing_extensions import TypeIs; print('✅ TypeIs import: OK')" || (echo "❌ TypeIs import failed" && pause && exit /b 1)
python -c "import pydantic; print('✅ Pydantic version:', pydantic.__version__)" || (echo "❌ Pydantic import failed" && pause && exit /b 1)
python -c "import fastapi; print('✅ FastAPI version:', fastapi.__version__)" || (echo "❌ FastAPI import failed" && pause && exit /b 1)
python -c "import numpy; print('✅ NumPy version:', numpy.__version__)" || (echo "❌ NumPy import failed" && pause && exit /b 1)
python -c "import pandas; print('✅ Pandas version:', pandas.__version__)" || (echo "❌ Pandas import failed" && pause && exit /b 1)

echo [8/10] Testing persona system imports...
python -c "from personas.persona_characteristics import EthicalPersonaGenerator; print('✅ Persona Generator: OK')" || (echo "❌ Persona Generator import failed" && pause && exit /b 1)
python -c "from personas.temperature_optimization import AdvancedTemperatureController; print('✅ Temperature Optimization: OK')" || (echo "❌ Temperature Optimization import failed" && pause && exit /b 1)

echo [9/10] Testing main application...
python -c "from main import app; print('✅ Main application: OK')" || (echo "❌ Main application import failed" && pause && exit /b 1)

echo [10/10] Final system check...
python -c "
import sys
print('Python version:', sys.version)
print('Virtual environment:', sys.prefix)
print('✅ All systems ready!')
"

echo.
echo ========================================
echo   🎉 SETUP COMPLETED SUCCESSFULLY! 🎉
echo ========================================
echo.
echo Enhanced Persona System Features:
echo ✅ Context-Rich Prompting (1-2hr interviews)
echo ✅ Temperature Optimization (hierarchical sampling)  
echo ✅ Implicit Demographics (stereotype-free)
echo ✅ Temporal Context (Honduras 2024 events)
echo ✅ Staged Validation (3 academic levels)
echo.
echo To start the server:
echo   python main.py
echo.
echo To view documentation:
echo   http://localhost:8000/docs
echo.
echo Advanced endpoints:
echo   /api/persona-enhanced-generate
echo   /api/persona-enhanced-chat
echo   /api/persona-study-validation
echo   /api/persona-generate-transcripts
echo.
pause