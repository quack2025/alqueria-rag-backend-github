#!/usr/bin/env python3
"""
EJEMPLO DE USO DEL SISTEMA NEUTRAL
Demuestra cómo usar el DynamicConfigManager para múltiples clientes
"""

from core.dynamic_config_manager import DynamicConfigManager, initialize_with_common_clients


def main():
    print("🔧 SISTEMA DE CONFIGURACIÓN NEUTRAL - DEMO")
    print("=" * 60)

    # Inicializar el manager con clientes comunes
    manager = initialize_with_common_clients()

    print("\n📊 ESTADÍSTICAS DEL SISTEMA")
    stats = manager.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # Ejemplo 1: Configurar para Alquería
    print("\n🥛 EJEMPLO 1: ALQUERÍA (Lácteos)")
    print("-" * 40)

    if manager.set_active_client("alqueria"):
        # Generar prompts para diferentes modos
        modes_to_test = ["pure", "creative", "hybrid"]

        for mode in modes_to_test:
            print(f"\n📝 Prompt {mode.upper()}:")
            prompt = manager.get_system_prompt(mode, rag_percentage=80 if mode == "hybrid" else None)
            print(prompt[:200] + "..." if len(prompt) > 200 else prompt)

    # Ejemplo 2: Configurar para Tigo (si existe)
    print("\n📱 EJEMPLO 2: TIGO (Telecomunicaciones)")
    print("-" * 40)

    if manager.set_active_client("tigo"):
        prompt_tigo = manager.get_system_prompt("pure")
        print(f"📝 Prompt Tigo Pure:")
        print(prompt_tigo[:200] + "..." if len(prompt_tigo) > 200 else prompt_tigo)
    else:
        print("⚠️ Configuración de Tigo no disponible")

    # Ejemplo 3: Cliente genérico (sin configuración específica)
    print("\n🏢 EJEMPLO 3: CLIENTE GENÉRICO")
    print("-" * 40)

    manager.active_client = None  # Sin cliente activo
    generic_prompt = manager.get_system_prompt("pure")
    print(f"📝 Prompt Genérico:")
    print(generic_prompt[:200] + "..." if len(generic_prompt) > 200 else generic_prompt)

    # Mostrar información de clientes
    print("\n👥 CLIENTES DISPONIBLES")
    print("-" * 40)
    for client in manager.list_clients():
        info = manager.get_client_info(client)
        print(f"   🏢 {client.upper()}")
        print(f"      Industry: {info.get('industry', 'N/A')}")
        print(f"      Market: {info.get('market', 'N/A')}")
        print(f"      Competitors: {info.get('main_competitors', 'N/A')}")

    print("\n✅ DEMO COMPLETADA")
    print("El sistema puede manejar múltiples clientes sin código sesgado")


if __name__ == "__main__":
    main()