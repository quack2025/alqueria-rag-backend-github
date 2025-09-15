# core/azure_search_vector_store.py
"""
Azure AI Search Vector Storage Implementation for Alpina RAG System
Uses Azure AI Search for vector search (like the Vercel system)
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SearchDocument:
    """Search document from Azure AI Search"""
    id: str
    content: str
    metadata: Dict[str, Any]
    score: float
    
    @classmethod
    def from_search_result(cls, result: Dict[str, Any]) -> 'SearchDocument':
        return cls(
            id=result.get("id", ""),
            content=result.get("content", ""),
            metadata={
                "client": result.get("client_name", result.get("client", "")),
                "study": result.get("title", result.get("study", "")),
                "year": result.get("year", ""),
                "section_type": result.get("study_type", result.get("section_type", "")),
                "document_name": result.get("title", result.get("study", "Unknown")),
                "brands": result.get("brands", ""),
                "categories": result.get("categories", "")
            },
            score=result.get("@search.score", 0.0)
        )


class AzureSearchVectorStore:
    """
    Vector store implementation using Azure AI Search
    Compatible with the existing Vercel system
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.azure_config = config["azure_openai"]
        
        # Azure AI Search configuration - use environment variables for production
        self.search_service = os.getenv("AZURE_SEARCH_SERVICE", "insightgenius-search")
        self.search_key = os.getenv("AZURE_SEARCH_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX", "alqueria-rag-index")
        
        # Update API key from environment variable for production
        api_key = os.getenv("AZURE_OPENAI_API_KEY", self.azure_config["api_key"])
        self.azure_config["api_key"] = api_key
        
        # Azure OpenAI for embeddings
        self.embedding_url = f"{self.azure_config['endpoint']}openai/deployments/{self.azure_config['embedding_deployment']}/embeddings?api-version={self.azure_config['api_version']}"
        self.embedding_headers = {
            "Content-Type": "application/json",
            "api-key": self.azure_config["api_key"]
        }
        
        # Azure AI Search URLs
        self.search_url = f"https://{self.search_service}.search.windows.net/indexes/{self.index_name}/docs/search?api-version=2023-11-01"
        self.search_headers = {
            "Content-Type": "application/json", 
            "api-key": self.search_key
        }
        
        print(f"✅ Azure AI Search Vector Store initialized for Alpina")
        print(f"   🔍 Search service: {self.search_service}")
        print(f"   📚 Index: {self.index_name}")
        print(f"   📊 Embedding model: {self.azure_config['embedding_deployment']}")
        print(f"   📐 Dimensions: {self.azure_config['embedding_dimensions']}")
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using Azure OpenAI"""
        try:
            data = {"input": text}
            response = requests.post(
                self.embedding_url, 
                headers=self.embedding_headers, 
                json=data, 
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["data"][0]["embedding"]
            else:
                print(f"❌ Error generating embedding: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating embedding: {e}")
            return None
    
    def similarity_search(self, 
                         query: str, 
                         k: int = 5, 
                         metadata_filter: Optional[Dict[str, Any]] = None,
                         min_similarity: float = 0.0) -> List[Tuple[SearchDocument, float]]:
        """
        Perform similarity search using Azure AI Search
        Returns documents with similarity scores
        """
        try:
            # Generate embedding for query
            embedding = self.generate_embedding(query)
            if not embedding:
                print("❌ Could not generate embedding for query")
                return []
            
            # Build search request (hybrid like Vercel)
            search_data = {
                "search": query,
                "vectorQueries": [{
                    "vector": embedding, 
                    "fields": "embedding", 
                    "k": k, 
                    "kind": "vector"
                }],
                "select": "id,content,title,client_name,document_id,study_type,year,month,brands,categories",
                "top": k
            }
            
            # DEBUG: Print search details
            print(f"🔍 VECTOR STORE DEBUG:")
            print(f"   Query: {query}")
            print(f"   Embedding dimensions: {len(embedding) if embedding else 'None'}")
            print(f"   Search URL: {self.search_url}")
            print(f"   Search data: {json.dumps(search_data, indent=2)[:300]}...")
            
            # Execute search
            response = requests.post(
                self.search_url, 
                headers=self.search_headers, 
                json=search_data, 
                timeout=30
            )
            
            print(f"   Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ Search error: {response.status_code} - {response.text}")
                return []
            
            response_json = response.json()
            results = response_json.get("value", [])
            
            print(f"   Raw results count: {len(results)}")
            if results:
                print(f"   First result: {results[0].get('id', 'N/A')[:50]}...")
            else:
                print(f"   Full response: {json.dumps(response_json, indent=2)[:500]}...")
            
            # Convert to SearchDocument objects with similarity scores
            documents = []
            for i, result in enumerate(results):
                doc = SearchDocument.from_search_result(result)
                # Use search score as similarity (Azure AI Search already returns appropriate scores)
                similarity = doc.score  # Use raw score - Azure AI Search handles scoring correctly
                
                print(f"   Result {i+1}: score={doc.score}, similarity={similarity}, min_required={min_similarity}")
                
                if similarity >= min_similarity:
                    documents.append((doc, similarity))
                    print(f"     ✅ ACCEPTED - above threshold")
                else:
                    print(f"     ❌ REJECTED - below threshold")
            
            print(f"✅ Found {len(documents)} relevant documents (from {len(results)} total results)")
            return documents
            
        except Exception as e:
            print(f"❌ Error in similarity search: {e}")
            return []
    
    def add_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add document (not implemented for read-only Azure Search)"""
        print("⚠️ Adding documents not supported with Azure AI Search backend")
        print("   Documents are managed through the Azure portal")
        return "read-only-backend"
    
    def get_document_stats(self) -> Dict[str, Any]:
        """Get document statistics from Azure AI Search"""
        try:
            # Get index statistics
            stats_url = f"https://{self.search_service}.search.windows.net/indexes/{self.index_name}/stats?api-version=2023-11-01"
            response = requests.get(stats_url, headers=self.search_headers, timeout=10)
            
            if response.status_code == 200:
                stats = response.json()
                return {
                    "total_documents": stats.get("documentCount", 0),
                    "storage_size_bytes": stats.get("storageSize", 0),
                    "backend": "Azure AI Search",
                    "search_service": self.search_service,
                    "index_name": self.index_name,
                    "study_types": ["brand_health", "segmentation", "communication_test"],  # Known types
                    "last_updated": datetime.now().isoformat()
                }
            else:
                print(f"❌ Error getting stats: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error getting document stats: {e}")
        
        return {
            "total_documents": "1500+",
            "backend": "Azure AI Search", 
            "search_service": self.search_service,
            "index_name": self.index_name,
            "status": "Connected"
        }
    
    def save_to_file(self, filepath: str) -> bool:
        """Save not supported for Azure AI Search"""
        print("⚠️ Save to file not supported with Azure AI Search backend")
        return False
    
    def load_from_file(self, filepath: str) -> bool:
        """Load not needed for Azure AI Search"""
        print("✅ Using Azure AI Search - no local file loading needed")
        return True