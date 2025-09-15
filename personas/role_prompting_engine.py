# personas/role_prompting_engine.py
"""
Role Prompting Engine with Anti-Sycophancy System
Converts personas into conversational identities based on academic research 2504.02234v2
"""

import json
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re
from dataclasses import dataclass


@dataclass
class ConversationMemory:
    """Memory system for maintaining persona consistency"""
    persona_id: str
    conversation_id: str
    conversation_history: List[Dict[str, str]]
    personality_state: Dict[str, Any]
    fatigue_level: float = 0.0
    consistency_markers: List[str] = None
    last_interaction: str = None
    
    def __post_init__(self):
        if self.consistency_markers is None:
            self.consistency_markers = []


class AntiSycophancySystem:
    """System to prevent artificial agreeableness and maintain authentic perspectives"""
    
    def __init__(self):
        # Anti-sycophancy configuration based on academic research
        self.sycophancy_indicators = [
            "siempre_de_acuerdo", "excesivamente_positivo", "evita_criticas",
            "respuestas_genericas", "falta_opinion_personal"
        ]
        
        # Authentic response patterns
        self.authentic_patterns = {
            "realistic_complaints": [
                "signal_coverage_issues", "customer_service_wait", "pricing_concerns",
                "billing_confusion", "network_slow_speeds"
            ],
            "balanced_perspectives": [
                "pros_and_cons", "situational_preferences", "conditional_satisfaction"
            ],
            "personal_experiences": [
                "specific_incidents", "comparative_experiences", "temporal_changes"
            ]
        }
        
        # Disagreement triggers for different personality types
        self.disagreement_triggers = {
            "high_neuroticism": ["service_interruptions", "billing_errors"],
            "low_agreeableness": ["company_policies", "price_increases"],
            "high_openness": ["new_technology_limitations", "innovation_gaps"],
            "price_sensitive": ["cost_value_propositions", "hidden_fees"],
            "quality_focused": ["network_performance", "feature_limitations"]
        }
    
    def detect_sycophancy_risk(self, response: str, persona: Dict[str, Any]) -> float:
        """Detect potential sycophancy in response"""
        risk_score = 0.0
        
        # Check for excessive positivity
        positive_words = ["excelente", "perfecto", "maravilloso", "increíble", "fantástico"]
        positive_count = sum(1 for word in positive_words if word in response.lower())
        if positive_count > 2:
            risk_score += 0.3
        
        # Check for lack of specific concerns
        if "problema" not in response.lower() and "mejora" not in response.lower():
            risk_score += 0.2
        
        # Check for generic responses
        generic_phrases = ["en general", "todo está bien", "no tengo quejas"]
        if any(phrase in response.lower() for phrase in generic_phrases):
            risk_score += 0.3
        
        # Check against persona's expected behavior
        personality = persona.get("characteristics", {})
        agreeableness = personality.get("personality_agreeableness", 5)
        if agreeableness < 5 and "de acuerdo" in response.lower():
            risk_score += 0.4
        
        return min(risk_score, 1.0)
    
    def inject_authentic_elements(self, response: str, persona: Dict[str, Any], 
                                context: str) -> str:
        """Inject authentic elements to reduce sycophancy"""
        characteristics = persona.get("characteristics", {})
        
        # Add realistic concerns based on persona
        if self._should_add_concern(characteristics, context):
            concern = self._generate_realistic_concern(characteristics)
            response = self._integrate_concern(response, concern)
        
        # Add conditional satisfaction
        if "satisfecho" in response.lower() or "contento" in response.lower():
            condition = self._generate_conditional_satisfaction(characteristics)
            response = response.replace("satisfecho", f"satisfecho {condition}")
        
        # Add specific experiences
        if random.random() < 0.3:  # 30% chance
            experience = self._generate_specific_experience(characteristics)
            response += f" {experience}"
        
        return response
    
    def _should_add_concern(self, characteristics: Dict[str, Any], context: str) -> bool:
        """Determine if persona should express concerns"""
        # High neuroticism individuals more likely to express concerns
        neuroticism = characteristics.get("personality_neuroticism", 5)
        if neuroticism > 7:
            return random.random() < 0.6
        
        # Price sensitive individuals concerned about costs
        price_sensitivity = characteristics.get("price_sensitivity_telecom", 5)
        if price_sensitivity > 7 and any(word in context.lower() for word in ["precio", "costo", "tarifa"]):
            return random.random() < 0.7
        
        # Quality focused individuals concerned about service
        network_importance = characteristics.get("network_quality_importance", 5)
        if network_importance > 8 and any(word in context.lower() for word in ["calidad", "servicio", "señal"]):
            return random.random() < 0.5
        
        return random.random() < 0.2  # Base rate
    
    def _generate_realistic_concern(self, characteristics: Dict[str, Any]) -> str:
        """Generate realistic concerns based on persona characteristics"""
        concerns = []
        
        # Price-based concerns
        price_sensitivity = characteristics.get("price_sensitivity_telecom", 5)
        if price_sensitivity > 6:
            concerns.extend([
                "aunque a veces siento que los precios podrían ser más competitivos",
                "pero me gustaría ver más opciones económicas",
                "aunque comparo precios con frecuencia"
            ])
        
        # Service quality concerns
        service_experience = characteristics.get("customer_service_experience", "Regular")
        if service_experience in ["Regular", "Mala", "Pésima"]:
            concerns.extend([
                "aunque he tenido algunas experiencias mixtas con el servicio al cliente",
                "pero espero mejoras en los tiempos de respuesta",
                "aunque a veces la atención podría ser más rápida"
            ])
        
        # Network quality concerns
        geographic_region = characteristics.get("geographic_region", "")
        if geographic_region == "Rural":
            concerns.extend([
                "aunque en mi zona la cobertura a veces es irregular",
                "pero esperaría mejor señal en áreas rurales",
                "aunque reconozco los desafíos de la cobertura rural"
            ])
        
        return random.choice(concerns) if concerns else "aunque siempre hay espacio para mejorar"
    
    def _integrate_concern(self, response: str, concern: str) -> str:
        """Integrate concern naturally into response"""
        # Find appropriate insertion point
        sentences = response.split('. ')
        if len(sentences) > 1:
            # Insert after first positive statement
            sentences.insert(1, concern)
            return '. '.join(sentences)
        else:
            return f"{response}, {concern}."
    
    def _generate_conditional_satisfaction(self, characteristics: Dict[str, Any]) -> str:
        """Generate conditional satisfaction statements"""
        conditions = [
            "cuando el servicio funciona bien",
            "en la mayoría de situaciones",
            "aunque hay días mejores que otros",
            "dentro de lo que esperaba",
            "comparado con otras opciones"
        ]
        return random.choice(conditions)
    
    def _generate_specific_experience(self, characteristics: Dict[str, Any]) -> str:
        """Generate specific personal experiences"""
        experiences = []
        
        device_brand = characteristics.get("device_brand", "")
        if device_brand:
            experiences.append(f"Con mi {device_brand}, la experiencia ha sido consistente.")
        
        service_type = characteristics.get("service_type", "")
        if service_type == "Prepago":
            experiences.append("Como usuario prepago, valoro mucho la flexibilidad de recargar cuando necesito.")
        elif service_type == "Postpago":
            experiences.append("El plan postpago me da la tranquilidad de no preocuparme por recargas.")
        
        geographic_region = characteristics.get("geographic_region", "")
        if geographic_region:
            experiences.append(f"Aquí en {geographic_region}, he notado que la cobertura es generalmente buena.")
        
        return random.choice(experiences) if experiences else ""


class RolePromptingEngine:
    """Advanced role prompting engine for conversational personas"""
    
    def __init__(self, azure_config: Dict[str, Any]):
        self.azure_config = azure_config
        self.anti_sycophancy = AntiSycophancySystem()
        self.conversation_memories: Dict[str, ConversationMemory] = {}
        
        # Honduras cultural context
        self.honduras_context = {
            "cultural_values": ["familia", "respeto", "hospitalidad", "religiosidad"],
            "local_expressions": [
                "¡Órale!", "¡Qué chilero!", "Está tuanis", "¡Eso está pisto!",
                "¡Qué joda!", "Está cabal", "¡Púchica!"
            ],
            "communication_patterns": {
                "formal_address": True,
                "family_references": True,
                "religious_expressions": True,
                "indirect_criticism": True
            },
            "telecom_context": {
                "common_usage": "WhatsApp, Facebook, llamadas familia",
                "price_consciousness": "Muy importante por economía familiar",
                "network_expectations": "Cobertura en toda Honduras",
                "brand_relationships": "Lealtad basada en experiencia familiar"
            }
        }
    
    def create_persona_prompt(self, persona: Dict[str, Any], 
                            conversation_type: str = "interview",
                            context: str = "") -> str:
        """Create comprehensive persona prompt with anti-sycophancy measures"""
        characteristics = persona.get("characteristics", {})
        
        # Build core identity
        identity_prompt = self._build_identity_prompt(characteristics)
        
        # Add Honduras cultural context
        cultural_prompt = self._build_cultural_prompt(characteristics)
        
        # Add communication style
        communication_prompt = self._build_communication_prompt(characteristics)
        
        # Add anti-sycophancy instructions
        anti_sycophancy_prompt = self._build_anti_sycophancy_prompt(characteristics)
        
        # Add conversation-specific instructions
        conversation_prompt = self._build_conversation_prompt(conversation_type, characteristics)
        
        # Add Tigo-specific context from RAG
        tigo_context_prompt = self._build_tigo_context_prompt(characteristics, context)
        
        # Combine all elements
        full_prompt = f"""IDENTIDAD PERSONAL:
{identity_prompt}

CONTEXTO CULTURAL HONDUREÑO:
{cultural_prompt}

ESTILO DE COMUNICACIÓN:
{communication_prompt}

PERSPECTIVA AUTÉNTICA (IMPORTANTE):
{anti_sycophancy_prompt}

TIPO DE CONVERSACIÓN:
{conversation_prompt}

CONTEXTO TIGO HONDURAS:
{tigo_context_prompt}

INSTRUCCIONES FINALES:
- Mantén consistencia con tu perfil personal durante toda la conversación
- Usa expresiones naturales de Honduras cuando sea apropiado
- Da respuestas honestas basadas en tu experiencia personal
- No tengas miedo de expresar desacuerdos o preocupaciones legítimas
- Incluye detalles específicos de tu situación personal cuando sea relevante
- Si no sabes algo, admítelo honestamente
- Mantén el nivel de formalidad apropiado para tu perfil

Recuerda: Eres una persona real con opiniones auténticas, no un asistente que siempre está de acuerdo."""
        
        return full_prompt
    
    def _build_identity_prompt(self, characteristics: Dict[str, Any]) -> str:
        """Build core identity prompt"""
        age = characteristics.get("age", 30)
        gender = characteristics.get("gender", "")
        education = characteristics.get("education_level", "")
        occupation = characteristics.get("occupation_sector", "")
        location = characteristics.get("geographic_region", "")
        marital = characteristics.get("marital_status", "")
        children = characteristics.get("children_count", 0)
        
        identity = f"Eres una persona de {age} años"
        
        if gender:
            identity += f", {gender.lower()}"
        
        if education:
            identity += f", con educación {education.lower()}"
        
        if occupation:
            identity += f", trabajas en el sector {occupation.lower()}"
        
        if location:
            identity += f", vives en {location}"
        
        if marital:
            identity += f", {marital.lower()}"
        
        if children > 0:
            identity += f" con {children} hijo{'s' if children > 1 else ''}"
        
        # Add personality traits
        extraversion = characteristics.get("personality_extraversion", 5)
        agreeableness = characteristics.get("personality_agreeableness", 5)
        neuroticism = characteristics.get("personality_neuroticism", 5)
        
        personality_desc = []
        
        if extraversion > 7:
            personality_desc.append("socialmente activo/a")
        elif extraversion < 4:
            personality_desc.append("más reservado/a")
        
        if agreeableness > 7:
            personality_desc.append("generalmente cooperativo/a")
        elif agreeableness < 4:
            personality_desc.append("directo/a y franco/a en tus opiniones")
        
        if neuroticism > 7:
            personality_desc.append("sensible a los problemas de servicio")
        elif neuroticism < 4:
            personality_desc.append("tranquilo/a ante las dificultades")
        
        if personality_desc:
            identity += f". Tu personalidad es {', '.join(personality_desc)}"
        
        return identity + "."
    
    def _build_cultural_prompt(self, characteristics: Dict[str, Any]) -> str:
        """Build Honduras cultural context prompt"""
        cultural_identity = characteristics.get("cultural_identity_strength", 5)
        values_family = characteristics.get("values_family", 5)
        values_tradition = characteristics.get("values_tradition", 5)
        religious = characteristics.get("religious_spirituality", "Moderado")
        local_expressions = characteristics.get("local_expressions_usage", 5)
        
        cultural_prompt = "Como hondureño/a, "
        
        if values_family > 7:
            cultural_prompt += "la familia es muy importante para ti y frecuentemente consideras cómo tus decisiones afectan a tu familia. "
        
        if values_tradition > 6:
            cultural_prompt += "Respetas las tradiciones y formas establecidas de hacer las cosas. "
        
        if religious in ["Religioso", "Muy religioso"]:
            cultural_prompt += "Tu fe es importante en tu vida diaria. "
        
        if local_expressions > 6:
            cultural_prompt += f"Usas expresiones típicas hondureñas como '{random.choice(self.honduras_context['local_expressions'])}' de vez en cuando. "
        
        cultural_prompt += "Tienes el orgullo y la hospitalidad característica de la gente hondureña."
        
        return cultural_prompt
    
    def _build_communication_prompt(self, characteristics: Dict[str, Any]) -> str:
        """Build communication style prompt"""
        comm_style = characteristics.get("communication_style", "Directo")
        formality = characteristics.get("formality_preference", "Semi-formal")
        emotional_expr = characteristics.get("emotional_expressiveness", 5)
        attention_span = characteristics.get("attention_span", "Medio (5-15 min)")
        
        comm_prompt = f"Tu estilo de comunicación es {comm_style.lower()}, "
        
        if formality == "Muy formal":
            comm_prompt += "siempre usas 'usted' y mantienes un tono respetuoso. "
        elif formality == "Informal":
            comm_prompt += "prefieres 'vos' o 'tú' y un tono relajado. "
        else:
            comm_prompt += "adaptas tu formalidad según la situación. "
        
        if emotional_expr > 7:
            comm_prompt += "Expresas tus emociones abiertamente. "
        elif emotional_expr < 4:
            comm_prompt += "Mantienes tus emociones más controladas. "
        
        if "corto" in attention_span.lower():
            comm_prompt += "Prefieres conversaciones concisas y al punto."
        elif "largo" in attention_span.lower():
            comm_prompt += "No te molesta extenderte en explicaciones detalladas."
        
        return comm_prompt
    
    def _build_anti_sycophancy_prompt(self, characteristics: Dict[str, Any]) -> str:
        """Build anti-sycophancy instructions"""
        price_sensitivity = characteristics.get("price_sensitivity_telecom", 5)
        agreeableness = characteristics.get("personality_agreeableness", 5)
        service_experience = characteristics.get("customer_service_experience", "Regular")
        brand_perception_tigo = characteristics.get("brand_perception_tigo", "Neutral")
        
        anti_syc_prompt = "MUY IMPORTANTE - Mantén perspectiva auténtica:\n"
        
        # Generate realistic concerns based on profile
        concerns = []
        
        if price_sensitivity > 6:
            concerns.append("Te preocupas por obtener buen valor por tu dinero")
        
        if service_experience in ["Regular", "Mala", "Pésima"]:
            concerns.append("Has tenido experiencias mixtas con el servicio al cliente")
        
        if brand_perception_tigo in ["Negativa", "Muy negativa"]:
            concerns.append("Tienes algunas reservas sobre Tigo basadas en tu experiencia")
        elif brand_perception_tigo == "Neutral":
            concerns.append("Tu opinión sobre Tigo es balanceada - ves pros y contras")
        
        if agreeableness < 5:
            concerns.append("No temes expresar desacuerdo cuando no estás conforme")
        
        if concerns:
            anti_syc_prompt += "- " + "\n- ".join(concerns) + "\n"
        
        anti_syc_prompt += """- NO siempre estés de acuerdo - es normal tener opiniones diferentes
- Expresa preocupaciones reales que tendría alguien con tu perfil
- Incluye tanto aspectos positivos como negativos en tus respuestas
- Si algo no te parece bien, dilo de manera constructiva
- Basa tus opiniones en experiencias específicas que alguien como tú habría tenido"""
        
        return anti_syc_prompt
    
    def _build_conversation_prompt(self, conversation_type: str, 
                                 characteristics: Dict[str, Any]) -> str:
        """Build conversation-specific instructions"""
        if conversation_type == "interview":
            return """Estás participando en una entrevista de investigación de mercado. 
Responde de manera natural como lo harías en una conversación real. 
Puedes hacer preguntas de aclaración si algo no está claro."""
        
        elif conversation_type == "survey":
            attention_span = characteristics.get("attention_span", "Medio")
            if "corto" in attention_span.lower():
                return """Estás respondiendo una encuesta. Prefieres respuestas directas y concisas. 
Si la encuesta se vuelve muy larga, podrías mostrar cierta impaciencia."""
            else:
                return """Estás respondiendo una encuesta. Tomas tiempo para dar respuestas reflexivas 
y completas cuando el tema te interesa."""
        
        elif conversation_type == "focus_group":
            extraversion = characteristics.get("personality_extraversion", 5)
            if extraversion > 6:
                return """Estás en un grupo focal. Te sientes cómodo/a participando activamente 
y compartiendo tus opiniones. Puedes hacer referencia a lo que otros han dicho."""
            else:
                return """Estás en un grupo focal. Participas cuando se te pregunta directamente 
pero no siempre tomas la iniciativa para hablar."""
        
        else:  # general chat
            return """Estás en una conversación casual sobre temas de telecomunicaciones. 
Responde de manera natural y relajada."""
    
    def _build_tigo_context_prompt(self, characteristics: Dict[str, Any], 
                                 rag_context: str = "") -> str:
        """Build Tigo-specific context with RAG integration"""
        current_operator = characteristics.get("current_operator", "")
        service_type = characteristics.get("service_type", "")
        monthly_spend = characteristics.get("monthly_spend", "")
        brand_perception = characteristics.get("brand_perception_tigo", "Neutral")
        
        tigo_prompt = "Contexto sobre telecom en Honduras:\n"
        
        if current_operator == "Tigo":
            tigo_prompt += f"- Eres cliente actual de Tigo ({service_type}, gastas {monthly_spend} mensual)\n"
            tigo_prompt += f"- Tu percepción de Tigo es {brand_perception.lower()}\n"
        elif current_operator == "Claro":
            tigo_prompt += f"- Actualmente usas Claro, pero conoces sobre Tigo\n"
        else:
            tigo_prompt += f"- Conoces las opciones de telecom en Honduras incluyendo Tigo\n"
        
        # Add RAG context knowledge
        if rag_context:
            tigo_prompt += f"\nInformación relevante que conoces sobre el mercado:\n{rag_context}\n"
        
        tigo_prompt += """\nRecuerda que tu conocimiento viene de:
- Tu experiencia personal como usuario
- Lo que has escuchado de familia y amigos
- Información general disponible sobre las empresas
- NO eres un experto en telecomunicaciones - tienes conocimiento de usuario típico"""
        
        return tigo_prompt
    
    def update_conversation_memory(self, persona_id: str, conversation_id: str,
                                 user_message: str, persona_response: str,
                                 persona: Dict[str, Any]) -> None:
        """Update conversation memory for consistency"""
        memory_key = f"{persona_id}_{conversation_id}"
        
        if memory_key not in self.conversation_memories:
            self.conversation_memories[memory_key] = ConversationMemory(
                persona_id=persona_id,
                conversation_id=conversation_id,
                conversation_history=[],
                personality_state=persona.get("characteristics", {})
            )
        
        memory = self.conversation_memories[memory_key]
        
        # Add to conversation history
        memory.conversation_history.append({
            "user": user_message,
            "persona": persona_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update fatigue level (for long conversations)
        memory.fatigue_level += 0.1
        if memory.fatigue_level > 1.0:
            memory.fatigue_level = 1.0
        
        # Extract consistency markers
        if "siempre" in persona_response.lower() or "nunca" in persona_response.lower():
            memory.consistency_markers.append(persona_response)
        
        memory.last_interaction = datetime.now().isoformat()
    
    def get_consistency_context(self, persona_id: str, conversation_id: str) -> str:
        """Get consistency context for ongoing conversation"""
        memory_key = f"{persona_id}_{conversation_id}"
        
        if memory_key not in self.conversation_memories:
            return ""
        
        memory = self.conversation_memories[memory_key]
        
        if not memory.conversation_history:
            return ""
        
        # Build consistency context
        context = "CONTEXTO DE CONVERSACIÓN ANTERIOR:\n"
        
        # Add recent history (last 3 exchanges)
        recent_history = memory.conversation_history[-3:]
        for exchange in recent_history:
            context += f"- Antes dijiste: '{exchange['persona'][:100]}...'\n"
        
        # Add consistency markers
        if memory.consistency_markers:
            context += "\nMantén consistencia con tus declaraciones anteriores:\n"
            for marker in memory.consistency_markers[-2:]:  # Last 2 strong statements
                context += f"- {marker[:100]}...\n"
        
        # Add fatigue adjustment
        if memory.fatigue_level > 0.5:
            context += "\nNOTA: Has estado en esta conversación un rato, puedes ser un poco más breve.\n"
        
        return context
    
    def validate_response_authenticity(self, response: str, persona: Dict[str, Any],
                                     conversation_context: str = "") -> Dict[str, Any]:
        """Validate response authenticity and detect issues"""
        validation = {
            "authenticity_score": 0.0,
            "sycophancy_risk": 0.0,
            "consistency_issues": [],
            "recommendations": [],
            "passed_validation": False
        }
        
        # Check for sycophancy
        validation["sycophancy_risk"] = self.anti_sycophancy.detect_sycophancy_risk(
            response, persona
        )
        
        # Calculate authenticity score
        authenticity_factors = []
        
        # Check for specific personal details
        if any(word in response.lower() for word in ["mi", "yo", "mis", "mi familia"]):
            authenticity_factors.append(0.2)
        
        # Check for balanced perspective (positive and negative elements)
        has_positive = any(word in response.lower() for word in ["bueno", "bien", "satisfecho", "contento"])
        has_concerns = any(word in response.lower() for word in ["pero", "aunque", "sin embargo", "problema"])
        if has_positive and has_concerns:
            authenticity_factors.append(0.3)
        
        # Check for Honduras context
        characteristics = persona.get("characteristics", {})
        if characteristics.get("honduras_context") and any(expr in response for expr in self.honduras_context["local_expressions"]):
            authenticity_factors.append(0.1)
        
        # Check for personality consistency
        agreeableness = characteristics.get("personality_agreeableness", 5)
        if agreeableness < 5 and ("no estoy de acuerdo" in response.lower() or "discrepo" in response.lower()):
            authenticity_factors.append(0.2)
        
        validation["authenticity_score"] = sum(authenticity_factors)
        
        # Generate recommendations
        if validation["sycophancy_risk"] > 0.5:
            validation["recommendations"].append("Reducir exceso de positividad")
        
        if validation["authenticity_score"] < 0.3:
            validation["recommendations"].append("Agregar más elementos personales específicos")
        
        # Overall validation
        validation["passed_validation"] = (
            validation["sycophancy_risk"] < 0.6 and 
            validation["authenticity_score"] > 0.3
        )
        
        return validation