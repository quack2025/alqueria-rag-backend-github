# core/multimodal_processor.py
"""
Multimodal Input Processing for Tigo Honduras RAG System
Handles text, images, and audio inputs using Azure OpenAI
"""

import os
import base64
import json
import tempfile
from typing import Dict, List, Any, Optional, Union
from io import BytesIO
import requests
from PIL import Image
import numpy as np


class MultimodalInputProcessor:
    """
    Process multimodal inputs (text, images, audio) for Tigo Honduras RAG system
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.azure_config = config["azure_openai"]
        self.prompts = config["prompts"]["multimodal"]
        
        # Supported formats
        self.supported_image_formats = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        self.supported_audio_formats = ['.mp3', '.wav', '.m4a', '.ogg']
        
        print("✅ Multimodal Input Processor initialized")
        print(f"   🖼️ Image formats: {', '.join(self.supported_image_formats)}")
        print(f"   🎵 Audio formats: {', '.join(self.supported_audio_formats)}")
    
    def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process multimodal input and return structured data
        
        Args:
            input_data: {
                "text": str,
                "images": List[str] (base64 or file paths),
                "audio": List[str] (base64 or file paths),
                "metadata": Dict[str, Any]
            }
        """
        try:
            processed_data = {
                "text_content": "",
                "image_analyses": [],
                "audio_transcriptions": [],
                "combined_content": "",
                "metadata": input_data.get("metadata", {}),
                "processing_info": {
                    "has_text": False,
                    "has_images": False,
                    "has_audio": False,
                    "total_content_length": 0
                }
            }
            
            # Process text input
            if "text" in input_data and input_data["text"]:
                processed_data["text_content"] = input_data["text"]
                processed_data["processing_info"]["has_text"] = True
            
            # Process image inputs
            if "images" in input_data and input_data["images"]:
                for i, image_input in enumerate(input_data["images"]):
                    try:
                        image_analysis = self._process_image(image_input, f"image_{i}")
                        if image_analysis:
                            processed_data["image_analyses"].append(image_analysis)
                            processed_data["processing_info"]["has_images"] = True
                    except Exception as e:
                        print(f"⚠️ Error processing image {i}: {e}")
            
            # Process audio inputs
            if "audio" in input_data and input_data["audio"]:
                for i, audio_input in enumerate(input_data["audio"]):
                    try:
                        audio_transcription = self._process_audio(audio_input, f"audio_{i}")
                        if audio_transcription:
                            processed_data["audio_transcriptions"].append(audio_transcription)
                            processed_data["processing_info"]["has_audio"] = True
                    except Exception as e:
                        print(f"⚠️ Error processing audio {i}: {e}")
            
            # Combine all content
            processed_data["combined_content"] = self._combine_content(processed_data)
            processed_data["processing_info"]["total_content_length"] = len(processed_data["combined_content"])
            
            return processed_data
            
        except Exception as e:
            print(f"❌ Error in multimodal processing: {e}")
            return {"error": str(e)}
    
    def _process_image(self, image_input: Union[str, bytes], image_id: str) -> Optional[Dict[str, Any]]:
        """Process image input using GPT-4 Vision"""
        try:
            # Handle different image input types
            if isinstance(image_input, str):
                if image_input.startswith('data:image') or image_input.startswith('/9j/'):
                    # Base64 encoded image
                    image_data = image_input
                else:
                    # File path
                    with open(image_input, 'rb') as f:
                        image_bytes = f.read()
                    image_data = base64.b64encode(image_bytes).decode()
            else:
                # Raw bytes
                image_data = base64.b64encode(image_input).decode()
            
            # Prepare for GPT-4 Vision
            if not image_data.startswith('data:image'):
                image_data = f"data:image/jpeg;base64,{image_data}"
            
            # Call GPT-4 Vision
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_config["api_key"]
            }
            
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.prompts["image_analysis"]
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_data
                                }
                            }
                        ]
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 1000
            }
            
            url = f"{self.azure_config['endpoint']}/openai/deployments/{self.azure_config['vision_deployment']}/chat/completions?api-version={self.azure_config['api_version']}"
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            analysis_text = result["choices"][0]["message"]["content"]
            
            return {
                "id": image_id,
                "analysis": analysis_text,
                "type": "image_analysis",
                "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                "confidence": 0.9  # GPT-4V is generally highly confident
            }
            
        except Exception as e:
            print(f"❌ Error processing image {image_id}: {e}")
            return None
    
    def _process_audio(self, audio_input: Union[str, bytes], audio_id: str) -> Optional[Dict[str, Any]]:
        """Process audio input using Whisper"""
        try:
            # Handle different audio input types
            if isinstance(audio_input, str):
                if os.path.exists(audio_input):
                    # File path
                    audio_file_path = audio_input
                    temp_file = False
                else:
                    # Assume base64 encoded audio
                    audio_bytes = base64.b64decode(audio_input)
                    # Create temporary file
                    temp_file = True
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                        tmp.write(audio_bytes)
                        audio_file_path = tmp.name
            else:
                # Raw bytes
                temp_file = True
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                    tmp.write(audio_input)
                    audio_file_path = tmp.name
            
            # Call Whisper API
            headers = {
                "api-key": self.azure_config["api_key"]
            }
            
            url = f"{self.azure_config['endpoint']}/openai/deployments/{self.azure_config['whisper_deployment']}/audio/transcriptions?api-version={self.azure_config['api_version']}"
            
            with open(audio_file_path, 'rb') as audio_file:
                files = {
                    'file': audio_file
                }
                data = {
                    'model': 'whisper-1',
                    'language': 'es',  # Spanish for Tigo Honduras
                    'response_format': 'json',
                    'temperature': 0.0
                }
                
                response = requests.post(url, headers=headers, files=files, data=data, timeout=120)
                response.raise_for_status()
            
            # Clean up temporary file
            if temp_file and os.path.exists(audio_file_path):
                os.unlink(audio_file_path)
            
            result = response.json()
            transcription_text = result.get("text", "")
            
            # Analyze transcription in market research context
            analysis_prompt = f"{self.prompts['audio_transcription']}\n\nTranscripción: {transcription_text}"
            
            analysis = self._analyze_transcription(analysis_prompt)
            
            return {
                "id": audio_id,
                "transcription": transcription_text,
                "analysis": analysis,
                "type": "audio_transcription",
                "language": result.get("language", "es"),
                "confidence": 0.85  # Whisper generally good for Spanish
            }
            
        except Exception as e:
            print(f"❌ Error processing audio {audio_id}: {e}")
            return None
    
    def _analyze_transcription(self, analysis_prompt: str) -> str:
        """Analyze transcription using GPT-4"""
        try:
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_config["api_key"]
            }
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un analista experto en investigación de mercado para Tigo Honduras. Analiza transcripciones de audio para extraer insights relevantes."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 800
            }
            
            url = f"{self.azure_config['endpoint']}/openai/deployments/{self.azure_config['chat_deployment']}/chat/completions?api-version={self.azure_config['api_version']}"
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"❌ Error analyzing transcription: {e}")
            return "Error al analizar la transcripción"
    
    def _combine_content(self, processed_data: Dict[str, Any]) -> str:
        """Combine all processed content into a single searchable text"""
        content_parts = []
        
        # Add text content
        if processed_data["text_content"]:
            content_parts.append(f"=== CONSULTA ORIGINAL ===\n{processed_data['text_content']}")
        
        # Add image analyses
        for img_analysis in processed_data["image_analyses"]:
            content_parts.append(f"=== ANÁLISIS DE IMAGEN ({img_analysis['id']}) ===\n{img_analysis['analysis']}")
        
        # Add audio transcriptions and analyses
        for audio_data in processed_data["audio_transcriptions"]:
            content_parts.append(f"=== TRANSCRIPCIÓN DE AUDIO ({audio_data['id']}) ===\n{audio_data['transcription']}")
            if audio_data["analysis"]:
                content_parts.append(f"=== ANÁLISIS DE AUDIO ({audio_data['id']}) ===\n{audio_data['analysis']}")
        
        return "\n\n".join(content_parts)
    
    def extract_query_intent(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract query intent and suggested metadata filters from processed content"""
        try:
            content = processed_data["combined_content"]
            
            # Use GPT-4 to extract intent and suggest filters
            intent_prompt = f"""Analiza el siguiente contenido multimodal y extrae:

1. Intención principal de la consulta
2. Tipo de estudio más relevante
3. Filtros de metadata sugeridos
4. Palabras clave para búsqueda vectorial

Contenido:
{content[:2000]}

Responde en formato JSON:
{{
  "intent": "descripción de la intención",
  "query_type": "tipo de consulta",
  "suggested_study_types": ["lista", "de", "tipos"],
  "suggested_filters": {{
    "year": {{"gte": 2020}},
    "content_type": ["text", "table"]
  }},
  "search_keywords": ["palabra1", "palabra2"],
  "confidence": 0.8
}}"""
            
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_config["api_key"]
            }
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un experto en análisis de intenciones para sistemas RAG de investigación de mercado."
                    },
                    {
                        "role": "user",
                        "content": intent_prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 500
            }
            
            url = f"{self.azure_config['endpoint']}/openai/deployments/{self.azure_config['chat_deployment']}/chat/completions?api-version={self.azure_config['api_version']}"
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            response_text = result["choices"][0]["message"]["content"]
            
            # Try to parse JSON response
            try:
                if "```json" in response_text:
                    json_str = response_text.split("```json")[1].split("```")[0]
                    intent_data = json.loads(json_str)
                else:
                    intent_data = json.loads(response_text)
                
                return intent_data
                
            except json.JSONDecodeError:
                # Fallback to basic intent extraction
                return {
                    "intent": "Consulta general de investigación de mercado",
                    "query_type": "general",
                    "suggested_study_types": ["general_research"],
                    "suggested_filters": {},
                    "search_keywords": content.split()[:10],
                    "confidence": 0.5
                }
            
        except Exception as e:
            print(f"❌ Error extracting query intent: {e}")
            return {
                "intent": "Error en análisis de intención",
                "query_type": "unknown",
                "suggested_study_types": [],
                "suggested_filters": {},
                "search_keywords": [],
                "confidence": 0.0
            }