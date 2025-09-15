# migrate_vectors.py
"""
Migrar vectores existentes al nuevo sistema Tigo RAG
Evita re-vectorización y costos innecesarios
"""

import json
import os
from typing import Dict, Any, List
from datetime import datetime

def migrate_from_json(source_path: str, target_path: str = "data/tigo_vector_store.json"):
    """
    Migrar desde archivo JSON existente
    """
    try:
        print(f"🔄 Migrando vectores desde: {source_path}")
        
        with open(source_path, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
        
        # Crear estructura compatible
        migrated_data = {
            "documents": {},
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "migrated_from": source_path,
                "client": "tigo_honduras",
                "total_documents": 0
            }
        }
        
        # Convertir documentos al nuevo formato
        documents = source_data.get("documents", {})
        
        for doc_id, doc_data in documents.items():
            migrated_doc = {
                "id": doc_id,
                "content": doc_data.get("content", ""),
                "embedding": doc_data.get("embedding", []),
                "metadata": {
                    "client": "tigo_honduras",
                    "document_name": doc_data.get("metadata", {}).get("document_name", "Unknown"),
                    "study_type": doc_data.get("metadata", {}).get("study_type", "general_research"),
                    "year": doc_data.get("metadata", {}).get("year", 2024),
                    "section_type": doc_data.get("metadata", {}).get("section_type", "content"),
                    "content_type": "text",
                    "processing_date": datetime.now().isoformat(),
                    **doc_data.get("metadata", {})
                },
                "created_at": doc_data.get("created_at", datetime.now().isoformat())
            }
            
            migrated_data["documents"][doc_id] = migrated_doc
        
        migrated_data["metadata"]["total_documents"] = len(migrated_data["documents"])
        
        # Guardar archivo migrado
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(migrated_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Migración completada:")
        print(f"   📄 Documentos migrados: {len(migrated_data['documents'])}")
        print(f"   📁 Archivo destino: {target_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        return False

def migrate_from_astra_export(astra_export_path: str, target_path: str = "data/tigo_vector_store.json"):
    """
    Migrar desde export de Astra DB
    """
    try:
        print(f"🔄 Migrando desde Astra DB export: {astra_export_path}")
        
        with open(astra_export_path, 'r', encoding='utf-8') as f:
            astra_data = json.load(f)
        
        migrated_data = {
            "documents": {},
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "migrated_from": astra_export_path,
                "source_type": "astra_db",
                "client": "tigo_honduras",
                "total_documents": 0
            }
        }
        
        # Procesar documentos de Astra
        for item in astra_data:
            doc_id = item.get("_id", item.get("id", f"doc_{len(migrated_data['documents'])}"))
            
            migrated_doc = {
                "id": doc_id,
                "content": item.get("content", item.get("text", "")),
                "embedding": item.get("$vector", item.get("embedding", [])),
                "metadata": {
                    "client": "tigo_honduras",
                    "document_name": item.get("document_name", item.get("filename", "Unknown")),
                    "study_type": item.get("study_type", "general_research"),
                    "year": item.get("year", 2024),
                    "section_type": item.get("section_type", "content"),
                    "content_type": "text",
                    "processing_date": datetime.now().isoformat(),
                    **{k: v for k, v in item.items() if k not in ["_id", "id", "content", "text", "$vector", "embedding"]}
                },
                "created_at": item.get("created_at", datetime.now().isoformat())
            }
            
            migrated_data["documents"][doc_id] = migrated_doc
        
        migrated_data["metadata"]["total_documents"] = len(migrated_data["documents"])
        
        # Guardar
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(migrated_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Migración desde Astra completada:")
        print(f"   📄 Documentos: {len(migrated_data['documents'])}")
        print(f"   📁 Archivo: {target_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error migrando desde Astra: {e}")
        return False

def validate_vector_store(vector_store_path: str):
    """
    Validar que el vector store esté en formato correcto
    """
    try:
        with open(vector_store_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        documents = data.get("documents", {})
        
        print(f"🔍 Validando vector store: {vector_store_path}")
        print(f"   📄 Total documentos: {len(documents)}")
        
        # Validar estructura
        valid_docs = 0
        for doc_id, doc in documents.items():
            if all(key in doc for key in ["id", "content", "embedding", "metadata"]):
                if len(doc["embedding"]) == 3072:  # text-embedding-3-large
                    valid_docs += 1
                else:
                    print(f"   ⚠️ Documento {doc_id}: embedding dimension incorrecta ({len(doc['embedding'])})")
            else:
                print(f"   ⚠️ Documento {doc_id}: estructura incompleta")
        
        print(f"   ✅ Documentos válidos: {valid_docs}/{len(documents)}")
        
        if valid_docs == len(documents):
            print("✅ Vector store válido y listo para usar")
            return True
        else:
            print("⚠️ Vector store tiene problemas de formato")
            return False
            
    except Exception as e:
        print(f"❌ Error validando vector store: {e}")
        return False

def main():
    """
    Script principal de migración
    """
    print("Tigo RAG - Migrador de Vectores")
    print("===============================")
    print()
    
    # Buscar archivos existentes
    possible_sources = [
        "../analysis_analytics.db",
        "../tigo_vector_store.json", 
        "../vector_3072.json",
        "../exports/analytics_export_all_*.json"
    ]
    
    found_sources = []
    for source in possible_sources:
        if os.path.exists(source):
            found_sources.append(source)
    
    if found_sources:
        print("📁 Archivos encontrados:")
        for i, source in enumerate(found_sources, 1):
            print(f"   {i}. {source}")
        print()
        
        # Interactivo: elegir fuente
        try:
            choice = input("Selecciona archivo fuente (número) o 'skip' para omitir migración: ")
            
            if choice.lower() == 'skip':
                print("⏭️ Saltando migración")
                return
            
            source_idx = int(choice) - 1
            if 0 <= source_idx < len(found_sources):
                source_path = found_sources[source_idx]
                
                # Determinar tipo y migrar
                if source_path.endswith('.json'):
                    if 'export' in source_path.lower() or 'astra' in source_path.lower():
                        success = migrate_from_astra_export(source_path)
                    else:
                        success = migrate_from_json(source_path)
                else:
                    print(f"⚠️ Tipo de archivo no soportado: {source_path}")
                    success = False
                
                if success:
                    validate_vector_store("data/tigo_vector_store.json")
            else:
                print("❌ Selección inválida")
                
        except ValueError:
            print("❌ Entrada inválida")
        except KeyboardInterrupt:
            print("\n⏹️ Cancelado por usuario")
    
    else:
        print("ℹ️ No se encontraron archivos de vectores existentes")
        print("   El sistema creará un vector store vacío al iniciar")
    
    print("\nℹ️ Para usar el sistema:")
    print("   1. python main.py")
    print("   2. Agrega documentos via /api/add-document")
    print("   3. O sube archivos via /api/upload-file")

if __name__ == "__main__":
    main()