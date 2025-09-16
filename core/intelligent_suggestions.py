# core/intelligent_suggestions.py
"""
Sistema de Sugerencias Inteligentes para RAG de Alquería Colombia
Propone acciones de seguimiento basadas en el contenido de la respuesta
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class IntelligentSuggestionEngine:
    """
    Motor de sugerencias inteligentes que analiza respuestas RAG
    y propone acciones de seguimiento relevantes
    """
    
    def __init__(self):
        # Patrones para detectar contenido visualizable
        self.visualization_patterns = {
            "demographics": [
                r"(\d+%.*?(años|edad))",
                r"(hombres?.*?\d+%)",
                r"(mujeres?.*?\d+%)",
                r"(género.*?\d+%)",
                r"(masculino.*?\d+%)",
                r"(femenino.*?\d+%)"
            ],
            "geographic": [
                r"(Bogotá.*?\d+%)",
                r"(Medellín.*?\d+%)",
                r"(Cali.*?\d+%)",
                r"(Costa Atlántica.*?\d+%)",
                r"(Eje Cafetero.*?\d+%)",
                r"(ciudades?.*?\d+%)",
                r"(región.*?\d+%)"
            ],
            "market_share": [
                r"(Alquería.*?\d+%)",
                r"(Alpina.*?\d+%)",
                r"(Colanta.*?\d+%)",
                r"(competencia.*?\d+%)",
                r"(marca.*?\d+%)",
                r"(liderazgo.*?\d+%)"
            ],
            "products": [
                r"(leche.*?\d+%)",
                r"(yogurt.*?\d+%)",
                r"(queso.*?\d+%)",
                r"(mantequilla.*?\d+%)",
                r"(crema.*?\d+%)",
                r"(lácteo.*?\d+%)"
            ],
            "nutrition": [
                r"(proteína.*?\d+%)",
                r"(probiótico.*?\d+%)",
                r"(deslactosad.*?\d+%)",
                r"(orgánic.*?\d+%)",
                r"(natural.*?\d+%)",
                r"(funcional.*?\d+%)"
            ]
        }
        
        # Palabras clave para detectar temas profundizables
        self.deep_dive_keywords = {
            "competition": ["alpina", "colanta", "parmalat", "nestlé", "danone", "competencia", "vs", "comparación"],
            "demographics": ["jóvenes", "edad", "género", "segmento", "consumidor", "hogares", "familias"],
            "geography": ["bogotá", "medellín", "cali", "costa atlántica", "eje cafetero", "región", "colombia"],
            "products": ["leche", "yogurt", "yogur", "queso", "lácteo", "mantequilla", "crema", "arequipe", "kumis"],
            "nutrition": ["proteína", "probiótico", "deslactosada", "orgánico", "natural", "funcional", "calcio", "vitamina"],
            "marketing": ["campaña", "publicidad", "recordación", "mensaje", "marca", "tradición", "premium"],
            "satisfaction": ["satisfacción", "experiencia", "calidad", "percepción", "premium", "frescura"],
            "sustainability": ["sostenible", "sostenibilidad", "orgánico", "natural", "ecológico", "carbono neutro"]
        }
        
        # Templates de sugerencias
        self.suggestion_templates = {
            "visualization": {
                "pie_chart": "¿Te gustaría que genere un gráfico de torta mostrando la {topic}?",
                "bar_chart": "¿Quieres un gráfico de barras comparativo de {topic}?", 
                "line_chart": "¿Te interesa ver un gráfico de tendencia temporal de {topic}?",
                "table": "¿Necesitas una tabla detallada con los datos de {topic}?"
            },
            "deep_dive": {
                "competition": "¿Quieres profundizar en el análisis competitivo con Alpina y Colanta?",
                "demographics": "¿Te interesa un análisis más detallado del perfil demográfico?",
                "geography": "¿Quieres explorar las diferencias regionales en más detalle?",
                "products": "¿Necesitas comparar el desempeño de diferentes productos lácteos?",
                "nutrition": "¿Te gustaría analizar los aspectos nutricionales y funcionales en profundidad?",
                "marketing": "¿Quieres revisar el performance de campañas específicas?",
                "satisfaction": "¿Te interesa analizar drivers de satisfacción del cliente?",
                "sustainability": "¿Quieres explorar oportunidades de sostenibilidad en el portafolio lácteo?"
            },
            "related_queries": {
                "competition": [
                    "¿Cuáles son las ventajas competitivas de Alquería vs Alpina y Colanta?",
                    "¿Cómo perciben los consumidores la calidad de los productos lácteos de cada marca?",
                    "¿Qué estrategias de precio están usando los competidores en lácteos premium?"
                ],
                "demographics": [
                    "¿Cómo varían las preferencias de lácteos por grupo de edad?",
                    "¿Hay diferencias de consumo lácteo entre hombres y mujeres?",
                    "¿Qué segmentos tienen mayor potencial de crecimiento en lácteos funcionales?"
                ],
                "geography": [
                    "¿Cuál es la penetración de productos Alquería por ciudad colombiana?",
                    "¿Hay diferencias de preferencias lácteas entre regiones?",
                    "¿Dónde están las mayores oportunidades de expansión para lácteos premium?"
                ],
                "products": [
                    "¿Qué productos lácteos tienen mayor potencial de innovación?",
                    "¿Cómo se compara el desempeño de leche vs yogurt vs quesos?",
                    "¿Qué nuevas categorías lácteas podría explorar Alquería?"
                ],
                "nutrition": [
                    "¿Qué beneficios nutricionales valoran más los consumidores?",
                    "¿Hay oportunidad en lácteos funcionales con probióticos?",
                    "¿Cómo está evolucionando la demanda de productos deslactosados?"
                ],
                "sustainability": [
                    "¿Qué iniciativas de sostenibilidad valoran los consumidores?",
                    "¿Cómo puede Alquería liderar en lácteos sostenibles?",
                    "¿Hay oportunidad en empaques eco-amigables para lácteos?"
                ]
            }
        }
    
    def analyze_response(self, answer: str, citations: List[Dict], metadata: Dict) -> Dict[str, Any]:
        """
        Analiza una respuesta RAG y genera sugerencias inteligentes
        """
        suggestions = {
            "visualizations": self._suggest_visualizations(answer),
            "deep_dive": self._suggest_deep_dive(answer, citations),
            "related_queries": self._suggest_related_queries(answer),
            "follow_up_actions": self._suggest_follow_up_actions(answer, metadata)
        }
        
        return self._format_suggestions(suggestions)
    
    def _suggest_visualizations(self, answer: str) -> List[Dict[str, Any]]:
        """Sugiere visualizaciones basadas en el contenido"""
        viz_suggestions = []
        
        for viz_type, patterns in self.visualization_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, answer.lower(), re.IGNORECASE)
                if matches:
                    # Detectar tipo de gráfico más apropiado
                    if "%" in answer and len(matches) >= 2:
                        if viz_type == "demographics":
                            viz_suggestions.append({
                                "type": "pie_chart",
                                "title": "Distribución Demográfica",
                                "description": f"¿Te gustaría ver un gráfico de torta mostrando la distribución demográfica?",
                                "data_detected": matches[:5],
                                "priority": "high"
                            })
                        elif viz_type == "geographic":
                            viz_suggestions.append({
                                "type": "bar_chart", 
                                "title": "Distribución Geográfica",
                                "description": f"¿Quieres un gráfico de barras con la distribución por ciudades?",
                                "data_detected": matches[:5],
                                "priority": "high"
                            })
                        elif viz_type == "market_share":
                            viz_suggestions.append({
                                "type": "pie_chart",
                                "title": "Market Share",
                                "description": f"¿Te interesa ver un gráfico de participación de mercado?",
                                "data_detected": matches[:5],
                                "priority": "medium"
                            })
        
        return viz_suggestions[:3]  # Máximo 3 sugerencias
    
    def _suggest_deep_dive(self, answer: str, citations: List[Dict]) -> List[Dict[str, Any]]:
        """Sugiere análisis más profundos"""
        deep_dive_suggestions = []
        
        for topic, keywords in self.deep_dive_keywords.items():
            keyword_count = sum(1 for keyword in keywords if keyword in answer.lower())
            
            if keyword_count >= 2:  # Al menos 2 keywords del tema
                template = self.suggestion_templates["deep_dive"].get(topic)
                if template:
                    deep_dive_suggestions.append({
                        "topic": topic,
                        "description": template,
                        "relevance_score": keyword_count,
                        "available_studies": len([c for c in citations if any(kw in c.get("document", "").lower() for kw in keywords)])
                    })
        
        # Ordenar por relevancia
        deep_dive_suggestions.sort(key=lambda x: x["relevance_score"], reverse=True)
        return deep_dive_suggestions[:2]  # Máximo 2 sugerencias
    
    def _suggest_related_queries(self, answer: str) -> List[Dict[str, Any]]:
        """Sugiere consultas relacionadas"""
        related_suggestions = []
        
        for topic, keywords in self.deep_dive_keywords.items():
            if any(keyword in answer.lower() for keyword in keywords):
                queries = self.suggestion_templates["related_queries"].get(topic, [])
                if queries:
                    related_suggestions.extend([
                        {
                            "query": query,
                            "topic": topic,
                            "type": "related_question"
                        } for query in queries[:2]  # Máximo 2 por tema
                    ])
        
        return related_suggestions[:3]  # Máximo 3 total
    
    def _suggest_follow_up_actions(self, answer: str, metadata: Dict) -> List[Dict[str, Any]]:
        """Sugiere acciones de seguimiento"""
        actions = []
        
        # Si hay muchos datos, sugerir exportar
        if metadata.get("chunks_retrieved", 0) >= 3:
            actions.append({
                "action": "export_data",
                "description": "¿Quieres exportar estos datos a Excel para análisis más detallado?",
                "type": "data_export"
            })
        
        # Si es modo pure, sugerir modo creative
        if metadata.get("mode") == "pure":
            actions.append({
                "action": "creative_analysis",
                "description": "¿Te gustaría un análisis más creativo con insights y recomendaciones?",
                "type": "mode_switch"
            })
        
        # Si no hay visualizaciones, sugerir crearlas
        if not metadata.get("has_visualizations", False):
            actions.append({
                "action": "add_visualizations",
                "description": "¿Quieres que agregue gráficos y visualizaciones a esta respuesta?",
                "type": "visualization_add"
            })
        
        return actions
    
    def _format_suggestions(self, suggestions: Dict[str, Any]) -> Dict[str, Any]:
        """Formatea las sugerencias para la respuesta final"""
        formatted = {
            "has_suggestions": False,
            "suggestion_count": 0,
            "categories": {}
        }
        
        # Visualizaciones
        if suggestions["visualizations"]:
            formatted["categories"]["visualizations"] = {
                "title": "📊 Visualizaciones Disponibles",
                "items": suggestions["visualizations"]
            }
            formatted["has_suggestions"] = True
        
        # Análisis profundo
        if suggestions["deep_dive"]:
            formatted["categories"]["deep_dive"] = {
                "title": "🔍 Análisis Más Profundo",
                "items": suggestions["deep_dive"]
            }
            formatted["has_suggestions"] = True
        
        # Consultas relacionadas
        if suggestions["related_queries"]:
            formatted["categories"]["related_queries"] = {
                "title": "❓ Preguntas Relacionadas",
                "items": suggestions["related_queries"]
            }
            formatted["has_suggestions"] = True
        
        # Acciones de seguimiento
        if suggestions["follow_up_actions"]:
            formatted["categories"]["follow_up_actions"] = {
                "title": "⚡ Acciones Recomendadas",
                "items": suggestions["follow_up_actions"]
            }
            formatted["has_suggestions"] = True
        
        formatted["suggestion_count"] = sum(len(cat["items"]) for cat in formatted["categories"].values())
        
        return formatted
    
    def generate_suggestion_text(self, suggestions: Dict[str, Any]) -> str:
        """Genera texto de sugerencias para agregar al final de la respuesta"""
        if not suggestions["has_suggestions"]:
            return ""
        
        suggestion_text = "\n\n---\n\n### 💡 ¿Qué más te gustaría explorar?\n\n"
        
        for category_key, category in suggestions["categories"].items():
            suggestion_text += f"**{category['title']}**\n"
            
            for item in category["items"][:3]:  # Máximo 3 por categoría
                if category_key == "visualizations":
                    suggestion_text += f"• {item['description']}\n"
                elif category_key == "deep_dive":
                    suggestion_text += f"• {item['description']}\n"
                elif category_key == "related_queries":
                    suggestion_text += f"• {item['query']}\n"
                elif category_key == "follow_up_actions":
                    suggestion_text += f"• {item['description']}\n"
            
            suggestion_text += "\n"
        
        suggestion_text += "*Solo menciona qué te interesa y te ayudo a profundizar en esa área.*"
        
        return suggestion_text