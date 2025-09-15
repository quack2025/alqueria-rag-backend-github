# core/prompt_manager.py
"""
Configurable Prompt Management System for Tigo Honduras RAG
Allows dynamic prompt configuration with metadata filtering
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class PromptManager:
    """
    Manage configurable prompts with metadata-based filtering and customization
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_prompts = config["prompts"]
        # COMPATIBILITY FIX: Handle both tigo_context and alqueria_context
        self.tigo_context = config.get("tigo_context", config.get("alqueria_context", {
            "brand_positioning": "Empresa líder",
            "main_competitors": [],
            "key_markets": [],
            "segments": []
        }))
        self.metadata_filters = config["metadata_filters"]
        
        # Custom prompt templates storage
        self.custom_prompts = {}
        self.prompt_history = []
        
        # Load custom prompts if they exist
        self._load_custom_prompts()
        
        print("✅ Prompt Manager initialized")
        print(f"   📝 Base prompts: {len(self.base_prompts)} categories")
        print(f"   🎯 Custom prompts: {len(self.custom_prompts)} loaded")
    
    def _load_custom_prompts(self):
        """Load custom prompts from file"""
        custom_prompts_path = "config/custom_prompts.json"
        try:
            if os.path.exists(custom_prompts_path):
                with open(custom_prompts_path, 'r', encoding='utf-8') as f:
                    self.custom_prompts = json.load(f)
                print(f"✅ Loaded custom prompts from {custom_prompts_path}")
        except Exception as e:
            print(f"⚠️ Could not load custom prompts: {e}")
    
    def save_custom_prompts(self):
        """Save custom prompts to file"""
        try:
            os.makedirs("config", exist_ok=True)
            with open("config/custom_prompts.json", 'w', encoding='utf-8') as f:
                json.dump(self.custom_prompts, f, ensure_ascii=False, indent=2)
            print("✅ Custom prompts saved")
        except Exception as e:
            print(f"❌ Error saving custom prompts: {e}")
    
    def get_system_prompt(self, 
                         mode: str,
                         metadata_context: Optional[Dict[str, Any]] = None,
                         custom_context: Optional[str] = None) -> str:
        """
        Generate system prompt based on mode and metadata context
        
        Args:
            mode: "pure", "creative", or "hybrid"
            metadata_context: Context from retrieved documents metadata
            custom_context: Additional custom context
        """
        try:
            # Base system prompt
            base_prompt = self.base_prompts["system_base"]
            
            # Mode-specific prompt
            mode_prompt = self.base_prompts.get(f"rag_{mode}", {}).get("system", "")
            
            # Build Tigo context
            tigo_context_text = self._build_tigo_context(metadata_context)
            
            # Build metadata-aware context
            metadata_context_text = self._build_metadata_context(metadata_context)
            
            # Combine all parts
            system_prompt_parts = [
                base_prompt,
                "",
                mode_prompt,
                "",
                "CONTEXTO TIGO HONDURAS:",
                tigo_context_text,
            ]
            
            if metadata_context_text:
                system_prompt_parts.extend([
                    "",
                    "CONTEXTO DE DOCUMENTOS DISPONIBLES:",
                    metadata_context_text
                ])
            
            if custom_context:
                system_prompt_parts.extend([
                    "",
                    "CONTEXTO ADICIONAL:",
                    custom_context
                ])
            
            # Add response format
            response_format = self.base_prompts.get(f"rag_{mode}", {}).get("response_format", "")
            if response_format:
                system_prompt_parts.extend([
                    "",
                    "FORMATO DE RESPUESTA:",
                    response_format
                ])
            
            return "\n".join(system_prompt_parts)
            
        except Exception as e:
            print(f"❌ Error generating system prompt: {e}")
            return self.base_prompts["system_base"]
    
    def _build_tigo_context(self, metadata_context: Optional[Dict[str, Any]] = None) -> str:
        """Build Tigo Honduras specific context"""
        context_parts = [
            f"- {self.tigo_context['brand_positioning']}",
            f"- Competidores principales: {', '.join(self.tigo_context['main_competitors'])}",
            f"- Mercados clave: {', '.join(self.tigo_context['key_markets'])}",
            f"- Segmentos: {', '.join(self.tigo_context['segments'])}"
        ]
        
        # Add relevant brand attributes based on context
        if metadata_context:
            study_types = metadata_context.get("study_types", [])
            if "brand_health" in study_types or "communication_test" in study_types:
                context_parts.append(f"- Atributos clave: {', '.join(self.tigo_context['brand_attributes'])}")
            
            if "segmentation" in study_types or "usage_attitudes" in study_types:
                context_parts.append("- Insights de consumidor:")
                for insight in self.tigo_context['consumer_insights']:
                    context_parts.append(f"  • {insight}")
        
        return "\n".join(context_parts)
    
    def _build_metadata_context(self, metadata_context: Optional[Dict[str, Any]] = None) -> str:
        """Build context from document metadata"""
        if not metadata_context:
            return ""
        
        context_parts = []
        
        # Study types available
        study_types = metadata_context.get("study_types", [])
        if study_types:
            context_parts.append(f"Tipos de estudio disponibles: {', '.join(study_types)}")
        
        # Years covered
        years = metadata_context.get("years", [])
        if years:
            context_parts.append(f"Período temporal: {min(years)}-{max(years)}")
        
        # Content types
        content_types = metadata_context.get("content_types", [])
        if content_types:
            context_parts.append(f"Tipos de contenido: {', '.join(content_types)}")
        
        # Document count
        doc_count = metadata_context.get("document_count", 0)
        if doc_count:
            context_parts.append(f"Documentos disponibles: {doc_count}")
        
        return "\n".join(context_parts)
    
    def get_user_prompt(self, 
                       mode: str,
                       query: str,
                       context: str,
                       metadata_info: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate user prompt with context and query
        """
        try:
            mode_config = self.base_prompts.get(f"rag_{mode}", {})
            
            context_prefix = mode_config.get("context_prefix", "=== CONTEXTO ===")
            context_suffix = mode_config.get("context_suffix", "=== FIN DEL CONTEXTO ===")
            
            prompt_parts = []
            
            # Add context if available
            if context.strip():
                prompt_parts.extend([
                    context_prefix,
                    context,
                    context_suffix,
                    ""
                ])
            
            # Add metadata information if available
            if metadata_info:
                citations = metadata_info.get("citations", [])
                if citations:
                    prompt_parts.append("FUENTES DE INFORMACIÓN:")
                    for i, citation in enumerate(citations, 1):
                        prompt_parts.append(f"{i}. {citation.get('document', 'Unknown')} ({citation.get('year', 'N/A')}) - {citation.get('study_type', 'Unknown')}")
                    prompt_parts.append("")
            
            # Add the actual query
            prompt_parts.append(f"PREGUNTA: {query}")
            
            return "\n".join(prompt_parts)
            
        except Exception as e:
            print(f"❌ Error generating user prompt: {e}")
            return f"PREGUNTA: {query}"
    
    def create_custom_prompt(self, 
                           name: str,
                           prompt_data: Dict[str, Any],
                           metadata_filters: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create custom prompt template
        
        Args:
            name: Unique name for the prompt
            prompt_data: Prompt configuration
            metadata_filters: When to use this prompt (optional)
        """
        try:
            custom_prompt = {
                "name": name,
                "created_at": datetime.now().isoformat(),
                "prompt_data": prompt_data,
                "metadata_filters": metadata_filters or {},
                "usage_count": 0,
                "last_used": None
            }
            
            self.custom_prompts[name] = custom_prompt
            self.save_custom_prompts()
            
            print(f"✅ Custom prompt created: {name}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating custom prompt: {e}")
            return False
    
    def get_best_prompt_for_context(self, 
                                   mode: str,
                                   metadata_context: Dict[str, Any]) -> str:
        """
        Get the best prompt template based on context metadata
        """
        try:
            # Check if any custom prompts match the context
            for prompt_name, prompt_config in self.custom_prompts.items():
                if self._matches_metadata_filters(metadata_context, prompt_config.get("metadata_filters", {})):
                    # Update usage statistics
                    prompt_config["usage_count"] = prompt_config.get("usage_count", 0) + 1
                    prompt_config["last_used"] = datetime.now().isoformat()
                    
                    print(f"🎯 Using custom prompt: {prompt_name}")
                    return self._build_custom_system_prompt(prompt_config, mode, metadata_context)
            
            # Fall back to default prompts
            return self.get_system_prompt(mode, metadata_context)
            
        except Exception as e:
            print(f"❌ Error getting best prompt: {e}")
            return self.get_system_prompt(mode, metadata_context)
    
    def _matches_metadata_filters(self, 
                                 context: Dict[str, Any], 
                                 filters: Dict[str, Any]) -> bool:
        """Check if context matches metadata filters"""
        try:
            for filter_key, filter_value in filters.items():
                context_value = context.get(filter_key)
                
                if isinstance(filter_value, list):
                    if context_value not in filter_value:
                        return False
                elif isinstance(filter_value, dict):
                    # Range filters
                    if "gte" in filter_value and context_value < filter_value["gte"]:
                        return False
                    if "lte" in filter_value and context_value > filter_value["lte"]:
                        return False
                else:
                    # Exact match
                    if context_value != filter_value:
                        return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error matching metadata filters: {e}")
            return False
    
    def _build_custom_system_prompt(self, 
                                   prompt_config: Dict[str, Any],
                                   mode: str,
                                   metadata_context: Dict[str, Any]) -> str:
        """Build system prompt from custom configuration"""
        try:
            prompt_data = prompt_config["prompt_data"]
            
            # Start with base or custom system prompt
            if "system_base" in prompt_data:
                base_prompt = prompt_data["system_base"]
            else:
                base_prompt = self.base_prompts["system_base"]
            
            # Add mode-specific instructions
            if f"rag_{mode}" in prompt_data:
                mode_instructions = prompt_data[f"rag_{mode}"]
            else:
                mode_instructions = self.base_prompts.get(f"rag_{mode}", {}).get("system", "")
            
            # Build Tigo context
            tigo_context = self._build_tigo_context(metadata_context)
            
            # Combine
            prompt_parts = [
                base_prompt,
                "",
                mode_instructions,
                "",
                "CONTEXTO TIGO HONDURAS:",
                tigo_context
            ]
            
            # Add custom context if provided
            if "custom_context" in prompt_data:
                prompt_parts.extend([
                    "",
                    "CONTEXTO PERSONALIZADO:",
                    prompt_data["custom_context"]
                ])
            
            return "\n".join(prompt_parts)
            
        except Exception as e:
            print(f"❌ Error building custom system prompt: {e}")
            return self.get_system_prompt(mode, metadata_context)
    
    def get_prompt_analytics(self) -> Dict[str, Any]:
        """Get analytics about prompt usage"""
        try:
            total_custom = len(self.custom_prompts)
            used_prompts = sum(1 for p in self.custom_prompts.values() if p.get("usage_count", 0) > 0)
            
            usage_stats = {}
            for name, config in self.custom_prompts.items():
                usage_stats[name] = {
                    "usage_count": config.get("usage_count", 0),
                    "last_used": config.get("last_used"),
                    "created_at": config.get("created_at")
                }
            
            return {
                "total_custom_prompts": total_custom,
                "used_custom_prompts": used_prompts,
                "base_prompts": len(self.base_prompts),
                "usage_statistics": usage_stats,
                "most_used": max(usage_stats.items(), key=lambda x: x[1]["usage_count"])[0] if usage_stats else None
            }
            
        except Exception as e:
            print(f"❌ Error getting prompt analytics: {e}")
            return {"error": str(e)}