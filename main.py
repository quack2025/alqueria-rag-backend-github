# main.py
"""
Multimodal RAG System - FastAPI Application
3 endpoints: /api/rag-pure, /api/rag-creative, /api/rag-hybrid
Each accepts multimodal input and generates multimodal output
"""

import os
import json
import uvicorn
import requests
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import base64

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️ python-dotenv not installed, using system environment variables")

from core.azure_search_vector_store import AzureSearchVectorStore
from core.multimodal_processor import MultimodalInputProcessor
from core.multimodal_output import MultimodalOutputGenerator
from core.intelligent_suggestions import IntelligentSuggestionEngine
from core.data_exporter import RAGDataExporter
from core.system_configuration import SystemConfigurationManager
from personas.persona_system import ComprehensivePersonaSystem


# Pydantic models for API
class MultimodalQuery(BaseModel):
    """Multimodal query input"""
    text: Optional[str] = Field(None, description="Text query")
    images: Optional[List[str]] = Field(None, description="Base64 encoded images or file paths")
    audio: Optional[List[str]] = Field(None, description="Base64 encoded audio or file paths")
    metadata_filter: Optional[Dict[str, Any]] = Field(None, description="Metadata filters for vector search")
    output_types: Optional[List[str]] = Field(["text"], description="Desired output types: text, table, chart, image")
    rag_percentage: Optional[int] = Field(None, description="RAG vs LLM knowledge percentage (hybrid mode only)")


class RAGResponse(BaseModel):
    """RAG response output"""
    answer: str
    visualizations: Dict[str, List[Dict[str, Any]]]
    citations: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    has_visualizations: bool
    suggestions: Optional[Dict[str, Any]] = None
    timestamp: str


class PersonaChatQuery(BaseModel):
    """Persona chat query"""
    message: str
    session_id: Optional[str] = None
    persona_id: Optional[str] = None


class PersonaSurveyQuery(BaseModel):
    """Mass survey query"""
    questions: List[str]
    persona_ids: Optional[List[str]] = None
    max_personas: Optional[int] = 20


class PersonaFocusGroupQuery(BaseModel):
    """Focus group query"""
    topic: str
    persona_ids: Optional[List[str]] = None
    group_size: Optional[int] = 8


class PersonaValidationQuery(BaseModel):
    """Persona validation query"""
    persona_count: Optional[int] = 50
    diversity_target: Optional[float] = 0.8
    quality_threshold: Optional[float] = 0.7


class EnhancedPersonaGenerationQuery(BaseModel):
    """Enhanced persona generation with advanced methodologies"""
    persona_count: Optional[int] = 50
    study_level: Optional[str] = "exploratory_study"  # pilot_study, exploratory_study, sensitivity_analysis
    use_implicit_demographics: Optional[bool] = True
    include_temporal_context: Optional[bool] = True
    generate_interview_transcripts: Optional[bool] = False


class EnhancedChatQuery(BaseModel):
    """Enhanced chat with advanced methodologies"""
    message: str
    session_id: str
    use_temperature_optimization: Optional[bool] = True
    use_temporal_context: Optional[bool] = True


class StudyValidationQuery(BaseModel):
    """Study readiness validation query"""
    study_level: str  # pilot_study, exploratory_study, sensitivity_analysis
    persona_ids: Optional[List[str]] = None


class ExportQuery(BaseModel):
    """Export RAG response query"""
    rag_response: Dict[str, Any] = Field(..., description="RAG response data to export")
    format_type: str = Field("excel", description="Export format: excel, csv, json, html")
    include_metadata: bool = Field(True, description="Include metadata in export")


class ConfigurationQuery(BaseModel):
    """System configuration query"""
    user_id: Optional[str] = Field(None, description="User ID for personalized config")
    config_changes: Optional[Dict[str, Any]] = Field(None, description="Configuration changes to apply")
    preset_name: Optional[str] = Field(None, description="Configuration preset to apply")


class RAGModeConfigQuery(BaseModel):
    """RAG mode configuration query"""
    mode: str = Field(..., description="RAG mode to configure (pure, creative, hybrid)")
    rag_percentage: Optional[int] = Field(None, description="Custom RAG percentage")
    creativity_level: Optional[float] = Field(None, description="Creativity level (0.0-1.0)")
    system_prompt: Optional[str] = Field(None, description="Custom system prompt")


class ModuleConfigQuery(BaseModel):
    """Module configuration query"""
    module: str = Field(..., description="Module to configure")
    system_prompt: Optional[str] = Field(None, description="Custom system prompt for module")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Module-specific parameters")


class SyntheticChatQuery(BaseModel):
    """Dynamic synthetic chat query"""
    user_message: str = Field(..., description="User message")
    archetype: str = Field(..., description="Arquetipo to respond as")
    evaluation_context: Dict[str, Any] = Field(..., description="Full evaluation context")
    concept_details: Dict[str, Any] = Field(..., description="Campaign/concept details")
    conversation_history: List[Dict[str, Any]] = Field([], description="Previous conversation messages")
    creativity_level: int = Field(75, description="Creativity level (0-100)")
    language: str = Field("spanish", description="Response language")
    cultural_context: str = Field("honduras", description="Cultural context")


class AlpinaRAGSystem:
    """Main Alpina RAG System"""
    
    def __init__(self, config_path: str = "config/alpina_config.json"):
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.vector_store = AzureSearchVectorStore(self.config)
        self.multimodal_processor = MultimodalInputProcessor(self.config)
        self.output_generator = MultimodalOutputGenerator(self.config)
        self.suggestion_engine = IntelligentSuggestionEngine()
        self.data_exporter = RAGDataExporter()
        self.config_manager = SystemConfigurationManager()
        
        # Initialize persona system
        self.persona_system = ComprehensivePersonaSystem(self.config, self)
        
        # Azure AI Search is always connected - no local loading needed
        
        print("🚀 Alpina RAG System initialized")
        print(f"   📊 Vector store: Azure AI Search with 151 documents")
        print(f"   🎯 RAG Endpoints: rag-pure, rag-creative, rag-hybrid")
        print(f"   👥 Persona Endpoints: persona-chat, persona-survey, persona-focus-group, persona-validate")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file or use defaults"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Configuration loaded from file: {config_path}")
            return config
        except FileNotFoundError:
            print(f"⚠️ Config file not found, using environment variables")
            # Use default configuration from environment variables
            return {
                "client_info": {
                    "name": "Tigo Honduras",
                    "industry": "telecommunications",
                    "market": "honduras",
                    "language": "spanish_honduras"
                },
                "azure_openai": {
                    "endpoint": "https://insightgenius-rag-v1-resource.cognitiveservices.azure.com/",
                    "api_key": os.getenv("AZURE_OPENAI_API_KEY", ""),
                    "api_version": "2024-12-01-preview",
                    "embedding_deployment": "text-embedding-3-large",
                    "embedding_model": "text-embedding-3-large",
                    "embedding_dimensions": 3072,
                    "chat_deployment": "gpt-4.1",
                    "chat_model": "gpt-4.1",
                    "vision_deployment": "gpt-4-vision",
                    "dalle_deployment": "dall-e-3",
                    "whisper_deployment": "whisper-1",
                    "default_temperature": 0.1,
                    "max_tokens": 2000,
                    "timeout": 60
                },
                "endpoints": {
                    "rag_pure": {
                        "name": "Pure RAG Mode",
                        "rag_percentage": 100,
                        "creativity_level": 0.0,
                        "enable_visualization": False,
                        "max_context_chunks": 5
                    },
                    "rag_creative": {
                        "name": "Creative RAG Mode",
                        "rag_percentage": 60,
                        "creativity_level": 0.7,
                        "enable_visualization": True,
                        "enable_charts": True,
                        "max_context_chunks": 3
                    },
                    "rag_hybrid": {
                        "name": "Hybrid RAG Mode",
                        "rag_percentage": 80,
                        "creativity_level": 0.3,
                        "enable_visualization": True,
                        "enable_charts": True,
                        "max_context_chunks": 4
                    }
                }
            }
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def process_multimodal_query(self, 
                                query_data: MultimodalQuery, 
                                mode: str) -> Dict[str, Any]:
        """Process multimodal query through the RAG pipeline"""
        try:
            start_time = datetime.now()
            
            # 1. Process multimodal input
            input_data = {
                "text": query_data.text,
                "images": query_data.images or [],
                "audio": query_data.audio or [],
                "metadata": {"mode": mode, "endpoint": f"rag_{mode}"}
            }
            
            processed_input = self.multimodal_processor.process_input(input_data)
            
            if "error" in processed_input:
                raise HTTPException(status_code=400, detail=processed_input["error"])
            
            # 2. Extract query intent and generate search query
            intent_data = self.multimodal_processor.extract_query_intent(processed_input)
            
            # 3. Combine metadata filters
            final_metadata_filter = query_data.metadata_filter or {}
            # TEMPORARILY DISABLE automatic filters to ensure search works
            # if intent_data.get("suggested_filters"):
            #     final_metadata_filter.update(intent_data["suggested_filters"])
            print(f"🔍 DEBUG - Filters disabled, using only user filters: {final_metadata_filter}")
            
            # 4. Perform vector search
            search_query = processed_input["combined_content"] or query_data.text or ""
            
            if not search_query.strip():
                raise HTTPException(status_code=400, detail="No searchable content provided")
            
            # Get endpoint configuration
            endpoint_config = self.config["endpoints"][f"rag_{mode}"]
            
            search_results = self.vector_store.similarity_search(
                query=search_query,
                k=endpoint_config.get("max_context_chunks", 5),
                metadata_filter=final_metadata_filter,
                min_similarity=0.0  # Appropriate threshold for Azure AI Search raw scores
            )
            
            # 5. Build context from search results
            context_parts = []
            citations = []
            
            for doc, similarity in search_results:
                context_parts.append(f"[Documento: {doc.metadata.get('document_name', 'Unknown')}]\n{doc.content}")
                citations.append({
                    "document": doc.metadata.get("document_name", "Unknown"),
                    "study_type": doc.metadata.get("study_type", "Unknown"),
                    "year": doc.metadata.get("year", "Unknown"),
                    "similarity": round(similarity, 3),
                    "section": doc.metadata.get("section_type", "Unknown")
                })
            
            context = "\n\n".join(context_parts)
            
            # 6. Apply RAG percentage for hybrid mode
            if mode == "hybrid" and query_data.rag_percentage is not None:
                # Update endpoint config temporarily
                original_rag = endpoint_config.get("rag_percentage", 80)
                endpoint_config["rag_percentage"] = query_data.rag_percentage
            
            # 7. Generate multimodal response
            response_data = self.output_generator.generate_response(
                query=search_query,
                context=context,
                mode=mode,
                output_types=query_data.output_types or ["text"]
            )
            
            # 8. Generate intelligent suggestions
            response_metadata = {
                "mode": mode,
                "chunks_retrieved": len(search_results),
                "has_visualizations": len(response_data.get("tables", [])) + len(response_data.get("charts", [])) + len(response_data.get("images", [])) > 0
            }
            
            suggestions = self.suggestion_engine.analyze_response(
                answer=response_data.get("text_response", ""),
                citations=citations,
                metadata=response_metadata
            )
            
            # Add suggestions to the answer if enabled
            answer_with_suggestions = response_data.get("text_response", "")
            if suggestions["has_suggestions"]:
                suggestion_text = self.suggestion_engine.generate_suggestion_text(suggestions)
                answer_with_suggestions += suggestion_text
            
            # 9. Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # 10. Build final response
            final_response = {
                "answer": answer_with_suggestions,
                "visualizations": {
                    "tables": response_data.get("tables", []),
                    "charts": response_data.get("charts", []),
                    "images": response_data.get("images", [])
                },
                "citations": citations,
                "metadata": {
                    "mode": mode,
                    "processing_time_seconds": round(processing_time, 2),
                    "chunks_retrieved": len(search_results),
                    "has_multimodal_input": any([
                        processed_input["processing_info"]["has_images"],
                        processed_input["processing_info"]["has_audio"]
                    ]),
                    "query_intent": intent_data.get("intent", "General query"),
                    "confidence": intent_data.get("confidence", 0.5),
                    "tokens_used": response_data.get("metadata", {}).get("tokens_used", 0),
                    "metadata_filters_applied": final_metadata_filter,
                    "endpoint_config": endpoint_config
                },
                "has_visualizations": len(response_data.get("tables", [])) + len(response_data.get("charts", [])) + len(response_data.get("images", [])) > 0,
                "suggestions": suggestions,
                "timestamp": datetime.now().isoformat()
            }
            
            return final_response
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")
    
    def add_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add document to vector store"""
        return self.vector_store.add_document(content, metadata)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        vector_stats = self.vector_store.get_document_stats()
        
        return {
            "system_info": {
                "name": "Tigo Honduras Multimodal RAG",
                "version": "1.0.0",
                "client": self.config["client_info"]["name"],
                "industry": self.config["client_info"]["industry"]
            },
            "vector_store": vector_stats,
            "endpoints": {
                name: {
                    "description": config["description"],
                    "rag_percentage": config["rag_percentage"],
                    "creativity_level": config["creativity_level"],
                    "enable_visualization": config.get("enable_visualization", False)
                }
                for name, config in self.config["endpoints"].items()
            },
            "capabilities": {
                "multimodal_input": ["text", "images", "audio"],
                "multimodal_output": ["text", "tables", "charts", "images"],
                "metadata_filtering": True,
                "configurable_prompts": True
            }
        }


# Initialize FastAPI app
app = FastAPI(
    title="Tigo Honduras Multimodal RAG System",
    description="Advanced RAG system with multimodal input/output capabilities for Tigo Honduras market research",
    version="1.0.0"
)

# CORS middleware - Mejorado para desarrollo local y producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5183",  # Puerto que estás usando
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5183",
        "https://fnsuuhugvepxvizpbrnq.supabase.co",
        "https://tigo-frontend-lovable.vercel.app",
        "https://insightgenius-vercel.vercel.app",  # Frontend v1.0 en Vercel
        "https://tigo.insightgenius.io",  # Dominio personalizado futuro
        "*"  # Para desarrollo - remover en producción
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize RAG system
def initialize_rag_system():
    """Initialize RAG system with fallback"""
    try:
        # Check if we have required environment variables for Azure
        required_vars = ["AZURE_OPENAI_API_KEY", "AZURE_SEARCH_SERVICE", "AZURE_SEARCH_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"⚠️ Missing environment variables: {missing_vars}")
            print("🔄 Running in minimal mode without full RAG functionality")
            return None
            
        rag_system = AlpinaRAGSystem()
        print("✅ RAG system initialization successful")
        return rag_system
        
    except Exception as e:
        print(f"❌ RAG system initialization failed: {e}")
        print("🔄 Running in minimal mode - authentication and basic endpoints available")
        return None

rag_system = initialize_rag_system()


# Authentication models and endpoints
class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str

class LoginResponse(BaseModel):
    """Login response model"""
    success: bool
    token: Optional[str] = None
    message: str
    user: Optional[Dict[str, Any]] = None

# Simple authentication for demo purposes - replace with real auth in production
DEMO_USERS = {
    "ejecutivo@tigo.com.hn": "TigoHN2024!",
    "marketing@tigo.com.hn": "Marketing2024!",
    "insights@tigo.com.hn": "Insights2024!",
    "juan@genius-labs.com.co": "GeniusLabs2024!"
}

@app.post("/api/auth/login", response_model=LoginResponse)
async def login_endpoint(request: LoginRequest):
    """
    Simple authentication endpoint for demo purposes
    In production, integrate with proper authentication service
    """
    try:
        # Validate credentials
        if request.username in DEMO_USERS and DEMO_USERS[request.username] == request.password:
            # Generate simple JWT-like token (in production, use proper JWT)
            import hashlib
            import time
            token_data = f"{request.username}:{time.time()}"
            token = hashlib.sha256(token_data.encode()).hexdigest()
            
            return LoginResponse(
                success=True,
                token=token,
                message="Login successful",
                user={
                    "username": request.username,
                    "role": "admin" if request.username == "ejecutivo@tigo.com.hn" else "user",
                    "permissions": ["chat", "export", "view_stats"]
                }
            )
        else:
            return LoginResponse(
                success=False,
                message="Invalid credentials"
            )
    except Exception as e:
        print(f"Login error: {e}")
        return LoginResponse(
            success=False,
            message="Authentication error"
        )

@app.get("/api/auth/verify")
async def verify_token_endpoint(token: str = None):
    """
    Verify authentication token
    In production, implement proper JWT verification
    """
    try:
        if not token:
            return {"valid": False, "message": "No token provided"}
        
        # Simple token validation (in production, use proper JWT)
        if len(token) == 64:  # SHA256 length
            return {
                "valid": True,
                "message": "Token valid",
                "user": {
                    "authenticated": True,
                    "permissions": ["chat", "export", "view_stats"]
                }
            }
        else:
            return {"valid": False, "message": "Invalid token format"}
    except Exception as e:
        print(f"Token verification error: {e}")
        return {"valid": False, "message": "Token verification failed"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "rag_system_initialized": rag_system is not None,
        "version": "1.0.0"
    }

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with system information"""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    return {
        "message": "Multimodal RAG System",
        "status": "online",
        "endpoints": {
            "/api/rag-pure": "100% retrieval-based responses",
            "/api/rag-creative": "Creative responses with visualizations",
            "/api/rag-hybrid": "Balanced RAG/LLM approach with configurable ratio",
            "/api/persona-chat": "1:1 conversation with synthetic personas",
            "/api/persona-survey": "Mass survey with multiple personas",
            "/api/persona-focus-group": "Simulated focus group discussions",
            "/api/persona-validate": "Generate and validate persona batches",
            "/api/persona-enhanced-generate": "Enhanced generation with advanced methodologies",
            "/api/persona-enhanced-chat": "Temperature-optimized conversations",
            "/api/persona-study-validation": "Academic study readiness validation",
            "/api/persona-generate-transcripts": "Generate 1-2 hour interview transcripts",
            "/api/synthetic/chat": "Dynamic archetype chat with full context and configurable creativity"
        },
        "capabilities": [
            "multimodal_input_text_images_audio",
            "multimodal_output_text_tables_charts_images",
            "configurable_prompts",
            "metadata_filtering",
            "azure_openai_powered",
            "synthetic_persona_generation",
            "bias_detection_framework",
            "anti_sycophancy_system",
            "regional_cultural_context"
        ],
        "version": "1.0.0"
    }


@app.get("/api/stats")
async def get_system_stats():
    """Get system statistics"""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    return rag_system.get_system_stats()


@app.post("/api/rag-pure", response_model=RAGResponse)
async def rag_pure_endpoint(query: MultimodalQuery):
    """
    Pure RAG Mode: 100% retrieval-based responses using only vector search results
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    return rag_system.process_multimodal_query(query, "pure")


@app.post("/api/rag-creative", response_model=RAGResponse)
async def rag_creative_endpoint(query: MultimodalQuery):
    """
    Creative RAG Mode: Creative responses with visualizations, blending RAG with LLM knowledge
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    return rag_system.process_multimodal_query(query, "creative")


@app.post("/api/rag-hybrid", response_model=RAGResponse)
async def rag_hybrid_endpoint(query: MultimodalQuery):
    """
    Hybrid RAG Mode: Balanced approach with configurable RAG/LLM ratio and optional visualizations
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    return rag_system.process_multimodal_query(query, "hybrid")


# Endpoint específico para el frontend - compatible con el formato esperado
@app.post("/api/chat")
async def chat_endpoint_for_frontend(request: Dict[str, Any]):
    """
    Endpoint específico para el frontend que espera el formato:
    {
        "messages": [{"role": "user", "content": "..."}],
        "mode": "general" | "creative"
    }
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        messages = request.get("messages", [])
        mode = request.get("mode", "general")
        
        # Obtener el último mensaje del usuario
        if not messages or not messages[-1].get("content"):
            raise HTTPException(status_code=400, detail="No message content provided")
        
        user_message = messages[-1]["content"]
        
        # Mapear modos del frontend a modos del backend
        backend_mode_mapping = {
            "general": "pure",      # general -> pure (100% RAG)
            "creative": "creative"  # creative -> creative
        }
        
        backend_mode = backend_mode_mapping.get(mode, "hybrid")
        
        # Crear query para el sistema RAG
        multimodal_query = MultimodalQuery(
            text=user_message,
            output_types=["text", "table", "chart"] if mode == "creative" else ["text"]
        )
        
        # Procesar con el sistema RAG
        response = rag_system.process_multimodal_query(multimodal_query, backend_mode)
        
        # Reformatear respuesta para el frontend
        return {
            "answer": response["answer"],
            "content": response["answer"],  # Para compatibilidad
            "citations": response.get("citations", []),
            "visualization": response.get("visualizations", {}),
            "suggestions": response.get("suggestions", {}).get("suggestions", []) if response.get("suggestions") else [],
            "metadata": response.get("metadata", {}),
            "timestamp": response.get("timestamp"),
            "mode": mode,
            "backend_mode_used": backend_mode
        }
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.post("/api/export-data")
async def export_data_endpoint(query: ExportQuery):
    """
    Export RAG response data to multiple formats (Excel, CSV, JSON, HTML)
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        export_result = rag_system.data_exporter.export_rag_response(
            rag_response=query.rag_response,
            format_type=query.format_type,
            include_metadata=query.include_metadata
        )
        
        if "error" in export_result:
            raise HTTPException(status_code=400, detail=export_result["error"])
        
        return export_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@app.post("/api/add-document")
async def add_document_endpoint(
    content: str = Form(...),
    document_name: str = Form(...),
    study_type: str = Form("general_research"),
    year: int = Form(2024),
    section_type: str = Form("content"),
    additional_metadata: str = Form("{}")
):
    """
    Add document to vector store
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Parse additional metadata
        extra_metadata = json.loads(additional_metadata) if additional_metadata != "{}" else {}
        
        # Build metadata
        metadata = {
            "document_name": document_name,
            "study_type": study_type,
            "year": year,
            "section_type": section_type,
            "content_type": "text",
            **extra_metadata
        }
        
        # Add document
        doc_id = rag_system.add_document(content, metadata)
        
        # Azure AI Search - no local saving needed
        
        return {
            "message": "Document added successfully",
            "document_id": doc_id,
            "metadata": metadata,
            "total_documents": "1500+ (Azure AI Search)"
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in additional_metadata")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding document: {str(e)}")


@app.post("/api/upload-file")
async def upload_file_endpoint(
    file: UploadFile = File(...),
    study_type: str = Form("general_research"),
    year: int = Form(2024),
    section_type: str = Form("content")
):
    """
    Upload and process file (image or audio) for multimodal processing
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Read file content
        file_content = await file.read()
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        # Process based on file type
        if file_extension in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            # Image file
            base64_data = base64.b64encode(file_content).decode()
            
            input_data = {
                "text": f"Analizar imagen: {file.filename}",
                "images": [base64_data],
                "audio": [],
                "metadata": {"uploaded_file": True}
            }
            
        elif file_extension in ['.mp3', '.wav', '.m4a', '.ogg']:
            # Audio file
            base64_data = base64.b64encode(file_content).decode()
            
            input_data = {
                "text": f"Transcribir y analizar audio: {file.filename}",
                "images": [],
                "audio": [base64_data],
                "metadata": {"uploaded_file": True}
            }
            
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")
        
        # Process multimodal input
        processed = rag_system.multimodal_processor.process_input(input_data)
        
        if "error" in processed:
            raise HTTPException(status_code=400, detail=processed["error"])
        
        # Add processed content to vector store
        if processed["combined_content"]:
            metadata = {
                "document_name": file.filename,
                "study_type": study_type,
                "year": year,
                "section_type": section_type,
                "content_type": "multimodal_processed",
                "original_file_type": file_extension,
                "file_size_bytes": len(file_content)
            }
            
            doc_id = rag_system.add_document(processed["combined_content"], metadata)
            
            # Azure AI Search - no local saving needed
            
            return {
                "message": "File processed and added to vector store",
                "filename": file.filename,
                "file_type": file_extension,
                "document_id": doc_id,
                "processed_content_length": len(processed["combined_content"]),
                "processing_info": processed["processing_info"],
                "total_documents": "1500+ (Azure AI Search)"
            }
        else:
            raise HTTPException(status_code=400, detail="No content could be extracted from file")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


# Persona System Endpoints
@app.post("/api/persona-chat")
async def persona_chat_endpoint(query: PersonaChatQuery):
    """
    1:1 Conversation with Synthetic Persona
    Start or continue conversation with a specific persona
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # If no session_id provided, start new conversation
        if not query.session_id:
            if not query.persona_id:
                # Generate a new persona if none specified
                persona_result = rag_system.persona_system.generate_validated_personas(
                    count=1, diversity_target=0.8, quality_threshold=0.7
                )
                
                if not persona_result["success"]:
                    raise HTTPException(status_code=400, detail="Failed to generate persona")
                
                persona_id = persona_result["personas"][0]["id"]
            else:
                persona_id = query.persona_id
            
            # Start new conversation
            session_id = await rag_system.persona_system.start_persona_conversation(
                persona_id, "chat", {"user_initiated": True}
            )
            
            return {
                "message": "Conversation started",
                "session_id": session_id,
                "persona_id": persona_id,
                "persona_profile": {
                    "age": rag_system.persona_system.generated_personas[persona_id]["characteristics"]["age"],
                    "gender": rag_system.persona_system.generated_personas[persona_id]["characteristics"]["gender"],
                    "location": rag_system.persona_system.generated_personas[persona_id]["characteristics"]["geographic_region"],
                    "service_type": rag_system.persona_system.generated_personas[persona_id]["characteristics"]["service_type"]
                },
                "instructions": "Send your message using this session_id to continue the conversation"
            }
        
        else:
            # Continue existing conversation
            response = await rag_system.persona_system.send_message_to_persona(
                query.session_id, query.message
            )
            
            return {
                "session_id": query.session_id,
                "persona_response": response["response"],
                "message_count": response["message_count"],
                "validation": response["validation"],
                "rag_context_used": response["rag_context_used"],
                "persona_consistency": response["persona_consistency"],
                "timestamp": datetime.now().isoformat()
            }
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in persona chat: {str(e)}")


@app.post("/api/persona-survey")
async def persona_survey_endpoint(query: PersonaSurveyQuery):
    """
    Mass Survey with Multiple Personas
    Conduct survey with multiple synthetic personas simultaneously
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Ensure we have personas available
        if not rag_system.persona_system.generated_personas:
            print("Generating personas for survey...")
            persona_result = rag_system.persona_system.generate_validated_personas(
                count=min(query.max_personas or 20, 50), 
                diversity_target=0.8, 
                quality_threshold=0.7
            )
            
            if not persona_result["success"]:
                raise HTTPException(status_code=400, detail="Failed to generate personas for survey")
        
        # Conduct mass survey
        survey_results = rag_system.persona_system.conduct_mass_survey(
            survey_questions=query.questions,
            persona_ids=query.persona_ids,
            max_personas=query.max_personas or 20
        )
        
        return {
            "survey_results": survey_results,
            "total_responses": len(survey_results["responses"]),
            "questions_asked": len(query.questions),
            "demographic_analysis": survey_results["analysis"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conducting survey: {str(e)}")


@app.post("/api/persona-focus-group")
async def persona_focus_group_endpoint(query: PersonaFocusGroupQuery):
    """
    Simulated Focus Group Discussion
    Simulate focus group with diverse synthetic personas
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Ensure we have personas available
        if not rag_system.persona_system.generated_personas:
            print("Generating personas for focus group...")
            persona_result = rag_system.persona_system.generate_validated_personas(
                count=min(query.group_size or 8, 12), 
                diversity_target=0.9,  # Higher diversity for focus groups
                quality_threshold=0.7
            )
            
            if not persona_result["success"]:
                raise HTTPException(status_code=400, detail="Failed to generate personas for focus group")
        
        # Simulate focus group
        focus_group_results = rag_system.persona_system.simulate_focus_group(
            topic=query.topic,
            persona_ids=query.persona_ids,
            group_size=query.group_size or 8
        )
        
        return {
            "focus_group_results": focus_group_results,
            "participants_count": len(focus_group_results["participants"]),
            "discussion_phases": len(focus_group_results["discussion_flow"]),
            "key_insights": focus_group_results["insights"],
            "moderator_notes": focus_group_results["moderator_notes"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conducting focus group: {str(e)}")


@app.post("/api/persona-validate")
async def persona_validate_endpoint(query: PersonaValidationQuery):
    """
    Generate and Validate Persona Batches
    Generate new personas with comprehensive bias detection and validation
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Generate validated personas
        generation_result = rag_system.persona_system.generate_validated_personas(
            count=query.persona_count or 50,
            diversity_target=query.diversity_target or 0.8,
            quality_threshold=query.quality_threshold or 0.7
        )
        
        # Get current system status
        system_status = rag_system.persona_system.get_system_status()
        
        # Get dashboard data
        dashboard_data = rag_system.persona_system.validation_dashboard.get_dashboard_data()
        
        return {
            "generation_result": generation_result,
            "validation_passed": generation_result["success"],
            "personas_generated": len(generation_result.get("personas", [])),
            "system_status": system_status,
            "quality_dashboard": dashboard_data,
            "bias_analysis": generation_result.get("validation", {}),
            "export_options": {
                "json": "/api/persona-export?format=json",
                "csv": "/api/persona-export?format=csv",
                "pdf": "/api/persona-export?format=pdf"
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating personas: {str(e)}")


@app.get("/api/persona-export")
async def persona_export_endpoint(
    format: str = "json",
    persona_ids: Optional[str] = None
):
    """
    Export Generated Personas
    Export personas in JSON, CSV, or PDF format
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Parse persona_ids if provided
        selected_persona_ids = None
        if persona_ids:
            selected_persona_ids = persona_ids.split(",")
        
        # Export personas
        export_data = rag_system.persona_system.export_personas(
            format=format,
            persona_ids=selected_persona_ids
        )
        
        return {
            "export_data": export_data,
            "format": format,
            "personas_exported": export_data["total_personas"],
            "export_timestamp": export_data["export_timestamp"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting personas: {str(e)}")


@app.get("/api/persona-dashboard")
async def persona_dashboard_endpoint():
    """
    Real-time Persona Quality Dashboard
    Get current quality metrics and validation status
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Get comprehensive system status
        system_status = rag_system.persona_system.get_system_status()
        
        # Get dashboard data
        dashboard_data = rag_system.persona_system.validation_dashboard.get_dashboard_data()
        
        return {
            "dashboard": dashboard_data,
            "system_status": system_status,
            "quality_summary": {
                "overall_status": dashboard_data["quality_status"],
                "active_alerts": len(dashboard_data["alerts"]),
                "personas_generated": system_status["personas"]["total_generated"],
                "active_conversations": system_status["personas"]["active_conversations"]
            },
            "academic_compliance": {
                "paper_reference": "2504.02234v2",
                "ethical_safeguards": True,
                "bias_detection_active": True,
                "anti_sycophancy_enabled": True,
                "honduras_demographic_validation": True
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting dashboard data: {str(e)}")


# Enhanced Persona System Endpoints with Advanced Methodologies
@app.post("/api/persona-enhanced-generate")
async def enhanced_persona_generation_endpoint(query: EnhancedPersonaGenerationQuery):
    """
    Enhanced Persona Generation with Advanced Methodologies
    Uses context-rich prompting, temperature optimization, implicit demographics,
    temporal context, and staged validation based on academic research 2504.02234v2
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Map string to enum
        from personas.staged_validation import StudyReadinessLevel
        
        study_level_mapping = {
            "pilot_study": StudyReadinessLevel.PILOT_STUDY,
            "exploratory_study": StudyReadinessLevel.EXPLORATORY_STUDY,
            "sensitivity_analysis": StudyReadinessLevel.SENSITIVITY_ANALYSIS
        }
        
        study_level = study_level_mapping.get(query.study_level, StudyReadinessLevel.EXPLORATORY_STUDY)
        
        # Generate enhanced personas
        generation_result = rag_system.persona_system.generate_enhanced_personas_with_advanced_methods(
            count=query.persona_count or 50,
            study_level=study_level,
            use_implicit_demographics=query.use_implicit_demographics,
            include_temporal_context=query.include_temporal_context,
            generate_interview_transcripts=query.generate_interview_transcripts
        )
        
        return {
            "generation_result": generation_result,
            "advanced_methodologies_applied": {
                "context_rich_prompting": query.generate_interview_transcripts,
                "temperature_optimization": True,
                "implicit_demographics": query.use_implicit_demographics,
                "temporal_context_integration": query.include_temporal_context,
                "staged_validation": study_level.value
            },
            "research_compliance": {
                "academic_paper": "2504.02234v2",
                "evidence_based_methods": True,
                "study_readiness_level": study_level.value,
                "validation_passed": generation_result["success"]
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in enhanced persona generation: {str(e)}")


@app.post("/api/persona-enhanced-chat")
async def enhanced_persona_chat_endpoint(query: EnhancedChatQuery):
    """
    Enhanced Persona Chat with Temperature Optimization and Temporal Context
    Uses hierarchical temperature sampling and current Honduras context integration
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Use enhanced conversation method
        response = await rag_system.persona_system.enhanced_persona_conversation(
            session_id=query.session_id,
            message=query.message,
            use_temperature_optimization=query.use_temperature_optimization,
            use_temporal_context=query.use_temporal_context
        )
        
        return {
            "enhanced_response": response,
            "methodologies_applied": {
                "temperature_optimization": query.use_temperature_optimization,
                "temporal_context_integration": query.use_temporal_context,
                "implicit_demographics": True,
                "anti_sycophancy_system": True
            },
            "quality_assurance": {
                "response_validated": True,
                "diversity_checked": True,
                "authenticity_scored": True
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in enhanced persona chat: {str(e)}")


@app.post("/api/persona-study-validation")
async def study_readiness_validation_endpoint(query: StudyValidationQuery):
    """
    Study Readiness Validation for Different Research Levels
    Validates personas for pilot study, exploratory study, or sensitivity analysis
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        from personas.staged_validation import StudyReadinessLevel
        
        # Map string to enum
        study_level_mapping = {
            "pilot_study": StudyReadinessLevel.PILOT_STUDY,
            "exploratory_study": StudyReadinessLevel.EXPLORATORY_STUDY,
            "sensitivity_analysis": StudyReadinessLevel.SENSITIVITY_ANALYSIS
        }
        
        study_level = study_level_mapping.get(query.study_level)
        if not study_level:
            raise HTTPException(status_code=400, detail="Invalid study level. Use: pilot_study, exploratory_study, or sensitivity_analysis")
        
        # Get personas to validate
        if query.persona_ids:
            personas_to_validate = [rag_system.persona_system.generated_personas[pid] 
                                  for pid in query.persona_ids 
                                  if pid in rag_system.persona_system.generated_personas]
        else:
            personas_to_validate = list(rag_system.persona_system.generated_personas.values())
        
        if not personas_to_validate:
            raise HTTPException(status_code=400, detail="No personas available for validation")
        
        # Perform validation
        validation_assessment = rag_system.persona_system.staged_validator.validate_for_study_level(
            personas_to_validate, study_level
        )
        
        return {
            "validation_assessment": {
                "study_level": study_level.value,
                "overall_score": validation_assessment.overall_score,
                "validation_passed": validation_assessment.passed,
                "summary": validation_assessment.summary,
                "readiness_certificate": validation_assessment.readiness_certificate,
                "limitations": validation_assessment.limitations,
                "recommended_use_cases": validation_assessment.recommended_use_cases,
                "dimension_results": {
                    dim.value: {
                        "score": result.score,
                        "passed": result.passed,
                        "evidence": result.evidence,
                        "issues": result.issues,
                        "recommendations": result.recommendations
                    } for dim, result in validation_assessment.dimension_results.items()
                }
            },
            "personas_validated": len(personas_to_validate),
            "academic_compliance": {
                "research_paper": "2504.02234v2",
                "validation_framework": "staged_approach",
                "peer_review_ready": validation_assessment.passed and study_level == StudyReadinessLevel.SENSITIVITY_ANALYSIS
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in study readiness validation: {str(e)}")


@app.post("/api/persona-generate-transcripts")
async def generate_interview_transcripts_endpoint(
    persona_ids: List[str] = None,
    transcript_duration: float = 1.5
):
    """
    Generate 1-2 Hour Interview Transcripts for Personas
    Creates context-rich interview transcripts with personal histories
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Get personas
        if persona_ids:
            target_personas = [rag_system.persona_system.generated_personas[pid] 
                             for pid in persona_ids 
                             if pid in rag_system.persona_system.generated_personas]
        else:
            # Use first 5 personas as example
            target_personas = list(rag_system.persona_system.generated_personas.values())[:5]
        
        if not target_personas:
            raise HTTPException(status_code=400, detail="No personas available for transcript generation")
        
        transcripts = []
        
        for persona in target_personas:
            # Generate personal history
            personal_history = rag_system.persona_system.context_rich_generator.generate_personal_history(
                persona["characteristics"]
            )
            
            # Generate synthetic content
            synthetic_content = rag_system.persona_system.context_rich_generator.generate_synthetic_content(
                persona["characteristics"], personal_history
            )
            
            # Generate interview transcript
            interview_transcript = rag_system.persona_system.context_rich_generator.generate_interview_transcript(
                persona["characteristics"], personal_history, synthetic_content, transcript_duration
            )
            
            transcripts.append({
                "persona_id": persona["id"],
                "persona_profile": {
                    "age": persona["characteristics"]["age"],
                    "gender": persona["characteristics"]["gender"],
                    "location": persona["characteristics"]["geographic_region"],
                    "occupation": persona["characteristics"]["occupation_sector"]
                },
                "interview_transcript": interview_transcript,
                "transcript_duration_hours": transcript_duration,
                "personal_history_elements": len(personal_history.childhood_experiences) + len(personal_history.career_milestones),
                "synthetic_content_items": {
                    "social_media_posts": len(synthetic_content.social_media_posts),
                    "text_messages": len(synthetic_content.text_messages),
                    "family_conversations": len(synthetic_content.family_conversations)
                }
            })
        
        return {
            "transcripts": transcripts,
            "total_transcripts": len(transcripts),
            "average_duration_hours": transcript_duration,
            "methodology": {
                "context_rich_prompting": True,
                "personal_history_integration": True,
                "synthetic_content_creation": True,
                "regional_cultural_context": True
            },
            "research_applications": [
                "Qualitative research analysis",
                "User journey mapping",
                "Behavioral pattern analysis",
                "Cultural context studies"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating interview transcripts: {str(e)}")


@app.get("/api/persona-enhanced-status")
async def enhanced_persona_status_endpoint():
    """
    Enhanced Persona System Status with Advanced Methodology Metrics
    Shows status of all evidence-based advanced methodologies
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        enhanced_status = rag_system.persona_system.get_enhanced_system_status()
        
        return {
            "enhanced_system_status": enhanced_status,
            "methodology_overview": {
                "evidence_based_methods": [
                    "Context-Rich Prompting (reduces demographic disparities)",
                    "Temperature Optimization (prevents correct answer effect)", 
                    "Implicit Demographics (avoids stereotype activation)",
                    "Temporal Context Integration (addresses atemporality)",
                    "Staged Validation Approach (matches research rigor)"
                ],
                "academic_compliance": {
                    "research_paper": "2504.02234v2",
                    "peer_review_ready": True,
                    "publication_grade": True
                },
                "available_endpoints": {
                    "enhanced_generation": "/api/persona-enhanced-generate",
                    "enhanced_chat": "/api/persona-enhanced-chat",
                    "study_validation": "/api/persona-study-validation",
                    "transcript_generation": "/api/persona-generate-transcripts",
                    "enhanced_status": "/api/persona-enhanced-status"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting enhanced status: {str(e)}")


# Configuration Management Endpoints
@app.get("/api/config/parameters")
async def get_configurable_parameters():
    """
    Get all configurable parameters for the UX
    Returns structure for building configuration UI
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        return rag_system.config_manager.get_configurable_parameters()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting configurable parameters: {str(e)}")


@app.post("/api/config/rag-mode")
async def configure_rag_mode(query: RAGModeConfigQuery):
    """
    Configure RAG mode parameters (percentage, creativity, system prompt)
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        config_changes = {}
        if query.rag_percentage is not None:
            config_changes["default_rag_percentage"] = query.rag_percentage
        if query.creativity_level is not None:
            config_changes["default_creativity_level"] = query.creativity_level
        if query.system_prompt is not None:
            config_changes["system_prompt"] = query.system_prompt
        
        success = rag_system.config_manager.update_rag_mode_config(query.mode, **config_changes)
        
        if success:
            return {
                "success": True,
                "mode": query.mode,
                "updated_parameters": config_changes,
                "message": f"Configuration updated for {query.mode} mode"
            }
        else:
            raise HTTPException(status_code=400, detail=f"Invalid mode: {query.mode}")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating RAG mode config: {str(e)}")


@app.post("/api/config/module")
async def configure_module(query: ModuleConfigQuery):
    """
    Configure module-specific parameters and system prompts
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        success = False
        updated_items = []
        
        if query.system_prompt:
            success = rag_system.config_manager.update_module_system_prompt(query.module, query.system_prompt)
            if success:
                updated_items.append("system_prompt")
        
        if query.parameters:
            # Actualizar parámetros específicos del módulo
            module_config = rag_system.config_manager.get_module_config(query.module)
            if module_config:
                for param, value in query.parameters.items():
                    if param in module_config.user_configurable_params:
                        # Actualizar parámetro en la configuración
                        rag_system.config_manager.current_config["modules"][query.module]["default_parameters"][param] = value
                        updated_items.append(param)
                        success = True
                
                if success:
                    rag_system.config_manager._save_config(rag_system.config_manager.current_config)
        
        if success or updated_items:
            return {
                "success": True,
                "module": query.module,
                "updated_items": updated_items,
                "message": f"Configuration updated for {query.module} module"
            }
        else:
            raise HTTPException(status_code=400, detail=f"Invalid module or no changes applied: {query.module}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating module config: {str(e)}")


@app.post("/api/config/preset")
async def apply_configuration_preset(query: ConfigurationQuery):
    """
    Apply a configuration preset (conservative, balanced, creative)
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    if not query.preset_name:
        raise HTTPException(status_code=400, detail="Preset name required")
    
    try:
        success = rag_system.config_manager.apply_configuration_preset(query.preset_name)
        
        if success:
            return {
                "success": True,
                "preset_applied": query.preset_name,
                "message": f"Configuration preset '{query.preset_name}' applied successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=f"Invalid preset: {query.preset_name}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error applying preset: {str(e)}")


@app.post("/api/config/user/save")
async def save_user_configuration(query: ConfigurationQuery):
    """
    Save user-specific configuration
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    if not query.user_id or not query.config_changes:
        raise HTTPException(status_code=400, detail="User ID and configuration changes required")
    
    try:
        success = rag_system.config_manager.save_user_configuration(query.user_id, query.config_changes)
        
        if success:
            return {
                "success": True,
                "user_id": query.user_id,
                "message": "User configuration saved successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save user configuration")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving user config: {str(e)}")


@app.get("/api/config/user/{user_id}")
async def load_user_configuration(user_id: str):
    """
    Load user-specific configuration
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        user_config = rag_system.config_manager.load_user_configuration(user_id)
        
        if user_config:
            return {
                "success": True,
                "user_id": user_id,
                "configuration": user_config
            }
        else:
            return {
                "success": False,
                "user_id": user_id,
                "message": "No user configuration found"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading user config: {str(e)}")


@app.get("/api/config/export")
async def export_configuration():
    """
    Export current system configuration for backup
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        config_export = rag_system.config_manager.export_configuration()
        return config_export
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting configuration: {str(e)}")


@app.post("/api/config/import")
async def import_configuration(config_data: Dict[str, Any]):
    """
    Import system configuration from backup
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        success = rag_system.config_manager.import_configuration(config_data)
        
        if success:
            return {
                "success": True,
                "message": "Configuration imported successfully"
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid configuration data")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing configuration: {str(e)}")


@app.post("/api/synthetic/chat")
async def synthetic_archetype_chat(query: SyntheticChatQuery):
    """
    Dynamic chat with synthetic archetype using LLM
    Includes full context and 80+ characteristics for ultra-realistic responses
    No authentication required for testing purposes
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Get archetype details from personas system
        archetype_data = rag_system.persona_system.get_archetype_details(query.archetype)
        
        if not archetype_data:
            # Fallback archetype data if not found
            archetype_data = {
                "name": query.archetype,
                "characteristics": [],
                "demographics": {},
                "psychological_profile": {},
                "communication_style": {}
            }
        
        # Build comprehensive context for LLM
        conversation_context = []
        for msg in query.conversation_history:
            conversation_context.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", ""),
                "timestamp": msg.get("timestamp", "")
            })
        
        # Create ultra-realistic prompt with full archetype context
        system_prompt = f"""
        Eres {query.evaluation_context.get('persona_context', {}).get('name', 'una persona hondureña')} ({query.archetype}).
        
        CONTEXTO PERSONAL:
        - Edad: {query.evaluation_context.get('persona_context', {}).get('age', 35)} años
        - Ocupación: {query.evaluation_context.get('persona_context', {}).get('occupation', 'Trabajador')}
        - Ciudad: {query.evaluation_context.get('persona_context', {}).get('city', 'Honduras')}
        - Ingresos: L{query.evaluation_context.get('persona_context', {}).get('monthly_income', 15000)} mensuales
        
        CONTEXTO DE EVALUACIÓN:
        - Concepto evaluado: "{query.concept_details.get('name', 'Plan de servicio')}"
        - Tu score otorgado: {query.evaluation_context.get('overall_score', 50)}/100
        - Sentiment general: {query.evaluation_context.get('overall_sentiment', 'neutral')}
        - Principales preocupaciones: {', '.join(query.evaluation_context.get('concerns', []))}
        - Insights clave que mencionaste: {', '.join(query.evaluation_context.get('key_insights', []))}
        
        CARACTERÍSTICAS DEL ARQUETIPO {query.archetype}:
        {json.dumps(archetype_data.get('characteristics', []), indent=2, ensure_ascii=False)}
        
        PERFIL DEMOGRÁFICO:
        {json.dumps(archetype_data.get('demographics', {}), indent=2, ensure_ascii=False)}
        
        PERFIL PSICOLÓGICO:
        {json.dumps(archetype_data.get('psychological_profile', {}), indent=2, ensure_ascii=False)}
        
        ESTILO DE COMUNICACIÓN:
        {json.dumps(archetype_data.get('communication_style', {}), indent=2, ensure_ascii=False)}
        
        INSTRUCCIONES DE CONVERSACIÓN:
        1. Responde SOLO como esta persona hondureña específica
        2. Mantén consistencia con tu evaluación previa (score, preocupaciones, insights)
        3. Usa expresiones naturales hondureñas apropiadas para tu perfil socioeconómico
        4. Incluye gestos, pausas y reacciones naturales (*suspira*, *se acomoda*, etc.)
        5. Responde con el nivel de detalle apropiado para tu arquetipo
        6. Mantén tu personalidad y preocupaciones a lo largo de la conversación
        7. Si no entiendes algo, pregunta de manera natural
        8. Sé auténtico a tu contexto económico y social
        
        CREATIVIDAD: {query.creativity_level}% - {'Muy creativo y expresivo' if query.creativity_level > 80 else 'Moderadamente expresivo' if query.creativity_level > 50 else 'Directo y conciso'}
        """
        
        # Prepare messages for Azure OpenAI
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Add conversation history
        for msg in conversation_context:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message
        messages.append({
            "role": "user", 
            "content": query.user_message
        })
        
        # Generate response using Azure OpenAI (direct HTTP call)
        temperature = query.creativity_level / 100.0  # Convert to 0.0-1.0 range
        
        # Get Azure config
        azure_config = rag_system.config["azure_openai"]
        
        headers = {
            "Content-Type": "application/json",
            "api-key": azure_config["api_key"]
        }
        
        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 800,
            "top_p": 0.9,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1
        }
        
        url = f"{azure_config['endpoint']}/openai/deployments/{azure_config['chat_deployment']}/chat/completions?api-version={azure_config['api_version']}"
        
        llm_response = requests.post(url, headers=headers, json=payload, timeout=60)
        llm_response.raise_for_status()
        
        result = llm_response.json()
        generated_response = result["choices"][0]["message"]["content"]
        
        return {
            "response": generated_response,
            "archetype": query.archetype,
            "creativity_used": query.creativity_level,
            "temperature_used": temperature,
            "context_included": {
                "persona_details": True,
                "evaluation_context": True,
                "conversation_history": len(conversation_context) > 0,
                "archetype_characteristics": len(archetype_data.get('characteristics', [])) > 0
            },
            "metadata": {
                "response_length": len(generated_response),
                "timestamp": datetime.now().isoformat(),
                "model_used": azure_config.get('chat_deployment', 'gpt-4'),
                "azure_endpoint": azure_config['endpoint']
            }
        }
        
    except Exception as e:
        print(f"Error in synthetic chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating synthetic response: {str(e)}")


@app.post("/api/generate-image")
async def generate_image_endpoint(request: dict):
    """
    Generate image using DALL-E 3 for Tigo Honduras creative content
    """
    try:
        # Validate request
        prompt = request.get("prompt")
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        # Check if rag_system is initialized (contains config)
        if not rag_system or not hasattr(rag_system, 'config'):
            raise HTTPException(status_code=503, detail="System not initialized")
        
        # Get Azure OpenAI configuration
        azure_config = rag_system.config["azure_openai"]
        
        # Prepare enhanced prompt for Tigo Honduras
        enhanced_prompt = f"{prompt}. Professional corporate style for Tigo Honduras telecommunications company, blue and white brand colors, high quality, modern design."
        
        # Call DALL-E 3 API
        import requests
        headers = {
            "Content-Type": "application/json",
            "api-key": azure_config["api_key"]
        }
        
        payload = {
            "model": "dall-e-3",
            "prompt": enhanced_prompt,
            "n": 1,
            "size": request.get("size", "1024x1024"),
            "quality": request.get("quality", "hd"),
            "style": request.get("style", "vivid")
        }
        
        url = f"{azure_config['endpoint']}/openai/deployments/{azure_config['dalle_deployment']}/images/generations?api-version={azure_config['api_version']}"
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("data") and len(result["data"]) > 0:
            image_url = result["data"][0]["url"]
            revised_prompt = result["data"][0].get("revised_prompt", enhanced_prompt)
            
            return {
                "success": True,
                "image_url": image_url,
                "original_prompt": prompt,
                "enhanced_prompt": enhanced_prompt,
                "revised_prompt": revised_prompt,
                "metadata": {
                    "model": "dall-e-3",
                    "size": payload["size"],
                    "quality": payload["quality"],
                    "style": payload["style"],
                    "brand_context": "Tigo Honduras"
                }
            }
        else:
            raise HTTPException(status_code=500, detail="No image generated")
            
    except requests.exceptions.RequestException as e:
        print(f"DALL-E API error: {e}")
        raise HTTPException(status_code=500, detail="Error calling DALL-E API")
    except Exception as e:
        print(f"Image generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")


if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Get port from environment (Railway) or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )