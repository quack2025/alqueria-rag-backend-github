# 🔄 GitHub Actions Setup - Automatic Deployments

Esta configuración permite que yo (Claude) haga commits al repositorio y se desplieguen automáticamente a Azure.

## 📋 Setup Checklist

### ✅ Paso 1: Crear Repositorio GitHub
```bash
# 1. Ve a https://github.com/new
# 2. Nombre: tigo-rag-backend
# 3. Descripción: Tigo Honduras RAG System - Enterprise Backend
# 4. Public o Private (tu elección)
# 5. NO inicializar con README (ya tenemos código)
```

### ✅ Paso 2: Conectar con GitHub
```bash
cd C:\Users\jorge\proyectos_python\tigo_rag_refactored

# Agregar GitHub remote (reemplaza TU-USERNAME)
git remote add origin https://github.com/TU-USERNAME/tigo-rag-backend.git

# Push inicial
git branch -M main
git push -u origin main
```

### ✅ Paso 3: Configurar Secrets de GitHub

En GitHub, ve a: `Settings > Secrets and Variables > Actions`

Agregar estos secrets:

| Secret Name | Value | Descripción |
|-------------|--------|-------------|
| `AZUREAPPSERVICE_PUBLISHPROFILE` | [Download from Azure] | Profile de publish de Azure App Service |

**Para obtener el Publish Profile:**
1. Ve a Azure Portal > App Services > tigo-rag-backend
2. Click en "Get publish profile"
3. Copia todo el contenido XML
4. Pégalo como valor del secret en GitHub

## 🚀 Flujo de Trabajo

### Para Claude (Automático):
1. Hago commit de nuevas features
2. Push a GitHub
3. GitHub Actions detecta el cambio
4. Deploy automático a Azure
5. ✅ Nueva funcionalidad disponible

### Para ti (Solo setup inicial):
1. Crear el repositorio GitHub (5 min)
2. Configurar secrets (5 min)  
3. Deploy inicial manual (10 min)
4. ¡Todo automático después!

## 📊 Monitoreo

- **GitHub Actions**: https://github.com/TU-USERNAME/tigo-rag-backend/actions
- **Azure Portal**: https://portal.azure.com > App Services > tigo-rag-backend
- **Backend URL**: https://tigo-rag-backend.azurewebsites.net

## 🔧 Ventajas de esta Setup

✅ **Para ti:**
- Control total sobre Azure resources
- Visibilidad completa de cambios en GitHub
- Deploy history y rollbacks fáciles
- No necesitas ejecutar comandos manuales

✅ **Para Claude:**
- Acceso directo para mejoras continuas
- Testing automático antes de deploy
- Historial completo de cambios
- Capacidad de agregar nuevas funcionalidades

## 🆘 Troubleshooting

**Si el deploy falla:**
1. Ve a GitHub Actions tab
2. Click en el workflow que falló
3. Revisa los logs para identificar el error
4. Los errores más comunes son variables de entorno faltantes

**Si necesitas rollback:**
1. En Azure Portal > Deployment Center
2. Selecciona un deployment anterior
3. Click "Redeploy"

---

**🎯 Next Steps:**
1. Crear repo GitHub
2. Configurar secrets
3. Deploy inicial
4. ¡Funcionalidades automáticas desde Claude!