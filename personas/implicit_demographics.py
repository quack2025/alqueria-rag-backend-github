# personas/implicit_demographics.py
"""
Implicit Demographics System for Stereotype-Free Persona Generation
Based on academic research showing explicit demographics activate harmful LLM stereotypes.

AVOID: 'You are a 40-year old Hispanic man' (activates LLM stereotypes)
USE: Names, neighborhoods, behavioral indicators, cultural context clues

Research shows explicit demographics cause LLMs to assume modal stereotypes,
while implicit cues allow for more authentic and diverse persona generation.
"""

import json
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ImplicitCueType(Enum):
    """Types of implicit demographic cues"""
    NAME_CULTURAL = "name_cultural"
    NEIGHBORHOOD = "neighborhood"
    BEHAVIORAL = "behavioral"
    LINGUISTIC = "linguistic"
    ECONOMIC_CONTEXT = "economic_context"
    SOCIAL_CONTEXT = "social_context"
    CULTURAL_REFERENCES = "cultural_references"


@dataclass
class ImplicitCue:
    """Single implicit demographic cue"""
    cue_type: ImplicitCueType
    value: str
    implied_demographics: Dict[str, Any]
    cultural_context: str
    strength: float  # How strongly this cue implies demographics (0.0-1.0)


class HondurasImplicitDemographics:
    """Generate implicit demographic cues for Honduras context"""
    
    def __init__(self):
        # Honduras-specific implicit cues database
        self.implicit_cues_database = {
            ImplicitCueType.NAME_CULTURAL: {
                # Names that imply cultural/regional background without explicit demographics
                "traditional_central": {
                    "male": ["Carlos Eduardo", "José Luis", "Mario Roberto", "Fernando Antonio"],
                    "female": ["María Elena", "Ana Cristina", "Rosa María", "Carmen Lucia"],
                    "context": "Traditional Central American naming patterns",
                    "economic_implication": "middle_class",
                    "regional_implication": "urban_traditional"
                },
                "modern_urban": {
                    "male": ["Diego", "Sebastián", "Mateo", "Santiago"],
                    "female": ["Sofía", "Isabella", "Valentina", "Camila"],
                    "context": "Modern urban naming trends",
                    "economic_implication": "middle_to_upper",
                    "regional_implication": "urban_modern"
                },
                "traditional_rural": {
                    "male": ["Juan", "Pedro", "Miguel", "Francisco"],
                    "female": ["María", "Carmen", "Rosa", "Ana"],
                    "context": "Traditional rural naming patterns",
                    "economic_implication": "working_class",
                    "regional_implication": "rural_traditional"
                }
            },
            
            ImplicitCueType.NEIGHBORHOOD: {
                "upscale_tegucigalpa": {
                    "areas": ["Lomas del Mayab", "Colonia Palmira", "Residencial Las Minitas"],
                    "economic_context": "middle_to_upper_class",
                    "lifestyle_indicators": ["seguridad privada", "áreas verdes", "centros comerciales cercanos"],
                    "telecom_usage": "high_data_usage"
                },
                "middle_class_sps": {
                    "areas": ["Colonia Trejo", "Barrio Guanacaste", "Residencial Los Andes"],
                    "economic_context": "middle_class",
                    "lifestyle_indicators": ["transporte público", "escuelas públicas", "pequeños comercios"],
                    "telecom_usage": "moderate_usage"
                },
                "working_class_urban": {
                    "areas": ["Colonia Kennedy", "Barrio Concepción", "Colonia Nueva Suyapa"],
                    "economic_context": "working_class",
                    "lifestyle_indicators": ["buses urbanos", "mercados locales", "pulperías"],
                    "telecom_usage": "basic_usage_prepaid"
                },
                "rural_communities": {
                    "areas": ["rural communities near", "aldeas cercanas a", "communities in"],
                    "economic_context": "rural_economy",
                    "lifestyle_indicators": ["agricultura", "ganadería", "cooperativas"],
                    "telecom_usage": "basic_voice_sms"
                }
            },
            
            ImplicitCueType.BEHAVIORAL: {
                "education_implied": {
                    "higher_education": {
                        "speech_patterns": ["technical vocabulary", "formal grammar", "analytical thinking"],
                        "references": ["university experiences", "professional development", "academic concepts"],
                        "decision_making": "research-based, analytical"
                    },
                    "practical_education": {
                        "speech_patterns": ["practical wisdom", "experiential knowledge", "common sense"],
                        "references": ["life experiences", "family teachings", "community wisdom"],
                        "decision_making": "experience-based, intuitive"
                    }
                },
                "economic_behavior": {
                    "price_conscious": {
                        "indicators": ["compares prices", "waits for promotions", "budgets carefully"],
                        "telecom_behavior": "switches for better deals, monitors usage",
                        "decision_factors": "value for money, family budget"
                    },
                    "quality_focused": {
                        "indicators": ["invests in durability", "researches before buying", "values reliability"],
                        "telecom_behavior": "pays for premium service, values network quality",
                        "decision_factors": "service quality, reliability"
                    }
                }
            },
            
            ImplicitCueType.LINGUISTIC: {
                "regional_expressions": {
                    "central_honduras": {
                        "expressions": ["¡Qué chilero!", "Está tuanis", "¡Púchica!"],
                        "formality": "mixed formal and informal",
                        "cultural_context": "central region, mixed urban-rural"
                    },
                    "northern_coast": {
                        "expressions": ["¡Órale!", "Está cabal", "¡Qué joda!"],
                        "formality": "more informal, coastal influence",
                        "cultural_context": "northern coast, Caribbean influence"
                    },
                    "formal_educated": {
                        "expressions": ["Por supuesto", "Evidentemente", "Sin lugar a dudas"],
                        "formality": "consistently formal",
                        "cultural_context": "formal education, professional environment"
                    }
                },
                "communication_style": {
                    "direct_communicator": {
                        "patterns": ["says what they think", "straightforward questions", "clear preferences"],
                        "personality_implication": "low agreeableness, high assertiveness"
                    },
                    "diplomatic_communicator": {
                        "patterns": ["considers others' feelings", "indirect suggestions", "balanced perspectives"],
                        "personality_implication": "high agreeableness, cultural harmony"
                    },
                    "analytical_communicator": {
                        "patterns": ["explains reasoning", "provides context", "systematic thinking"],
                        "personality_implication": "high openness, education-influenced"
                    }
                }
            },
            
            ImplicitCueType.ECONOMIC_CONTEXT: {
                "transportation_references": {
                    "private_vehicle": {
                        "context": "owns car, references parking, gas prices, traffic",
                        "economic_implication": "middle_class_plus",
                        "lifestyle": "suburban, convenience-oriented"
                    },
                    "public_transport": {
                        "context": "bus routes, waiting times, crowded transport",
                        "economic_implication": "working_to_middle_class",
                        "lifestyle": "urban, time-conscious"
                    },
                    "walking_mototaxi": {
                        "context": "walking distances, mototaxi fares, neighborhood accessibility",
                        "economic_implication": "working_class",
                        "lifestyle": "local, community-based"
                    }
                },
                "housing_references": {
                    "homeowner": {
                        "context": "home improvements, property concerns, neighborhood issues",
                        "economic_implication": "established, investment-minded",
                        "life_stage": "settled, family-oriented"
                    },
                    "renter": {
                        "context": "landlord relations, moving considerations, rent concerns",
                        "economic_implication": "flexible, cost-conscious",
                        "life_stage": "transitional, adaptable"
                    }
                }
            },
            
            ImplicitCueType.SOCIAL_CONTEXT: {
                "family_structure_references": {
                    "extended_family": {
                        "context": "Sunday family gatherings, multiple generations, shared decisions",
                        "cultural_implication": "traditional values, collective decision-making",
                        "telecom_behavior": "family plans, group communication"
                    },
                    "nuclear_family": {
                        "context": "individual family decisions, couple dynamics, immediate family focus",
                        "cultural_implication": "modern values, individual autonomy",
                        "telecom_behavior": "personal plans, individual usage"
                    },
                    "single_lifestyle": {
                        "context": "personal time, individual decisions, friend networks",
                        "cultural_implication": "independent values, peer-oriented",
                        "telecom_behavior": "social media focus, entertainment usage"
                    }
                },
                "community_involvement": {
                    "church_community": {
                        "context": "church activities, faith-based decisions, religious calendar",
                        "cultural_implication": "traditional values, community-oriented",
                        "decision_making": "values-based, community consensus"
                    },
                    "neighborhood_active": {
                        "context": "community meetings, local issues, neighbor relations",
                        "cultural_implication": "civic-minded, locally engaged",
                        "decision_making": "community-aware, socially responsible"
                    },
                    "work_social": {
                        "context": "colleague relationships, professional networks, work events",
                        "cultural_implication": "career-focused, professional identity",
                        "decision_making": "professional considerations, network-influenced"
                    }
                }
            },
            
            ImplicitCueType.CULTURAL_REFERENCES: {
                "media_consumption": {
                    "traditional_media": {
                        "references": ["telenovelas", "radio news", "local newspapers"],
                        "cultural_implication": "traditional media habits, family-shared content",
                        "age_implication": "older_millennial_plus"
                    },
                    "digital_native": {
                        "references": ["TikTok", "Instagram stories", "YouTube channels"],
                        "cultural_implication": "digital-first lifestyle, individual content",
                        "age_implication": "younger_millennial_genz"
                    },
                    "mixed_consumption": {
                        "references": ["Facebook", "WhatsApp groups", "online news"],
                        "cultural_implication": "transitional media habits, bridge generation",
                        "age_implication": "middle_millennial"
                    }
                },
                "cultural_events": {
                    "traditional_celebrations": {
                        "references": ["Feria Juniana", "Semana Santa traditions", "patron saint festivals"],
                        "cultural_implication": "deep cultural roots, traditional participation",
                        "community_connection": "strong local ties"
                    },
                    "modern_events": {
                        "references": ["concerts", "festivals", "cultural centers"],
                        "cultural_implication": "modern cultural engagement, urban lifestyle",
                        "community_connection": "broader cultural participation"
                    }
                }
            }
        }
    
    def generate_implicit_persona_profile(self, target_demographics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implicit persona profile that avoids explicit demographic statements"""
        
        # Extract target demographics
        target_age = target_demographics.get("age", 30)
        target_gender = target_demographics.get("gender", "Masculino")
        target_education = target_demographics.get("education_level", "Secundaria")
        target_income = target_demographics.get("income_bracket", "Medio")
        target_region = target_demographics.get("geographic_region", "Tegucigalpa")
        
        # Generate implicit cues
        implicit_profile = {
            "identity_cues": self._generate_identity_cues(target_age, target_gender, target_education),
            "behavioral_cues": self._generate_behavioral_cues(target_education, target_income),
            "linguistic_cues": self._generate_linguistic_cues(target_region, target_education),
            "economic_cues": self._generate_economic_cues(target_income),
            "social_cues": self._generate_social_cues(target_age, target_demographics.get("marital_status")),
            "cultural_cues": self._generate_cultural_cues(target_age, target_region),
            "implied_characteristics": self._extract_implied_characteristics(target_demographics)
        }
        
        return implicit_profile
    
    def _generate_identity_cues(self, age: int, gender: str, education: str) -> Dict[str, Any]:
        """Generate identity cues through names and context"""
        
        # Select name category based on age and education
        if age < 30 and "superior" in education.lower():
            name_category = "modern_urban"
        elif age > 40 or "primaria" in education.lower():
            name_category = "traditional_rural"
        else:
            name_category = "traditional_central"
        
        name_data = self.implicit_cues_database[ImplicitCueType.NAME_CULTURAL][name_category]
        gender_key = "male" if gender == "Masculino" else "female"
        
        selected_name = random.choice(name_data[gender_key])
        
        return {
            "name": selected_name,
            "name_cultural_context": name_data["context"],
            "implied_economic_level": name_data["economic_implication"],
            "implied_regional_background": name_data["regional_implication"]
        }
    
    def _generate_behavioral_cues(self, education: str, income: str) -> Dict[str, Any]:
        """Generate behavioral indicators that imply education and economic status"""
        
        # Education behavioral cues
        if "superior" in education.lower() or "universit" in education.lower():
            education_behavior = self.implicit_cues_database[ImplicitCueType.BEHAVIORAL]["education_implied"]["higher_education"]
        else:
            education_behavior = self.implicit_cues_database[ImplicitCueType.BEHAVIORAL]["education_implied"]["practical_education"]
        
        # Economic behavioral cues
        if "bajo" in income.lower():
            economic_behavior = self.implicit_cues_database[ImplicitCueType.BEHAVIORAL]["economic_behavior"]["price_conscious"]
        else:
            economic_behavior = self.implicit_cues_database[ImplicitCueType.BEHAVIORAL]["economic_behavior"]["quality_focused"]
        
        return {
            "speech_patterns": education_behavior["speech_patterns"],
            "reference_types": education_behavior["references"],
            "decision_making_style": education_behavior["decision_making"],
            "economic_behavior_indicators": economic_behavior["indicators"],
            "telecom_behavior_pattern": economic_behavior["telecom_behavior"],
            "primary_decision_factors": economic_behavior["decision_factors"]
        }
    
    def _generate_linguistic_cues(self, region: str, education: str) -> Dict[str, Any]:
        """Generate linguistic patterns that imply regional and educational background"""
        
        # Regional linguistic patterns
        if "san pedro" in region.lower() or "ceiba" in region.lower():
            regional_pattern = "northern_coast"
        elif "superior" in education.lower():
            regional_pattern = "formal_educated"
        else:
            regional_pattern = "central_honduras"
        
        linguistic_data = self.implicit_cues_database[ImplicitCueType.LINGUISTIC]["regional_expressions"][regional_pattern]
        
        # Communication style based on implied personality
        communication_styles = list(self.implicit_cues_database[ImplicitCueType.LINGUISTIC]["communication_style"].keys())
        selected_style = random.choice(communication_styles)
        style_data = self.implicit_cues_database[ImplicitCueType.LINGUISTIC]["communication_style"][selected_style]
        
        return {
            "regional_expressions": linguistic_data["expressions"],
            "formality_level": linguistic_data["formality"],
            "regional_cultural_context": linguistic_data["cultural_context"],
            "communication_style": selected_style,
            "communication_patterns": style_data["patterns"],
            "implied_personality_traits": style_data["personality_implication"]
        }
    
    def _generate_economic_cues(self, income: str) -> Dict[str, Any]:
        """Generate economic context cues through lifestyle references"""
        
        # Transportation context
        if "alto" in income.lower():
            transport_context = "private_vehicle"
        elif "medio" in income.lower():
            transport_context = "public_transport"
        else:
            transport_context = "walking_mototaxi"
        
        transport_data = self.implicit_cues_database[ImplicitCueType.ECONOMIC_CONTEXT]["transportation_references"][transport_context]
        
        # Housing context (randomly selected to add variety)
        housing_contexts = list(self.implicit_cues_database[ImplicitCueType.ECONOMIC_CONTEXT]["housing_references"].keys())
        housing_context = random.choice(housing_contexts)
        housing_data = self.implicit_cues_database[ImplicitCueType.ECONOMIC_CONTEXT]["housing_references"][housing_context]
        
        return {
            "transportation_context": transport_data["context"],
            "transportation_economic_implication": transport_data["economic_implication"],
            "lifestyle_pattern": transport_data["lifestyle"],
            "housing_context": housing_data["context"],
            "housing_economic_implication": housing_data["economic_implication"],
            "housing_life_stage": housing_data["life_stage"]
        }
    
    def _generate_social_cues(self, age: int, marital_status: Optional[str]) -> Dict[str, Any]:
        """Generate social context cues that imply family and community dynamics"""
        
        # Family structure based on age and marital status
        if marital_status and "casado" in marital_status.lower():
            if age > 35:
                family_structure = "extended_family"
            else:
                family_structure = "nuclear_family"
        else:
            family_structure = "single_lifestyle"
        
        family_data = self.implicit_cues_database[ImplicitCueType.SOCIAL_CONTEXT]["family_structure_references"][family_structure]
        
        # Community involvement (randomly selected for variety)
        community_types = list(self.implicit_cues_database[ImplicitCueType.SOCIAL_CONTEXT]["community_involvement"].keys())
        community_type = random.choice(community_types)
        community_data = self.implicit_cues_database[ImplicitCueType.SOCIAL_CONTEXT]["community_involvement"][community_type]
        
        return {
            "family_context_references": family_data["context"],
            "cultural_values_implication": family_data["cultural_implication"],
            "telecom_usage_pattern": family_data["telecom_behavior"],
            "community_involvement_type": community_type,
            "community_context": community_data["context"],
            "community_values": community_data["cultural_implication"],
            "decision_making_influence": community_data["decision_making"]
        }
    
    def _generate_cultural_cues(self, age: int, region: str) -> Dict[str, Any]:
        """Generate cultural reference cues that imply age and regional background"""
        
        # Media consumption patterns based on age
        if age < 25:
            media_pattern = "digital_native"
        elif age > 45:
            media_pattern = "traditional_media"
        else:
            media_pattern = "mixed_consumption"
        
        media_data = self.implicit_cues_database[ImplicitCueType.CULTURAL_REFERENCES]["media_consumption"][media_pattern]
        
        # Cultural events participation
        cultural_events = list(self.implicit_cues_database[ImplicitCueType.CULTURAL_REFERENCES]["cultural_events"].keys())
        event_type = random.choice(cultural_events)
        event_data = self.implicit_cues_database[ImplicitCueType.CULTURAL_REFERENCES]["cultural_events"][event_type]
        
        return {
            "media_references": media_data["references"],
            "media_cultural_implication": media_data["cultural_implication"],
            "implied_age_group": media_data["age_implication"],
            "cultural_event_references": event_data["references"],
            "cultural_participation_level": event_data["cultural_implication"],
            "community_connection_strength": event_data["community_connection"]
        }
    
    def _extract_implied_characteristics(self, target_demographics: Dict[str, Any]) -> Dict[str, Any]:
        """Extract characteristics that can be implied without explicit mention"""
        
        return {
            "life_stage_indicators": self._get_life_stage_indicators(
                target_demographics.get("age", 30),
                target_demographics.get("marital_status"),
                target_demographics.get("children_count", 0)
            ),
            "value_system_indicators": self._get_value_system_indicators(
                target_demographics.get("values_family", 5),
                target_demographics.get("values_tradition", 5),
                target_demographics.get("religious_spirituality", "Moderado")
            ),
            "lifestyle_indicators": self._get_lifestyle_indicators(
                target_demographics.get("technology_adoption", "Promedio"),
                target_demographics.get("social_media_usage", "Moderado")
            )
        }
    
    def _get_life_stage_indicators(self, age: int, marital_status: Optional[str], children: int) -> List[str]:
        """Get indicators that imply life stage without explicit demographics"""
        indicators = []
        
        if age < 25:
            indicators.extend(["establishing independence", "exploring opportunities", "building future"])
        elif age < 35:
            indicators.extend(["career building", "relationship focus", "life planning"])
        elif age < 50:
            indicators.extend(["family priorities", "stability seeking", "responsibility focus"])
        else:
            indicators.extend(["experience sharing", "legacy thinking", "wisdom offering"])
        
        if marital_status and "casado" in marital_status.lower():
            indicators.extend(["partnership decisions", "shared responsibilities", "couple dynamics"])
        
        if children > 0:
            indicators.extend(["family planning", "educational concerns", "future generations"])
        
        return indicators
    
    def _get_value_system_indicators(self, family_values: int, traditional_values: int, religiosity: str) -> List[str]:
        """Get indicators that imply value system without explicit statements"""
        indicators = []
        
        if family_values > 7:
            indicators.extend(["collective decision-making", "family consultation", "generational wisdom"])
        
        if traditional_values > 6:
            indicators.extend(["established practices", "cultural continuity", "respectful approaches"])
        
        if religiosity in ["Religioso", "Muy religioso"]:
            indicators.extend(["faith-informed decisions", "moral considerations", "spiritual reflection"])
        
        return indicators
    
    def _get_lifestyle_indicators(self, tech_adoption: str, social_media: str) -> List[str]:
        """Get indicators that imply lifestyle preferences without explicit tech usage"""
        indicators = []
        
        if "innovador" in tech_adoption.lower():
            indicators.extend(["efficiency seeking", "solution oriented", "adaptation focused"])
        elif "conservador" in tech_adoption.lower():
            indicators.extend(["stability preferring", "proven methods", "cautious adoption"])
        
        if "alto" in social_media.lower():
            indicators.extend(["social connectivity", "information sharing", "community participation"])
        elif "bajo" in social_media.lower():
            indicators.extend(["privacy conscious", "direct communication", "personal interaction"])
        
        return indicators
    
    def create_implicit_persona_prompt(self, implicit_profile: Dict[str, Any], 
                                     conversation_context: str = "") -> str:
        """Create persona prompt using only implicit cues, avoiding explicit demographics"""
        
        # Extract implicit cues
        identity = implicit_profile["identity_cues"]
        behavioral = implicit_profile["behavioral_cues"]
        linguistic = implicit_profile["linguistic_cues"]
        economic = implicit_profile["economic_cues"]
        social = implicit_profile["social_cues"]
        cultural = implicit_profile["cultural_cues"]
        characteristics = implicit_profile["implied_characteristics"]
        
        # Build implicit persona prompt
        prompt = f"""IDENTIDAD PERSONAL IMPLICITA:
Te llamas {identity["name"]}. Vives en Honduras y tu forma de hablar y actuar refleja {identity["name_cultural_context"].lower()}. Tu manera de tomar decisiones es {behavioral["decision_making_style"]}, y cuando hablas, {", ".join(behavioral["speech_patterns"][:2])}.

CONTEXTO DE VIDA:
En tu dia a dia, {economic["transportation_context"]}. Tu situacion de vivienda se caracteriza por {economic["housing_context"]}. {social["family_context_references"]}. Tu participacion en la comunidad incluye {social["community_context"]}.

ESTILO DE COMUNICACION:
Tu forma de expresarte es {linguistic["formality_level"]} y ocasionalmente usas expresiones como "{random.choice(linguistic["regional_expressions"])}". Tu estilo de comunicacion se caracteriza por {", ".join(linguistic["communication_patterns"][:2])}.

REFERENCIAS CULTURALES Y MEDIOS:
Te relacionas con contenido como {", ".join(cultural["media_references"][:2])} y participas en {", ".join(cultural["cultural_event_references"][:2])}. Esto refleja {cultural["media_cultural_implication"]}.

PATRONES DE COMPORTAMIENTO:
{", ".join(behavioral["economic_behavior_indicators"][:2])}. En telecomunicaciones, {behavioral["telecom_behavior_pattern"]}. Tus decisiones se basan principalmente en {behavioral["primary_decision_factors"]}.

VALORES Y PERSPECTIVA DE VIDA:
Tu enfoque de vida se caracteriza por {", ".join(characteristics["life_stage_indicators"][:2])}. Tus valores se reflejan en {", ".join(characteristics["value_system_indicators"][:2])}. Tu estilo de vida muestra {", ".join(characteristics["lifestyle_indicators"][:2])}.

INSTRUCCIONES IMPORTANTES:
- Nunca menciones explicitamente tu edad, genero, nivel educativo o ingresos
- Deja que estas caracteristicas se infieran naturalmente de tu forma de hablar y referencias
- Manten consistencia con el contexto cultural y economico implicito
- Usa referencias especificas de tu experiencia de vida sin categorizar demograficamente
- Responde de manera autentica basada en tu contexto de vida implicito

{conversation_context}

Recuerda: Eres una persona real con experiencias especificas. Tu identidad se revela a traves de tus experiencias, no de categorias demograficas."""
        
        return prompt
    
    def validate_implicit_effectiveness(self, prompt: str, response: str) -> Dict[str, Any]:
        """Validate that implicit approach is working effectively"""
        
        # Check for explicit demographic mentions (problematic)
        explicit_demographics = [
            "soy hombre", "soy mujer", "tengo X años", "soy de clase", 
            "mi nivel educativo", "mis ingresos", "soy profesional",
            "years old", "I am a", "my gender", "my age"
        ]
        
        problematic_mentions = []
        response_lower = response.lower()
        
        for explicit_demo in explicit_demographics:
            if explicit_demo.lower() in response_lower:
                problematic_mentions.append(explicit_demo)
        
        # Check for implicit cue effectiveness (positive)
        implicit_indicators = [
            "cultural_references", "behavioral_context", "linguistic_patterns",
            "economic_context", "social_context", "life_experience_references"
        ]
        
        effective_implications = []
        
        # Cultural references check
        honduras_cultural_words = ["honduras", "hondureño", "tegucigalpa", "san pedro", "semana santa", "feria"]
        if any(word in response_lower for word in honduras_cultural_words):
            effective_implications.append("cultural_references")
        
        # Behavioral context check
        decision_words = ["decidí", "prefiero", "siempre", "acostumbro", "suelo"]
        if any(word in response_lower for word in decision_words):
            effective_implications.append("behavioral_context")
        
        # Economic context check
        economic_words = ["presupuesto", "precio", "costo", "invertir", "ahorrar", "gasto"]
        if any(word in response_lower for word in economic_words):
            effective_implications.append("economic_context")
        
        # Social context check
        social_words = ["familia", "comunidad", "vecinos", "amigos", "trabajo"]
        if any(word in response_lower for word in social_words):
            effective_implications.append("social_context")
        
        # Calculate effectiveness score
        effectiveness_score = len(effective_implications) / len(implicit_indicators)
        problematic_score = len(problematic_mentions)
        
        overall_score = max(0, effectiveness_score - (problematic_score * 0.2))
        
        return {
            "effectiveness_score": round(effectiveness_score, 2),
            "problematic_mentions": problematic_mentions,
            "effective_implications": effective_implications,
            "overall_score": round(overall_score, 2),
            "status": "Excellent" if overall_score > 0.7 else "Good" if overall_score > 0.5 else "Needs Improvement",
            "recommendations": self._generate_improvement_recommendations(
                problematic_mentions, effective_implications
            )
        }
    
    def _generate_improvement_recommendations(self, problematic_mentions: List[str], 
                                           effective_implications: List[str]) -> List[str]:
        """Generate recommendations for improving implicit demographic approach"""
        recommendations = []
        
        if problematic_mentions:
            recommendations.append("Remove explicit demographic mentions and replace with experiential context")
            recommendations.append("Use life experiences and behavioral patterns instead of categories")
        
        if len(effective_implications) < 3:
            recommendations.append("Add more cultural and social context references")
            recommendations.append("Include specific behavioral and economic indicators")
        
        if "cultural_references" not in effective_implications:
            recommendations.append("Include more Honduras-specific cultural references")
        
        if "economic_context" not in effective_implications:
            recommendations.append("Add lifestyle and economic behavior indicators")
        
        if not recommendations:
            recommendations.append("Implicit approach is working effectively")
        
        return recommendations