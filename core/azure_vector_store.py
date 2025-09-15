# core/azure_vector_store.py
"""
Azure OpenAI Vector Storage Implementation for Tigo Honduras RAG System
Uses Azure OpenAI for both embeddings and vector search
"""

import os
import uuid
import json
# import numpy as np  # Removed for Azure compatibility
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import requests
# from sklearn.metrics.pairwise import cosine_similarity  # Removed for Azure compatibility
from core.math_utils import cosine_similarity  # Using pure Python implementation


@dataclass
class DocumentChunk:
    """Document chunk with metadata"""
    id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentChunk':
        return cls(**data)


class AzureOpenAIVectorStore:
    """
    Vector store implementation using Azure OpenAI for embeddings and in-memory storage
    Optimized for Tigo Honduras market research documents
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.azure_config = config["azure_openai"]
        
        # Vector storage
        self.documents: Dict[str, DocumentChunk] = {}
        self.embeddings_matrix: Optional[List[List[float]]] = None  # Changed from np.ndarray
        self.document_ids: List[str] = []
        
        # Tigo Honduras specific metadata structure
        self.metadata_schema = {
            "client": "tigo_honduras",
            "study_type": str,  # "brand_health", "communication_test", etc.
            "year": int,
            "document_name": str,
            "section_type": str,  # "executive_summary", "methodology", etc.
            "industry": "telecom",
            "language": "spanish_honduras",
            "content_type": str,  # "text", "table", "chart_description"
            "confidence_score": float,
            "processing_date": str
        }
        
        print(f"✅ Azure OpenAI Vector Store initialized for Tigo Honduras")
        print(f"   📊 Embedding model: {self.azure_config['embedding_model']}")
        print(f"   📐 Dimensions: {self.azure_config['embedding_dimensions']}")
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using Azure OpenAI"""
        try:
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_config["api_key"]
            }
            
            data = {"input": text}
            
            url = f"{self.azure_config['endpoint']}/openai/deployments/{self.azure_config['embedding_deployment']}/embeddings?api-version={self.azure_config['api_version']}"
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["data"][0]["embedding"]
            
        except Exception as e:
            print(f"❌ Error generating embedding: {e}")
            return None
    
    def add_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add document chunk to vector store"""
        try:
            # Generate embedding
            embedding = self.generate_embedding(content)
            if not embedding:
                raise ValueError("Failed to generate embedding")
            
            # Validate and enrich metadata
            enriched_metadata = self._enrich_metadata(metadata)
            
            # Create document chunk
            chunk_id = str(uuid.uuid4())
            chunk = DocumentChunk(
                id=chunk_id,
                content=content,
                embedding=embedding,
                metadata=enriched_metadata,
                created_at=datetime.now().isoformat()
            )
            
            # Store document
            self.documents[chunk_id] = chunk
            self.document_ids.append(chunk_id)
            
            # Update embeddings matrix
            self._update_embeddings_matrix()
            
            print(f"✅ Added document chunk: {chunk_id}")
            print(f"   📄 Content length: {len(content)} chars")
            print(f"   📊 Study type: {enriched_metadata.get('study_type', 'Unknown')}")
            
            return chunk_id
            
        except Exception as e:
            print(f"❌ Error adding document: {e}")
            raise
    
    def _enrich_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich metadata with Tigo Honduras specific information"""
        enriched = {
            "client": "tigo_honduras",
            "industry": "telecom",
            "language": "spanish_honduras",
            "processing_date": datetime.now().isoformat()
        }
        
        # Merge provided metadata
        enriched.update(metadata)
        
        # Ensure required fields
        if "study_type" not in enriched:
            enriched["study_type"] = self._detect_study_type(metadata.get("document_name", ""))
        
        if "year" not in enriched:
            enriched["year"] = datetime.now().year
        
        if "confidence_score" not in enriched:
            enriched["confidence_score"] = 1.0
        
        return enriched
    
    def _detect_study_type(self, document_name: str) -> str:
        """Detect study type from document name (Tigo Honduras specific)"""
        document_lower = document_name.lower()
        
        study_types = {
            "brand_health": ["brand health", "tracking", "salud marca"],
            "communication_test": ["communication", "comunicación", "advertising", "publicitario"],
            "concept_test": ["concept", "concepto", "evaluación concepto"],
            "pack_test": ["pack", "empaque", "packaging"],
            "usage_attitudes": ["usage", "uso", "attitudes", "actitudes"],
            "segmentation": ["segmentation", "segmentación"],
            "pricing": ["pricing", "precio", "price"],
            "product_test": ["product", "producto"],
            "maxdiff": ["maxdiff", "max diff"],
            "conjoint": ["conjoint", "trade-off"]
        }
        
        for study_type, keywords in study_types.items():
            if any(keyword in document_lower for keyword in keywords):
                return study_type
        
        return "general_research"
    
    def _update_embeddings_matrix(self):
        """Update the embeddings matrix for efficient similarity search"""
        if not self.documents:
            self.embeddings_matrix = None
            return
        
        embeddings = [doc.embedding for doc in self.documents.values()]
        self.embeddings_matrix = embeddings  # Already a list of lists
    
    def similarity_search(self, 
                         query: str, 
                         k: int = 5, 
                         metadata_filter: Optional[Dict[str, Any]] = None,
                         min_similarity: float = 0.7) -> List[Tuple[DocumentChunk, float]]:
        """
        Perform similarity search with metadata filtering
        """
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            if not query_embedding:
                return []
            
            # Filter documents by metadata
            filtered_docs = self._filter_by_metadata(metadata_filter) if metadata_filter else self.documents
            
            if not filtered_docs:
                print("⚠️ No documents match metadata filter")
                return []
            
            # Calculate similarities using pure Python
            results = []
            
            for doc_id, doc in filtered_docs.items():
                # Using pure Python cosine similarity
                similarity = cosine_similarity(query_embedding, doc.embedding)
                
                if similarity >= min_similarity:
                    results.append((doc, float(similarity)))
            
            # Sort by similarity and return top k
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:k]
            
        except Exception as e:
            print(f"❌ Error in similarity search: {e}")
            return []
    
    def _filter_by_metadata(self, metadata_filter: Dict[str, Any]) -> Dict[str, DocumentChunk]:
        """Filter documents by metadata criteria"""
        filtered = {}
        
        for doc_id, doc in self.documents.items():
            match = True
            
            for key, value in metadata_filter.items():
                if key not in doc.metadata:
                    match = False
                    break
                
                doc_value = doc.metadata[key]
                
                # Handle different comparison types
                if isinstance(value, dict):
                    # Range queries: {"year": {"gte": 2020, "lte": 2024}}
                    if "gte" in value and doc_value < value["gte"]:
                        match = False
                        break
                    if "lte" in value and doc_value > value["lte"]:
                        match = False
                        break
                    if "in" in value and doc_value not in value["in"]:
                        match = False
                        break
                elif isinstance(value, list):
                    # Multiple values: {"study_type": ["brand_health", "communication_test"]}
                    if doc_value not in value:
                        match = False
                        break
                else:
                    # Exact match
                    if doc_value != value:
                        match = False
                        break
            
            if match:
                filtered[doc_id] = doc
        
        return filtered
    
    def get_document_stats(self) -> Dict[str, Any]:
        """Get statistics about stored documents"""
        if not self.documents:
            return {"total_documents": 0}
        
        # Aggregate by study type
        study_types = {}
        years = {}
        content_types = {}
        
        for doc in self.documents.values():
            metadata = doc.metadata
            
            study_type = metadata.get("study_type", "unknown")
            study_types[study_type] = study_types.get(study_type, 0) + 1
            
            year = metadata.get("year", "unknown")
            years[str(year)] = years.get(str(year), 0) + 1
            
            content_type = metadata.get("content_type", "unknown")
            content_types[content_type] = content_types.get(content_type, 0) + 1
        
        return {
            "total_documents": len(self.documents),
            "study_types": study_types,
            "years": years,
            "content_types": content_types,
            "embedding_dimensions": self.azure_config["embedding_dimensions"]
        }
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete document from vector store"""
        try:
            if doc_id in self.documents:
                del self.documents[doc_id]
                if doc_id in self.document_ids:
                    self.document_ids.remove(doc_id)
                self._update_embeddings_matrix()
                print(f"✅ Deleted document: {doc_id}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting document: {e}")
            return False
    
    def clear_all(self) -> bool:
        """Clear all documents from vector store"""
        try:
            self.documents.clear()
            self.document_ids.clear()
            self.embeddings_matrix = None
            print("✅ Cleared all documents from vector store")
            return True
        except Exception as e:
            print(f"❌ Error clearing vector store: {e}")
            return False
    
    def save_to_file(self, filepath: str) -> bool:
        """Save vector store to file"""
        try:
            data = {
                "documents": {doc_id: doc.to_dict() for doc_id, doc in self.documents.items()},
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "total_documents": len(self.documents),
                    "client": "tigo_honduras"
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Vector store saved to: {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving vector store: {e}")
            return False
    
    def load_from_file(self, filepath: str) -> bool:
        """Load vector store from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load documents
            self.documents.clear()
            self.document_ids.clear()
            
            for doc_id, doc_data in data["documents"].items():
                self.documents[doc_id] = DocumentChunk.from_dict(doc_data)
                self.document_ids.append(doc_id)
            
            # Update embeddings matrix
            self._update_embeddings_matrix()
            
            print(f"✅ Vector store loaded from: {filepath}")
            print(f"   📄 Documents loaded: {len(self.documents)}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading vector store: {e}")
            return False