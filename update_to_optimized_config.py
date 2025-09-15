#!/usr/bin/env python3
"""
Script para actualizar la configuración de Alpina RAG con system prompts optimizados
"""

import json
import shutil
from datetime import datetime
import os

def backup_original_config():
    """Crear backup del archivo de configuración original"""
    original_file = "config/alpina_config.json"
    backup_file = f"config/alpina_config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    if os.path.exists(original_file):
        shutil.copy2(original_file, backup_file)
        print(f"SUCCESS: Backup creado: {backup_file}")
        return True
    else:
        print(f"ERROR: No se encontro el archivo original: {original_file}")
        return False

def apply_optimized_config():
    """Aplicar la configuración optimizada"""
    optimized_file = "config/alpina_config_optimized.json"
    target_file = "config/alpina_config.json"
    
    if not os.path.exists(optimized_file):
        print(f"ERROR: No se encontro el archivo optimizado: {optimized_file}")
        return False
    
    try:
        # Leer configuración optimizada
        with open(optimized_file, 'r', encoding='utf-8') as f:
            optimized_config = json.load(f)
        
        # Escribir como nueva configuración activa
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(optimized_config, f, indent=2, ensure_ascii=False)
        
        print(f"SUCCESS: Configuracion optimizada aplicada exitosamente")
        return True
        
    except Exception as e:
        print(f"ERROR: Error aplicando configuracion: {e}")
        return False

def verify_configuration():
    """Verificar que la configuración se aplicó correctamente"""
    config_file = "config/alpina_config.json"
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Verificar que tiene los nuevos campos optimizados
        checks = {
            "System prompt mejorado": "ANÁLISIS MULTICAPA" in json.dumps(config),
            "Context chunks aumentados": config["endpoints"]["rag_pure"]["max_context_chunks"] >= 10,
            "Cross-document analysis": config["processing"].get("enable_cross_document_analysis", False),
            "Strategic priorities": "strategic_priorities" in config.get("unilever_context", {}),
            "Analysis frameworks": "analysis_frameworks" in config
        }
        
        print("\nVerificacion de configuracion:")
        print("=" * 40)
        
        all_passed = True
        for check, passed in checks.items():
            status = "SUCCESS" if passed else "ERROR"
            print(f"{status}: {check} - {'Si' if passed else 'No'}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"ERROR: Error verificando configuracion: {e}")
        return False

def main():
    """Proceso principal de actualización"""
    print("ACTUALIZACION DE CONFIGURACION ALPINA RAG")
    print("=" * 50)
    print("Aplicando system prompts optimizados para insights profundos")
    print()
    
    # Paso 1: Backup
    print("1. Creando backup de configuracion original...")
    if not backup_original_config():
        print("WARNING: Continuando sin backup...")
    
    # Paso 2: Aplicar configuración optimizada
    print("\n2. Aplicando configuracion optimizada...")
    if not apply_optimized_config():
        print("ERROR: Fallo en la actualizacion")
        return False
    
    # Paso 3: Verificar
    print("\n3. Verificando configuracion...")
    if verify_configuration():
        print("\nSUCCESS: ACTUALIZACION COMPLETADA EXITOSAMENTE")
        print("\nMEJORAS IMPLEMENTADAS:")
        print("- System prompts con analisis multicapa")
        print("- Analisis cross-documento habilitado")
        print("- Contexto aumentado (10-20 chunks)")
        print("- Frameworks estrategicos integrados")
        print("- Insights profundos y accionables")
        print("\nEl sistema ahora generara insights estrategicos profundos")
        print("en lugar de solo reportar datos.")
    else:
        print("\nWARNING: La configuracion se aplico pero algunas verificaciones fallaron")
    
    return True

if __name__ == "__main__":
    main()