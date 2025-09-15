# app.py - Simple Azure entry point
"""
Simplified Azure App Service entry point for Alquería RAG System
"""

import os
import sys

# Set environment variables for Azure
os.environ.setdefault("PYTHONUNBUFFERED", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

try:
    # Import the FastAPI app
    print("Attempting to import main app...")
    from main import app
    print("Successfully imported main app - FULL RAG SYSTEM ACTIVE")
except Exception as e:
    print(f"Error importing main: {e}")
    import traceback
    traceback.print_exc()
    # Create a minimal FastAPI app as fallback
    from fastapi import FastAPI, HTTPException
    app = FastAPI(title="Alquería RAG Backend - Minimal")
    
    @app.get("/")
    async def health_check():
        return {"status": "ok", "message": "Alquería RAG Backend is running (minimal mode)"}
    
    @app.get("/debug")
    async def debug_info():
        import os
        debug_data = {
            "environment_variables": {
                "AZURE_OPENAI_API_KEY": "SET" if os.getenv("AZURE_OPENAI_API_KEY") else "NOT SET",
                "AZURE_SEARCH_SERVICE": os.getenv("AZURE_SEARCH_SERVICE", "NOT SET"),
                "AZURE_SEARCH_KEY": "SET" if os.getenv("AZURE_SEARCH_KEY") else "NOT SET",
                "AZURE_SEARCH_INDEX": os.getenv("AZURE_SEARCH_INDEX", "NOT SET")
            },
            "config_file_exists": os.path.exists("config/alqueria_config.json"),
            "current_directory": os.getcwd(),
            "files_in_root": os.listdir(".") if os.path.exists(".") else []
        }
        return debug_data
    
    @app.post("/api/auth/login")
    async def login(credentials: dict):
        # Simple credential check
        demo_users = {
            "ejecutivo@alqueria.com.co": "Alqueria2024!",
            "marketing@alqueria.com.co": "Marketing2024!",
            "insights@alqueria.com.co": "Insights2024!",
            "juan@genius-labs.com.co": "GeniusLabs2024!"
        }
        
        username = credentials.get("username")
        password = credentials.get("password")
        
        if username in demo_users and demo_users[username] == password:
            return {"access_token": "demo_token", "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

if __name__ == "__main__":
    import uvicorn
    # Azure uses PORT environment variable, default to 8000 for local
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")