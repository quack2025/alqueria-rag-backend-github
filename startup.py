# startup.py - Azure App Service entry point
"""
Azure App Service startup script for Tigo RAG System
"""

import os
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set environment variables for Azure
os.environ.setdefault("PYTHONUNBUFFERED", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# Import the FastAPI app (don't run it here, let Azure handle it)
from main import app

# For Azure App Service, we expose the app object directly
# Azure will handle the server startup automatically