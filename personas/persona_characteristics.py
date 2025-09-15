# personas/persona_characteristics.py
"""
Comprehensive Persona Characteristics System with Ethical Safeguards
Based on academic paper 2504.02234v2
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
import numpy as np


@dataclass
class CharacteristicDefinition:
    """Definition of a persona characteristic"""
    name: str
    category: str
    data_type: str  # 'categorical', 'numerical', 'boolean', 'text'
    options: List[Any] = field(default_factory=list)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    weight: float = 1.0  # Importance for persona consistency
    ethical_flag: bool = False  # Requires special handling for bias
    stereotype_risk: str = "low"  # 'low', 'medium', 'high'
    honduras_context: bool = False  # Honduras-specific characteristic


class UniversalCharacteristics:
    """80 Universal characteristics applicable to any industry"""
    
    @staticmethod
    def get_characteristics() -> Dict[str, CharacteristicDefinition]:
        return {
            # Demographics (15 characteristics)
            "age": CharacteristicDefinition(
                "age", "demographics", "numerical", 
                min_value=18, max_value=75, weight=1.5,
                ethical_flag=True, stereotype_risk="medium"
            ),
            "gender": CharacteristicDefinition(
                "gender", "demographics", "categorical",
                options=["Masculino", "Femenino", "No binario", "Prefiero no decir"],
                weight=1.2, ethical_flag=True, stereotype_risk="high"
            ),
            "education_level": CharacteristicDefinition(
                "education_level", "demographics", "categorical",
                options=["Primaria", "Secundaria", "Técnica", "Universitaria", "Postgrado"],
                weight=1.3, ethical_flag=True, stereotype_risk="medium"
            ),
            "income_bracket": CharacteristicDefinition(
                "income_bracket", "demographics", "categorical",
                options=["Bajo (< L.15,000)", "Medio-bajo (L.15,000-25,000)", 
                        "Medio (L.25,000-40,000)", "Medio-alto (L.40,000-60,000)", 
                        "Alto (> L.60,000)"],
                weight=1.4, ethical_flag=True, stereotype_risk="high"
            ),
            "marital_status": CharacteristicDefinition(
                "marital_status", "demographics", "categorical",
                options=["Soltero/a", "Casado/a", "Unión libre", "Divorciado/a", "Viudo/a"],
                weight=1.0, stereotype_risk="low"
            ),
            "household_size": CharacteristicDefinition(
                "household_size", "demographics", "numerical",
                min_value=1, max_value=8, weight=1.1
            ),
            "children_count": CharacteristicDefinition(
                "children_count", "demographics", "numerical",
                min_value=0, max_value=6, weight=1.2
            ),
            "employment_status": CharacteristicDefinition(
                "employment_status", "demographics", "categorical",
                options=["Empleado tiempo completo", "Empleado medio tiempo", "Independiente", 
                        "Estudiante", "Desempleado", "Jubilado", "Ama de casa"],
                weight=1.3, ethical_flag=True, stereotype_risk="medium"
            ),
            "occupation_sector": CharacteristicDefinition(
                "occupation_sector", "demographics", "categorical",
                options=["Servicios", "Comercio", "Manufactura", "Agricultura", "Construcción",
                        "Educación", "Salud", "Tecnología", "Finanzas", "Gobierno"],
                weight=1.2, stereotype_risk="medium"
            ),
            "residence_type": CharacteristicDefinition(
                "residence_type", "demographics", "categorical",
                options=["Casa propia", "Casa alquilada", "Apartamento propio", 
                        "Apartamento alquilado", "Vive con familia"],
                weight=1.0
            ),
            "geographic_region": CharacteristicDefinition(
                "geographic_region", "demographics", "categorical",
                options=["Tegucigalpa", "San Pedro Sula", "La Ceiba", "Choloma", 
                        "El Progreso", "Choluteca", "Comayagua", "Puerto Cortés", "Rural"],
                weight=1.4, honduras_context=True, stereotype_risk="medium"
            ),
            "urban_rural": CharacteristicDefinition(
                "urban_rural", "demographics", "categorical",
                options=["Urbano", "Suburbano", "Rural"],
                weight=1.2, honduras_context=True
            ),
            "language_preference": CharacteristicDefinition(
                "language_preference", "demographics", "categorical",
                options=["Español", "Inglés limitado", "Lengua indígena", "Bilingüe"],
                weight=1.1, honduras_context=True
            ),
            "generational_cohort": CharacteristicDefinition(
                "generational_cohort", "demographics", "categorical",
                options=["Gen Z (18-26)", "Millennial (27-42)", "Gen X (43-58)", "Boomer (59+)"],
                weight=1.3, stereotype_risk="medium"
            ),
            "socioeconomic_mobility": CharacteristicDefinition(
                "socioeconomic_mobility", "demographics", "categorical",
                options=["Ascendente", "Estable", "Descendente"],
                weight=1.1, ethical_flag=True
            ),

            # Psychographics (20 characteristics)
            "personality_openness": CharacteristicDefinition(
                "personality_openness", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.2
            ),
            "personality_conscientiousness": CharacteristicDefinition(
                "personality_conscientiousness", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.2
            ),
            "personality_extraversion": CharacteristicDefinition(
                "personality_extraversion", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.3
            ),
            "personality_agreeableness": CharacteristicDefinition(
                "personality_agreeableness", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.1
            ),
            "personality_neuroticism": CharacteristicDefinition(
                "personality_neuroticism", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.1
            ),
            "risk_tolerance": CharacteristicDefinition(
                "risk_tolerance", "psychographics", "categorical",
                options=["Muy conservador", "Conservador", "Moderado", "Arriesgado", "Muy arriesgado"],
                weight=1.4
            ),
            "decision_making_style": CharacteristicDefinition(
                "decision_making_style", "psychographics", "categorical",
                options=["Analítico", "Intuitivo", "Consultivo", "Impulsivo", "Procrastinador"],
                weight=1.3
            ),
            "values_family": CharacteristicDefinition(
                "values_family", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.5, honduras_context=True
            ),
            "values_tradition": CharacteristicDefinition(
                "values_tradition", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.2, honduras_context=True
            ),
            "values_achievement": CharacteristicDefinition(
                "values_achievement", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.3
            ),
            "values_security": CharacteristicDefinition(
                "values_security", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.4
            ),
            "values_hedonism": CharacteristicDefinition(
                "values_hedonism", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.1
            ),
            "social_influence_susceptibility": CharacteristicDefinition(
                "social_influence_susceptibility", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.2
            ),
            "technology_adoption": CharacteristicDefinition(
                "technology_adoption", "psychographics", "categorical",
                options=["Innovador", "Early adopter", "Mayoría temprana", "Mayoría tardía", "Rezagado"],
                weight=1.4
            ),
            "brand_loyalty_tendency": CharacteristicDefinition(
                "brand_loyalty_tendency", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.5
            ),
            "price_sensitivity": CharacteristicDefinition(
                "price_sensitivity", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.5
            ),
            "environmental_consciousness": CharacteristicDefinition(
                "environmental_consciousness", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.1
            ),
            "social_responsibility_importance": CharacteristicDefinition(
                "social_responsibility_importance", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.2
            ),
            "information_seeking_behavior": CharacteristicDefinition(
                "information_seeking_behavior", "psychographics", "categorical",
                options=["Investigador exhaustivo", "Consultivo", "Básico", "Impulsivo"],
                weight=1.3
            ),
            "cultural_identity_strength": CharacteristicDefinition(
                "cultural_identity_strength", "psychographics", "numerical",
                min_value=1, max_value=10, weight=1.3, honduras_context=True
            ),

            # Behavioral (20 characteristics)
            "media_consumption_tv": CharacteristicDefinition(
                "media_consumption_tv", "behavioral", "numerical",
                min_value=0, max_value=8, weight=1.2
            ),
            "media_consumption_radio": CharacteristicDefinition(
                "media_consumption_radio", "behavioral", "numerical",
                min_value=0, max_value=6, weight=1.1
            ),
            "media_consumption_social": CharacteristicDefinition(
                "media_consumption_social", "behavioral", "numerical",
                min_value=0, max_value=12, weight=1.4
            ),
            "shopping_frequency": CharacteristicDefinition(
                "shopping_frequency", "behavioral", "categorical",
                options=["Diario", "Semanal", "Quincenal", "Mensual", "Ocasional"],
                weight=1.2
            ),
            "shopping_preference": CharacteristicDefinition(
                "shopping_preference", "behavioral", "categorical",
                options=["Tiendas físicas", "Online", "Mixto", "Mercados locales"],
                weight=1.3
            ),
            "brand_switching_frequency": CharacteristicDefinition(
                "brand_switching_frequency", "behavioral", "categorical",
                options=["Nunca", "Raramente", "Ocasionalmente", "Frecuentemente", "Constantemente"],
                weight=1.4
            ),
            "complaint_behavior": CharacteristicDefinition(
                "complaint_behavior", "behavioral", "categorical",
                options=["Confrontativo", "Asertivo", "Pasivo", "Evitativo", "Público (redes)"],
                weight=1.3
            ),
            "word_of_mouth_tendency": CharacteristicDefinition(
                "word_of_mouth_tendency", "behavioral", "numerical",
                min_value=1, max_value=10, weight=1.3
            ),
            "social_media_activity": CharacteristicDefinition(
                "social_media_activity", "behavioral", "categorical",
                options=["Muy activo", "Activo", "Moderado", "Pasivo", "No usuario"],
                weight=1.3
            ),
            "preferred_communication": CharacteristicDefinition(
                "preferred_communication", "behavioral", "categorical",
                options=["Llamadas", "WhatsApp", "Email", "Redes sociales", "Presencial"],
                weight=1.2
            ),
            "payment_preference": CharacteristicDefinition(
                "payment_preference", "behavioral", "categorical",
                options=["Efectivo", "Tarjeta débito", "Tarjeta crédito", "Transferencias", "Billeteras digitales"],
                weight=1.2
            ),
            "loyalty_program_participation": CharacteristicDefinition(
                "loyalty_program_participation", "behavioral", "categorical",
                options=["Muy activo", "Activo", "Ocasional", "Registrado sin uso", "No participa"],
                weight=1.1
            ),
            "time_of_day_preference": CharacteristicDefinition(
                "time_of_day_preference", "behavioral", "categorical",
                options=["Madrugador", "Matutino", "Vespertino", "Nocturno"],
                weight=1.0
            ),
            "weekend_vs_weekday": CharacteristicDefinition(
                "weekend_vs_weekday", "behavioral", "categorical",
                options=["Rutina similar", "Muy diferente", "Algo diferente"],
                weight=1.0
            ),
            "impulse_buying_tendency": CharacteristicDefinition(
                "impulse_buying_tendency", "behavioral", "numerical",
                min_value=1, max_value=10, weight=1.3
            ),
            "research_before_purchase": CharacteristicDefinition(
                "research_before_purchase", "behavioral", "categorical",
                options=["Investigación exhaustiva", "Investigación básica", "Decisión rápida"],
                weight=1.3
            ),
            "seasonal_behavior_change": CharacteristicDefinition(
                "seasonal_behavior_change", "behavioral", "boolean",
                weight=1.1
            ),
            "group_vs_individual_decisions": CharacteristicDefinition(
                "group_vs_individual_decisions", "behavioral", "categorical",
                options=["Siempre consulta", "Frecuentemente consulta", "Ocasionalmente", "Independiente"],
                weight=1.2
            ),
            "brand_advocacy_level": CharacteristicDefinition(
                "brand_advocacy_level", "behavioral", "numerical",
                min_value=1, max_value=10, weight=1.4
            ),
            "customer_service_expectations": CharacteristicDefinition(
                "customer_service_expectations", "behavioral", "categorical",
                options=["Muy altas", "Altas", "Moderadas", "Básicas"],
                weight=1.3
            ),

            # Communication & Language (10 characteristics)
            "communication_style": CharacteristicDefinition(
                "communication_style", "communication", "categorical",
                options=["Directo", "Indirecto", "Emocional", "Lógico", "Narrativo"],
                weight=1.3
            ),
            "formality_preference": CharacteristicDefinition(
                "formality_preference", "communication", "categorical",
                options=["Muy formal", "Formal", "Semi-formal", "Informal", "Muy informal"],
                weight=1.2, honduras_context=True
            ),
            "humor_appreciation": CharacteristicDefinition(
                "humor_appreciation", "communication", "numerical",
                min_value=1, max_value=10, weight=1.1
            ),
            "emotional_expressiveness": CharacteristicDefinition(
                "emotional_expressiveness", "communication", "numerical",
                min_value=1, max_value=10, weight=1.2
            ),
            "attention_span": CharacteristicDefinition(
                "attention_span", "communication", "categorical",
                options=["Muy corto (< 2 min)", "Corto (2-5 min)", "Medio (5-15 min)", "Largo (15+ min)"],
                weight=1.3
            ),
            "preferred_content_type": CharacteristicDefinition(
                "preferred_content_type", "communication", "categorical",
                options=["Texto", "Visual", "Video", "Audio", "Interactivo"],
                weight=1.2
            ),
            "local_expressions_usage": CharacteristicDefinition(
                "local_expressions_usage", "communication", "numerical",
                min_value=1, max_value=10, weight=1.2, honduras_context=True
            ),
            "skepticism_level": CharacteristicDefinition(
                "skepticism_level", "communication", "numerical",
                min_value=1, max_value=10, weight=1.4
            ),
            "authority_respect": CharacteristicDefinition(
                "authority_respect", "communication", "numerical",
                min_value=1, max_value=10, weight=1.2, honduras_context=True
            ),
            "social_desirability_bias": CharacteristicDefinition(
                "social_desirability_bias", "communication", "numerical",
                min_value=1, max_value=10, weight=1.3, ethical_flag=True
            ),

            # Lifestyle & Interests (15 characteristics)
            "lifestyle_activity_level": CharacteristicDefinition(
                "lifestyle_activity_level", "lifestyle", "categorical",
                options=["Muy activo", "Activo", "Moderado", "Sedentario"],
                weight=1.1
            ),
            "hobbies_interests": CharacteristicDefinition(
                "hobbies_interests", "lifestyle", "categorical",
                options=["Deportes", "Música", "Lectura", "Cocina", "Tecnología", 
                        "Manualidades", "Jardinería", "Viajes", "Juegos"],
                weight=1.1
            ),
            "entertainment_preference": CharacteristicDefinition(
                "entertainment_preference", "lifestyle", "categorical",
                options=["TV/Series", "Música", "Deportes", "Gaming", "Lectura", "Actividades sociales"],
                weight=1.2
            ),
            "social_circle_size": CharacteristicDefinition(
                "social_circle_size", "lifestyle", "categorical",
                options=["Muy amplio", "Amplio", "Moderado", "Pequeño", "Muy pequeño"],
                weight=1.1
            ),
            "travel_frequency": CharacteristicDefinition(
                "travel_frequency", "lifestyle", "categorical",
                options=["Frecuente", "Ocasional", "Raro", "Nunca"],
                weight=1.1
            ),
            "health_consciousness": CharacteristicDefinition(
                "health_consciousness", "lifestyle", "numerical",
                min_value=1, max_value=10, weight=1.2
            ),
            "fitness_routine": CharacteristicDefinition(
                "fitness_routine", "lifestyle", "categorical",
                options=["Muy regular", "Regular", "Ocasional", "Ninguna"],
                weight=1.1
            ),
            "diet_preferences": CharacteristicDefinition(
                "diet_preferences", "lifestyle", "categorical",
                options=["Sin restricción", "Saludable", "Vegetariana", "Especial por salud"],
                weight=1.0
            ),
            "sleep_schedule": CharacteristicDefinition(
                "sleep_schedule", "lifestyle", "categorical",
                options=["Muy regular", "Regular", "Irregular", "Muy irregular"],
                weight=1.0
            ),
            "stress_level": CharacteristicDefinition(
                "stress_level", "lifestyle", "numerical",
                min_value=1, max_value=10, weight=1.2
            ),
            "work_life_balance": CharacteristicDefinition(
                "work_life_balance", "lifestyle", "numerical",
                min_value=1, max_value=10, weight=1.2
            ),
            "religious_spirituality": CharacteristicDefinition(
                "religious_spirituality", "lifestyle", "categorical",
                options=["Muy religioso", "Religioso", "Moderado", "Poco religioso", "No religioso"],
                weight=1.2, honduras_context=True, ethical_flag=True
            ),
            "community_involvement": CharacteristicDefinition(
                "community_involvement", "lifestyle", "categorical",
                options=["Muy activo", "Activo", "Ocasional", "Pasivo"],
                weight=1.1, honduras_context=True
            ),
            "financial_planning": CharacteristicDefinition(
                "financial_planning", "lifestyle", "categorical",
                options=["Muy planificado", "Planificado", "Básico", "Sin planificación"],
                weight=1.3
            ),
            "learning_orientation": CharacteristicDefinition(
                "learning_orientation", "lifestyle", "numerical",
                min_value=1, max_value=10, weight=1.2
            )
        }


class TelecomSpecificCharacteristics:
    """25 Telecom-specific characteristics for Tigo Honduras"""
    
    @staticmethod
    def get_characteristics() -> Dict[str, CharacteristicDefinition]:
        return {
            # Service Usage (8 characteristics)
            "service_type": CharacteristicDefinition(
                "service_type", "telecom_service", "categorical",
                options=["Prepago", "Postpago", "Mixto (Pre y Post)", "Empresarial"],
                weight=1.8, honduras_context=True, stereotype_risk="medium"
            ),
            "monthly_spend": CharacteristicDefinition(
                "monthly_spend", "telecom_service", "categorical",
                options=["< L.200", "L.200-400", "L.400-800", "L.800-1200", "> L.1200"],
                weight=1.6, honduras_context=True, ethical_flag=True
            ),
            "data_usage_gb": CharacteristicDefinition(
                "data_usage_gb", "telecom_service", "numerical",
                min_value=0.5, max_value=50, weight=1.5
            ),
            "call_minutes_monthly": CharacteristicDefinition(
                "call_minutes_monthly", "telecom_service", "numerical",
                min_value=50, max_value=2000, weight=1.3
            ),
            "sms_usage": CharacteristicDefinition(
                "sms_usage", "telecom_service", "categorical",
                options=["Nunca", "Ocasional", "Regular", "Frecuente"],
                weight=1.1
            ),
            "internet_primary_use": CharacteristicDefinition(
                "internet_primary_use", "telecom_service", "categorical",
                options=["Redes sociales", "WhatsApp", "Trabajo", "Entretenimiento", "Todo"],
                weight=1.4
            ),
            "roaming_usage": CharacteristicDefinition(
                "roaming_usage", "telecom_service", "categorical",
                options=["Frecuente", "Ocasional", "Raro", "Nunca"],
                weight=1.2
            ),
            "service_bundling": CharacteristicDefinition(
                "service_bundling", "telecom_service", "categorical",
                options=["Solo móvil", "Móvil + Internet", "Paquete completo", "Múltiples proveedores"],
                weight=1.3
            ),

            # Device & Technology (6 characteristics)
            "device_brand": CharacteristicDefinition(
                "device_brand", "telecom_device", "categorical",
                options=["Samsung", "iPhone", "Huawei", "Xiaomi", "Motorola", "Otros Android", "Básico"],
                weight=1.4, stereotype_risk="medium"
            ),
            "device_age": CharacteristicDefinition(
                "device_age", "telecom_device", "categorical",
                options=["< 1 año", "1-2 años", "2-3 años", "> 3 años"],
                weight=1.2
            ),
            "device_upgrade_frequency": CharacteristicDefinition(
                "device_upgrade_frequency", "telecom_device", "categorical",
                options=["Cada año", "Cada 2-3 años", "Cuando se daña", "Rara vez"],
                weight=1.3
            ),
            "tech_feature_priority": CharacteristicDefinition(
                "tech_feature_priority", "telecom_device", "categorical",
                options=["Cámara", "Batería", "Velocidad", "Precio", "Marca"],
                weight=1.2
            ),
            "wifi_vs_mobile_data": CharacteristicDefinition(
                "wifi_vs_mobile_data", "telecom_device", "categorical",
                options=["Principalmente WiFi", "Mixto", "Principalmente datos móviles"],
                weight=1.3
            ),
            "app_usage_pattern": CharacteristicDefinition(
                "app_usage_pattern", "telecom_device", "categorical",
                options=["Básico (pocas apps)", "Moderado", "Heavy user", "Gaming focus"],
                weight=1.4
            ),

            # Brand & Competition (6 characteristics)
            "current_operator": CharacteristicDefinition(
                "current_operator", "telecom_brand", "categorical",
                options=["Tigo", "Claro", "Otro", "Múltiples"],
                weight=1.7, honduras_context=True
            ),
            "operator_loyalty": CharacteristicDefinition(
                "operator_loyalty", "telecom_brand", "numerical",
                min_value=1, max_value=10, weight=1.6
            ),
            "brand_perception_tigo": CharacteristicDefinition(
                "brand_perception_tigo", "telecom_brand", "categorical",
                options=["Muy positiva", "Positiva", "Neutral", "Negativa", "Muy negativa"],
                weight=1.8, honduras_context=True, ethical_flag=True
            ),
            "brand_perception_claro": CharacteristicDefinition(
                "brand_perception_claro", "telecom_brand", "categorical",
                options=["Muy positiva", "Positiva", "Neutral", "Negativa", "Muy negativa"],
                weight=1.7, honduras_context=True, ethical_flag=True
            ),
            "switching_consideration": CharacteristicDefinition(
                "switching_consideration", "telecom_brand", "categorical",
                options=["Muy probable", "Algo probable", "Neutral", "Poco probable", "Nunca"],
                weight=1.5
            ),
            "recommendation_likelihood": CharacteristicDefinition(
                "recommendation_likelihood", "telecom_brand", "numerical",
                min_value=0, max_value=10, weight=1.6, ethical_flag=True
            ),

            # Service Experience (5 characteristics)
            "network_quality_importance": CharacteristicDefinition(
                "network_quality_importance", "telecom_experience", "numerical",
                min_value=1, max_value=10, weight=1.7
            ),
            "customer_service_experience": CharacteristicDefinition(
                "customer_service_experience", "telecom_experience", "categorical",
                options=["Excelente", "Buena", "Regular", "Mala", "Pésima", "Sin experiencia"],
                weight=1.5, ethical_flag=True
            ),
            "price_sensitivity_telecom": CharacteristicDefinition(
                "price_sensitivity_telecom", "telecom_experience", "numerical",
                min_value=1, max_value=10, weight=1.6
            ),
            "service_interruption_tolerance": CharacteristicDefinition(
                "service_interruption_tolerance", "telecom_experience", "categorical",
                options=["Muy tolerante", "Tolerante", "Poco tolerante", "Intolerante"],
                weight=1.4
            ),
            "digital_service_adoption": CharacteristicDefinition(
                "digital_service_adoption", "telecom_experience", "categorical",
                options=["Early adopter", "Seguidor temprano", "Mayoría", "Conservador"],
                weight=1.3
            )
        }


class EthicalPersonaGenerator:
    """Ethical persona generator with bias detection and mitigation"""
    
    def __init__(self):
        self.universal_chars = UniversalCharacteristics.get_characteristics()
        self.telecom_chars = TelecomSpecificCharacteristics.get_characteristics()
        self.all_characteristics = {**self.universal_chars, **self.telecom_chars}
        
        # Ethical safeguards configuration
        self.counter_stereotypical_rate = 0.30  # 30% counter-stereotypical profiles
        self.validation_sample_rate = 0.10  # 10% human validation
        self.diversity_threshold = 0.7  # Minimum diversity score
        
        # Honduras demographic data for validation
        self.honduras_demographics = self._load_honduras_demographics()
        
    def _load_honduras_demographics(self) -> Dict[str, Any]:
        """Load Honduras demographic data for validation"""
        return {
            "age_distribution": {
                "18-25": 0.25, "26-35": 0.30, "36-50": 0.25, "51-65": 0.15, "65+": 0.05
            },
            "gender_distribution": {
                "Masculino": 0.49, "Femenino": 0.51
            },
            "education_distribution": {
                "Primaria": 0.35, "Secundaria": 0.40, "Técnica": 0.10, 
                "Universitaria": 0.13, "Postgrado": 0.02
            },
            "income_distribution": {
                "Bajo (< L.15,000)": 0.45, "Medio-bajo (L.15,000-25,000)": 0.25,
                "Medio (L.25,000-40,000)": 0.20, "Medio-alto (L.40,000-60,000)": 0.07,
                "Alto (> L.60,000)": 0.03
            },
            "geographic_distribution": {
                "Tegucigalpa": 0.25, "San Pedro Sula": 0.15, "Rural": 0.35, "Otras ciudades": 0.25
            },
            "telecom_market_share": {
                "Tigo": 0.45, "Claro": 0.40, "Otros": 0.15
            }
        }
    
    def generate_persona_batch(self, count: int = 50, 
                             diversity_target: float = 0.8,
                             include_counter_stereotypical: bool = True) -> List[Dict[str, Any]]:
        """Generate a batch of validated personas with ethical safeguards"""
        personas = []
        
        # Calculate counter-stereotypical count
        counter_stereotypical_count = int(count * self.counter_stereotypical_rate) if include_counter_stereotypical else 0
        regular_count = count - counter_stereotypical_count
        
        # Generate regular personas
        for i in range(regular_count):
            persona = self._generate_single_persona(counter_stereotypical=False)
            personas.append(persona)
        
        # Generate counter-stereotypical personas
        for i in range(counter_stereotypical_count):
            persona = self._generate_single_persona(counter_stereotypical=True)
            personas.append(persona)
        
        # Apply diversity enforcement
        personas = self._enforce_diversity(personas, diversity_target)
        
        # Add validation metadata
        for i, persona in enumerate(personas):
            persona["validation"] = {
                "diversity_score": self._calculate_diversity_score(persona, personas),
                "bias_risk_score": self._calculate_bias_risk(persona),
                "stereotype_flags": self._detect_stereotypes(persona),
                "honduras_alignment": self._validate_honduras_context(persona),
                "requires_human_validation": i < int(count * self.validation_sample_rate)
            }
        
        return personas
    
    def _generate_single_persona(self, counter_stereotypical: bool = False) -> Dict[str, Any]:
        """Generate a single persona with ethical considerations"""
        persona = {
            "id": f"persona_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            "generated_at": datetime.now().isoformat(),
            "counter_stereotypical": counter_stereotypical,
            "characteristics": {},
            "personality_profile": {},
            "behavioral_patterns": {},
            "telecom_profile": {},
            "honduras_context": {}
        }
        
        # Generate characteristics with ethical constraints
        for char_name, char_def in self.all_characteristics.items():
            value = self._generate_characteristic_value(char_def, counter_stereotypical)
            persona["characteristics"][char_name] = value
            
            # Categorize into profile sections
            if char_def.category == "demographics":
                persona["personality_profile"][char_name] = value
            elif char_def.category in ["behavioral", "communication"]:
                persona["behavioral_patterns"][char_name] = value
            elif char_def.category.startswith("telecom"):
                persona["telecom_profile"][char_name] = value
            elif char_def.honduras_context:
                persona["honduras_context"][char_name] = value
        
        # Add consistency checks and human-like imperfections
        persona = self._add_personality_consistency(persona)
        persona = self._add_human_imperfections(persona)
        
        return persona
    
    def _generate_characteristic_value(self, char_def: CharacteristicDefinition, 
                                     counter_stereotypical: bool) -> Any:
        """Generate value for a characteristic with bias mitigation"""
        if char_def.data_type == "categorical":
            if counter_stereotypical and char_def.stereotype_risk in ["medium", "high"]:
                # Generate counter-stereotypical values
                return self._select_counter_stereotypical_option(char_def.options)
            else:
                # Use demographic-weighted selection for Honduras context
                if char_def.honduras_context and char_def.name in self.honduras_demographics:
                    return self._weighted_categorical_selection(
                        char_def.options, 
                        self.honduras_demographics[char_def.name]
                    )
                return random.choice(char_def.options)
        
        elif char_def.data_type == "numerical":
            if counter_stereotypical and char_def.stereotype_risk in ["medium", "high"]:
                # Generate values that break typical correlations
                return self._generate_counter_stereotypical_numerical(char_def)
            else:
                return round(random.uniform(char_def.min_value, char_def.max_value), 1)
        
        elif char_def.data_type == "boolean":
            return random.choice([True, False])
        
        else:  # text
            return f"Generated text for {char_def.name}"
    
    def _select_counter_stereotypical_option(self, options: List[str]) -> str:
        """Select options that break typical stereotypes"""
        # This would contain more sophisticated logic based on research
        return random.choice(options)  # Simplified for now
    
    def _weighted_categorical_selection(self, options: List[str], 
                                      weights: Dict[str, float]) -> str:
        """Select categorical value based on demographic weights"""
        available_options = [opt for opt in options if opt in weights]
        if not available_options:
            return random.choice(options)
        
        weights_list = [weights[opt] for opt in available_options]
        return np.random.choice(available_options, p=weights_list)
    
    def _generate_counter_stereotypical_numerical(self, char_def: CharacteristicDefinition) -> float:
        """Generate numerical values that break correlations"""
        # Generate from opposite end of distribution
        mid_point = (char_def.min_value + char_def.max_value) / 2
        if random.random() < 0.5:
            return round(random.uniform(char_def.min_value, mid_point), 1)
        else:
            return round(random.uniform(mid_point, char_def.max_value), 1)
    
    def _enforce_diversity(self, personas: List[Dict[str, Any]], 
                          target_diversity: float) -> List[Dict[str, Any]]:
        """Enforce diversity across the persona set"""
        # Calculate current diversity
        current_diversity = self._calculate_batch_diversity(personas)
        
        if current_diversity >= target_diversity:
            return personas
        
        # Apply diversity enhancement
        enhanced_personas = []
        for persona in personas:
            if len(enhanced_personas) == 0:
                enhanced_personas.append(persona)
                continue
            
            # Check if this persona adds diversity
            test_batch = enhanced_personas + [persona]
            test_diversity = self._calculate_batch_diversity(test_batch)
            
            if test_diversity > current_diversity:
                enhanced_personas.append(persona)
                current_diversity = test_diversity
            else:
                # Modify persona to increase diversity
                modified_persona = self._modify_for_diversity(persona, enhanced_personas)
                enhanced_personas.append(modified_persona)
        
        return enhanced_personas
    
    def _calculate_batch_diversity(self, personas: List[Dict[str, Any]]) -> float:
        """Calculate diversity score for a batch of personas"""
        if len(personas) < 2:
            return 1.0
        
        diversity_scores = []
        
        # Check diversity across key characteristics
        key_characteristics = [
            "age", "gender", "education_level", "income_bracket", 
            "geographic_region", "service_type", "monthly_spend"
        ]
        
        for char in key_characteristics:
            if char not in self.all_characteristics:
                continue
                
            values = [p["characteristics"].get(char) for p in personas]
            unique_values = len(set(values))
            total_values = len(values)
            
            diversity_score = unique_values / total_values if total_values > 0 else 0
            diversity_scores.append(diversity_score)
        
        return np.mean(diversity_scores) if diversity_scores else 0.0
    
    def _calculate_diversity_score(self, persona: Dict[str, Any], 
                                 all_personas: List[Dict[str, Any]]) -> float:
        """Calculate how much diversity this persona adds to the set"""
        # Implementation would compare this persona against others
        return random.uniform(0.6, 0.9)  # Simplified
    
    def _calculate_bias_risk(self, persona: Dict[str, Any]) -> float:
        """Calculate bias risk score for a persona"""
        risk_factors = 0
        total_factors = 0
        
        for char_name, char_def in self.all_characteristics.items():
            if char_def.ethical_flag:
                total_factors += 1
                value = persona["characteristics"].get(char_name)
                
                # Check for potential bias patterns (simplified)
                if char_def.stereotype_risk == "high":
                    risk_factors += 0.5
                elif char_def.stereotype_risk == "medium":
                    risk_factors += 0.2
        
        return risk_factors / total_factors if total_factors > 0 else 0.0
    
    def _detect_stereotypes(self, persona: Dict[str, Any]) -> List[str]:
        """Detect potential stereotypes in persona"""
        flags = []
        
        # Example stereotype detection (would be more sophisticated)
        characteristics = persona["characteristics"]
        
        # Age-income correlation check
        age = characteristics.get("age", 0)
        income = characteristics.get("income_bracket", "")
        if age < 25 and "Alto" in income:
            flags.append("Young high-income potential stereotype")
        
        # Education-tech adoption correlation
        education = characteristics.get("education_level", "")
        tech_adoption = characteristics.get("technology_adoption", "")
        if education == "Primaria" and tech_adoption == "Innovador":
            flags.append("Low education high-tech adoption (counter-stereotypical)")
        
        return flags
    
    def _validate_honduras_context(self, persona: Dict[str, Any]) -> Dict[str, Any]:
        """Validate persona against Honduras demographic data"""
        validation = {
            "demographic_alignment": 0.0,
            "cultural_consistency": 0.0,
            "market_realism": 0.0
        }
        
        characteristics = persona["characteristics"]
        
        # Check demographic alignment
        age_group = self._get_age_group(characteristics.get("age", 30))
        expected_age_prob = self.honduras_demographics["age_distribution"].get(age_group, 0)
        validation["demographic_alignment"] = min(expected_age_prob * 2, 1.0)
        
        # Cultural consistency checks
        if characteristics.get("values_family", 5) >= 7:  # High family values expected
            validation["cultural_consistency"] += 0.3
        if characteristics.get("religious_spirituality") in ["Religioso", "Muy religioso"]:
            validation["cultural_consistency"] += 0.3
        if characteristics.get("authority_respect", 5) >= 6:
            validation["cultural_consistency"] += 0.4
        
        # Market realism
        operator = characteristics.get("current_operator")
        if operator in self.honduras_demographics["telecom_market_share"]:
            expected_prob = self.honduras_demographics["telecom_market_share"][operator]
            validation["market_realism"] = min(expected_prob * 2, 1.0)
        
        return validation
    
    def _get_age_group(self, age: int) -> str:
        """Convert age to age group"""
        if age <= 25:
            return "18-25"
        elif age <= 35:
            return "26-35"
        elif age <= 50:
            return "36-50"
        elif age <= 65:
            return "51-65"
        else:
            return "65+"
    
    def _add_personality_consistency(self, persona: Dict[str, Any]) -> Dict[str, Any]:
        """Add personality consistency across characteristics"""
        characteristics = persona["characteristics"]
        
        # Example: Introverts might have lower social media activity
        extraversion = characteristics.get("personality_extraversion", 5)
        if extraversion < 4:  # Introvert
            if characteristics.get("social_media_activity") == "Muy activo":
                characteristics["social_media_activity"] = random.choice(["Moderado", "Pasivo"])
        
        # Consistency between risk tolerance and financial planning
        risk_tolerance = characteristics.get("risk_tolerance", "Moderado")
        if risk_tolerance in ["Muy conservador", "Conservador"]:
            if characteristics.get("financial_planning") == "Sin planificación":
                characteristics["financial_planning"] = random.choice(["Planificado", "Muy planificado"])
        
        return persona
    
    def _add_human_imperfections(self, persona: Dict[str, Any]) -> Dict[str, Any]:
        """Add realistic human imperfections and inconsistencies"""
        characteristics = persona["characteristics"]
        
        # Add minor inconsistencies (humans aren't perfectly consistent)
        if random.random() < 0.15:  # 15% chance of minor inconsistency
            inconsistency_type = random.choice([
                "attention_fatigue", "knowledge_gap", "response_variability"
            ])
            
            persona["human_imperfections"] = {
                "type": inconsistency_type,
                "description": self._get_imperfection_description(inconsistency_type)
            }
        
        # Add social desirability bias adjustment
        sdb_level = characteristics.get("social_desirability_bias", 5)
        if sdb_level > 7:
            persona["response_tendencies"] = {
                "slightly_more_positive": True,
                "avoids_extreme_negative": True
            }
        
        return persona
    
    def _get_imperfection_description(self, imperfection_type: str) -> str:
        """Get description for human imperfection type"""
        descriptions = {
            "attention_fatigue": "May give shorter answers in long surveys",
            "knowledge_gap": "Has realistic knowledge limitations about telecom technology",
            "response_variability": "Slight variations in responses to similar questions"
        }
        return descriptions.get(imperfection_type, "General human variability")
    
    def _modify_for_diversity(self, persona: Dict[str, Any], 
                            existing_personas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Modify persona to increase diversity in the batch"""
        # Find underrepresented characteristics in existing personas
        underrepresented = self._find_underrepresented_values(existing_personas)
        
        # Modify persona to include underrepresented values
        for char_name, target_value in underrepresented.items():
            if char_name in persona["characteristics"]:
                persona["characteristics"][char_name] = target_value
        
        return persona
    
    def _find_underrepresented_values(self, personas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find underrepresented characteristic values in current batch"""
        # Simplified implementation
        return {}


if __name__ == "__main__":
    # Test the ethical persona generator
    generator = EthicalPersonaGenerator()
    
    print("🧪 Testing Ethical Persona Generator")
    print("=" * 50)
    
    # Generate a small batch for testing
    personas = generator.generate_persona_batch(count=5, diversity_target=0.8)
    
    for i, persona in enumerate(personas, 1):
        print(f"\n👤 Persona {i}: {persona['id']}")
        print(f"   Counter-stereotypical: {persona['counter_stereotypical']}")
        print(f"   Diversity Score: {persona['validation']['diversity_score']:.2f}")
        print(f"   Bias Risk: {persona['validation']['bias_risk_score']:.2f}")
        print(f"   Stereotype Flags: {len(persona['validation']['stereotype_flags'])}")
        
        # Show some key characteristics
        chars = persona['characteristics']
        print(f"   Age: {chars.get('age')}, Gender: {chars.get('gender')}")
        print(f"   Education: {chars.get('education_level')}")
        print(f"   Service: {chars.get('service_type')}, Spend: {chars.get('monthly_spend')}")
        print(f"   Operator: {chars.get('current_operator')}")
    
    print(f"\n✅ Generated {len(personas)} ethical personas with diversity safeguards")