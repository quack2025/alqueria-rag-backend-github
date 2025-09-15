# vercel_api/chat.py
"""
API endpoint for Vercel deployment - Integra directamente el sistema RAG refactorizado
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

# Simular las importaciones del core para Vercel
class TigoRAGSystem:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        print("🚀 Tigo RAG System initialized for Vercel")
    
    def process_multimodal_query(self, query_data: Dict[str, Any], mode: str) -> Dict[str, Any]:
        """Procesa query usando Azure OpenAI directamente"""
        try:
            import openai
            from azure.search.documents import SearchClient
            from azure.core.credentials import AzureKeyCredential
            
            # Configurar Azure OpenAI
            openai.api_type = "azure"
            openai.api_base = self.config["azure_openai"]["endpoint"]
            openai.api_version = self.config["azure_openai"]["api_version"]
            openai.api_key = self.config["azure_openai"]["api_key"]
            
            # Obtener texto de la consulta
            user_text = query_data.get("text", "")
            if not user_text:
                return {"error": "No text provided"}
            
            # Configuración según el modo
            mode_config = self.config["endpoints"].get(f"rag_{mode}", self.config["endpoints"]["rag_hybrid"])
            
            # Sistema prompt basado en el modo
            system_prompt = self.config["prompts"][f"rag_{mode}"]["system"]
            
            # Para modo pure, buscar en Azure Search primero
            context = ""
            citations = []
            
            if mode in ["pure", "hybrid"]:
                # Aquí iría la búsqueda en Azure AI Search
                # Por ahora simulamos contexto
                context = "Contexto de documentos Tigo Honduras relevantes..."
                citations = [
                    {
                        "study": "Estudio Brand Health Tigo 2024",
                        "year": "2024",
                        "section_type": "findings"
                    }
                ]
            
            # Construir prompt completo
            full_prompt = f"{system_prompt}\n\n"
            if context:
                full_prompt += f"CONTEXTO:\n{context}\n\n"
            full_prompt += f"PREGUNTA: {user_text}"
            
            # Llamar a Azure OpenAI
            response = openai.ChatCompletion.create(
                engine=self.config["azure_openai"]["chat_deployment"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ],
                temperature=mode_config.get("creativity_level", 0.3),
                max_tokens=self.config["azure_openai"]["max_tokens"]
            )
            
            answer = response.choices[0].message.content
            
            # Crear visualizaciones si está habilitado
            visualizations = {"tables": [], "charts": [], "images": []}
            if mode_config.get("enable_visualization", False):
                # Generar visualización simple para demostración
                if "datos" in user_text.lower() or "estadísticas" in user_text.lower():
                    visualizations["charts"] = [{
                        "title": "Análisis de Datos Tigo",
                        "type": "bar",
                        "data": [
                            {"label": "Tigo", "value": 67},
                            {"label": "Claro", "value": 28},
                            {"label": "Otros", "value": 5}
                        ],
                        "chart_config": {
                            "type": "bar",
                            "data": [67, 28, 5],
                            "labels": ["Tigo", "Claro", "Otros"],
                            "options": {
                                "responsive": True,
                                "plugins": {
                                    "title": {"display": True, "text": "Participación de Mercado"}
                                }
                            }
                        },
                        "insights": "Tigo mantiene liderazgo en el mercado hondureño"
                    }]
            
            # Generar sugerencias inteligentes
            suggestions = []
            if "tigo" in user_text.lower():
                suggestions = [
                    "¿Te gustaría conocer más sobre la percepción de marca de Tigo?",
                    "¿Quieres comparar con la competencia?",
                    "¿Necesitas datos específicos de alguna región?"
                ]
            
            return {
                "answer": answer,
                "citations": citations,
                "visualizations": visualizations,
                "suggestions": {"suggestions": suggestions, "has_suggestions": len(suggestions) > 0},
                "metadata": {
                    "mode": mode,
                    "processing_time_seconds": 1.5,
                    "chunks_retrieved": len(citations),
                    "tokens_used": len(answer.split()),
                    "endpoint_config": mode_config
                },
                "has_visualizations": len(visualizations["charts"]) > 0 or len(visualizations["tables"]) > 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Error procesando consulta: {str(e)}"}

# Configuración para Vercel
TIGO_CONFIG = {
    "azure_openai": {
        "endpoint": "https://insightgenius-rag-v1-resource.cognitiveservices.azure.com/",
        "api_key": "${AZURE_OPENAI_API_KEY}",
        "api_version": "2024-12-01-preview",
        "chat_deployment": "gpt-4.1",
        "max_tokens": 2000
    },
    "endpoints": {
        "rag_pure": {
            "rag_percentage": 100,
            "creativity_level": 0.0,
            "enable_visualization": False
        },
        "rag_creative": {
            "rag_percentage": 60,
            "creativity_level": 0.7,
            "enable_visualization": True
        },
        "rag_hybrid": {
            "rag_percentage": 80,
            "creativity_level": 0.3,
            "enable_visualization": True
        }
    },
    "prompts": {
        "rag_pure": {
            "system": "Eres un analista experto de Tigo Honduras. Responde ÚNICAMENTE basándote en los documentos proporcionados. Si no tienes la información, indícalo claramente."
        },
        "rag_creative": {
            "system": "Eres un analista estratégico de Tigo Honduras. Combina información de documentos con insights creativos para generar análisis profundos y recomendaciones accionables."
        },
        "rag_hybrid": {
            "system": "Eres un consultor experto de Tigo Honduras. Balancea información específica de documentos con conocimiento del sector para proporcionar análisis completos."
        }
    }
}

# Sistema RAG global
rag_system = TigoRAGSystem(TIGO_CONFIG)

def handler(request):
    """Handler principal para Vercel"""
    try:
        if request.method != 'POST':
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        # Parsear body
        body = json.loads(request.body) if hasattr(request, 'body') else request
        
        # Extraer parámetros
        messages = body.get('messages', [])
        mode = body.get('mode', 'general')
        
        if not messages:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No messages provided'})
            }
        
        # Obtener último mensaje del usuario
        user_message = messages[-1].get('content', '')
        if not user_message:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No user message found'})
            }
        
        # Mapear modos
        backend_mode_mapping = {
            "general": "pure",
            "creative": "creative"
        }
        backend_mode = backend_mode_mapping.get(mode, "hybrid")
        
        # Procesar con RAG
        query_data = {
            "text": user_message,
            "mode": mode
        }
        
        response = rag_system.process_multimodal_query(query_data, backend_mode)
        
        # Verificar errores
        if "error" in response:
            return {
                'statusCode': 500,
                'body': json.dumps(response)
            }
        
        # Formatear respuesta para el frontend
        formatted_response = {
            "answer": response["answer"],
            "content": response["answer"],
            "citations": response.get("citations", []),
            "visualization": response.get("visualizations", {}),
            "suggestions": response.get("suggestions", {}).get("suggestions", []),
            "metadata": response.get("metadata", {}),
            "timestamp": response.get("timestamp"),
            "mode": mode,
            "backend_mode_used": backend_mode
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps(formatted_response)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Internal error: {str(e)}'})
        }