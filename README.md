# Alquería RAG Backend System

Sistema RAG para Alquería Colombia con Azure OpenAI - Análisis inteligente de investigación de mercado lácteo.

## 📊 Estado del Sistema
- ✅ **734 documentos** lácteos indexados en Azure Search
- ✅ **Configuración Alquería** aplicada completamente
- ✅ **3 modos RAG** operativos (Pure, Creative, Hybrid)
- ✅ **Sistema de sugerencias** optimizado para contexto lácteo
- ✅ **Frontend Integration Guide** disponible en `C:/Users/jorge/FRONTEND_INTEGRATION_GUIDE.md`
- 🔄 **Próximo**: Optimización para configuración multi-cliente neutral

## Deploy en Railway

1. Fork este repo
2. railway login
3. railway link
4. railway up

## Variables de Entorno Requeridas

### Azure OpenAI
- `AZURE_OPENAI_API_KEY` - Tu API key de Azure OpenAI
- `AZURE_SEARCH_SERVICE` - Nombre de tu servicio de Azure Cognitive Search
- `AZURE_SEARCH_KEY` - API key de Azure Cognitive Search
- `AZURE_SEARCH_INDEX` - Nombre del índice de búsqueda vectorial

### Configuración Opcional
- `CLIENT_NAME` - Nombre del cliente (default: "Alquería")
- `CONFIG_FILE` - Archivo de configuración a usar (default: "alqueria_config.json")

## Endpoints Disponibles

### 1. RAG Pure `/api/rag-pure`
- **Propósito**: Análisis 100% basado en documentos
- **Ideal para**: Reportes ejecutivos, métricas específicas, datos confirmados
- **Características**: Sin creatividad, máxima precisión

### 2. RAG Creative `/api/rag-creative`
- **Propósito**: Análisis creativo con insights innovadores
- **Ideal para**: Brainstorming, detección de tendencias, oportunidades emergentes
- **Características**: Con visualizaciones, alta creatividad

### 3. RAG Hybrid `/api/rag-hybrid`
- **Propósito**: Balance entre precisión y creatividad
- **Ideal para**: Estrategia, recomendaciones accionables, análisis competitivo
- **Características**: Análisis estratégico completo

## Especialización Alquería

Este sistema está optimizado para:
- **Mercado lácteo colombiano** (leches, yogurts, quesos, mantequillas)
- **Competencia específica** (Alpina, Colanta, Parmalat)
- **Contexto regional** (Bogotá, Medellín, Cali, regiones)
- **Insights estratégicos** para posicionamiento premium

## Uso Local

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

El servidor estará disponible en `http://localhost:8000`

## Documentación API

Una vez desplegado, visita `/docs` para la documentación interactiva de Swagger.
