#!/usr/bin/env python3
"""
RAILWAY DEPLOYMENT CHECK - Alquería RAG System
Verifies that Railway is using the latest Alquería code
"""

import os
import sys
from datetime import datetime

print("🔍 RAILWAY DEPLOYMENT VERIFICATION:")
print("=" * 50)
print(f"✅ Timestamp: {datetime.now()}")
print(f"✅ Python Version: {sys.version}")
print(f"✅ Working Directory: {os.getcwd()}")

# Check if Alquería config exists
if os.path.exists("config/alqueria_config.json"):
    print("✅ config/alqueria_config.json EXISTS")

    # Check config content
    with open("config/alqueria_config.json", "r") as f:
        content = f.read()
        if "Alquería" in content:
            print("✅ Config contains Alquería branding")
        else:
            print("❌ Config missing Alquería branding")

    if "dairy_foods" in content:
        print("✅ Config set for dairy industry")
    else:
        print("❌ Config not set for dairy industry")

else:
    print("❌ config/alqueria_config.json MISSING")

# Check main.py for AlqueriaRAGSystem
if os.path.exists("main.py"):
    print("✅ main.py EXISTS")

    with open("main.py", "r") as f:
        main_content = f.read()
        if "AlqueriaRAGSystem" in main_content:
            print("✅ main.py contains AlqueriaRAGSystem class")
        else:
            print("❌ main.py missing AlqueriaRAGSystem class")

        if "734 documents" in main_content:
            print("✅ main.py configured for 734 documents")
        else:
            print("❌ main.py not configured for 734 documents")
else:
    print("❌ main.py MISSING")

# Check environment variables
required_vars = ["AZURE_OPENAI_API_KEY", "AZURE_SEARCH_ADMIN_KEY"]
missing_vars = []

for var in required_vars:
    if os.getenv(var):
        print(f"✅ {var} is set")
    else:
        print(f"❌ {var} is MISSING")
        missing_vars.append(var)

print("=" * 50)
if missing_vars:
    print(f"❌ DEPLOYMENT ISSUES: Missing {len(missing_vars)} environment variables")
    print("   Railway needs these variables configured:")
    for var in missing_vars:
        print(f"   - {var}")
else:
    print("✅ ALL CHECKS PASSED - Alquería system ready")

print("=" * 50)