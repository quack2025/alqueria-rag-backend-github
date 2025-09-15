# personas/temporal_context.py
"""
Temporal Context Integration System for Contemporary Persona Generation
Addresses 'atemporality' issue where LLMs lack current context by integrating:
- Recent Honduras news and economic data
- Current telecom industry updates  
- Cultural events and social trends
- Real-time context for authentic contemporary personas
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TemporalContextType(Enum):
    """Types of temporal context"""
    ECONOMIC_CURRENT = "economic_current"
    POLITICAL_SOCIAL = "political_social"
    TELECOM_INDUSTRY = "telecom_industry"
    CULTURAL_EVENTS = "cultural_events"
    TECHNOLOGY_TRENDS = "technology_trends"
    SOCIAL_MEDIA_TRENDS = "social_media_trends"
    PANDEMIC_IMPACT = "pandemic_impact"
    CLIMATE_WEATHER = "climate_weather"


@dataclass
class TemporalContext:
    """Single temporal context item"""
    context_type: TemporalContextType
    title: str
    description: str
    impact_level: str  # "high", "medium", "low"
    affected_demographics: List[str]
    persona_implications: List[str]
    conversation_references: List[str]
    time_period: str
    relevance_score: float


class HondurasTemporalContextManager:
    """Manages current temporal context for Honduras personas"""
    
    def __init__(self):
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        # Initialize temporal context database with recent/current Honduras context
        self.temporal_contexts = {
            TemporalContextType.ECONOMIC_CURRENT: [
                TemporalContext(
                    context_type=TemporalContextType.ECONOMIC_CURRENT,
                    title="Post-Pandemic Economic Recovery",
                    description="Honduras continues recovering from COVID-19 economic impacts with focus on employment and small business support",
                    impact_level="high",
                    affected_demographics=["working_class", "small_business_owners", "young_adults"],
                    persona_implications=[
                        "More conscious of job security and income stability",
                        "Increased appreciation for reliable services during uncertainty",
                        "Budget considerations for non-essential services"
                    ],
                    conversation_references=[
                        "la economía se está recuperando poco a poco",
                        "después de la pandemia las cosas han cambiado",
                        "hay que ser más cuidadoso con los gastos"
                    ],
                    time_period="2022-2024",
                    relevance_score=0.9
                ),
                TemporalContext(
                    context_type=TemporalContextType.ECONOMIC_CURRENT,
                    title="Inflation and Cost of Living Concerns",
                    description="Rising costs of basic goods and services affecting household budgets across Honduras",
                    impact_level="high",
                    affected_demographics=["families", "fixed_income", "working_class"],
                    persona_implications=[
                        "More price-sensitive in telecom choices",
                        "Seeking value-for-money in all services",
                        "Comparing options more carefully before decisions"
                    ],
                    conversation_references=[
                        "todo está más caro que antes",
                        "hay que ajustar el presupuesto familiar",
                        "buscamos mejores ofertas en todo"
                    ],
                    time_period="2023-2024",
                    relevance_score=0.95
                ),
                TemporalContext(
                    context_type=TemporalContextType.ECONOMIC_CURRENT,
                    title="Remittances and Dollar Exchange",
                    description="Continued importance of family remittances from abroad and exchange rate considerations",
                    impact_level="medium",
                    affected_demographics=["families_with_migrants", "rural_communities"],
                    persona_implications=[
                        "International communication needs for family abroad",
                        "Interest in international calling/messaging plans",
                        "Economic decisions influenced by remittance timing"
                    ],
                    conversation_references=[
                        "la familia desde Estados Unidos nos ayuda",
                        "las remesas son importantes para nosotros",
                        "necesitamos comunicarnos con los familiares afuera"
                    ],
                    time_period="ongoing",
                    relevance_score=0.8
                )
            ],
            
            TemporalContextType.TELECOM_INDUSTRY: [
                TemporalContext(
                    context_type=TemporalContextType.TELECOM_INDUSTRY,
                    title="5G Network Rollout in Major Cities",
                    description="Gradual implementation of 5G technology in Tegucigalpa and San Pedro Sula",
                    impact_level="medium",
                    affected_demographics=["urban_professionals", "tech_early_adopters", "businesses"],
                    persona_implications=[
                        "Curiosity about faster internet speeds and new capabilities",
                        "Concerns about additional costs for 5G plans",
                        "Interest in how 5G will improve work and entertainment"
                    ],
                    conversation_references=[
                        "he escuchado sobre el 5G que está llegando",
                        "dicen que el internet va a ser mucho más rápido",
                        "me pregunto si va a costar más el servicio"
                    ],
                    time_period="2023-2024",
                    relevance_score=0.7
                ),
                TemporalContext(
                    context_type=TemporalContextType.TELECOM_INDUSTRY,
                    title="Increased Competition and Plan Options",
                    description="More competitive telecom market with diverse plan options and promotional campaigns",
                    impact_level="high",
                    affected_demographics=["all_users", "price_conscious_consumers"],
                    persona_implications=[
                        "More empowered to switch providers for better deals",
                        "Increased awareness of plan features and pricing",
                        "Higher expectations for customer service and transparency"
                    ],
                    conversation_references=[
                        "ahora hay más opciones que antes",
                        "las compañías están compitiendo más por los clientes",
                        "uno puede comparar mejor los planes"
                    ],
                    time_period="2022-2024",
                    relevance_score=0.9
                ),
                TemporalContext(
                    context_type=TemporalContextType.TELECOM_INDUSTRY,
                    title="Digital Payment Integration",
                    description="Growth in mobile payment options and digital wallet integration with telecom services",
                    impact_level="medium",
                    affected_demographics=["urban_users", "younger_adults", "small_businesses"],
                    persona_implications=[
                        "Interest in convenient payment methods for telecom services",
                        "Concerns about security in digital transactions",
                        "Appreciation for integrated financial and communication services"
                    ],
                    conversation_references=[
                        "ahora se puede pagar desde el teléfono",
                        "las billeteras digitales están creciendo",
                        "es más fácil manejar los pagos desde la app"
                    ],
                    time_period="2023-2024",
                    relevance_score=0.8
                )
            ],
            
            TemporalContextType.TECHNOLOGY_TRENDS: [
                TemporalContext(
                    context_type=TemporalContextType.TECHNOLOGY_TRENDS,
                    title="WhatsApp Business Growth",
                    description="Increased use of WhatsApp for business communications and customer service",
                    impact_level="high",
                    affected_demographics=["small_businesses", "entrepreneurs", "customers"],
                    persona_implications=[
                        "Expects businesses to be available via WhatsApp",
                        "Uses WhatsApp for both personal and business communications",
                        "Values data plans that support WhatsApp usage"
                    ],
                    conversation_references=[
                        "casi todos los negocios tienen WhatsApp ahora",
                        "es más fácil hacer pedidos por WhatsApp", 
                        "necesito datos suficientes para WhatsApp"
                    ],
                    time_period="2022-2024",
                    relevance_score=0.95
                ),
                TemporalContext(
                    context_type=TemporalContextType.TECHNOLOGY_TRENDS,
                    title="Online Education and Remote Work Legacy",
                    description="Continued adoption of digital tools for education and work, post-pandemic",
                    impact_level="medium",
                    affected_demographics=["students", "professionals", "parents"],
                    persona_implications=[
                        "Higher data usage needs for work/study from home",
                        "Reliability expectations for internet connectivity",
                        "Understanding of video call quality importance"
                    ],
                    conversation_references=[
                        "después de la pandemia seguimos trabajando desde casa",
                        "los estudiantes necesitan buen internet para las clases",
                        "las videollamadas son parte del trabajo ahora"
                    ],
                    time_period="2021-2024",
                    relevance_score=0.8
                )
            ],
            
            TemporalContextType.SOCIAL_MEDIA_TRENDS: [
                TemporalContext(
                    context_type=TemporalContextType.SOCIAL_MEDIA_TRENDS,
                    title="TikTok and Short Video Content Growth",
                    description="Rapid adoption of TikTok and short-form video content, especially among younger users",
                    impact_level="medium",
                    affected_demographics=["teenagers", "young_adults", "content_creators"],
                    persona_implications=[
                        "Higher data consumption for video content",
                        "Interest in plans with social media data packages",
                        "Influence of social media trends on communication style"
                    ],
                    conversation_references=[
                        "TikTok consume muchos datos",
                        "los jóvenes están todo el día viendo videos",
                        "necesito plan con redes sociales incluidas"
                    ],
                    time_period="2022-2024",
                    relevance_score=0.8
                ),
                TemporalContext(
                    context_type=TemporalContextType.SOCIAL_MEDIA_TRENDS,
                    title="Facebook Groups for Community Organization",
                    description="Continued importance of Facebook groups for local community organization and information sharing",
                    impact_level="medium",
                    affected_demographics=["community_leaders", "parents", "local_businesses"],
                    persona_implications=[
                        "Values social media for community connection",
                        "Uses Facebook for local news and community updates",
                        "Appreciates reliable social media access"
                    ],
                    conversation_references=[
                        "en el grupo de Facebook del barrio nos organizamos",
                        "ahí nos enteramos de lo que pasa en la comunidad",
                        "Facebook sigue siendo importante para estar conectados"
                    ],
                    time_period="ongoing",
                    relevance_score=0.7
                )
            ],
            
            TemporalContextType.CULTURAL_EVENTS: [
                TemporalContext(
                    context_type=TemporalContextType.CULTURAL_EVENTS,
                    title="Return of Traditional Festivals",
                    description="Gradual return of traditional festivals and cultural events after pandemic restrictions",
                    impact_level="medium",
                    affected_demographics=["families", "cultural_participants", "local_communities"],
                    persona_implications=[
                        "Renewed appreciation for community gatherings",
                        "Interest in sharing cultural moments via social media",
                        "Need for reliable communication during large events"
                    ],
                    conversation_references=[
                        "qué bueno que regresaron las fiestas tradicionales",
                        "después de tanto tiempo sin celebrar juntos",
                        "ahora compartimos más fotos de las celebraciones"
                    ],
                    time_period="2022-2024",
                    relevance_score=0.6
                ),
                TemporalContext(
                    context_type=TemporalContextType.CULTURAL_EVENTS,
                    title="Digital Cultural Content Growth",
                    description="Increased online cultural content and virtual events complementing traditional celebrations",
                    impact_level="low",
                    affected_demographics=["culturally_active", "digital_natives"],
                    persona_implications=[
                        "Appreciation for hybrid cultural experiences",
                        "Interest in streaming cultural content",
                        "Value in digital preservation of cultural events"
                    ],
                    conversation_references=[
                        "ahora también hay eventos culturales virtuales",
                        "se pueden ver presentaciones en línea",
                        "la cultura también se adaptó al mundo digital"
                    ],
                    time_period="2021-2024",
                    relevance_score=0.5
                )
            ],
            
            TemporalContextType.CLIMATE_WEATHER: [
                TemporalContext(
                    context_type=TemporalContextType.CLIMATE_WEATHER,
                    title="Climate Change Impact Awareness",
                    description="Increased awareness of climate change effects on Honduras, including extreme weather",
                    impact_level="medium",
                    affected_demographics=["rural_communities", "agricultural_workers", "environmentally_conscious"],
                    persona_implications=[
                        "Concerns about service reliability during extreme weather",
                        "Appreciation for communication networks during emergencies",
                        "Interest in sustainable technology practices"
                    ],
                    conversation_references=[
                        "el clima está más impredecible ahora",
                        "necesitamos comunicación confiable durante tormentas",
                        "el cambio climático nos afecta a todos"
                    ],
                    time_period="ongoing",
                    relevance_score=0.7
                ),
                TemporalContext(
                    context_type=TemporalContextType.CLIMATE_WEATHER,
                    title="Hurricane Season Preparedness",
                    description="Annual preparation for hurricane season with emphasis on emergency communication",
                    impact_level="high",
                    affected_demographics=["coastal_communities", "families", "emergency_responders"],
                    persona_implications=[
                        "Values network reliability during emergencies",
                        "Keeps multiple communication options available",
                        "Appreciates early warning systems via mobile"
                    ],
                    conversation_references=[
                        "en temporada de huracanes necesitamos comunicación segura",
                        "es importante tener el teléfono con batería y señal",
                        "las alertas por celular nos ayudan mucho"
                    ],
                    time_period="June-November annually",
                    relevance_score=0.8
                )
            ]
        }
    
    def get_relevant_temporal_context(self, persona_characteristics: Dict[str, Any],
                                    conversation_topic: str = "",
                                    max_contexts: int = 3) -> List[TemporalContext]:
        """Get relevant temporal contexts for persona based on demographics and topic"""
        
        # Extract persona demographics
        age = persona_characteristics.get("age", 30)
        region = persona_characteristics.get("geographic_region", "")
        occupation = persona_characteristics.get("occupation_sector", "")
        income = persona_characteristics.get("income_bracket", "")
        tech_adoption = persona_characteristics.get("technology_adoption", "")
        
        # Determine demographic categories
        demographic_categories = []
        
        if age < 25:
            demographic_categories.append("young_adults")
        elif age > 50:
            demographic_categories.append("older_adults")
        
        if "rural" in region.lower():
            demographic_categories.append("rural_communities")
        else:
            demographic_categories.append("urban_users")
        
        if "bajo" in income.lower():
            demographic_categories.append("working_class")
        elif "alto" in income.lower():
            demographic_categories.append("upper_class")
        
        if "innovador" in tech_adoption.lower():
            demographic_categories.append("tech_early_adopters")
        
        # Score contexts based on relevance
        scored_contexts = []
        
        for context_type, contexts in self.temporal_contexts.items():
            for context in contexts:
                relevance_score = context.relevance_score
                
                # Boost score for demographic match
                demographic_match = any(demo in context.affected_demographics 
                                      for demo in demographic_categories)
                if demographic_match:
                    relevance_score += 0.2
                
                # Boost score for topic relevance
                if conversation_topic:
                    topic_keywords = conversation_topic.lower().split()
                    context_keywords = (context.title + " " + context.description).lower()
                    
                    keyword_matches = sum(1 for keyword in topic_keywords 
                                        if keyword in context_keywords)
                    if keyword_matches > 0:
                        relevance_score += keyword_matches * 0.1
                
                # Boost score for current time relevance
                if "2024" in context.time_period or "ongoing" in context.time_period:
                    relevance_score += 0.1
                
                scored_contexts.append((context, relevance_score))
        
        # Sort by relevance score and return top contexts
        scored_contexts.sort(key=lambda x: x[1], reverse=True)
        
        return [context for context, score in scored_contexts[:max_contexts]]
    
    def integrate_temporal_context_into_prompt(self, base_prompt: str,
                                             temporal_contexts: List[TemporalContext]) -> str:
        """Integrate temporal context into persona prompt"""
        
        if not temporal_contexts:
            return base_prompt
        
        # Build temporal context section
        temporal_section = "\n\nCONTEXTO TEMPORAL ACTUAL (2024):\n"
        
        for context in temporal_contexts:
            temporal_section += f"• {context.description}\n"
            
            # Add persona implications
            if context.persona_implications:
                implications = random.sample(context.persona_implications, 
                                           min(2, len(context.persona_implications)))
                temporal_section += f"  Esto significa que: {' y '.join(implications)}\n"
            
            # Add potential conversation references
            if context.conversation_references:
                ref = random.choice(context.conversation_references)
                temporal_section += f"  Podrías mencionar: \"{ref}\"\n"
            
            temporal_section += "\n"
        
        # Add temporal awareness instructions
        temporal_section += """INSTRUCCIONES TEMPORALES:
- Tus respuestas deben reflejar la realidad actual de Honduras en 2024
- Incluye referencias naturales a eventos recientes cuando sea apropiado
- Mantén consciencia de los cambios sociales y económicos actuales
- No uses información desactualizada o pre-pandemia como si fuera actual
- Habla desde tu experiencia contemporánea, no histórica

"""
        
        # Insert temporal context into the base prompt
        # Find a good insertion point (after identity, before final instructions)
        insertion_point = base_prompt.find("INSTRUCCIONES FINALES:")
        if insertion_point == -1:
            insertion_point = base_prompt.find("Recuerda:")
        
        if insertion_point != -1:
            updated_prompt = (base_prompt[:insertion_point] + 
                            temporal_section + 
                            base_prompt[insertion_point:])
        else:
            updated_prompt = base_prompt + "\n" + temporal_section
        
        return updated_prompt
    
    def generate_conversation_starters_with_temporal_context(self, 
                                                          temporal_contexts: List[TemporalContext]) -> List[str]:
        """Generate conversation starters that incorporate current temporal context"""
        
        starters = []
        
        for context in temporal_contexts:
            if context.conversation_references:
                for ref in context.conversation_references:
                    starters.extend([
                        f"¿Qué opina sobre el hecho de que {ref}?",
                        f"¿Cómo le ha afectado que {ref}?",
                        f"¿Ha notado que {ref}?",
                        f"En su experiencia, ¿es cierto que {ref}?"
                    ])
        
        # Add general temporal awareness starters
        starters.extend([
            "¿Cómo han cambiado las cosas desde antes de la pandemia?",
            "¿Qué piensa sobre los cambios tecnológicos recientes?",
            "¿Cómo ve la situación económica actual del país?",
            "¿Qué cambios ha notado en los servicios de telecomunicaciones últimamente?"
        ])
        
        return starters
    
    def validate_temporal_relevance(self, response: str, 
                                  temporal_contexts: List[TemporalContext]) -> Dict[str, Any]:
        """Validate that response appropriately incorporates temporal context"""
        
        validation = {
            "temporal_awareness_score": 0.0,
            "context_references": [],
            "anachronisms_detected": [],
            "improvement_suggestions": [],
            "overall_rating": "Poor"
        }
        
        response_lower = response.lower()
        
        # Check for temporal context references
        context_references = 0
        for context in temporal_contexts:
            for ref in context.conversation_references:
                # Check for similar concepts, not exact matches
                ref_keywords = ref.lower().split()
                if any(keyword in response_lower for keyword in ref_keywords if len(keyword) > 3):
                    context_references += 1
                    validation["context_references"].append(ref)
        
        # Check for current time awareness
        current_time_indicators = [
            "ahora", "actualmente", "hoy en día", "en estos días", 
            "últimamente", "recientemente", "desde la pandemia",
            "después de la pandemia", "en 2024", "este año"
        ]
        
        temporal_awareness = sum(1 for indicator in current_time_indicators 
                               if indicator in response_lower)
        
        # Check for anachronisms (outdated references)
        anachronisms = [
            "antes de internet", "cuando no había celulares", 
            "en los años 90", "cuando era joven", "hace décadas"
        ]
        
        detected_anachronisms = [ana for ana in anachronisms if ana in response_lower]
        validation["anachronisms_detected"] = detected_anachronisms
        
        # Calculate temporal awareness score
        validation["temporal_awareness_score"] = min(1.0, 
            (context_references * 0.3) + (temporal_awareness * 0.1) - (len(detected_anachronisms) * 0.2))
        
        # Determine overall rating
        score = validation["temporal_awareness_score"]
        if score > 0.7:
            validation["overall_rating"] = "Excellent"
        elif score > 0.5:
            validation["overall_rating"] = "Good"
        elif score > 0.3:
            validation["overall_rating"] = "Acceptable"
        else:
            validation["overall_rating"] = "Poor"
        
        # Generate improvement suggestions
        if context_references == 0:
            validation["improvement_suggestions"].append("Include references to current events or trends")
        
        if temporal_awareness == 0:
            validation["improvement_suggestions"].append("Add temporal markers (ahora, actualmente, etc.)")
        
        if detected_anachronisms:
            validation["improvement_suggestions"].append("Remove outdated references and focus on current context")
        
        if not validation["improvement_suggestions"]:
            validation["improvement_suggestions"].append("Temporal context integration is appropriate")
        
        return validation
    
    def get_seasonal_context(self, month: Optional[int] = None) -> List[TemporalContext]:
        """Get seasonal/monthly relevant context for Honduras"""
        
        current_month = month or self.current_month
        
        seasonal_contexts = []
        
        # Hurricane season (June-November)
        if 6 <= current_month <= 11:
            hurricane_context = TemporalContext(
                context_type=TemporalContextType.CLIMATE_WEATHER,
                title="Hurricane Season Active",
                description="Currently in hurricane season, with heightened awareness of emergency preparedness",
                impact_level="high",
                affected_demographics=["all_users"],
                persona_implications=[
                    "More conscious of communication reliability during storms",
                    "Values emergency alert systems",
                    "Keeps devices charged and ready"
                ],
                conversation_references=[
                    "estamos en temporada de huracanes",
                    "hay que estar preparados para las tormentas",
                    "es importante tener comunicación en emergencias"
                ],
                time_period=f"June-November {self.current_year}",
                relevance_score=0.8
            )
            seasonal_contexts.append(hurricane_context)
        
        # School year context (February-November)
        if 2 <= current_month <= 11:
            school_context = TemporalContext(
                context_type=TemporalContextType.CULTURAL_EVENTS,
                title="School Year Active",
                description="School year in session, affecting family schedules and data usage patterns",
                impact_level="medium",
                affected_demographics=["families", "students", "parents"],
                persona_implications=[
                    "Higher data usage for educational needs",
                    "Family plans considerations for student devices",
                    "Schedule considerations around school activities"
                ],
                conversation_references=[
                    "los niños están en clases",
                    "necesitan internet para las tareas",
                    "el año escolar demanda más conectividad"
                ],
                time_period=f"February-November {self.current_year}",
                relevance_score=0.6
            )
            seasonal_contexts.append(school_context)
        
        # Holiday seasons
        if current_month == 12:
            holiday_context = TemporalContext(
                context_type=TemporalContextType.CULTURAL_EVENTS,
                title="December Holiday Season",
                description="Christmas and New Year celebrations with increased family communication",
                impact_level="medium",
                affected_demographics=["families", "all_users"],
                persona_implications=[
                    "Increased international calling to family abroad",
                    "More photo and video sharing during celebrations",
                    "Higher data usage for holiday content"
                ],
                conversation_references=[
                    "en Navidad hablamos más con la familia",
                    "compartimos muchas fotos de las celebraciones",
                    "necesitamos más datos para las fiestas"
                ],
                time_period=f"December {self.current_year}",
                relevance_score=0.7
            )
            seasonal_contexts.append(holiday_context)
        
        return seasonal_contexts
    
    def update_temporal_database(self, new_contexts: List[Dict[str, Any]]) -> None:
        """Update temporal database with new current events (for future enhancement)"""
        
        for context_data in new_contexts:
            context_type = TemporalContextType(context_data["context_type"])
            
            new_context = TemporalContext(
                context_type=context_type,
                title=context_data["title"],
                description=context_data["description"],
                impact_level=context_data["impact_level"],
                affected_demographics=context_data["affected_demographics"],
                persona_implications=context_data["persona_implications"],
                conversation_references=context_data["conversation_references"],
                time_period=context_data["time_period"],
                relevance_score=context_data["relevance_score"]
            )
            
            if context_type not in self.temporal_contexts:
                self.temporal_contexts[context_type] = []
            
            self.temporal_contexts[context_type].append(new_context)
        
        # Keep only recent contexts (remove old ones)
        self._cleanup_outdated_contexts()
    
    def _cleanup_outdated_contexts(self) -> None:
        """Remove outdated temporal contexts"""
        
        current_year = self.current_year
        
        for context_type, contexts in self.temporal_contexts.items():
            updated_contexts = []
            
            for context in contexts:
                # Keep if ongoing or recent (within 2 years)
                if ("ongoing" in context.time_period or 
                    str(current_year) in context.time_period or
                    str(current_year - 1) in context.time_period):
                    updated_contexts.append(context)
            
            self.temporal_contexts[context_type] = updated_contexts
    
    def get_context_statistics(self) -> Dict[str, Any]:
        """Get statistics about temporal context database"""
        
        total_contexts = sum(len(contexts) for contexts in self.temporal_contexts.values())
        
        context_by_type = {
            context_type.value: len(contexts) 
            for context_type, contexts in self.temporal_contexts.items()
        }
        
        high_impact_contexts = sum(
            1 for contexts in self.temporal_contexts.values()
            for context in contexts
            if context.impact_level == "high"
        )
        
        return {
            "total_contexts": total_contexts,
            "contexts_by_type": context_by_type,
            "high_impact_contexts": high_impact_contexts,
            "current_year": self.current_year,
            "last_updated": datetime.now().isoformat()
        }