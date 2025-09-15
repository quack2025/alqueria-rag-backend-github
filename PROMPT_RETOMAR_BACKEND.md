# 🔄 PROMPT PARA RETOMAR EL BACKEND DE ALQUERÍA

## Usa este prompt para continuar trabajando en el sistema RAG de Alquería:

---

```markdown
Necesito trabajar con el backend RAG de Alquería Colombia que ya está implementado y en producción. Aquí está el contexto completo del sistema:

## SISTEMA EXISTENTE:
- **Repositorio GitHub**: https://github.com/quack2025/alqueria-rag-backend
- **URL Producción**: https://web-production-ef8db.up.railway.app/
- **Plataforma**: Railway
- **Directorio Local**: C:\Users\jorge\alqueria-rag-backend-github\

## STACK TÉCNICO:
- FastAPI + Python 3.11
- Azure Cognitive Search (insightgenius-search)
- Azure OpenAI (GPT-4o)
- Índice: alqueria-rag-index (734 documentos vectorizados)
- 36 campos de metadata estructurada

## ENDPOINTS IMPLEMENTADOS:
- POST /api/v1/alqueria/search - Búsqueda RAG principal
- GET /api/v1/alqueria/filters - Filtros disponibles
- GET /api/v1/alqueria/stats - Estadísticas del índice
- GET /api/v1/alqueria/health - Health check

## ARCHIVOS CLAVE:
- main.py - Aplicación FastAPI principal
- alqueria_endpoints.py - Endpoints especializados para Alquería
- config/alqueria_config.json - Configuración del cliente
- core/azure_search_vector_store.py - Integración con Azure Search

## DOCUMENTACIÓN DISPONIBLE:
- ENTREGA_FINAL_ALQUERIA.md - Resumen ejecutivo completo
- ALQUERIA_SYSTEM_DOCUMENTATION.md - Documentación técnica detallada
- DEPLOYMENT_GUIDE.md - Guía de despliegue en Railway
- README.md - Documentación básica de uso

## DATOS PROCESADOS:
- 734 documentos de estudios de mercado lácteo
- Proveedores: ASI (450), Kantar (252), Intuito (148), BHT (132)
- Tipos: asi_live, kantar_panel, concept_testing, cualitativo, intuito
- Competidores analizados: Alpina, Colanta, Parmalat, Nestlé

## CONTEXTO DE NEGOCIO:
- Cliente: Alquería Colombia
- Industria: Lácteos (leches, yogurts, quesos, mantequillas)
- Mercado: Colombia (Bogotá, Medellín, Cali, Costa, Eje Cafetero)
- Especialización: Análisis de penetración, switching, competencia

## VARIABLES DE ENTORNO EN RAILWAY:
- AZURE_SEARCH_SERVICE=insightgenius-search
- AZURE_SEARCH_INDEX=alqueria-rag-index
- AZURE_SEARCH_KEY=[configurada en Railway]
- AZURE_OPENAI_API_KEY=[configurada en Railway]

## LO QUE NECESITO HACER AHORA:
[DESCRIBE AQUÍ TU TAREA ESPECÍFICA]

Por favor, revisa primero la documentación existente en el repositorio y ayúdame con esta tarea manteniendo la consistencia con el sistema ya implementado.
```

---

## 📝 EJEMPLOS DE TAREAS QUE PUEDES AGREGAR:

### **Para agregar nuevos endpoints:**
```
LO QUE NECESITO HACER AHORA:
Agregar un nuevo endpoint para análisis de tendencias históricas que compare datos de diferentes períodos en los estudios de Alquería.
```

### **Para actualizar configuración:**
```
LO QUE NECESITO HACER AHORA:
Actualizar la configuración para incluir nuevos competidores (Gloria, San Fernando) en el análisis competitivo.
```

### **Para optimizar búsquedas:**
```
LO QUE NECESITO HACER AHORA:
Optimizar las búsquedas RAG para que prioricen resultados con datos numéricos cuando se pregunta por métricas específicas.
```

### **Para debugging:**
```
LO QUE NECESITO HACER AHORA:
Diagnosticar por qué algunas búsquedas están tardando más de 3 segundos y optimizar el performance.
```

### **Para agregar features:**
```
LO QUE NECESITO HACER AHORA:
Implementar un sistema de caché para las consultas más frecuentes y reducir costos de Azure OpenAI.
```

### **Para mantenimiento:**
```
LO QUE NECESITO HACER AHORA:
Actualizar las dependencias del proyecto y verificar que todo siga funcionando correctamente en producción.
```

### **Para análisis de datos:**
```
LO QUE NECESITO HACER AHORA:
Crear un reporte de las consultas más frecuentes realizadas al sistema para entender mejor qué información buscan los usuarios.
```

### **Para seguridad:**
```
LO QUE NECESITO HACER AHORA:
Implementar autenticación JWT para proteger los endpoints y trackear el uso por usuario.
```

---

## 🎯 TIPS PARA USAR EL PROMPT:

1. **Sé específico** en la tarea que necesitas realizar
2. **Menciona si hay errores** específicos que estés encontrando
3. **Indica si necesitas** mantener compatibilidad con algo existente
4. **Especifica si los cambios** deben reflejarse en producción inmediatamente
5. **Menciona si necesitas** actualizar la documentación también

---

## 🔧 COMANDOS ÚTILES PARA RETOMAR:

```bash
# Clonar repositorio si no lo tienes local
git clone https://github.com/quack2025/alqueria-rag-backend.git

# Actualizar tu copia local
cd C:\Users\jorge\alqueria-rag-backend-github
git pull origin master

# Ver estado actual
git status

# Instalar dependencias
pip install -r requirements.txt

# Probar localmente
python main.py

# Ver logs en Railway
railway logs

# Deploy cambios
git add .
git commit -m "Tu mensaje"
git push origin master
```

---

## 📚 REFERENCIAS RÁPIDAS:

- **Repo**: https://github.com/quack2025/alqueria-rag-backend
- **Prod**: https://web-production-ef8db.up.railway.app/
- **Docs API**: https://web-production-ef8db.up.railway.app/docs
- **Health**: https://web-production-ef8db.up.railway.app/api/v1/alqueria/health

---

*Guarda este prompt para poder retomar el desarrollo del backend de Alquería en cualquier momento con todo el contexto necesario.*