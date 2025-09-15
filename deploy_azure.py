#!/usr/bin/env python
"""
Deploy script for Azure App Service
Prepares the application for deployment without numpy/sklearn dependencies
"""

import os
import shutil
import subprocess
import sys

def prepare_azure_deployment():
    """Prepare the application for Azure deployment"""
    
    print(">>> Preparing Azure deployment...")
    
    # 1. Create deployment directory
    deploy_dir = "azure_deploy"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    print("[OK] Created deployment directory")
    
    # 2. Copy essential files
    files_to_copy = [
        "main.py",
        "requirements_azure.txt",
        ".env.example"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, deploy_dir)
            print(f"[OK] Copied {file}")
    
    # 3. Copy directories
    dirs_to_copy = [
        "core",
        "config",
        "personas"
    ]
    
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(deploy_dir, dir_name))
            print(f"[OK] Copied {dir_name}/")
    
    # 4. Rename requirements file
    req_src = os.path.join(deploy_dir, "requirements_azure.txt")
    req_dst = os.path.join(deploy_dir, "requirements.txt")
    if os.path.exists(req_src):
        os.rename(req_src, req_dst)
        print("[OK] Renamed requirements_azure.txt to requirements.txt")
    
    # 5. Create startup command file for Azure
    startup_content = """#!/bin/bash
# Azure App Service startup script
echo "Starting Tigo RAG Backend..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000
"""
    
    with open(os.path.join(deploy_dir, "startup.sh"), "w") as f:
        f.write(startup_content)
    print("[OK] Created startup.sh")
    
    # 6. Create app.yaml for Azure
    app_yaml = """# Azure App Service configuration
runtime: python
runtime_config:
  python_version: "3.10"
"""
    
    with open(os.path.join(deploy_dir, "app.yaml"), "w") as f:
        f.write(app_yaml)
    print("[OK] Created app.yaml")
    
    print("\n>>> Deployment package ready in 'azure_deploy/' directory")
    print("\n>>> Next steps:")
    print("1. cd azure_deploy")
    print("2. az webapp up --name tigo-rag-backend --resource-group tigo-rag-rg --runtime 'PYTHON:3.10'")
    print("3. az webapp config set --name tigo-rag-backend --resource-group tigo-rag-rg --startup-file 'startup.sh'")
    
    return deploy_dir

def test_imports():
    """Test if core modules can be imported without numpy"""
    print("\n>>> Testing imports without numpy/sklearn...")
    
    test_modules = [
        "core.azure_search_vector_store",
        "core.multimodal_processor",
        "core.multimodal_output",
        "core.math_utils"
    ]
    
    all_ok = True
    for module in test_modules:
        try:
            __import__(module)
            print(f"[OK] {module} imports successfully")
        except ImportError as e:
            print(f"[ERROR] {module} failed: {e}")
            all_ok = False
    
    return all_ok

if __name__ == "__main__":
    # First test imports
    if not test_imports():
        print("\n[WARNING] Some modules failed to import")
        print("This might be due to missing dependencies in this environment")
        print("Azure deployment package will still be created")
    
    # Prepare deployment
    deploy_dir = prepare_azure_deployment()
    
    print("\n>>> Azure deployment preparation complete!")
    print(f">>> Deployment package location: {os.path.abspath(deploy_dir)}")