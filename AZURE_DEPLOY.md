# 🚀 Despliegue a Azure App Service - Tigo RAG Backend

## 📋 Pre-requisitos

1. **Azure CLI instalado** - https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
2. **Cuenta Azure activa** con créditos disponibles
3. **Git instalado** y configurado

## ⚡ Despliegue Rápido (5 minutos)

### 1. Login a Azure
```bash
az login
```

### 2. Crear Resource Group
```bash
az group create --name tigo-rag-resources --location "East US"
```

### 3. Crear App Service Plan (Tier gratuito)
```bash
az appservice plan create \
    --name tigo-rag-plan \
    --resource-group tigo-rag-resources \
    --sku B1 \
    --is-linux
```

### 4. Crear Web App con Python 3.10
```bash
az webapp create \
    --resource-group tigo-rag-resources \
    --plan tigo-rag-plan \
    --name tigo-rag-backend \
    --runtime "PYTHON|3.10" \
    --deployment-local-git
```

### 5. Configurar Variables de Entorno
```bash
# Configurar variables de entorno críticas
az webapp config appsettings set \
    --resource-group tigo-rag-resources \
    --name tigo-rag-backend \
    --settings \
    AZURE_OPENAI_API_KEY="tu_azure_openai_key" \
    AZURE_SEARCH_SERVICE="insightgenius-search" \
    AZURE_SEARCH_KEY="tu_azure_search_key" \
    AZURE_SEARCH_INDEX="tigo-insights" \
    PYTHONPATH="/home/site/wwwroot" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="1" \
    WEBSITES_ENABLE_APP_SERVICE_STORAGE="false"
```

### 6. Deploy con Git
```bash
cd C:\Users\jorge\proyectos_python\tigo_rag_refactored

# Inicializar repo Git si no existe
git init
git add .
git commit -m "Initial backend deployment"

# Obtener Git URL
az webapp deployment source config-local-git \
    --name tigo-rag-backend \
    --resource-group tigo-rag-resources \
    --query url --output tsv

# Agregar Azure remote (reemplaza con la URL obtenida arriba)
git remote add azure https://tigo-rag-backend.scm.azurewebsites.net:443/tigo-rag-backend.git

# Deploy
git push azure main
```

## 🎯 URL Final

Tu backend estará disponible en:
**https://tigo-rag-backend.azurewebsites.net**

## 🔧 Variables de Entorno Requeridas

| Variable | Descripción |
|----------|-------------|
| `AZURE_OPENAI_API_KEY` | Tu clave de Azure OpenAI |
| `AZURE_SEARCH_SERVICE` | Nombre del servicio (insightgenius-search) |
| `AZURE_SEARCH_KEY` | Clave de Azure Search |
| `AZURE_SEARCH_INDEX` | Nombre del índice (tigo-insights) |

## 🧪 Verificar Deployment

```bash
# Test health endpoint
curl https://tigo-rag-backend.azurewebsites.net/

# Test authentication
curl -X POST "https://tigo-rag-backend.azurewebsites.net/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username":"ejecutivo@tigo.com.hn","password":"TigoHN2024!"}'
```

## 🔄 Updates Futuros

Para actualizar el backend:
```bash
git add .
git commit -m "Update backend"
git push azure main
```

## 📊 Monitoreo

- **Logs**: Portal Azure > App Services > tigo-rag-backend > Logs
- **Performance**: Portal Azure > App Services > tigo-rag-backend > Metrics
- **Environment**: Portal Azure > App Services > tigo-rag-backend > Configuration

## 💰 Costos Estimados

- **Basic B1**: ~$13-20 USD/mes
- **Free Tier**: $0 (limitaciones de compute)
- **Con créditos Azure**: $0 hasta agotar créditos

---

## 🚨 Importante

1. **Backup configuraciones** antes de deploy
2. **Variables de entorno** deben estar configuradas ANTES del primer deploy
3. **DNS**: Configurar custom domain después del deploy exitoso

**Status**: 🟢 Listo para deploy  
**Tiempo estimado**: 5-10 minutos  
**Complejidad**: ⭐⭐ Moderada