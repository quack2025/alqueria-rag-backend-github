# personas/context_rich_prompting.py
"""
Context-Rich Prompting System for Enhanced Persona Realism
Based on academic research showing context-rich prompting reduces demographic disparities
by incorporating individualized variation and detailed personal histories.
"""

import json
import random
import uuid
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import re


@dataclass
class PersonalHistory:
    """Detailed personal history for context-rich prompting"""
    childhood_experiences: List[str]
    educational_journey: List[str]
    career_milestones: List[str]
    family_relationships: List[str]
    significant_events: List[str]
    cultural_experiences: List[str]
    telecom_history: List[str]


@dataclass
class SyntheticContent:
    """Synthetic social media and communication content"""
    social_media_posts: List[Dict[str, Any]]
    text_messages: List[Dict[str, Any]]
    family_conversations: List[Dict[str, Any]]
    work_communications: List[Dict[str, Any]]


class ContextRichPromptGenerator:
    """Generate context-rich prompts with detailed personal histories"""
    
    def __init__(self, honduras_context: Dict[str, Any]):
        self.honduras_context = honduras_context
        
        # Personal history templates for Honduras context
        self.history_templates = {
            "childhood_experiences": [
                "Crecí en {location} donde {childhood_detail}",
                "Recuerdo cuando era niño/a en {location}, {childhood_memory}",
                "Mi infancia en {location} estuvo marcada por {childhood_event}",
                "En mi barrio de {location}, {neighborhood_experience}",
                "Durante mi niñez, mi familia {family_situation}"
            ],
            
            "educational_journey": [
                "Estudié en {school_type} donde {educational_experience}",
                "Mi experiencia educativa en {location} fue {education_quality}",
                "Recuerdo que en {educational_level}, {learning_experience}",
                "La educación en mi época {educational_context}",
                "Mi formación académica me enseñó {educational_outcome}"
            ],
            
            "career_milestones": [
                "Mi primer trabajo fue {first_job} donde aprendí {work_lesson}",
                "En mi carrera profesional, {career_achievement}",
                "Trabajo en {current_sector} porque {career_motivation}",
                "Mi experiencia laboral me ha enseñado {work_wisdom}",
                "El mercado laboral en Honduras {labor_market_observation}"
            ],
            
            "family_relationships": [
                "Mi familia es {family_characteristic} y siempre {family_value}",
                "Con mis hijos/padres/hermanos, {family_dynamic}",
                "En mi casa, {family_tradition}",
                "Mi esposo/a y yo {relationship_dynamic}",
                "Los domingos familiares {family_routine}"
            ],
            
            "telecom_history": [
                "Mi primera experiencia con celulares fue {telecom_first_experience}",
                "Cambié de operador cuando {telecom_switch_reason}",
                "En mi trabajo/familia usamos telecom para {telecom_usage_pattern}",
                "He notado que el servicio {telecom_service_observation}",
                "Mi relación con la tecnología {tech_relationship}"
            ]
        }
        
        # Context details for Honduras
        self.honduras_details = {
            "locations": [
                "Tegucigalpa", "San Pedro Sula", "La Ceiba", "El Progreso", 
                "Choluteca", "Comayagua", "Siguatepeque", "Danlí", "Juticalpa"
            ],
            "neighborhoods": [
                "Colonia Palmira", "Residencial Las Minitas", "Barrio Guanacaste",
                "Colonia Kennedy", "Residencial Plaza", "Barrio La Granja",
                "Colonia Tepeyac", "Residencial Los Profesionales"
            ],
            "cultural_events": [
                "Feria Juniana", "Festival de la Lluvia", "Carnaval de La Ceiba",
                "Semana Santa", "Festival del Maíz", "Día de la Independencia"
            ],
            "local_businesses": [
                "Pulpería Don Juan", "Farmacia Kielsa", "Supermercados La Antorcha",
                "Panadería Espiga de Oro", "Restaurante Típico Honduras"
            ]
        }
        
        # Real-world content patterns
        self.content_patterns = {
            "social_media_style": {
                "casual": ["jaja", "que chilero", "uff", "genial", "bendiciones"],
                "formal": ["muy interesante", "gracias por compartir", "excelente punto"],
                "family_oriented": ["mi familia", "los nenes", "en casa", "domingo familiar"],
                "tech_savvy": ["app nueva", "actualización", "funciona bien", "problema técnico"]
            },
            
            "text_message_style": {
                "quick_responses": ["ok", "si", "perfecto", "dale", "listo"],
                "emotional": ["❤️", "😊", "🙏", "😅", "👍"],
                "local_expressions": ["tuanis", "pisto", "joda", "cabal", "púchica"]
            }
        }
    
    def generate_personal_history(self, persona_characteristics: Dict[str, Any]) -> PersonalHistory:
        """Generate detailed personal history based on persona characteristics"""
        
        # Extract key characteristics
        age = persona_characteristics.get("age", 30)
        location = persona_characteristics.get("geographic_region", "Tegucigalpa")
        education = persona_characteristics.get("education_level", "Secundaria")
        occupation = persona_characteristics.get("occupation_sector", "Servicios")
        family_situation = persona_characteristics.get("marital_status", "Soltero")
        
        # Generate childhood experiences
        childhood_experiences = []
        for _ in range(random.randint(2, 4)):
            template = random.choice(self.history_templates["childhood_experiences"])
            experience = template.format(
                location=random.choice(self.honduras_details["neighborhoods"]),
                childhood_detail=self._generate_childhood_detail(age),
                childhood_memory=self._generate_childhood_memory(),
                childhood_event=self._generate_childhood_event(),
                neighborhood_experience=self._generate_neighborhood_experience(),
                family_situation=self._generate_family_situation(family_situation)
            )
            childhood_experiences.append(experience)
        
        # Generate educational journey
        educational_journey = []
        for _ in range(random.randint(2, 3)):
            template = random.choice(self.history_templates["educational_journey"])
            journey = template.format(
                school_type=self._get_school_type(education),
                educational_experience=self._generate_educational_experience(),
                location=location,
                education_quality=self._generate_education_quality(),
                educational_level=education,
                learning_experience=self._generate_learning_experience(),
                educational_context=self._generate_educational_context(age),
                educational_outcome=self._generate_educational_outcome()
            )
            educational_journey.append(journey)
        
        # Generate career milestones
        career_milestones = []
        for _ in range(random.randint(2, 4)):
            template = random.choice(self.history_templates["career_milestones"])
            milestone = template.format(
                first_job=self._generate_first_job(),
                work_lesson=self._generate_work_lesson(),
                career_achievement=self._generate_career_achievement(),
                current_sector=occupation,
                career_motivation=self._generate_career_motivation(),
                work_wisdom=self._generate_work_wisdom(),
                labor_market_observation=self._generate_labor_market_observation()
            )
            career_milestones.append(milestone)
        
        # Generate family relationships
        family_relationships = []
        for _ in range(random.randint(2, 3)):
            template = random.choice(self.history_templates["family_relationships"])
            relationship = template.format(
                family_characteristic=self._generate_family_characteristic(),
                family_value=self._generate_family_value(),
                family_dynamic=self._generate_family_dynamic(family_situation),
                family_tradition=self._generate_family_tradition(),
                relationship_dynamic=self._generate_relationship_dynamic(family_situation),
                family_routine=self._generate_family_routine()
            )
            family_relationships.append(relationship)
        
        # Generate telecom history
        telecom_history = []
        for _ in range(random.randint(2, 4)):
            template = random.choice(self.history_templates["telecom_history"])
            history = template.format(
                telecom_first_experience=self._generate_telecom_first_experience(age),
                telecom_switch_reason=self._generate_telecom_switch_reason(),
                telecom_usage_pattern=self._generate_telecom_usage_pattern(),
                telecom_service_observation=self._generate_telecom_service_observation(),
                tech_relationship=self._generate_tech_relationship(persona_characteristics)
            )
            telecom_history.append(history)
        
        return PersonalHistory(
            childhood_experiences=childhood_experiences,
            educational_journey=educational_journey,
            career_milestones=career_milestones,
            family_relationships=family_relationships,
            significant_events=self._generate_significant_events(age),
            cultural_experiences=self._generate_cultural_experiences(),
            telecom_history=telecom_history
        )
    
    def generate_synthetic_content(self, persona_characteristics: Dict[str, Any], 
                                 history: PersonalHistory) -> SyntheticContent:
        """Generate synthetic social media posts, messages, and communications"""
        
        personality = self._extract_personality_style(persona_characteristics)
        
        # Generate social media posts
        social_media_posts = []
        for _ in range(random.randint(8, 15)):
            post = self._generate_social_media_post(personality, history)
            social_media_posts.append(post)
        
        # Generate text messages
        text_messages = []
        for _ in range(random.randint(10, 20)):
            message = self._generate_text_message(personality)
            text_messages.append(message)
        
        # Generate family conversations
        family_conversations = []
        for _ in range(random.randint(3, 6)):
            conversation = self._generate_family_conversation(personality, history)
            family_conversations.append(conversation)
        
        # Generate work communications
        work_communications = []
        for _ in range(random.randint(4, 8)):
            communication = self._generate_work_communication(personality, persona_characteristics)
            work_communications.append(communication)
        
        return SyntheticContent(
            social_media_posts=social_media_posts,
            text_messages=text_messages,
            family_conversations=family_conversations,
            work_communications=work_communications
        )
    
    def generate_interview_transcript(self, persona_characteristics: Dict[str, Any],
                                    history: PersonalHistory,
                                    content: SyntheticContent,
                                    duration_hours: float = 1.5) -> str:
        """Generate 1-2 hour synthetic interview transcript"""
        
        # Calculate approximate number of exchanges for given duration
        # Assuming 3-4 exchanges per minute in conversational interview
        total_exchanges = int(duration_hours * 60 * 3.5)
        
        transcript_parts = []
        
        # Interview introduction
        transcript_parts.append("=== ENTREVISTA DE INVESTIGACIÓN ===")
        transcript_parts.append(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
        transcript_parts.append(f"Duración: {duration_hours} horas")
        transcript_parts.append(f"Participante: {self._generate_implicit_name(persona_characteristics)}")
        transcript_parts.append("")
        
        # Opening rapport building
        transcript_parts.append("MODERADOR: Hola, muchas gracias por participar en esta entrevista. ¿Cómo está usted hoy?")
        
        opening_response = self._generate_opening_response(persona_characteristics, history)
        transcript_parts.append(f"PARTICIPANTE: {opening_response}")
        transcript_parts.append("")
        
        # Main interview sections with context-rich responses
        sections = [
            ("BACKGROUND_PERSONAL", "Cuénteme un poco sobre usted y su vida"),
            ("FAMILY_COMMUNITY", "¿Cómo es su vida familiar y comunitaria?"),
            ("WORK_EDUCATION", "Hablemos sobre su trabajo y experiencia educativa"),
            ("TECHNOLOGY_USAGE", "¿Cómo usa la tecnología en su día a día?"),
            ("TELECOM_EXPERIENCE", "Cuénteme sobre su experiencia con servicios de telecom"),
            ("TIGO_SPECIFIC", "¿Qué opina específicamente sobre Tigo?"),
            ("FUTURE_EXPECTATIONS", "¿Qué espera del futuro en telecom?")
        ]
        
        exchanges_per_section = total_exchanges // len(sections)
        
        for section_type, opening_question in sections:
            transcript_parts.append(f"--- {section_type.replace('_', ' ')} ---")
            transcript_parts.append(f"MODERADOR: {opening_question}")
            
            # Generate detailed response with personal history
            main_response = self._generate_detailed_response(
                section_type, persona_characteristics, history, content
            )
            transcript_parts.append(f"PARTICIPANTE: {main_response}")
            
            # Generate follow-up exchanges
            for _ in range(random.randint(2, exchanges_per_section)):
                follow_up_q = self._generate_follow_up_question(section_type, main_response)
                transcript_parts.append(f"MODERADOR: {follow_up_q}")
                
                follow_up_r = self._generate_follow_up_response(
                    section_type, follow_up_q, persona_characteristics, history
                )
                transcript_parts.append(f"PARTICIPANTE: {follow_up_r}")
            
            transcript_parts.append("")
        
        # Interview conclusion
        transcript_parts.append("--- CONCLUSIÓN ---")
        transcript_parts.append("MODERADOR: ¿Hay algo más que le gustaría agregar?")
        
        final_response = self._generate_final_response(persona_characteristics, history)
        transcript_parts.append(f"PARTICIPANTE: {final_response}")
        
        transcript_parts.append("")
        transcript_parts.append("=== FIN DE ENTREVISTA ===")
        
        return "\n".join(transcript_parts)
    
    # Helper methods for generating specific content
    def _generate_childhood_detail(self, age: int) -> str:
        if age < 25:
            return random.choice([
                "jugábamos fútbol en la calle",
                "había menos tecnología pero más comunidad",
                "los vecinos se conocían bien"
            ])
        else:
            return random.choice([
                "no había tanta tecnología como ahora", 
                "la vida era más tranquila",
                "teníamos más tiempo en familia"
            ])
    
    def _generate_childhood_memory(self) -> str:
        return random.choice([
            "siempre había niños jugando en el parque",
            "mi abuela me llevaba a la iglesia los domingos",
            "los fines de semana íbamos al mercado",
            "celebrábamos cumpleaños con toda la familia"
        ])
    
    def _generate_childhood_event(self) -> str:
        return random.choice([
            "las fiestas patrias con desfiles escolares",
            "las temporadas de lluvia que duraban meses",
            "los apagones frecuentes en esa época",
            "los huracanes que a veces llegaban"
        ])
    
    def _generate_neighborhood_experience(self) -> str:
        return random.choice([
            "todos nos conocíamos y nos cuidábamos",
            "había una pulpería donde comprábamos todo",
            "los fines de semana había música y baile",
            "la gente era muy solidaria entre vecinos"
        ])
    
    def _generate_family_situation(self, marital_status: str) -> str:
        if "casado" in marital_status.lower():
            return random.choice([
                "siempre priorizaba la unión familiar",
                "me enseñó valores de compromiso",
                "era muy unida y trabajadora"
            ])
        else:
            return random.choice([
                "era muy protectora conmigo",
                "me dio mucha independencia",
                "siempre me apoyó en mis decisiones"
            ])
    
    def _get_school_type(self, education: str) -> str:
        if "superior" in education.lower() or "universit" in education.lower():
            return "la universidad"
        elif "secundaria" in education.lower():
            return "el instituto"
        else:
            return "la escuela primaria"
    
    def _generate_educational_experience(self) -> str:
        return random.choice([
            "tuve profesores muy dedicados",
            "aprendí la importancia del esfuerzo",
            "conocí amigos que conservo hasta hoy",
            "me formé en valores y conocimiento"
        ])
    
    def _generate_education_quality(self) -> str:
        return random.choice([
            "buena considerando las circunstancias",
            "exigente pero formativa",
            "limitada por recursos pero con buena voluntad",
            "sólida en lo fundamental"
        ])
    
    def _generate_learning_experience(self) -> str:
        return random.choice([
            "me di cuenta de mi vocación",
            "desarrollé habilidades importantes",
            "aprendí a trabajar en equipo",
            "descubrí mis fortalezas"
        ])
    
    def _generate_educational_context(self, age: int) -> str:
        if age > 40:
            return "era más estricta que ahora"
        else:
            return "empezaba a modernizarse"
    
    def _generate_educational_outcome(self) -> str:
        return random.choice([
            "disciplina y responsabilidad",
            "a valorar el conocimiento",
            "la importancia de la preparación",
            "habilidades para la vida"
        ])
    
    def _generate_first_job(self) -> str:
        return random.choice([
            "en una tienda del barrio",
            "ayudando en un negocio familiar",
            "en una oficina pequeña",
            "vendiendo en el mercado"
        ])
    
    def _generate_work_lesson(self) -> str:
        return random.choice([
            "el valor del trabajo honesto",
            "a tratar bien a los clientes",
            "la importancia de la puntualidad",
            "que todo trabajo digno merece respeto"
        ])
    
    def _generate_career_achievement(self) -> str:
        return random.choice([
            "he logrado estabilidad económica",
            "gané experiencia valiosa",
            "construí una buena reputación",
            "he podido ayudar a mi familia"
        ])
    
    def _generate_career_motivation(self) -> str:
        return random.choice([
            "me gusta ayudar a las personas",
            "es donde tengo más experiencia",
            "me permite balancear trabajo y familia",
            "ofrece oportunidades de crecimiento"
        ])
    
    def _generate_work_wisdom(self) -> str:
        return random.choice([
            "la paciencia y constancia",
            "que la honestidad siempre funciona",
            "a manejar situaciones difíciles",
            "el valor del trabajo en equipo"
        ])
    
    def _generate_labor_market_observation(self) -> str:
        return random.choice([
            "está difícil pero hay oportunidades",
            "requiere más preparación que antes",
            "la tecnología ha cambiado todo",
            "necesita más estabilidad"
        ])
    
    def _generate_family_characteristic(self) -> str:
        return random.choice([
            "muy unida", "trabajadora", "religiosa", 
            "hospitalaria", "tradicional", "moderna"
        ])
    
    def _generate_family_value(self) -> str:
        return random.choice([
            "nos apoyamos mutuamente",
            "priorizamos el respeto",
            "compartimos las responsabilidades",
            "mantenemos nuestras tradiciones"
        ])
    
    def _generate_family_dynamic(self, marital_status: str) -> str:
        if "casado" in marital_status.lower():
            return random.choice([
                "compartimos las decisiones importantes",
                "cada uno tiene sus responsibilidades",
                "tratamos de dar buen ejemplo a los hijos"
            ])
        else:
            return random.choice([
                "mantengo buena comunicación",
                "nos visitamos regularmente",
                "siempre estamos ahí cuando nos necesitamos"
            ])
    
    def _generate_family_tradition(self) -> str:
        return random.choice([
            "celebramos todos los cumpleaños juntos",
            "los domingos almorzamos en familia",
            "vamos a misa los domingos",
            "hacemos tamales en Navidad"
        ])
    
    def _generate_relationship_dynamic(self, marital_status: str) -> str:
        if "casado" in marital_status.lower():
            return random.choice([
                "nos comunicamos bien",
                "compartimos las responsabilidades del hogar",
                "siempre buscamos tiempo para nosotros"
            ])
        else:
            return ""
    
    def _generate_family_routine(self) -> str:
        return random.choice([
            "siempre incluyen una buena comida",
            "vemos televisión o jugamos",
            "visitamos a los abuelos",
            "salimos a caminar o al parque"
        ])
    
    def _generate_significant_events(self, age: int) -> List[str]:
        events = []
        if age > 25:
            events.append("El huracán Mitch cambió mucho el país")
        if age > 35:
            events.append("La crisis política del 2009 nos afectó a todos")
        events.extend([
            "La pandemia cambió nuestra forma de comunicarnos",
            "Los avances en tecnología móvil han sido increíbles",
            "El crecimiento de las redes sociales transformó las relaciones"
        ])
        return random.sample(events, min(3, len(events)))
    
    def _generate_cultural_experiences(self) -> List[str]:
        return random.sample([
            "Las ferias juninas en San Pedro Sula son impresionantes",
            "La Semana Santa tiene tradiciones muy profundas",
            "El carnaval de La Ceiba es único en Centroamérica",
            "Las festividades de independencia unen a todos",
            "La comida típica hondureña es parte de nuestra identidad"
        ], 3)
    
    def _generate_telecom_first_experience(self, age: int) -> str:
        if age > 40:
            return random.choice([
                "cuando llegaron los primeros celulares a Honduras",
                "con teléfonos públicos y después celulares básicos",
                "cuando aún era muy caro tener celular"
            ])
        else:
            return random.choice([
                "con un Nokia básico para mensajes",
                "cuando empezaron los planes prepago accesibles",
                "con mi primer smartphone hace algunos años"
            ])
    
    def _generate_telecom_switch_reason(self) -> str:
        return random.choice([
            "buscaba mejor cobertura en mi zona",
            "necesitaba precios más accesibles",
            "quería mejor servicio al cliente",
            "mis amigos/familia usaban otro operador"
        ])
    
    def _generate_telecom_usage_pattern(self) -> str:
        return random.choice([
            "mantenernos comunicados durante el día",
            "coordinar actividades familiares y de trabajo",
            "compartir fotos y mantenernos conectados",
            "emergencias y comunicación esencial"
        ])
    
    def _generate_telecom_service_observation(self) -> str:
        return random.choice([
            "ha mejorado mucho en los últimos años",
            "todavía tiene áreas donde puede mejorar",
            "depende mucho de la zona donde uno esté",
            "la competencia ha beneficiado a los usuarios"
        ])
    
    def _generate_tech_relationship(self, characteristics: Dict[str, Any]) -> str:
        tech_adoption = characteristics.get("technology_adoption", "Promedio")
        if "innovador" in tech_adoption.lower():
            return "me gusta probar cosas nuevas"
        elif "conservador" in tech_adoption.lower():
            return "prefiero esperar que las cosas se establezcan"
        else:
            return "es práctica, uso lo que necesito"
    
    def _extract_personality_style(self, characteristics: Dict[str, Any]) -> str:
        extraversion = characteristics.get("personality_extraversion", 5)
        formality = characteristics.get("formality_preference", "Semi-formal")
        
        if extraversion > 7 and "informal" in formality.lower():
            return "casual_outgoing" 
        elif extraversion > 7:
            return "formal_outgoing"
        elif "formal" in formality.lower():
            return "formal_reserved"
        else:
            return "casual_reserved"
    
    def _generate_social_media_post(self, personality_style: str, history: PersonalHistory) -> Dict[str, Any]:
        post_types = ["family", "work", "opinion", "local_event", "gratitude"]
        post_type = random.choice(post_types)
        
        if post_type == "family":
            content = random.choice([
                "Domingo en familia, bendecidos 🙏",
                "Los nenes creciendo tan rápido ❤️",
                "Almuerzo familiar como siempre"
            ])
        elif post_type == "work":
            content = random.choice([
                "Otro día de trabajo, dando lo mejor",
                "Agradecido por las oportunidades",
                "El trabajo duro siempre vale la pena"
            ])
        elif post_type == "opinion":
            content = random.choice([
                "Honduras tiene tanto potencial",
                "La tecnología nos está conectando más",
                "Cada día aprendemos algo nuevo"
            ])
        else:
            content = f"Compartiendo un momento especial"
        
        return {
            "content": content,
            "post_type": post_type,
            "engagement": random.randint(5, 50),
            "timestamp": datetime.now() - timedelta(days=random.randint(1, 30))
        }
    
    def _generate_text_message(self, personality_style: str) -> Dict[str, Any]:
        style_patterns = self.content_patterns["text_message_style"]
        
        if "casual" in personality_style:
            content = random.choice(style_patterns["quick_responses"] + style_patterns["local_expressions"])
        else:
            content = random.choice(["Perfecto, muchas gracias", "Entendido", "De acuerdo"])
        
        return {
            "content": content,
            "message_type": "response",
            "timestamp": datetime.now() - timedelta(hours=random.randint(1, 48))
        }
    
    def _generate_family_conversation(self, personality_style: str, history: PersonalHistory) -> Dict[str, Any]:
        topics = ["plans", "concerns", "celebrations", "daily_life"]
        topic = random.choice(topics)
        
        conversations = {
            "plans": "¿Qué vamos a hacer el fin de semana?",
            "concerns": "Me preocupa el tema de los gastos este mes",
            "celebrations": "¡No olviden el cumpleaños de la abuela!",
            "daily_life": "¿Cómo les fue hoy en el trabajo/escuela?"
        }
        
        return {
            "content": conversations[topic],
            "topic": topic,
            "participants": random.randint(2, 4),
            "timestamp": datetime.now() - timedelta(days=random.randint(1, 7))
        }
    
    def _generate_work_communication(self, personality_style: str, characteristics: Dict[str, Any]) -> Dict[str, Any]:
        sector = characteristics.get("occupation_sector", "Servicios")
        
        work_messages = {
            "Servicios": "Confirmo la cita para mañana en la tarde",
            "Comercio": "El inventario está listo para revisión",
            "Educación": "Los estudiantes necesitan más apoyo en matemáticas",
            "Salud": "El paciente evolucionó favorablemente"
        }
        
        content = work_messages.get(sector, "Coordinando actividades del día")
        
        return {
            "content": content,
            "communication_type": "coordination",
            "formality": "professional",
            "timestamp": datetime.now() - timedelta(days=random.randint(1, 5))
        }
    
    def _generate_implicit_name(self, characteristics: Dict[str, Any]) -> str:
        """Generate implicit demographic indicators through names"""
        gender = characteristics.get("gender", "Otro")
        
        honduras_names = {
            "Masculino": ["Carlos", "José", "Luis", "Mario", "Roberto", "Miguel", "Juan", "Fernando"],
            "Femenino": ["María", "Ana", "Carmen", "Rosa", "Patricia", "Gloria", "Claudia", "Sofía"]
        }
        
        if gender in honduras_names:
            first_name = random.choice(honduras_names[gender])
        else:
            first_name = random.choice(honduras_names["Masculino"] + honduras_names["Femenino"])
        
        # Avoid explicit demographic markers, use cultural context instead
        return first_name  # Just first name, no explicit demographic info
    
    def _generate_opening_response(self, characteristics: Dict[str, Any], history: PersonalHistory) -> str:
        responses = [
            "Muy bien, gracias. Contento de poder participar y compartir mi experiencia.",
            "Todo bien por aquí, trabajando como siempre. Gracias por la oportunidad.",
            "Excelente, agradecido por este espacio para conversar.",
            "Bien, gracias a Dios. Listo para platicar sobre estos temas."
        ]
        return random.choice(responses)
    
    def _generate_detailed_response(self, section_type: str, characteristics: Dict[str, Any], 
                                  history: PersonalHistory, content: SyntheticContent) -> str:
        """Generate detailed responses incorporating personal history"""
        
        if section_type == "BACKGROUND_PERSONAL":
            background_elements = random.sample(history.childhood_experiences + history.family_relationships, 2)
            return f"{background_elements[0]} {background_elements[1]} Eso ha marcado mucho mi forma de ser."
        
        elif section_type == "TELECOM_EXPERIENCE":
            telecom_elements = random.sample(history.telecom_history, 2)
            return f"{telecom_elements[0]} {telecom_elements[1]} En general, he visto mucha evolución en este sector."
        
        elif section_type == "TIGO_SPECIFIC":
            brand_perception = characteristics.get("brand_perception_tigo", "Neutral")
            service_exp = characteristics.get("customer_service_experience", "Regular")
            
            if brand_perception == "Muy positiva":
                return "Tigo me ha dado buen servicio. La cobertura en mi zona es confiable y el servicio al cliente, aunque a veces toma tiempo, generalmente resuelve los problemas. He comparado con otras opciones y me parece una buena relación calidad-precio."
            elif brand_perception == "Negativa":
                return "He tenido algunas experiencias difíciles con Tigo. A veces la señal falla en momentos importantes, y el servicio al cliente puede ser lento. Aunque reconozco que han mejorado, aún hay áreas donde podrían hacer mejor trabajo."
            else:
                return "Tigo está bien, como cualquier operador tiene sus pros y contras. Cuando funciona bien, estoy satisfecho. Cuando hay problemas, trato de resolverlos con paciencia. En general, cumple con lo básico que necesito."
        
        else:
            # Generic detailed response
            relevant_history = random.choice(history.childhood_experiences + history.career_milestones)
            return f"{relevant_history} Esta experiencia me ha enseñado mucho sobre lo que realmente importa."
    
    def _generate_follow_up_question(self, section_type: str, previous_response: str) -> str:
        questions = {
            "BACKGROUND_PERSONAL": [
                "¿Y cómo influyó eso en sus decisiones actuales?",
                "¿Qué recuerda más de esa época?",
                "¿Cómo ve esos cambios ahora?"
            ],
            "TELECOM_EXPERIENCE": [
                "¿Qué lo hizo cambiar de operador?",
                "¿Cómo compara el servicio de antes con el de ahora?",
                "¿Qué es lo más importante para usted en telecom?"
            ],
            "TIGO_SPECIFIC": [
                "¿Qué podría mejorar Tigo en su opinión?",
                "¿Recomendaría Tigo a su familia?",
                "¿Cómo ve el futuro de Tigo en Honduras?"
            ]
        }
        
        section_questions = questions.get(section_type, [
            "¿Puede contarme más sobre eso?",
            "¿Qué opina al respecto?",
            "¿Cómo ha sido su experiencia?"
        ])
        
        return random.choice(section_questions)
    
    def _generate_follow_up_response(self, section_type: str, question: str, 
                                   characteristics: Dict[str, Any], history: PersonalHistory) -> str:
        # Generate contextually appropriate follow-up based on question and history
        if "cambiar" in question.lower():
            return random.choice([
                "Principalmente fue por la cobertura. En mi zona anterior operador no llegaba bien.",
                "Buscaba mejor precio. La familia necesitaba ahorrar en esos gastos.",
                "Mis compañeros de trabajo usaban otro operador y nos convenía para comunicarnos."
            ])
        elif "recomienda" in question.lower():
            loyalty = characteristics.get("recommendation_likelihood", 5)
            if loyalty > 7:
                return "Sí, se lo he recomendado a algunos familiares. No es perfecto, pero cumple."
            else:
                return "Depende de sus necesidades. Les digo que comparen bien antes de decidir."
        else:
            return "Bueno, cada situación es diferente, pero en mi experiencia ha sido así."
    
    def _generate_final_response(self, characteristics: Dict[str, Any], history: PersonalHistory) -> str:
        return random.choice([
            "Agradezco la oportunidad de compartir mi experiencia. Espero que sea útil para mejorar los servicios.",
            "Ha sido una buena conversación. Me gusta que las empresas escuchen a sus clientes.",
            "Solo espero que estas opiniones ayuden a que el servicio sea mejor para todos los hondureños.",
            "Gracias por el tiempo. Siempre es bueno poder expresar nuestras opiniones."
        ])