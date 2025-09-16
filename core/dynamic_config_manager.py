# core/dynamic_config_manager.py
"""
Sistema de Configuración Dinámica Multi-Cliente
Carga configuraciones específicas por cliente y mantiene neutralidad en el core
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime


class DynamicConfigManager:
    """
    Gestor de configuraciones dinámicas que permite:
    1. Cargar configuraciones neutrales base
    2. Aplicar configuraciones específicas por cliente
    3. Interpolar placeholders con datos reales
    4. Mantener el core neutral y reutilizable
    """

    def __init__(self, base_config_path: str = "config/system_config_neutral.json"):
        self.base_config_path = base_config_path
        self.base_config = self._load_base_config()
        self.client_configs = {}
        self.active_client = None

        print("✅ Dynamic Config Manager initialized")
        print(f"   📋 Base config: {base_config_path}")
        print(f"   🎛️ Modes available: {', '.join(self.base_config['rag_modes'].keys())}")

    def _load_base_config(self) -> Dict[str, Any]:
        """Carga la configuración base neutral"""
        try:
            with open(self.base_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Base config loaded: v{config.get('version', '1.0')}")
            return config
        except Exception as e:
            print(f"❌ Error loading base config: {e}")
            return self._get_fallback_config()

    def _get_fallback_config(self) -> Dict[str, Any]:
        """Configuración de emergencia si no se puede cargar la base"""
        return {
            "version": "2.0-fallback",
            "rag_modes": {
                "pure": {
                    "system_prompt_template": "Eres un asistente de análisis. Responde basándote en los documentos proporcionados.",
                    "default_rag_percentage": 100
                }
            },
            "default_values": {
                "client_name": "Cliente",
                "industry": "General"
            }
        }

    def load_client_config(self, client_name: str, config_path: Optional[str] = None) -> bool:
        """
        Carga configuración específica de un cliente

        Args:
            client_name: Nombre del cliente (ej: "alqueria", "tigo", "unilever")
            config_path: Ruta opcional del archivo de config, si no se proporciona
                        busca "config/{client_name}_config.json"
        """
        try:
            if not config_path:
                config_path = f"config/{client_name.lower()}_config.json"

            with open(config_path, 'r', encoding='utf-8') as f:
                client_config = json.load(f)

            # Extraer datos del cliente para interpolación
            client_data = self._extract_client_data(client_config)

            self.client_configs[client_name] = {
                "config": client_config,
                "data": client_data,
                "loaded_at": datetime.now().isoformat(),
                "config_path": config_path
            }

            print(f"✅ Client config loaded: {client_name}")
            print(f"   📁 Path: {config_path}")
            print(f"   🏢 Industry: {client_data.get('industry', 'Unknown')}")
            print(f"   🌍 Market: {client_data.get('market', 'Unknown')}")

            return True

        except Exception as e:
            print(f"❌ Error loading client config for {client_name}: {e}")
            return False

    def _extract_client_data(self, client_config: Dict[str, Any]) -> Dict[str, str]:
        """Extrae datos del cliente para interpolación de placeholders"""

        # Obtener contexto del cliente (alqueria_context, tigo_context, etc.)
        client_context = None
        possible_contexts = [
            f"{client_config.get('client_info', {}).get('name', '').lower()}_context",
            "client_context",
            "brand_context"
        ]

        for context_key in possible_contexts:
            if context_key in client_config:
                client_context = client_config[context_key]
                break

        # Si no encuentra contexto específico, usar valores de client_info
        if not client_context:
            client_context = client_config.get('client_info', {})

        # Extraer datos para interpolación
        extracted_data = {
            "client_name": client_config.get('client_info', {}).get('name', 'Cliente'),
            "industry": client_config.get('client_info', {}).get('industry', 'General'),
            "market": client_config.get('client_info', {}).get('market', 'General'),
            "brand_positioning": client_context.get('brand_positioning', 'Empresa líder'),
            "main_competitors": ', '.join(client_context.get('main_competitors', ['Competencia'])),
            "key_markets": ', '.join(client_context.get('key_markets', ['Mercado Principal'])),
            "segments": ', '.join(client_context.get('segments', ['Segmento General']))
        }

        return extracted_data

    def set_active_client(self, client_name: str) -> bool:
        """
        Establece el cliente activo para las consultas
        """
        if client_name in self.client_configs:
            self.active_client = client_name
            print(f"✅ Active client set: {client_name}")
            return True
        else:
            print(f"❌ Client not found: {client_name}")
            print(f"   Available clients: {', '.join(self.client_configs.keys())}")
            return False

    def get_system_prompt(self, mode: str, rag_percentage: Optional[int] = None) -> str:
        """
        Genera system prompt interpolado para el cliente activo

        Args:
            mode: Modo RAG (pure, creative, hybrid, etc.)
            rag_percentage: Porcentaje RAG para modos configurables
        """
        try:
            # Obtener template base
            mode_config = self.base_config['rag_modes'].get(mode, {})
            prompt_template = mode_config.get('system_prompt_template',
                                            "Eres un asistente de análisis de {client_name}.")

            # Obtener datos del cliente activo
            if self.active_client and self.active_client in self.client_configs:
                client_data = self.client_configs[self.active_client]['data']
            else:
                client_data = self.base_config.get('default_values', {})

            # Calcular porcentajes dinámicos
            if rag_percentage is not None:
                client_data['rag_percentage'] = rag_percentage
                client_data['creativity_percentage'] = 100 - rag_percentage
                client_data['llm_percentage'] = 100 - rag_percentage
            else:
                default_rag = mode_config.get('default_rag_percentage', 100)
                client_data['rag_percentage'] = default_rag
                client_data['creativity_percentage'] = 100 - default_rag
                client_data['llm_percentage'] = 100 - default_rag

            # Interpolar placeholders
            interpolated_prompt = prompt_template.format(**client_data)

            return interpolated_prompt

        except Exception as e:
            print(f"❌ Error generating system prompt: {e}")
            fallback = f"Eres un asistente de análisis para {client_data.get('client_name', 'Cliente')}."
            return fallback

    def get_mode_config(self, mode: str) -> Dict[str, Any]:
        """Obtiene configuración completa de un modo"""
        return self.base_config['rag_modes'].get(mode, {})

    def get_available_modes(self) -> List[str]:
        """Obtiene lista de modos disponibles"""
        return list(self.base_config['rag_modes'].keys())

    def get_client_info(self, client_name: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene información de un cliente específico o el activo"""
        target_client = client_name or self.active_client

        if target_client and target_client in self.client_configs:
            return self.client_configs[target_client]['data']
        else:
            return self.base_config.get('default_values', {})

    def list_clients(self) -> List[str]:
        """Lista todos los clientes cargados"""
        return list(self.client_configs.keys())

    def reload_client(self, client_name: str) -> bool:
        """Recarga configuración de un cliente"""
        if client_name in self.client_configs:
            config_path = self.client_configs[client_name]['config_path']
            return self.load_client_config(client_name, config_path)
        return False

    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema"""
        return {
            "base_config_version": self.base_config.get('version', 'Unknown'),
            "available_modes": len(self.base_config['rag_modes']),
            "loaded_clients": len(self.client_configs),
            "active_client": self.active_client,
            "clients": list(self.client_configs.keys())
        }


# Función de utilidad para inicializar el manager con clientes comunes
def initialize_with_common_clients() -> DynamicConfigManager:
    """
    Inicializa el manager y carga clientes comunes si sus configs existen
    """
    manager = DynamicConfigManager()

    common_clients = [
        ("alqueria", "config/alqueria_config.json"),
        ("tigo", "config/tigo_config.json"),
        ("alpina", "config/alpina_config.json"),
        ("unilever", "config/unilever_config.json"),
        ("nestle", "config/nestle_config.json")
    ]

    loaded_count = 0
    for client_name, config_path in common_clients:
        if os.path.exists(config_path):
            if manager.load_client_config(client_name, config_path):
                loaded_count += 1

    print(f"✅ Auto-loaded {loaded_count} client configurations")
    return manager