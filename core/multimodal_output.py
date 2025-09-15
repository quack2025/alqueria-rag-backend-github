# core/multimodal_output.py
"""
Multimodal Output Generation for Tigo Honduras RAG System
Generates text, images, tables, and charts using Azure OpenAI
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class MultimodalOutputGenerator:
    """
    Generate multimodal outputs (text, images, tables, charts) for Tigo Honduras RAG
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.azure_config = config["azure_openai"]
        self.output_formats = config["output_formats"]
        # COMPATIBILITY FIX: Handle both tigo_context and alqueria_context
        self.tigo_context = config.get("tigo_context", config.get("alqueria_context", {
            "brand_positioning": "Empresa líder",
            "main_competitors": [],
            "key_markets": [],
            "segments": []
        }))
        
        # Tigo brand colors
        self.brand_colors = {
            "primary": "#1E40AF",
            "secondary": "#3B82F6", 
            "accent": "#60A5FA",
            "light": "#93C5FD",
            "background": "#DBEAFE"
        }
        
        print("✅ Multimodal Output Generator initialized")
        print(f"   📊 Chart types: bar, line, pie, scatter, table")
        print(f"   🎨 Brand colors: {len(self.brand_colors)} Tigo colors")
    
    def generate_response(self, 
                         query: str,
                         context: str,
                         mode: str,
                         output_types: List[str] = ["text"]) -> Dict[str, Any]:
        """
        Generate multimodal response based on mode and requested output types
        
        Args:
            query: User query
            context: RAG context from vector search
            mode: "pure", "creative", or "hybrid"
            output_types: List of desired outputs ["text", "image", "table", "chart"]
        """
        try:
            response_data = {
                "text_response": "",
                "visualizations": [],
                "tables": [],
                "charts": [],
                "images": [],
                "metadata": {
                    "mode": mode,
                    "output_types_requested": output_types,
                    "generation_timestamp": datetime.now().isoformat(),
                    "tokens_used": 0
                }
            }
            
            # Generate text response first (always required)
            text_response = self._generate_text_response(query, context, mode)
            response_data["text_response"] = text_response["content"]
            response_data["metadata"]["tokens_used"] += text_response.get("tokens_used", 0)
            
            # Analyze if data visualization would be valuable
            should_visualize = self._should_generate_visualization(query, text_response["content"], mode)
            
            # Generate requested outputs
            for output_type in output_types:
                try:
                    if output_type == "table" and ("table" in query.lower() or should_visualize):
                        table = self._generate_table(query, context, text_response["content"])
                        if table:
                            response_data["tables"].append(table)
                    
                    elif output_type == "chart" and should_visualize:
                        chart = self._generate_chart(query, context, text_response["content"])
                        if chart:
                            response_data["charts"].append(chart)
                    
                    elif output_type == "image" and (mode == "creative" or "imagen" in query.lower()):
                        image = self._generate_image(query, text_response["content"])
                        if image:
                            response_data["images"].append(image)
                
                except Exception as e:
                    print(f"⚠️ Error generating {output_type}: {e}")
            
            # Update metadata
            response_data["metadata"]["visualizations_generated"] = (
                len(response_data["tables"]) + 
                len(response_data["charts"]) + 
                len(response_data["images"])
            )
            
            return response_data
            
        except Exception as e:
            print(f"❌ Error in multimodal response generation: {e}")
            return {"error": str(e)}
    
    def _generate_text_response(self, query: str, context: str, mode: str) -> Dict[str, Any]:
        """Generate text response based on mode"""
        try:
            prompts = self.config["prompts"]
            mode_config = self.config["endpoints"].get(f"rag_{mode}", {})
            
            # Build system prompt
            system_prompt = f"""{prompts['system_base']}

{prompts[f'rag_{mode}']['system']}

CONTEXTO TIGO HONDURAS:
- {self.tigo_context['brand_positioning']}
- Competidores principales: {', '.join(self.tigo_context['main_competitors'])}
- Mercados clave: {', '.join(self.tigo_context['key_markets'])}
- Segmentos: {', '.join(self.tigo_context['segments'])}

{prompts[f'rag_{mode}']['response_format']}"""
            
            # Build user prompt with context
            if context.strip():
                user_prompt = f"""{prompts[f'rag_{mode}']['context_prefix']}
{context}
{prompts[f'rag_{mode}']['context_suffix']}

PREGUNTA: {query}"""
            else:
                user_prompt = f"PREGUNTA: {query}"
            
            # Call Azure OpenAI
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_config["api_key"]
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": mode_config.get("creativity_level", 0.1),
                "max_tokens": self.azure_config["max_tokens"],
                "top_p": 0.95
            }
            
            url = f"{self.azure_config['endpoint']}/openai/deployments/{self.azure_config['chat_deployment']}/chat/completions?api-version={self.azure_config['api_version']}"
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "content": result["choices"][0]["message"]["content"],
                "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                "model": self.azure_config["chat_model"]
            }
            
        except Exception as e:
            print(f"❌ Error generating text response: {e}")
            return {"content": f"Error generando respuesta: {str(e)}", "tokens_used": 0}
    
    def _should_generate_visualization(self, query: str, response: str, mode: str) -> bool:
        """Determine if visualization would be valuable"""
        if mode == "pure":
            return False
        
        # Check for quantitative indicators
        text_to_check = (query + " " + response).lower()
        
        quantitative_indicators = [
            '%', 'porcentaje', 'gráfico', 'comparación', 'tendencia', 'evolución',
            'datos', 'estadística', 'métrica', 'cifra', 'número', 'cantidad',
            'ranking', 'top', 'mayor', 'menor', 'crecimiento', 'declive',
            'tabla', 'chart', 'visualizar', 'mostrar'
        ]
        
        # Check for numbers and percentages
        has_numbers = bool(re.search(r'\d+%|\d+\.\d+%|\d+,\d+', text_to_check))
        has_quantitative = any(indicator in text_to_check for indicator in quantitative_indicators)
        
        # Count data points
        percentage_count = len(re.findall(r'\d+%', text_to_check))
        
        return (has_numbers and percentage_count >= 2) or has_quantitative
    
    def _generate_table(self, query: str, context: str, response: str) -> Optional[Dict[str, Any]]:
        """Generate structured table from data"""
        try:
            table_prompt = f"""Extrae datos cuantitativos del siguiente análisis y crea una tabla estructurada para Tigo Honduras.

CONTEXTO: {context[:1000]}
ANÁLISIS: {response[:1000]}
CONSULTA: {query}

Genera una tabla en formato JSON con:
- Título descriptivo
- Columnas apropiadas
- Datos numéricos cuando sea posible
- Totales o resúmenes si es relevante

Formato de respuesta:
{{
  "title": "Título de la tabla",
  "headers": ["Columna 1", "Columna 2", "Columna 3"],
  "rows": [
    ["Dato 1", "Dato 2", "Dato 3"],
    ["Dato 4", "Dato 5", "Dato 6"]
  ],
  "footer": "Información adicional o totales",
  "insights": "Insights clave de los datos"
}}"""
            
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_config["api_key"]
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": "Eres experto en estructuración de datos para investigación de mercado."},
                    {"role": "user", "content": table_prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 800
            }
            
            url = f"{self.azure_config['endpoint']}/openai/deployments/{self.azure_config['chat_deployment']}/chat/completions?api-version={self.azure_config['api_version']}"
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            response_text = result["choices"][0]["message"]["content"]
            
            # Parse JSON response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0]
                table_data = json.loads(json_str)
            else:
                table_data = json.loads(response_text)
            
            # Add metadata
            table_data["type"] = "data_table"
            table_data["generated_at"] = datetime.now().isoformat()
            table_data["source"] = "tigo_rag_analysis"
            
            return table_data
            
        except Exception as e:
            print(f"❌ Error generating table: {e}")
            return None
    
    def _generate_chart(self, query: str, context: str, response: str) -> Optional[Dict[str, Any]]:
        """Generate chart configuration and data"""
        try:
            chart_prompt = f"""Extrae datos para crear un gráfico profesional basado en el análisis para Tigo Honduras.

CONTEXTO: {context[:1000]}
ANÁLISIS: {response[:1000]}
CONSULTA: {query}

Crea configuración de gráfico en formato JSON:
{{
  "title": "Título del gráfico",
  "chart_type": "bar|line|pie|scatter",
  "data": {{
    "labels": ["Etiqueta 1", "Etiqueta 2"],
    "datasets": [{{
      "label": "Serie de datos",
      "data": [45, 30, 25],
      "backgroundColor": ["{self.brand_colors['primary']}", "{self.brand_colors['secondary']}"]
    }}]
  }},
  "insights": "Insights clave del gráfico",
  "recommendation": "Recomendación basada en los datos"
}}"""
            
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_config["api_key"]
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": "Eres experto en visualización de datos para investigación de mercado."},
                    {"role": "user", "content": chart_prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 800
            }
            
            url = f"{self.azure_config['endpoint']}/openai/deployments/{self.azure_config['chat_deployment']}/chat/completions?api-version={self.azure_config['api_version']}"
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            response_text = result["choices"][0]["message"]["content"]
            
            # Parse JSON response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0]
                chart_data = json.loads(json_str)
            else:
                chart_data = json.loads(response_text)
            
            # Add Chart.js configuration
            chart_data["chartjs_config"] = self._generate_chartjs_config(chart_data)
            chart_data["type"] = "data_chart"
            chart_data["generated_at"] = datetime.now().isoformat()
            
            return chart_data
            
        except Exception as e:
            print(f"❌ Error generating chart: {e}")
            return None
    
    def _generate_chartjs_config(self, chart_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Chart.js configuration"""
        chart_type = chart_data.get("chart_type", "bar")
        
        return {
            "type": chart_type,
            "data": chart_data.get("data", {}),
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": chart_data.get("title", "Datos Tigo Honduras"),
                        "color": self.brand_colors["primary"]
                    },
                    "legend": {
                        "display": True,
                        "position": "top"
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "grid": {"color": "#E5E7EB"},
                        "ticks": {"color": "#6B7280"}
                    },
                    "x": {
                        "grid": {"color": "#E5E7EB"},
                        "ticks": {"color": "#6B7280"}
                    }
                } if chart_type in ["bar", "line"] else {}
            }
        }
    
    def _generate_image(self, query: str, response: str) -> Optional[Dict[str, Any]]:
        """Generate image using DALL-E 3"""
        try:
            # Create image prompt based on query and response
            image_prompt = f"""Crea una infografía profesional para Tigo Honduras mostrando: {query}

Basándote en este análisis: {response[:500]}

Estilo: Infografía corporativa moderna, colores azules de Tigo, diseño limpio y profesional, incluye datos visuales, gráficos simples, logo placement area.

Elementos a incluir:
- Datos clave en formato visual
- Colores corporativos azules
- Diseño moderno y limpio
- Espacio para branding Tigo"""
            
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_config["api_key"]
            }
            
            payload = {
                "prompt": image_prompt,
                "size": self.output_formats["image"]["size"],
                "quality": self.output_formats["image"]["quality"],
                "style": "vivid",
                "response_format": "url"
            }
            
            url = f"{self.azure_config['endpoint']}/openai/deployments/{self.azure_config['dalle_deployment']}/images/generations?api-version={self.azure_config['api_version']}"
            
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "type": "generated_image",
                "url": result["data"][0]["url"],
                "prompt": image_prompt,
                "generated_at": datetime.now().isoformat(),
                "model": "dall-e-3"
            }
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return None
    
    def format_response_for_api(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format response data for API consumption"""
        formatted = {
            "answer": response_data.get("text_response", ""),
            "visualizations": {
                "tables": response_data.get("tables", []),
                "charts": response_data.get("charts", []),
                "images": response_data.get("images", [])
            },
            "metadata": response_data.get("metadata", {}),
            "has_visualizations": len(response_data.get("tables", [])) + len(response_data.get("charts", [])) + len(response_data.get("images", [])) > 0
        }
        
        return formatted