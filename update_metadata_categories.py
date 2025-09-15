# update_metadata_categories.py
"""
Update metadata categories in existing vector store WITHOUT re-vectorizing
Consolidate methodology categories while preserving embeddings to avoid costs
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, Any, List, Optional


class MetadataCategoryUpdater:
    """
    Update vector store metadata categories without touching embeddings
    """
    
    def __init__(self, vector_store_path: str = "data/tigo_vector_store.json"):
        self.vector_store_path = vector_store_path
        self.backup_path = f"{vector_store_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Category consolidation mapping
        self.category_mapping = {
            # Current -> New mapping
            "Panel Online": "Cuantitativa",
            "Cuantitativa": "Cuantitativa",  # Keep as is
            "Focus Groups": "Cualitativa", 
            "Cualitativa": "Cualitativa",   # Keep as is
            
            # Alternative spellings/variations
            "panel online": "Cuantitativa",
            "cuantitativa": "Cuantitativa",
            "focus groups": "Cualitativa",
            "cualitativa": "Cualitativa",
            "PANEL ONLINE": "Cuantitativa",
            "CUANTITATIVA": "Cuantitativa",
            "FOCUS GROUPS": "Cualitativa",
            "CUALITATIVA": "Cualitativa"
        }
        
        # Fields that might contain methodology information
        self.methodology_fields = [
            "study_type",
            "methodology", 
            "research_type",
            "study_methodology",
            "method",
            "tipo_estudio",
            "metodologia"
        ]
        
        print("🔧 Metadata Category Updater initialized")
        print(f"   📁 Vector store: {vector_store_path}")
        print(f"   💾 Backup will be created: {self.backup_path}")
        print(f"   🔄 Consolidations:")
        print(f"     • 'Panel Online' → 'Cuantitativa'")
        print(f"     • 'Focus Groups' → 'Cualitativa'")
    
    def load_vector_store(self) -> Optional[Dict[str, Any]]:
        """Load existing vector store"""
        try:
            if not os.path.exists(self.vector_store_path):
                print(f"❌ Vector store not found: {self.vector_store_path}")
                return None
            
            with open(self.vector_store_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ Vector store loaded:")
            print(f"   📄 Documents: {len(data.get('documents', {}))}")
            
            return data
            
        except Exception as e:
            print(f"❌ Error loading vector store: {e}")
            return None
    
    def create_backup(self) -> bool:
        """Create backup of original vector store"""
        try:
            shutil.copy2(self.vector_store_path, self.backup_path)
            print(f"✅ Backup created: {self.backup_path}")
            return True
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    
    def analyze_current_categories(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current methodology categories in the vector store"""
        category_analysis = {
            "total_documents": 0,
            "categories_found": {},
            "fields_with_categories": {},
            "documents_to_update": []
        }
        
        documents = data.get("documents", {})
        category_analysis["total_documents"] = len(documents)
        
        for doc_id, doc in documents.items():
            metadata = doc.get("metadata", {})
            doc_categories = {}
            needs_update = False
            
            # Check all methodology fields
            for field in self.methodology_fields:
                if field in metadata:
                    value = metadata[field]
                    if isinstance(value, str):
                        # Track current categories
                        if value not in category_analysis["categories_found"]:
                            category_analysis["categories_found"][value] = 0
                        category_analysis["categories_found"][value] += 1
                        
                        # Track which fields contain categories
                        if field not in category_analysis["fields_with_categories"]:
                            category_analysis["fields_with_categories"][field] = {}
                        if value not in category_analysis["fields_with_categories"][field]:
                            category_analysis["fields_with_categories"][field][value] = 0
                        category_analysis["fields_with_categories"][field][value] += 1
                        
                        # Check if this document needs updating
                        if value in self.category_mapping and self.category_mapping[value] != value:
                            needs_update = True
                            doc_categories[field] = {
                                "current": value,
                                "new": self.category_mapping[value]
                            }
            
            if needs_update:
                category_analysis["documents_to_update"].append({
                    "doc_id": doc_id,
                    "document_name": metadata.get("document_name", "Unknown"),
                    "updates": doc_categories
                })
        
        return category_analysis
    
    def print_analysis_report(self, analysis: Dict[str, Any]):
        """Print detailed analysis report"""
        print("\n📊 CURRENT CATEGORY ANALYSIS")
        print("=" * 50)
        
        print(f"📄 Total documents: {analysis['total_documents']}")
        print(f"🔄 Documents to update: {len(analysis['documents_to_update'])}")
        
        print(f"\n🏷️ Categories found:")
        for category, count in sorted(analysis["categories_found"].items()):
            new_category = self.category_mapping.get(category, category)
            status = "→ " + new_category if new_category != category else "✓ (no change)"
            print(f"   • '{category}': {count} docs {status}")
        
        print(f"\n📋 Fields containing categories:")
        for field, categories in analysis["fields_with_categories"].items():
            print(f"   • {field}:")
            for category, count in categories.items():
                print(f"     - '{category}': {count} docs")
        
        if analysis["documents_to_update"]:
            print(f"\n🔄 Sample documents to update:")
            for i, doc_info in enumerate(analysis["documents_to_update"][:5]):
                print(f"   {i+1}. {doc_info['document_name']}")
                for field, change in doc_info["updates"].items():
                    print(f"      {field}: '{change['current']}' → '{change['new']}'")
            
            if len(analysis["documents_to_update"]) > 5:
                print(f"   ... and {len(analysis['documents_to_update']) - 5} more")
    
    def update_metadata_categories(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update metadata categories without touching embeddings"""
        updates_made = {
            "documents_updated": 0,
            "fields_updated": 0,
            "category_changes": {},
            "embedding_vectors_preserved": 0
        }
        
        documents = data.get("documents", {})
        
        for doc_id, doc in documents.items():
            metadata = doc.get("metadata", {})
            doc_updated = False
            
            # Preserve embeddings (CRITICAL - don't touch these!)
            original_embedding = doc.get("embedding", [])
            updates_made["embedding_vectors_preserved"] += 1 if original_embedding else 0
            
            # Update methodology fields
            for field in self.methodology_fields:
                if field in metadata:
                    current_value = metadata[field]
                    if isinstance(current_value, str) and current_value in self.category_mapping:
                        new_value = self.category_mapping[current_value]
                        
                        if new_value != current_value:
                            # Track the change
                            change_key = f"{current_value} → {new_value}"
                            if change_key not in updates_made["category_changes"]:
                                updates_made["category_changes"][change_key] = 0
                            updates_made["category_changes"][change_key] += 1
                            
                            # Make the update
                            metadata[field] = new_value
                            updates_made["fields_updated"] += 1
                            doc_updated = True
                            
                            print(f"   📝 {doc.get('metadata', {}).get('document_name', doc_id)[:50]}...")
                            print(f"      {field}: '{current_value}' → '{new_value}'")
            
            if doc_updated:
                # Update processing metadata
                metadata["metadata_updated_at"] = datetime.now().isoformat()
                metadata["category_consolidation_applied"] = True
                updates_made["documents_updated"] += 1
        
        # Update global metadata
        if "metadata" not in data:
            data["metadata"] = {}
        
        data["metadata"]["last_category_update"] = datetime.now().isoformat()
        data["metadata"]["category_consolidation"] = {
            "applied": True,
            "mapping": self.category_mapping,
            "updates_summary": updates_made
        }
        
        return data, updates_made
    
    def save_updated_vector_store(self, data: Dict[str, Any]) -> bool:
        """Save updated vector store"""
        try:
            with open(self.vector_store_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Updated vector store saved: {self.vector_store_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving updated vector store: {e}")
            return False
    
    def validate_update(self, original_data: Dict[str, Any], updated_data: Dict[str, Any]) -> bool:
        """Validate that embeddings were preserved and only metadata was changed"""
        try:
            original_docs = original_data.get("documents", {})
            updated_docs = updated_data.get("documents", {})
            
            if len(original_docs) != len(updated_docs):
                print("❌ Validation failed: Document count mismatch")
                return False
            
            embeddings_preserved = 0
            metadata_changes = 0
            
            for doc_id in original_docs:
                if doc_id not in updated_docs:
                    print(f"❌ Validation failed: Document {doc_id} missing")
                    return False
                
                orig_doc = original_docs[doc_id]
                updt_doc = updated_docs[doc_id]
                
                # Check embeddings are identical
                orig_embedding = orig_doc.get("embedding", [])
                updt_embedding = updt_doc.get("embedding", [])
                
                if orig_embedding == updt_embedding:
                    embeddings_preserved += 1
                else:
                    print(f"❌ Validation failed: Embedding changed for {doc_id}")
                    return False
                
                # Check content is identical
                if orig_doc.get("content") != updt_doc.get("content"):
                    print(f"❌ Validation failed: Content changed for {doc_id}")
                    return False
                
                # Count metadata changes
                orig_meta = orig_doc.get("metadata", {})
                updt_meta = updt_doc.get("metadata", {})
                
                for field in self.methodology_fields:
                    if field in orig_meta and field in updt_meta:
                        if orig_meta[field] != updt_meta[field]:
                            metadata_changes += 1
            
            print(f"✅ Validation successful:")
            print(f"   🔒 Embeddings preserved: {embeddings_preserved}/{len(original_docs)}")
            print(f"   📝 Metadata fields updated: {metadata_changes}")
            
            return True
            
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
    
    def run_update(self, dry_run: bool = False) -> bool:
        """Run the complete metadata update process"""
        print("🚀 Starting Metadata Category Update")
        print("=" * 60)
        
        # Load vector store
        data = self.load_vector_store()
        if not data:
            return False
        
        # Analyze current categories
        analysis = self.analyze_current_categories(data)
        self.print_analysis_report(analysis)
        
        if len(analysis["documents_to_update"]) == 0:
            print("\n✅ No updates needed - all categories are already consolidated!")
            return True
        
        if dry_run:
            print(f"\n🔍 DRY RUN - No changes will be made")
            print(f"   Would update {len(analysis['documents_to_update'])} documents")
            return True
        
        # Confirm update
        print(f"\n⚠️ ABOUT TO UPDATE {len(analysis['documents_to_update'])} DOCUMENTS")
        confirm = input("\nProceed with metadata update? (yes/no): ").lower().strip()
        
        if confirm != 'yes':
            print("❌ Update cancelled by user")
            return False
        
        # Create backup
        if not self.create_backup():
            print("❌ Cannot proceed without backup")
            return False
        
        # Keep original for validation
        original_data = json.loads(json.dumps(data))  # Deep copy
        
        # Update categories
        print(f"\n🔄 Updating metadata categories...")
        updated_data, updates_summary = self.update_metadata_categories(data)
        
        # Validate update
        print(f"\n🔍 Validating updates...")
        if not self.validate_update(original_data, updated_data):
            print("❌ Validation failed - restoring from backup")
            shutil.copy2(self.backup_path, self.vector_store_path)
            return False
        
        # Save updated vector store
        if not self.save_updated_vector_store(updated_data):
            print("❌ Failed to save - restoring from backup")
            shutil.copy2(self.backup_path, self.vector_store_path)
            return False
        
        # Print final summary
        self.print_update_summary(updates_summary)
        
        return True
    
    def print_update_summary(self, updates_summary: Dict[str, Any]):
        """Print final update summary"""
        print(f"\n🎉 METADATA UPDATE COMPLETED")
        print("=" * 50)
        print(f"✅ Documents updated: {updates_summary['documents_updated']}")
        print(f"✅ Fields updated: {updates_summary['fields_updated']}")
        print(f"🔒 Embedding vectors preserved: {updates_summary['embedding_vectors_preserved']}")
        
        print(f"\n📊 Category consolidations:")
        for change, count in updates_summary["category_changes"].items():
            print(f"   • {change}: {count} documents")
        
        print(f"\n💾 Backup available: {self.backup_path}")
        print(f"💰 NO RE-VECTORIZATION COSTS - Embeddings preserved!")
        
        print(f"\n✅ Your vector store is ready with consolidated categories:")
        print(f"   • 'Cuantitativa' (includes former 'Panel Online')")
        print(f"   • 'Cualitativa' (includes former 'Focus Groups')")


def main():
    """Main execution function"""
    print("Tigo RAG - Metadata Category Consolidator")
    print("========================================")
    print("Consolidate methodology categories WITHOUT re-vectorizing")
    print()
    
    # Parse command line arguments
    import sys
    dry_run = "--dry-run" in sys.argv or "-d" in sys.argv
    vector_store_path = "data/tigo_vector_store.json"
    
    # Check if custom path provided
    for arg in sys.argv:
        if arg.endswith('.json') and os.path.exists(arg):
            vector_store_path = arg
            break
    
    # Initialize updater
    updater = MetadataCategoryUpdater(vector_store_path)
    
    # Run update
    success = updater.run_update(dry_run=dry_run)
    
    if success:
        if dry_run:
            print("\n🔍 Dry run completed - run without --dry-run to apply changes")
        else:
            print("\n🌟 Metadata consolidation successful!")
            print("\nNext steps:")
            print("1. Test your RAG system: python main.py")
            print("2. Verify queries work with new categories")
            print("3. Update any hardcoded category filters in your code")
    else:
        print("\n❌ Update failed - check errors above")
        print("Your original vector store is safe!")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())