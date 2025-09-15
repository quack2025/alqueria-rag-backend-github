# 🚀 Guía de Despliegue - Alquería RAG Backend

## 1. Pre-requisitos

### Servicios de Azure requeridos:
- **Azure OpenAI Service** (ya configurado)
- **Azure Cognitive Search** con índice vectorial
- Datos de estudios de mercado indexados

### Cuentas necesarias:
- Cuenta de **Railway** (o GitHub para Railway)
- Repositorio en **GitHub** (público o privado)

## 2. Despliegue en Railway

### Opción A: Desde GitHub
1. Sube este código a tu repositorio GitHub
2. Ve a [Railway.app](https://railway.app)
3. **New Project** → **Deploy from GitHub repo**
4. Selecciona tu repositorio `alqueria-rag-backend`
5. Railway detectará automáticamente el `railway.json`

### Opción B: Desde CLI
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

## 3. Variables de Entorno

En el dashboard de Railway, configura:

```env
AZURE_OPENAI_API_KEY=tu-azure-openai-key
AZURE_SEARCH_SERVICE=tu-servicio-search
AZURE_SEARCH_KEY=tu-api-key-search
AZURE_SEARCH_INDEX=alqueria-index
CLIENT_NAME=Alquería
CONFIG_FILE=alqueria_config.json
```

## 4. Verificación del Despliegue

1. **Health Check**: `GET https://tu-app.railway.app/`
2. **Debug Info**: `GET https://tu-app.railway.app/debug`
3. **API Docs**: `GET https://tu-app.railway.app/docs`

## 5. Endpoints Activos

### RAG Pure (Análisis Riguroso)
```
POST https://tu-app.railway.app/api/rag-pure
{
  "text": "¿Cuál es el market share de yogurt en Colombia?",
  "output_types": ["text"]
}
```

### RAG Creative (Con Visualizaciones)
```
POST https://tu-app.railway.app/api/rag-creative
{
  "text": "Tendencias emergentes en lácteos Colombia",
  "output_types": ["text", "chart"]
}
```

### RAG Hybrid (Estratégico)
```
POST https://tu-app.railway.app/api/rag-hybrid
{
  "text": "Estrategia de posicionamiento vs Alpina",
  "output_types": ["text", "table"]
}
```

## 6. Monitoreo

- **Logs**: Railway dashboard → tu proyecto → Deployments
- **Métricas**: Railway analytics built-in
- **Errors**: Logs + Sentry integration (opcional)

## 7. Escalabilidad

Railway auto-escala basado en:
- CPU usage
- Memory usage
- Request volume

## 8. Costos Estimados

- **Railway**: $5-20/mes dependiendo del uso
- **Azure OpenAI**: $0.0015/1K tokens (GPT-4)
- **Azure Search**: $250-500/mes por 100GB storage

## 9. Soporte

- **Documentación**: `/docs` endpoint
- **Debug Info**: `/debug` endpoint
- **Health Check**: `/` endpoint