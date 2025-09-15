# core/system_configuration.py
"""
Sistema de Configuración Dinámica para RAG de Tigo Honduras
Permite personalizar porcentajes RAG y system prompts para cada módulo
"""

import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class RAGModeConfig:
    """Configuración para un modo RAG específico"""
    name: str
    description: str
    default_rag_percentage: int
    min_rag_percentage: int
    max_rag_percentage: int
    default_creativity_level: float
    enable_visualization: bool
    max_context_chunks: int
    system_prompt: str
    custom_parameters: Dict[str, Any]


@dataclass
class ModuleConfig:
    """Configuración para un módulo específico del sistema"""
    module_name: str
    display_name: str
    system_prompt: str
    default_parameters: Dict[str, Any]
    user_configurable_params: List[str]
    description: str


class SystemConfigurationManager:
    """
    Administrador de configuración del sistema RAG
    Permite personalización completa desde la UX
    """
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Archivo de configuración principal
        self.main_config_file = self.config_dir / "system_config.json"
        self.user_configs_dir = self.config_dir / "user_configs"
        self.user_configs_dir.mkdir(exist_ok=True)
        
        # Configuraciones por defecto
        self.default_rag_modes = self._get_default_rag_modes()
        self.default_modules = self._get_default_modules()
        
        # Cargar configuración actual
        self.current_config = self._load_or_create_config()
    
    def _get_default_rag_modes(self) -> Dict[str, RAGModeConfig]:
        """Configuraciones por defecto para los modos RAG"""
        return {
            "pure": RAGModeConfig(
                name="pure",
                description="100% retrieval-based responses using only vector search results",
                default_rag_percentage=100,
                min_rag_percentage=90,
                max_rag_percentage=100,
                default_creativity_level=0.0,
                enable_visualization=False,
                max_context_chunks=5,
                system_prompt="""Eres el asistente de insights de mercado de Tigo Honduras. Responde ÚNICAMENTE basándote en los documentos proporcionados.

INSTRUCCIONES ESTRICTAS:
- USA SOLO la información de los documentos RAG proporcionados
- NO agregues conocimiento general o suposiciones
- Si no hay información suficiente en los documentos, dilo claramente
- Cita siempre las fuentes específicas
- Mantén un tono profesional y preciso

CONTEXTO EMPRESARIAL:
- Tigo lidera en cobertura/señal (67% asociación según estudios)
- Competidores principales: Claro
- Mercados clave: Tegucigalpa, San Pedro Sula
- Segmentos: Prepago (masivo), Postpago (premium), Hogar""",
                custom_parameters={"strict_retrieval": True}
            ),
            
            "creative": RAGModeConfig(
                name="creative",
                description="Balanced approach combining RAG data with creative insights and recommendations",
                default_rag_percentage=60,  # Configurable por el usuario
                min_rag_percentage=30,
                max_rag_percentage=80,
                default_creativity_level=0.7,
                enable_visualization=True,
                max_context_chunks=5,
                system_prompt="""Eres el analista senior de insights de mercado de Tigo Honduras. Combina los datos RAG con tu experiencia para generar insights estratégicos.

BALANCE RAG/CREATIVIDAD: {rag_percentage}% RAG + {creativity_percentage}% Insights creativos

INSTRUCCIONES:
- Prioriza los datos RAG como base fundamental ({rag_percentage}% peso)
- Complementa con insights creativos y recomendaciones estratégicas ({creativity_percentage}% peso)
- Genera recomendaciones accionables para el negocio
- Identifica patrones y oportunidades no obvias
- Sugiere próximos pasos y acciones concretas

CONTEXTO EMPRESARIAL:
- Tigo: Líder en cobertura/señal, asociación premium
- Posicionamiento: Tecnología, calidad, confiabilidad
- Mercado: Competitivo con Claro, oportunidades en digital
- Audiencia: Desde prepago masivo hasta postpago premium

ESTILO: Ejecutivo estratégico, insights profundos, recomendaciones concretas.""",
                custom_parameters={
                    "enable_strategic_insights": True,
                    "enable_recommendations": True,
                    "creativity_temperature": 0.7
                }
            ),
            
            "hybrid": RAGModeConfig(
                name="hybrid",
                description="Fully customizable mode with user-defined RAG/LLM balance",
                default_rag_percentage=70,
                min_rag_percentage=10,
                max_rag_percentage=100,
                default_creativity_level=0.5,
                enable_visualization=True,
                max_context_chunks=7,
                system_prompt="""Eres el consultor de inteligencia de mercado de Tigo Honduras. Adapta tu análisis según el balance RAG/LLM configurado.

BALANCE DINÁMICO: {rag_percentage}% RAG + {llm_percentage}% Conocimiento LLM

MODO DE OPERACIÓN:
- Si RAG > 80%: Enfoque principalmente en datos, mínima interpretación
- Si RAG 60-80%: Balance equilibrado, insights moderados
- Si RAG 40-60%: Interpretación creativa significativa
- Si RAG < 40%: Análisis altamente interpretativo y estratégico

ADAPTABILIDAD:
- Ajusta el tono según el balance configurado
- Más conservador con alto RAG, más creativo con bajo RAG
- Siempre mantén relevancia para Tigo Honduras
- Identifica cuando necesitas más datos vs más análisis

CONTEXTO EMPRESARIAL:
- Tigo Honduras: Operador líder en calidad y cobertura
- Mercado competitivo: Claro como principal rival
- Segmentos diversos: Prepago masivo, postpago premium, hogar""",
                custom_parameters={
                    "adaptive_temperature": True,
                    "dynamic_prompting": True
                }
            )
        }
    
    def _get_default_modules(self) -> Dict[str, ModuleConfig]:
        """Configuraciones por defecto para módulos del sistema"""
        return {
            "data_exporter": ModuleConfig(
                module_name="data_exporter",
                display_name="Exportador de Datos",
                system_prompt="""Eres el especialista en estructuración de datos de Tigo Honduras. Tu función es organizar y preparar datos para export.

OBJETIVOS:
- Extraer datos numéricos y patrones estructurales
- Identificar insights clave para visualización
- Organizar información de manera lógica y accesible
- Preparar datos para análisis posterior

CRITERIOS DE CALIDAD:
- Precisión en extracción de datos
- Categorización lógica de información
- Formato consistente y profesional
- Metadatos completos y útiles""",
                default_parameters={
                    "extract_percentages": True,
                    "categorize_data": True,
                    "include_metadata": True,
                    "format_for_excel": True
                },
                user_configurable_params=["extract_percentages", "categorize_data", "include_metadata"],
                description="Configura cómo se extraen y estructuran los datos para exportación"
            ),
            
            "intelligent_suggestions": ModuleConfig(
                module_name="intelligent_suggestions",
                display_name="Motor de Sugerencias",
                system_prompt="""Eres el asistente proactivo de Tigo Honduras. Generas sugerencias inteligentes para profundizar el análisis.

TIPOS DE SUGERENCIAS:
- Visualizaciones relevantes basadas en datos detectados
- Preguntas de seguimiento que aporten valor
- Análisis complementarios según el contexto
- Acciones recomendadas para el usuario

CRITERIOS:
- Relevancia para el negocio de Tigo
- Practicidad y accionabilidad
- Diversidad de opciones
- Valor agregado real

PERSONALIZACIÓN:
- Adapta sugerencias al tipo de consulta
- Considera el nivel de detalle apropiado
- Prioriza según importancia estratégica""",
                default_parameters={
                    "max_suggestions_per_category": 3,
                    "prioritize_visualizations": True,
                    "enable_follow_up_questions": True,
                    "strategic_focus": True
                },
                user_configurable_params=["max_suggestions_per_category", "prioritize_visualizations"],
                description="Personaliza las sugerencias inteligentes que se muestran al usuario"
            ),
            
            "multimodal_output": ModuleConfig(
                module_name="multimodal_output",
                display_name="Generador de Visualizaciones",
                system_prompt="""Eres el especialista en visualización de datos de Tigo Honduras. Creas gráficos y contenido visual impactante.

PRINCIPIOS DE DISEÑO:
- Claridad y legibilidad ante todo
- Consistencia con la identidad visual de Tigo
- Foco en insights clave, no en decoración
- Accesibilidad para diferentes audiencias

TIPOS DE VISUALIZACIÓN:
- Gráficos ejecutivos para presentaciones
- Dashboards interactivos para análisis
- Infografías para comunicación masiva
- Tablas estructuradas para referencia

ESTILO VISUAL:
- Colores corporativos de Tigo (azules)
- Tipografía profesional y legible
- Espaciado apropiado y jerarquía visual
- Elementos gráficos minimalistas""",
                default_parameters={
                    "use_tigo_colors": True,
                    "chart_style": "professional",
                    "include_data_labels": True,
                    "responsive_design": True
                },
                user_configurable_params=["chart_style", "include_data_labels", "use_tigo_colors"],
                description="Configura el estilo y comportamiento de las visualizaciones generadas"
            ),
            
            "persona_system": ModuleConfig(
                module_name="persona_system",
                display_name="Sistema de Personas",
                system_prompt="""Eres el experto en segmentación y personas de Tigo Honduras. Creas y mantienes perfiles realistas de usuarios.

METODOLOGÍA:
- Base en datos reales de estudios de mercado
- Diversidad demográfica y psicográfica representativa
- Comportamientos auténticos del mercado hondureño
- Evolución temporal de patrones de uso

CALIDAD DE PERSONAS:
- Realismo y autenticidad cultural
- Consistencia en comportamientos
- Relevancia para decisiones de negocio
- Representatividad estadística

APLICACIONES:
- Testing de campañas publicitarias
- Validación de productos y servicios
- Análisis de sensibilidad de precios
- Predicción de comportamientos de mercado""",
                default_parameters={
                    "cultural_authenticity": True,
                    "statistical_representativeness": True,
                    "temporal_evolution": True,
                    "business_relevance": True
                },
                user_configurable_params=["cultural_authenticity", "statistical_representativeness"],
                description="Personaliza cómo se generan y comportan las personas sintéticas"
            )
        }
    
    def _load_or_create_config(self) -> Dict[str, Any]:
        """Carga configuración existente o crea una nueva"""
        if self.main_config_file.exists():
            try:
                with open(self.main_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        # Crear configuración por defecto
        config = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "rag_modes": {name: asdict(mode) for name, mode in self.default_rag_modes.items()},
            "modules": {name: asdict(module) for name, module in self.default_modules.items()},
            "user_preferences": {
                "default_rag_mode": "hybrid",
                "default_export_format": "excel",
                "enable_suggestions": True,
                "auto_generate_visualizations": True
            }
        }
        
        self._save_config(config)
        return config
    
    def _save_config(self, config: Dict[str, Any]):
        """Guarda configuración en archivo"""
        with open(self.main_config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get_rag_mode_config(self, mode: str) -> Optional[RAGModeConfig]:
        """Obtiene configuración de un modo RAG"""
        if mode in self.current_config["rag_modes"]:
            mode_dict = self.current_config["rag_modes"][mode]
            return RAGModeConfig(**mode_dict)
        return None
    
    def update_rag_mode_config(self, mode: str, **kwargs) -> bool:
        """Actualiza configuración de un modo RAG"""
        if mode not in self.current_config["rag_modes"]:
            return False
        
        # Validar parámetros
        mode_config = self.current_config["rag_modes"][mode]
        
        if "rag_percentage" in kwargs:
            rag_pct = kwargs["rag_percentage"]
            min_pct = mode_config.get("min_rag_percentage", 0)
            max_pct = mode_config.get("max_rag_percentage", 100)
            
            if not (min_pct <= rag_pct <= max_pct):
                raise ValueError(f"RAG percentage must be between {min_pct}% and {max_pct}%")
        
        # Actualizar configuración
        for key, value in kwargs.items():
            if key in mode_config:
                self.current_config["rag_modes"][mode][key] = value
        
        # Actualizar system prompt si se cambió el rag_percentage
        if "rag_percentage" in kwargs:
            self._update_system_prompt_with_percentage(mode, kwargs["rag_percentage"])
        
        self._save_config(self.current_config)
        return True
    
    def _update_system_prompt_with_percentage(self, mode: str, rag_percentage: int):
        """Actualiza system prompt con nuevo porcentaje RAG"""
        creativity_percentage = 100 - rag_percentage
        mode_config = self.current_config["rag_modes"][mode]
        
        # Actualizar placeholders en el prompt
        current_prompt = mode_config["system_prompt"]
        updated_prompt = current_prompt.format(
            rag_percentage=rag_percentage,
            creativity_percentage=creativity_percentage,
            llm_percentage=creativity_percentage
        )
        
        self.current_config["rag_modes"][mode]["system_prompt"] = updated_prompt
    
    def update_module_system_prompt(self, module: str, new_prompt: str) -> bool:
        """Actualiza system prompt de un módulo"""
        if module not in self.current_config["modules"]:
            return False
        
        self.current_config["modules"][module]["system_prompt"] = new_prompt
        self._save_config(self.current_config)
        return True
    
    def get_module_config(self, module: str) -> Optional[ModuleConfig]:
        """Obtiene configuración de un módulo"""
        if module in self.current_config["modules"]:
            module_dict = self.current_config["modules"][module]
            return ModuleConfig(**module_dict)
        return None
    
    def save_user_configuration(self, user_id: str, config: Dict[str, Any]) -> bool:
        """Guarda configuración específica de usuario"""
        try:
            user_config_file = self.user_configs_dir / f"{user_id}_config.json"
            config["updated_at"] = datetime.now().isoformat()
            config["user_id"] = user_id
            
            with open(user_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving user config: {e}")
            return False
    
    def load_user_configuration(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Carga configuración específica de usuario"""
        try:
            user_config_file = self.user_configs_dir / f"{user_id}_config.json"
            if user_config_file.exists():
                with open(user_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading user config: {e}")
        
        return None
    
    def get_configurable_parameters(self) -> Dict[str, Any]:
        """Retorna todos los parámetros configurables para la UX"""
        configurable = {
            "rag_modes": {},
            "modules": {},
            "global_settings": {
                "default_rag_mode": {
                    "type": "select",
                    "options": list(self.current_config["rag_modes"].keys()),
                    "current": self.current_config["user_preferences"]["default_rag_mode"],
                    "description": "Modo RAG por defecto al iniciar"
                },
                "default_export_format": {
                    "type": "select", 
                    "options": ["excel", "csv", "json", "html"],
                    "current": self.current_config["user_preferences"]["default_export_format"],
                    "description": "Formato de exportación por defecto"
                }
            }
        }
        
        # RAG modes configurables
        for mode, config in self.current_config["rag_modes"].items():
            configurable["rag_modes"][mode] = {
                "display_name": config["name"].title() + " Mode",
                "description": config["description"],
                "parameters": {
                    "rag_percentage": {
                        "type": "slider",
                        "min": config["min_rag_percentage"],
                        "max": config["max_rag_percentage"],
                        "current": config.get("default_rag_percentage", 70),
                        "description": "Porcentaje de peso para datos RAG vs creatividad LLM"
                    },
                    "creativity_level": {
                        "type": "slider",
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.1,
                        "current": config.get("default_creativity_level", 0.5),
                        "description": "Nivel de creatividad en las respuestas"
                    },
                    "system_prompt": {
                        "type": "textarea",
                        "current": config["system_prompt"],
                        "description": "Prompt del sistema para este modo"
                    }
                }
            }
        
        # Módulos configurables
        for module, config in self.current_config["modules"].items():
            configurable["modules"][module] = {
                "display_name": config["display_name"],
                "description": config["description"],
                "parameters": {
                    "system_prompt": {
                        "type": "textarea",
                        "current": config["system_prompt"],
                        "description": f"Prompt del sistema para {config['display_name']}"
                    }
                }
            }
            
            # Agregar parámetros específicos configurables por usuario
            for param in config.get("user_configurable_params", []):
                if param in config["default_parameters"]:
                    param_value = config["default_parameters"][param]
                    configurable["modules"][module]["parameters"][param] = {
                        "type": "boolean" if isinstance(param_value, bool) else "text",
                        "current": param_value,
                        "description": f"Configuración de {param.replace('_', ' ')}"
                    }
        
        return configurable
    
    def apply_configuration_preset(self, preset_name: str) -> bool:
        """Aplica un preset de configuración predefinido"""
        presets = {
            "conservative": {
                "description": "Configuración conservadora, alta fidelidad a datos",
                "rag_modes": {
                    "pure": {"default_rag_percentage": 100},
                    "creative": {"default_rag_percentage": 80},
                    "hybrid": {"default_rag_percentage": 85}
                }
            },
            "balanced": {
                "description": "Configuración equilibrada, balance RAG/creatividad",
                "rag_modes": {
                    "pure": {"default_rag_percentage": 100},
                    "creative": {"default_rag_percentage": 60},
                    "hybrid": {"default_rag_percentage": 70}
                }
            },
            "creative": {
                "description": "Configuración creativa, mayor peso a insights",
                "rag_modes": {
                    "pure": {"default_rag_percentage": 90},
                    "creative": {"default_rag_percentage": 40},
                    "hybrid": {"default_rag_percentage": 50}
                }
            }
        }
        
        if preset_name not in presets:
            return False
        
        preset = presets[preset_name]
        
        # Aplicar configuraciones del preset
        for mode, config in preset["rag_modes"].items():
            for param, value in config.items():
                self.update_rag_mode_config(mode, **{param: value})
        
        return True
    
    def export_configuration(self) -> Dict[str, Any]:
        """Exporta configuración actual para backup o transferencia"""
        return {
            "export_timestamp": datetime.now().isoformat(),
            "system_version": self.current_config["version"],
            "configuration": self.current_config
        }
    
    def import_configuration(self, config_data: Dict[str, Any]) -> bool:
        """Importa configuración desde backup"""
        try:
            if "configuration" in config_data:
                self.current_config = config_data["configuration"]
                self.current_config["imported_at"] = datetime.now().isoformat()
                self._save_config(self.current_config)
                return True
        except Exception as e:
            print(f"Error importing configuration: {e}")
        
        return False