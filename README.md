# 🩸 API de Análisis de Homicidios México 2024

## 📋 Descripción

API REST completa desarrollada con FastAPI para el análisis avanzado de datos de homicidios en México durante 2024. Esta herramienta está diseñada para ser comercialmente valiosa y proporcionar insights profundos sobre patrones de violencia, demografía y geografía de homicidios.

## 🎯 Usuarios Objetivo

- **Analistas de Seguridad Pública**: Índices de violencia, mapas de riesgo
- **Investigadores Académicos**: Datos demográficos y patrones sociales
- **Empresas de Seguros**: Evaluación de riesgos por región
- **Gobierno y Política**: Estadísticas para toma de decisiones
- **Medios de Comunicación**: Datos para reportajes especializados
- **Organizaciones de Derechos Humanos**: Análisis de tendencias

## 🚀 Características Principales

### 📊 **Análisis Demográfico Detallado**
- Perfiles por sexo, edad y etnia
- Distribución por grupos poblacionales
- Análisis de factores culturales

### 🗺️ **Análisis Geográfico Avanzado**
- Mapas de calor por entidad y municipio
- Identificación de zonas calientes
- Coordenadas geoespaciales

### 📅 **Análisis Temporal**
- Tendencias mensuales, semanales y diarias
- Patrones estacionales
- Detección de picos de violencia

### 🔒 **Índices de Seguridad**
- Índices de violencia calculados científicamente
- Percentiles nacionales
- Clasificaciones de riesgo

### ⚖️ **Análisis Comparativo**
- Comparaciones entre entidades federativas
- Análisis de tendencias regionales
- Rankings nacionales

### 🔮 **Predicciones y Escenarios**
- Modelado predictivo básico
- Escenarios optimistas/pesimistas
- Análisis de tendencias futuras

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar los archivos**
```bash
# Si tienes git
git clone <repository-url>
cd homicides-api-mexico

# O simplemente descargar los archivos
```

2. **Instalar dependencias**
```bash
# Instalar desde requirements.txt
pip install -r requirements.txt

# O instalar manualmente
pip install fastapi pandas numpy uvicorn pydantic python-multipart
```

3. **Verificar datos**
Asegúrate de que el archivo `Homicidios_2024_clean.csv` esté en el mismo directorio que `app.py`

## 🚀 Ejecución

### Iniciar la API
```bash
# Método 1: Ejecutar directamente
python app.py

# Método 2: Usar uvicorn (recomendado para desarrollo)
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Método 3: Usar uvicorn sin recarga automática
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Verificar Funcionamiento
Una vez ejecutándose, abre tu navegador en:
- **API Principal**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs
- **Manual de Usuario**: http://localhost:8000/manual

## 📖 Uso Básico

### 🔍 **Consulta Rápida - Estadísticas Generales**
```bash
curl http://localhost:8000/estadisticas/general
```

### 👥 **Análisis Demográfico por Entidad**
```bash
# Análisis de Aguascalientes (clave: 01)
curl "http://localhost:8000/demografico/perfil?entidad=01"

# Análisis de Baja California (clave: 02)  
curl "http://localhost:8000/demografico/perfil?entidad=02"
```

### 🗺️ **Mapa de Calor Geográfico**
```bash
# Tasa de homicidios por entidad
curl "http://localhost:8000/geografico/mapa-calor?tipo=entidad&metrica=tasa"

# Total de casos por municipio
curl "http://localhost:8000/geografico/mapa-calor?tipo=municipio&metrica=total"
```

### 📊 **Índices de Violencia**
```bash
# Top 10 entidades más violentas
curl "http://localhost:8000/indices/violencia?tipo=entidad&limite=10"

# Top 15 municipios más violentos
curl "http://localhost:8000/indices/violencia?tipo=municipio&limite=15"
```

### 📅 **Tendencias Temporales**
```bash
# Tendencias mensuales
curl "http://localhost:8000/temporal/tendencias?periodo=mensual"

# Tendencias por entidad específica
curl "http://localhost:8000/temporal/tendencias?periodo=mensual&entidad=01"
```

## 🔧 Ejemplos Avanzados

### 🔍 **Identificar Zonas de Alto Riesgo**
```bash
# Obtener las zonas más problemáticas
curl "http://localhost:8000/geografico/zonas-calientes?limite=20"

# Obtener índices de violencia detallados
curl "http://localhost:8000/indices/violencia?tipo=municipio&limite=25"
```

### ⚖️ **Comparar Entidades**
```bash
# Comparar Baja California (02) vs Aguascalientes (01)
curl "http://localhost:8000/comparativo/entidades?entidades=01,02&metrica=tasa"

# Comparar múltiples entidades por índice de violencia
curl "http://localhost:8000/comparativo/entidades?entidades=01,02,03&metrica=indice"
```

### 📤 **Exportar Datos**
```bash
# Exportar datos en JSON
curl "http://localhost:8000/exportar/datos?formato=json&entidad=01"

# Exportar datos con filtros específicos
curl "http://localhost:8000/exportar/datos?formato=csv"
```

### 📋 **Generar Reportes**
```bash
# Reporte ejecutivo
curl "http://localhost:8000/exportar/reporte?tipo=ejecutivo&entidad=01"

# Reporte técnico completo
curl "http://localhost:8000/exportar/reporte?tipo=completo"
```

## 🎯 Casos de Uso Comerciales

### 🏢 **Para Empresas de Seguros**
```bash
# Evaluar riesgos por región para cálculo de primas
curl "http://localhost:8000/indices/violencia?tipo=entidad" | jq '.top_regiones[]'

# Obtener coordenadas para análisis geoespacial
curl "http://localhost:8000/geografico/mapa-calor?tipo=municipio&metrica=tasa"
```

### 🎓 **Para Investigadores Académicos**
```bash
# Análisis demográfico completo
curl "http://localhost:8000/demografico/perfil" | jq '.analisis_sexo'

# Patrones temporales para investigación
curl "http://localhost:8000/temporal/patrones" | jq '.estacionalidad'
```

### 🏛️ **Para Gobierno y Política Pública**
```bash
# Identificar prioridades de seguridad
curl "http://localhost:8000/indices/violencia?tipo=municipio&limite=50" | jq '.top_regiones[]'

# Exportar datos para análisis externos
curl "http://localhost:8000/exportar/datos?formato=csv" > homicidios_datos.csv
```

### 📺 **Para Medios de Comunicación**
```bash
# Obtener datos para artículos y reportajes
curl "http://localhost:8000/estadisticas/general" | jq '.casos_recientes'

# Reporte ejecutivo para publicaciones
curl "http://localhost:8000/exportar/reporte?tipo=ejecutivo"
```

## 📊 Interpretación de Resultados

### 🔒 **Índices de Violencia**
- **0-19**: ✅ MUY BAJO - Situación controlada
- **20-39**: 🟢 BAJO - Prevención normal  
- **40-59**: 🟡 MEDIO - Vigilancia reforzada
- **60-79**: 🟠 ALTO - Medidas de seguridad intensivas
- **80+**: 🔴 CRÍTICO - Acción inmediata requerida

### 📈 **Métricas Disponibles**
- **Tasa**: Casos por 100,000 habitantes (permite comparación)
- **Total**: Volumen absoluto de casos
- **Índice**: Métrica compuesta (60% tasa + 40% volumen)

## 🛠️ Solución de Problemas

### ❌ **Error: No hay datos disponibles**
- Verificar que el archivo `Homicidios_2024_clean.csv` esté presente
- Comprobar que el archivo no esté corrupto
- Revisar permisos de lectura del archivo

### ❌ **Error: Puerto en uso**
```bash
# Usar un puerto diferente
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

### ❌ **Error de dependencias**
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt

# O instalar individualmente
pip install fastapi pandas numpy uvicorn --upgrade
```

### ❌ **Endpoints no responden**
- Verificar que la API esté ejecutándose en el puerto correcto
- Comprobar firewall y permisos de red
- Revisar logs de la terminal para errores

## 📚 Documentación Adicional

- **Swagger UI Interactivo**: http://localhost:8000/docs
- **ReDoc Alternativo**: http://localhost:8000/redoc
- **Manual Completo**: http://localhost:8000/manual
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🤝 Soporte y Contacto

- **Documentación Técnica**: Incluye ejemplos completos en cada endpoint
- **Manual de Usuario**: http://localhost:8000/manual
- **Issues**: Reportar problemas técnicos
- **Licencias**: Disponibles para uso comercial

## 📄 Licencia

Esta API está diseñada para uso comercial. Contactar para licencias empresariales y soporte técnico especializado.

---

**💡 Tip**: Para obtener la mejor experiencia, usa la documentación interactiva en http://localhost:8000/docs donde puedes probar todos los endpoints directamente desde el navegador.

**🎯 Objetivo**: Proporcionar insights valiosos para la toma de decisiones informadas en seguridad pública, investigación académica y análisis comercial.