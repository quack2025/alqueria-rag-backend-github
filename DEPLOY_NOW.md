# ⚡ DEPLOY INMEDIATO - Comandos Exactos

Copia y pega estos comandos **exactamente como están**:

## 🎯 Opción A: Deploy Rápido (15 minutos)

```bash
cd C:\Users\jorge\proyectos_python\tigo_rag_refactored

# 1. Login a Azure (abre el browser)
az login

# 2. Crear todo de una vez
az group create --name tigo-rag-rg --location "East US"

az appservice plan create --name tigo-rag-plan --resource-group tigo-rag-rg --sku B1 --is-linux

az webapp create --resource-group tigo-rag-rg --plan tigo-rag-plan --name tigo-rag-backend-$(date +%s) --runtime "PYTHON|3.10" --deployment-local-git

# 3. Configurar startup
az webapp config set --resource-group tigo-rag-rg --name tigo-rag-backend-$(date +%s) --startup-file startup.py

# 4. Obtener Git URL para deploy
az webapp deployment source config-local-git --name tigo-rag-backend-$(date +%s) --resource-group tigo-rag-rg --query url --output tsv
```

**IMPORTANTE:** Guarda la URL que te dé el último comando.

```bash
# 5. Agregar Azure remote (reemplaza [URL_DE_ARRIBA])
git remote add azure [PEGA_AQUÍ_LA_URL_QUE_TE_DIO]

# 6. Deploy
git push azure master
```

## 🎯 Opción B: Si quieres nombre específico

```bash
cd C:\Users\jorge\proyectos_python\tigo_rag_refactored

az login

az group create --name tigo-rag-rg --location "East US"

az appservice plan create --name tigo-rag-plan --resource-group tigo-rag-rg --sku B1 --is-linux

az webapp create --resource-group tigo-rag-rg --plan tigo-rag-plan --name tigo-rag-backend --runtime "PYTHON|3.10" --deployment-local-git

az webapp config set --resource-group tigo-rag-rg --name tigo-rag-backend --startup-file startup.py

az webapp deployment source config-local-git --name tigo-rag-backend --resource-group tigo-rag-rg --query url --output tsv

# Copia la URL y ejecútala aquí:
git remote add azure [PEGA_LA_URL_AQUÍ]
git push azure master
```

## 🔑 Después del Deploy: Configurar Variables

Ve a: https://portal.azure.com > App Services > [tu-app-name] > Configuration

Agregar estas **Application Settings**:

| Name | Value |
|------|-------|
| `AZURE_OPENAI_API_KEY` | `[Tu clave Azure OpenAI]` |
| `AZURE_SEARCH_SERVICE` | `insightgenius-search` |
| `AZURE_SEARCH_KEY` | `[Tu clave Azure Search]` |
| `AZURE_SEARCH_INDEX` | `tigo-insights` |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `1` |

Click **Save** y espera que se reinicie la app.

## ✅ Verificar que Funciona

```bash
# Test health check
curl https://[TU-APP-NAME].azurewebsites.net/

# Test login
curl -X POST "https://[TU-APP-NAME].azurewebsites.net/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username":"ejecutivo@tigo.com.hn","password":"TigoHN2024!"}'
```

## 🕐 Timeline Esperado

- **Minutos 1-3**: Crear recursos Azure
- **Minutos 4-8**: Build y deploy del código  
- **Minutos 9-12**: Configurar variables de entorno
- **Minutos 13-15**: Testing y verificación

## 🆘 Si algo falla

1. **Error de login**: `az login` otra vez
2. **Error de permisos**: Asegúrate que tu cuenta tiene permisos para crear recursos
3. **Error de build**: Los logs están en Azure Portal > App Service > Log stream

## 📞 Cuando esté listo

Una vez que funcione, me avisas y:
1. Configuramos el GitHub repo
2. Conectamos GitHub Actions  
3. Actualizamos el frontend para usar el nuevo backend
4. ¡Todo automático después!

---

**🎯 ¿Listo? Copia el primer bloque de comandos y ejecútalos!**