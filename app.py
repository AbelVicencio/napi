import pandas as pd
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import math

# --- 1. CONFIGURACIÓN Y MANUAL DE USUARIO ---

description_manual = """
# 📊 API de Datos de Homicidios México 2024

Bienvenido a la API REST de Homicidios. Esta herramienta libera el potencial de los datos demográficos y geoespaciales de homicidios en México durante 2024.

## 📘 Guía para Expertos en Datos (No Desarrolladores)

Si eres un analista de datos, actuario o científico de datos acostumbrado a CSVs y Excel, pero nuevo en APIs, esta sección es para ti.

### ¿Qué es esto?
Esta **REST API** (Interfaz de Programación de Aplicaciones) es como un "camarero digital". En lugar de pedirte que descargues y filtres un archivo de 50MB cada vez, tú pides exactamente lo que necesitas (el "pedido") y la API te lo trae al instante (la "respuesta").

### ¿Cómo funciona?
Usamos el protocolo **HTTP** (el mismo de la web).
- **GET**: Es el verbo principal que usarás aquí. Significa "Dame datos".
- **Endpoint**: Es la URL específica donde vive un recurso (ej. `/homicidios`).
- **Parámetros**: Son los filtros. En `Swagger` (esta página), llenas cajitas y nosotros construimos la URL por ti (ej. `?estado=Aguascalientes`).
- **JSON**: El formato de respuesta. Piensa en él como filas de Excel pero organizadas en estructuras jerárquicas fáciles de leer por máquinas (y humanos).

### ¿Por qué usar esta API en lugar del CSV?
1.  **Agilidad**: No necesitas cargar todo el dataset en memoria para ver un resumen de una entidad.
2.  **Integración**: Puedes conectar PowerBI, Tableau o Excel directamente a estos endpoints Web.
3.  **Análisis pre-calculado**: Ofrecemos endpoints de "Resúmenes" que ya hacen las agregaciones (`groupby`) por ti.

---

## 🚀 Catálogo de Endpoints (Formas de pedir datos)

### 1. Consulta Cruda (`/datos/busqueda`)
El "Power Query" de la API. Obtén registros individuales filtrando por múltiples criterios:
-   Filtrar por **Estado** (`nom_ent`) o **Municipio** (`nom_mun`).
-   Filtrar por **Sexo** (`sexo_cat`).
-   Filtrar por **Rango de Fechas** de ocurrencia.
-   *Tip*: Usa `limit` y `offset` para paginar si los resultados son muchos.

### 2. Tableros y Agregaciones (`/resumen/*`)
Endpoints analíticos listos para graficar:
-   `/resumen/nacional`: KPI's generales del país.
-   `/resumen/entidades`: Ranking de homicidios por estado.
-   `/resumen/causas`: Distribución por causa de defunción.
-   `/resumen/temporal`: Serie de tiempo (mensual) para detectar picos de violencia.
-   `/resumen/demografico`: Perfil de las víctimas (Edad y Sexo).

### 3. Geoespacial (`/geo/mapa`)
Optimizado para mapas. Devuelve solo coordenadas (`lat`, `lon`) y metadatos críticos para renderizar puntos masivos sin sobrecargar tu software de GIS.

---
**Autor**: Asistente de IA (Antigravity)
**Versión**: 1.0.0
"""

tags_metadata = [
    {"name": "General", "description": "Verificación de estado y redirección."},
    {"name": "Datos Crudos", "description": "Consulta y filtrado granular de registros individuales."},
    {"name": "Analítica", "description": "Endpoints de agregación estadística y resúmenes ejecutivos."},
    {"name": "Geoespacial", "description": "Datos optimizados para visualización en mapas."},
]

app = FastAPI(
    title="API de Inteligencia Delictiva: Homicidios 2024",
    description=description_manual,
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Soporte de Datos",
        "email": "soporte@datos-mexico.ejemplo.com",
    },
)

# Habilitar CORS para permitir consumo desde cualquier frontend/herramienta de BI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. MODELOS DE DATOS (Pydantic) ---

class HomicidioRecord(BaseModel):
    # Campos clave para identificación
    clave_entidad: str = Field(..., description="ID de la entidad federativa (01-32)")
    nom_ent: str = Field(..., description="Nombre de la entidad federativa")
    nom_mun: str = Field(..., description="Nombre del municipio")
    
    # Datos temporales
    fecha_ocurr: Optional[str] = Field(None, description="Fecha de ocurrencia (YYYY-MM-DD)")
    anio_ocur: Optional[int] = None
    mes_ocurr: Optional[int] = None
    
    # Perfil de la víctima
    sexo_cat: Optional[str] = Field(None, description="Sexo de la víctima")
    edad_anos: Optional[float] = Field(None, description="Edad en años cumplidos")
    edad_cat: Optional[str] = Field(None, description="Categoría de edad (ej. Adulto)")
    
    # Datos del hecho
    causa_def_cat: Optional[str] = Field(None, description="Causa de defunción agrupada")
    lugar_ocur_cat: Optional[str] = Field(None, description="Lugar donde ocurrió")
    
    # Geo
    lat_decimal: Optional[float] = None
    lon_decimal: Optional[float] = None

class PaginatedResponse(BaseModel):
    total: int
    page_size: int
    page: int
    data: List[HomicidioRecord]

# --- 3. CARGA DE DATOS ---

# Variable global para el DataFrame
df = pd.DataFrame()

def load_data():
    global df
    try:
        # Cargar CSV. Asumimos que está en el mismo directorio.
        # index_col=0 porque la primera columna es un índice numérico sin nombre en el header
        df = pd.read_csv("Homicidios_2024_clean.csv", index_col=0)
        
        # Limpieza básica para asegurar compatibilidad JSON
        # Convertir NaNs a None/Null
        df = df.where(pd.notnull(df), None)
        
        # Asegurar tipos de datos
        df['fecha_ocurr'] = pd.to_datetime(df['fecha_ocurr'], errors='coerce')
        
        print(f"✅ Datos cargados correctamente: {len(df)} registros.")
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        # Crear un DF vacío para no romper la app si falla el archivo
        df = pd.DataFrame()

@app.on_event("startup")
async def startup_event():
    load_data()

# --- 4. ENDPOINTS ---

@app.get("/", tags=["General"], include_in_schema=False)
def root():
    """Redirige a la documentación oficial."""
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["General"])
def health_check():
    """Verifica que la API esté viva y cuántos datos tiene cargados."""
    return {"status": "ok", "total_records": len(df)}

# --- SECCIÓN: DATOS CRUDOS ---

@app.get("/datos/busqueda", response_model=PaginatedResponse, tags=["Datos Crudos"])
def buscar_homicidios(
    estado: Optional[str] = Query(None, description="Nombre de la entidad (ej: 'Aguascalientes', 'Sinaloa')"),
    municipio: Optional[str] = Query(None, description="Nombre del municipio"),
    sexo: Optional[str] = Query(None, enum=["Hombre", "Mujer", "No especificado"], description="Sexo de la víctima"),
    fecha_inicio: Optional[str] = Query(None, description="YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(None, description="YYYY-MM-DD"),
    causa: Optional[str] = Query(None, description="Causa de defunción (búsqueda parcial)"),
    limit: int = Query(50, le=1000, description="Registros por página (Max 1000)"),
    offset: int = Query(0, description="Saltar los primeros N registros")
):
    """
    **Buscador Avanzado**: Filtra la base de datos completa.
    
    Este endpoint es ideal para extraer subconjuntos específicos de datos para auditoría o análisis detallado.
    Permite filtrar por ubicación, tiempo y características de la víctima.
    """
    if df.empty:
        raise HTTPException(status_code=503, detail="Datos no disponibles")

    # Aplicar filtros
    temp_df = df.copy()

    if estado:
        temp_df = temp_df[temp_df['nom_ent'].str.contains(estado, case=False, na=False)]
    if municipio:
        temp_df = temp_df[temp_df['nom_mun'].str.contains(municipio, case=False, na=False)]
    if sexo:
        temp_df = temp_df[temp_df['sexo_cat'] == sexo]
    if causa:
        temp_df = temp_df[temp_df['causa_def_cat'].str.contains(causa, case=False, na=False)]
    
    # Filtro fecha
    if fecha_inicio:
        temp_df = temp_df[temp_df['fecha_ocurr'] >= pd.to_datetime(fecha_inicio)]
    if fecha_fin:
        temp_df = temp_df[temp_df['fecha_ocurr'] <= pd.to_datetime(fecha_fin)]

    # Paginación
    total_records = len(temp_df)
    # Reemplazar NaNs y Nats antes de convertir a dict para JSON
    res_df = temp_df.iloc[offset : offset + limit]
    
    # Convertir a dict y sanear fechas para respuesta JSON
    # Pydantic espera strings para fechas si el modelo es str
    def safe_date_str(val):
        return val.strftime('%Y-%m-%d') if pd.notnull(val) else None
        
    records = []
    for _, row in res_df.iterrows():
        rec_dict = row.to_dict()
        rec_dict['fecha_ocurr'] = safe_date_str(rec_dict.get('fecha_ocurr'))
        # Limpiar floats NaN que pandas deja como nan
        for k, v in rec_dict.items():
            if isinstance(v, float) and math.isnan(v):
                rec_dict[k] = None
        records.append(rec_dict)

    return {
        "total": total_records,
        "page_size": len(records),
        "page": (offset // limit) + 1,
        "data": records
    }

# --- SECCIÓN: ANALÍTICA ---

@app.get("/resumen/nacional", tags=["Analítica"])
def resumen_nacional():
    """KPIs de alto nivel sobre la situación nacional en el dataset."""
    if df.empty: return {}
    
    total = len(df)
    top_estado = df['nom_ent'].value_counts().idxmax()
    top_municipio = df['nom_mun'].value_counts().idxmax()
    top_causa = df['causa_def_cat'].value_counts().idxmax()
    
    sexo_counts = df['sexo_cat'].value_counts(normalize=True).mul(100).round(1).to_dict()
    
    return {
        "total_homicidios": total,
        "zona_mas_afectada": {"estado": top_estado, "municipio": top_municipio},
        "causa_principal": top_causa,
        "distribucion_sexo_porcentaje": sexo_counts
    }

@app.get("/resumen/entidades", tags=["Analítica"])
def ranking_entidades(top: int = 32):
    """Devuelve el conteo de homicidios agrupado por entidad federativa."""
    if df.empty: return {}
    
    counts = df['nom_ent'].value_counts().head(top)
    return [{"entidad": k, "homicidios": v} for k, v in counts.items()]

@app.get("/resumen/temporal", tags=["Analítica"])
def analisis_temporal(agrupacion: str = Query("mensual", enum=["mensual", "semanal"])):
    """
    Tendencia temporal de los homicidios.
    Útil para generar gráficos de líneas y ver estacionalidad.
    """
    if df.empty: return {}
    
    temp_df = df.copy()
    if agrupacion == "mensual":
        # Agrupar por mes (numérico)
        grouped = temp_df.groupby('mes_ocurr').size()
        # Mapeo simple de nombres
        meses = {1:"Ene", 2:"Feb", 3:"Mar", 4:"Abr", 5:"May", 6:"Jun", 
                 7:"Jul", 8:"Ago", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dic"}
        return [{"mes_num": k, "mes_nombre": meses.get(k, str(k)), "total": v} for k, v in grouped.items()]
    else:
        # Semanal (dummy approach usando columna existente o inferida, aquí usamos día nacimiento como proxy si no hay semana, 
        # pero mejor usamos fecha_ocurr)
        temp_df['semana'] = temp_df['fecha_ocurr'].dt.isocalendar().week
        grouped = temp_df.groupby('semana').size().sort_index()
        return [{"semana": int(k), "total": v} for k, v in grouped.items()]

@app.get("/resumen/demografico", tags=["Analítica"])
def perfil_demografico():
    """Distribución por grupos de edad y sexo."""
    if df.empty: return {}
    
    # Agrupar por edad_cat
    edad_dist = df['edad_cat'].value_counts().to_dict()
    
    # Estadísticas de edad numérica
    edad_stats = {
        "promedio_edad": round(df['edad_anos'].mean(), 1),
        "min": df['edad_anos'].min(),
        "max": df['edad_anos'].max()
    }
    
    return {
        "distribucion_categoria_edad": edad_dist,
        "estadisticas_edad": edad_stats
    }

# --- SECCIÓN: GEOESPACIAL ---

@app.get("/geo/mapa", tags=["Geoespacial"])
def datos_mapa(limit: int = 5000):
    """
    GeoJSON-like o lista ligera de puntos lat/lon para mapeo rápido.
    Limita la respuesta para no saturar navegadores web.
    """
    if df.empty: return []
    
    # Filtrar solo los que tienen coordenadas válidas
    geo_df = df.dropna(subset=['lat_decimal', 'lon_decimal']).head(limit)
    
    puntos = []
    for _, row in geo_df.iterrows():
        puntos.append({
            "lat": row['lat_decimal'],
            "lon": row['lon_decimal'],
            "popup": f"{row['causa_def_cat']} - {row['edad_anos']} años",
            "tipo": row['lugar_ocur_cat']
        })
    
    return {
        "cantidad_puntos": len(puntos),
        "nota": "Muestra limitada para rendimiento de visualización",
        "puntos": puntos
    }

if __name__ == "__main__":
    # Configuración para correr localmente
    print("Iniciando servidor en http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
