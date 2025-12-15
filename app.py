#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST para Análisis de Homicidios México 2024
===============================================

API completa para análisis de datos de homicidios en México durante 2024.
Incluye análisis demográficos, geográficos, temporales y servicios especializados.

Autor: DataScience Mexico
Fecha: 2024
Versión: 1.0.0

REQUISITOS:
- Python 3.8+
- FastAPI
- pandas
- numpy
- uvicorn
- pydantic

INSTALACIÓN:
pip install fastapi pandas numpy uvicorn pydantic python-multipart

EJECUCIÓN:
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

DOCUMENTACIÓN AUTOMÁTICA:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
"""

from fastapi import FastAPI, HTTPException, Query, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime, date
import pandas as pd
import numpy as np
import json
from pathlib import Path as FilePath
import warnings
warnings.filterwarnings('ignore')

# Configuración de la aplicación
app = FastAPI(
    title="API de Análisis de Homicidios México 2024",
    description="""
    ## 📊 API Especializada en Análisis de Homicidios
    
    Esta API proporciona acceso completo a los datos de homicidios de México 2024 con 
    análisis avanzados para:
    
    ### 🎯 **Usuarios Objetivo**
    - **Analistas de Seguridad**: Índices de violencia, mapas de riesgo
    - **Investigadores Académicos**: Datos demográficos y patrones sociales
    - **Empresas de Seguros**: Evaluación de riesgos por región
    - **Gobierno y Política**: Estadísticas para toma de decisiones
    - **Medios de Comunicación**: Datos para reportajes especializados
    
    ### 🚀 **Características Principales**
    - Análisis demográfico detallado por edad, sexo y ubicación
    - Índices de violencia comparativos por entidad/municipio
    - Análisis temporal y detección de tendencias
    - Servicios geoespaciales con coordenadas
    - Comparaciones multi-regionales
    - Predicciones y modelado básico
    - Exportación de datos para análisis externos
    
    ### 📈 **Endpoints Especializados**
    - `/indices/violencia` - Índices de violencia por región
    - `/demografico/perfil` - Perfiles demográficos detallados
    - `/geografico/calor` - Mapas de calor geográfico
    - `/temporal/tendencias` - Análisis de tendencias temporales
    - `/comparativo/entidades` - Comparaciones entre entidades
    - `/predictivo/tendencias` - Predicciones básicas
    """,
    version="1.0.0",
    contact={
        "name": "DataScience Mexico",
        "email": "contacto@datasciencemexico.com",
        "url": "https://datasciencemexico.com",
    },
    license_info={
        "name": "Licencia Comercial",
        "url": "https://datasciencemexico.com/licencia",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración CORS para permitir acceso desde diferentes dominios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para validación de datos
class FiltroConsulta(BaseModel):
    """Filtros para consultas personalizadas"""
    entidades: Optional[List[str]] = Field(None, description="Lista de claves de entidades")
    municipios: Optional[List[str]] = Field(None, description="Lista de claves de municipios")
    sexo: Optional[List[str]] = Field(None, description="Lista de sexos (Hombre, Mujer)")
    edades: Optional[List[str]] = Field(None, description="Lista de categorías de edad")
    causas: Optional[List[str]] = Field(None, description="Lista de causas de defunción")
    fecha_inicio: Optional[date] = Field(None, description="Fecha de inicio (YYYY-MM-DD)")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin (YYYY-MM-DD)")
    area_urbana: Optional[List[str]] = Field(None, description="Lista de áreas (Urbana, Rural)")

class EstadisticaRegional(BaseModel):
    """Estadísticas por región"""
    entidad: str
    municipio: str
    total_casos: int
    tasa_por_100k: float
    poblacion_total: int
    indice_violencia: float
    casos_por_sexo: Dict[str, int]
    casos_por_edad: Dict[str, int]
    causas_principales: List[Dict[str, Any]]
    coordenadas: Optional[Dict[str, float]] = None

class AnalisisTemporal(BaseModel):
    """Análisis temporal de datos"""
    periodo: str
    total_casos: int
    tendencia: str
    variacion_porcentual: float
    casos_por_mes: List[Dict[str, Any]]
    dia_mas_violento: str
    hora_pico: Optional[str] = None
    estacionalidad: Dict[str, Any]

class IndiceSeguridad(BaseModel):
    """Índice de seguridad por región"""
    entidad: str
    municipio: Optional[str] = None
    indice_seguridad: float
    categoria_riesgo: str
    percentil_nacional: int
    comparacion_promedio: float
    factores_riesgo: List[str]
    recomendaciones: List[str]

# Carga y procesamiento de datos
class HomicidiosDataProcessor:
    """Procesador principal de datos de homicidios"""
    
    def __init__(self):
        self.df = None
        self.entidades_info = {}
        self.municipios_info = {}
        self.estadisticas_cache = {}
        
    def cargar_datos(self, archivo_csv: str = "Homicidios_2024_clean.csv"):
        """Carga y procesa los datos del archivo CSV"""
        try:
            print(f"📊 Cargando datos desde {archivo_csv}...")
            
            # Cargar CSV
            self.df = pd.read_csv(archivo_csv)
            
            # Limpiar y procesar datos
            self.df = self._limpiar_datos(self.df)
            
            # Crear índices para búsquedas rápidas
            self._crear_indices()
            
            print(f"✅ Datos cargados exitosamente: {len(self.df)} registros")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando datos: {str(e)}")
            return False
    
    def _limpiar_datos(self, df):
        """Limpia y normaliza los datos"""
        # Copiar DataFrame
        df = df.copy()
        
        # Convertir fechas
        df['fecha_ocurr'] = pd.to_datetime(df['fecha_ocurr'], errors='coerce')
        df['fecha_nac'] = pd.to_datetime(df['fecha_nac'], errors='coerce')
        
        # Limpiar coordenadas
        df['lat_decimal'] = pd.to_numeric(df['lat_decimal'], errors='coerce')
        df['lon_decimal'] = pd.to_numeric(df['lon_decimal'], errors='coerce')
        
        # Limpiar edades
        df['edad_anos'] = pd.to_numeric(df['edad_anos'], errors='coerce')
        
        # Limpiar población
        df['pob_total'] = pd.to_numeric(df['pob_total'], errors='coerce')
        
        # Filtrar registros válidos
        df = df.dropna(subset=['fecha_ocurr'])
        df = df[df['anio_ocur'] == 2024]  # Solo 2024
        
        # Agregar columnas calculadas
        df['mes_ocurr'] = df['fecha_ocurr'].dt.month
        df['dia_semana'] = df['fecha_ocurr'].dt.day_name()
        df['semana_año'] = df['fecha_ocurr'].dt.isocalendar().week
        
        return df
    
    def _crear_indices(self):
        """Crea índices para búsquedas optimizadas"""
        # Índice de entidades
        self.entidades_info = self.df.groupby('clave_entidad').agg({
            'nom_ent': 'first',
            'pob_total': 'max',
            'lat_decimal': 'mean',
            'lon_decimal': 'mean'
        }).to_dict('index')
        
        # Índice de municipios
        self.municipios_info = self.df.groupby(['clave_entidad', 'clave_municipio']).agg({
            'nom_mun': 'first',
            'nom_ent': 'first',
            'pob_total': 'max',
            'lat_decimal': 'mean',
            'lon_decimal': 'mean'
        }).to_dict('index')

# Instancia global del procesador de datos
processor = HomicidiosDataProcessor()

# Dependencia para obtener datos
def get_data():
    """Dependencia para obtener datos procesados"""
    if processor.df is None:
        processor.cargar_datos()
    return processor

# ================================
# ENDPOINTS DE INFORMACIÓN GENERAL
# ================================

@app.get("/", tags=["🏠 Información General"])
async def raiz():
    """Endpoint raíz con información de la API"""
    return {
        "mensaje": "🩸 API de Análisis de Homicidios México 2024",
        "version": "1.0.0",
        "estado": "🟢 Activa",
        "total_registros": len(processor.df) if processor.df is not None else 0,
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "manual": "/manual"
        },
        "endpoints_principales": {
            "estadisticas": "/estadisticas/general",
            "entidades": "/entidades/lista",
            "demografico": "/demografico/perfil",
            "geografico": "/geografico/mapa-calor",
            "temporal": "/temporal/tendencias",
            "seguridad": "/indices/violencia"
        }
    }

@app.get("/estadisticas/general", tags=["📊 Estadísticas Generales"])
async def estadisticas_generales(data: HomicidiosDataProcessor = Depends(get_data)):
    """Estadísticas generales del dataset"""
    if data.df is None or len(data.df) == 0:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df
    
    # Estadísticas básicas
    total_casos = len(df)
    entidades_unicas = df['clave_entidad'].nunique()
    municipios_unicos = df['clave_municipio'].nunique()
    
    # Distribución por sexo
    sexo_dist = df['sexo_cat'].value_counts().to_dict()
    
    # Distribución por edad
    edad_dist = df['edad_cat'].value_counts().to_dict()
    
    # Distribución por causa
    causa_dist = df['causa_def_cat'].value_counts().head(10).to_dict()
    
    # Distribución por lugar
    lugar_dist = df['lugar_ocur_cat'].value_counts().to_dict()
    
    # Distribución por área
    area_dist = df['area_ur'].value_counts().to_dict()
    
    # Estadísticas temporales
    casos_por_mes = df.groupby('mes_ocurr').size().to_dict()
    
    # Casos más recientes
    casos_recientes = df.nlargest(5, 'fecha_ocurr')[
        ['fecha_ocurr', 'nom_ent', 'nom_mun', 'sexo_cat', 'edad_cat', 'causa_def_cat']
    ].to_dict('records')
    
    return {
        "resumen": {
            "total_casos": total_casos,
            "entidades_afectadas": entidades_unicas,
            "municipios_afectados": municipios_unicos,
            "periodo_datos": "2024",
            "fecha_actualizacion": datetime.now().isoformat()
        },
        "distribuciones": {
            "por_sexo": sexo_dist,
            "por_edad": edad_dist,
            "por_causa": causa_dist,
            "por_lugar": lugar_dist,
            "por_area": area_dist,
            "por_mes": casos_por_mes
        },
        "casos_recientes": casos_recientes
    }

@app.get("/entidades/lista", tags=["🗺️ Entidades"])
async def lista_entidades(data: HomicidiosDataProcessor = Depends(get_data)):
    """Lista todas las entidades federativas con estadísticas básicas"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df
    
    # Estadísticas por entidad
    entidades_stats = df.groupby(['clave_entidad', 'nom_ent']).agg({
        '': 'count',  # Esto será el total de casos
        'pob_total': 'max',
        'lat_decimal': 'mean',
        'lon_decimal': 'mean'
    }).reset_index()
    
    entidades_stats.columns = ['clave_entidad', 'nombre_entidad', 'total_casos', 'poblacion', 'lat_promedio', 'lon_promedio']
    
    # Calcular tasas por 100k habitantes
    entidades_stats['tasa_por_100k'] = (entidades_stats['total_casos'] / entidades_stats['poblacion'] * 100000).round(2)
    
    # Ordenar por tasa descendente
    entidades_stats = entidades_stats.sort_values('tasa_por_100k', ascending=False)
    
    return entidades_stats.to_dict('records')

# ================================
# ENDPOINTS DEMOGRÁFICOS
# ================================

@app.get("/demografico/perfil", tags=["👥 Análisis Demográfico"])
async def perfil_demografico(
    entidad: Optional[str] = Query(None, description="Clave de entidad específica"),
    municipio: Optional[str] = Query(None, description="Clave de municipio específico"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Análisis demográfico detallado por región"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df.copy()
    
    # Aplicar filtros
    if entidad:
        df = df[df['clave_entidad'] == entidad]
    if municipio:
        df = df[df['clave_municipio'] == municipio]
    
    if len(df) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron datos para los filtros especificados")
    
    # Análisis por sexo
    sexo_analisis = {}
    for sexo in df['sexo_cat'].unique():
        if pd.notna(sexo):
            df_sexo = df[df['sexo_cat'] == sexo]
            sexo_analisis[sexo] = {
                "total_casos": len(df_sexo),
                "porcentaje": round(len(df_sexo) / len(df) * 100, 2),
                "edad_promedio": round(df_sexo['edad_anos'].mean(), 1) if df_sexo['edad_anos'].notna().any() else None,
                "edad_mediana": round(df_sexo['edad_anos'].median(), 1) if df_sexo['edad_anos'].notna().any() else None,
                "causas_principales": df_sexo['causa_def_cat'].value_counts().head(3).to_dict(),
                "lugares_principales": df_sexo['lugar_ocur_cat'].value_counts().head(3).to_dict()
            }
    
    # Análisis por grupos de edad
    edad_analisis = {}
    for edad in df['edad_cat'].unique():
        if pd.notna(edad):
            df_edad = df[df['edad_cat'] == edad]
            edad_analisis[edad] = {
                "total_casos": len(df_edad),
                "porcentaje": round(len(df_edad) / len(df) * 100, 2),
                "distribucion_sexo": df_edad['sexo_cat'].value_counts().to_dict(),
                "causas_principales": df_edad['causa_def_cat'].value_counts().head(3).to_dict()
            }
    
    # Análisis de distribución étnica/cultural
    cultura_analisis = {
        "afromexicano": {
            "si": len(df[df['afromex'] == '1']),
            "no": len(df[df['afromex'] == '2']),
            "no_especificado": len(df[df['afromex'].isin(['9', '8'])])
        },
        "indigena": {
            "si": len(df[df['conindig'] == '1']),
            "no": len(df[df['conindig'] == '2']),
            "no_especificado": len(df[df['conindig'].isin(['9', '8'])])
        }
    }
    
    # Análisis de patrones de edad
    edad_stats = {
        "edad_promedio_general": round(df['edad_anos'].mean(), 1) if df['edad_anos'].notna().any() else None,
        "edad_mediana_general": round(df['edad_anos'].median(), 1) if df['edad_anos'].notna().any() else None,
        "edad_minima": int(df['edad_anos'].min()) if df['edad_anos'].notna().any() else None,
        "edad_maxima": int(df['edad_anos'].max()) if df['edad_anos'].notna().any() else None,
        "desviacion_estandar": round(df['edad_anos'].std(), 1) if df['edad_anos'].notna().any() else None
    }
    
    # Contexto geográfico
    contexto = {
        "entidad": df['nom_ent'].iloc[0] if entidad else "Nacional",
        "municipio": df['nom_mun'].iloc[0] if municipio else None,
        "total_casos_analizados": len(df),
        "porcentaje_del_total": round(len(df) / len(data.df) * 100, 2)
    }
    
    return {
        "contexto": contexto,
        "analisis_sexo": sexo_analisis,
        "analisis_edad": edad_analisis,
        "analisis_cultura": cultura_analisis,
        "estadisticas_edad": edad_stats
    }

# ================================
# ENDPOINTS GEOGRÁFICOS
# ================================

@app.get("/geografico/mapa-calor", tags=["🗺️ Análisis Geográfico"])
async def mapa_calor_geografico(
    tipo: str = Query("entidad", regex="^(entidad|municipio)$", description="Tipo de agregación geográfica"),
    metrica: str = Query("tasa", regex="^(tasa|total|casos_por_sexo)$", description="Métrica a calcular"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Genera datos para mapas de calor geográfico"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df
    
    if tipo == "entidad":
        # Agrupar por entidad
        resultado = df.groupby(['clave_entidad', 'nom_ent', 'lat_decimal', 'lon_decimal']).agg({
            '': 'count',  # Total de casos
            'pob_total': 'max',
            'sexo_cat': lambda x: x.value_counts().to_dict()
        }).reset_index()
        
        resultado.columns = ['clave', 'nombre', 'latitud', 'longitud', 'total_casos', 'poblacion', 'casos_por_sexo']
        
    else:
        # Agrupar por municipio
        resultado = df.groupby(['clave_municipio', 'nom_mun', 'nom_ent', 'lat_decimal', 'lon_decimal']).agg({
            '': 'count',
            'pob_total': 'max',
            'sexo_cat': lambda x: x.value_counts().to_dict()
        }).reset_index()
        
        resultado.columns = ['clave', 'nombre', 'entidad', 'latitud', 'longitud', 'total_casos', 'poblacion', 'casos_por_sexo']
    
    # Calcular métrica solicitada
    if metrica == "tasa":
        resultado['valor'] = (resultado['total_casos'] / resultado['poblacion'] * 100000).round(2)
        resultado['metrica'] = "Tasa por 100,000 habitantes"
    elif metrica == "total":
        resultado['valor'] = resultado['total_casos']
        resultado['metrica'] = "Total de casos"
    else:  # casos_por_sexo
        # Para casos por sexo, devolver el desglose completo
        resultado = resultado.to_dict('records')
        for item in resultado:
            item['metrica'] = "Casos por sexo"
        return {
            "tipo": tipo,
            "metrica": metrica,
            "datos": resultado,
            "descripcion": "Distribución de casos por sexo para cada región"
        }
    
    # Ordenar por valor descendente
    resultado = resultado.sort_values('valor', ascending=False)
    
    # Convertir a lista de diccionarios
    resultado = resultado.to_dict('records')
    
    return {
        "tipo": tipo,
        "metrica": metrica,
        "datos": resultado,
        "descripcion": f"Datos de {metrica} por {tipo} para mapas de calor"
    }

@app.get("/geografico/zonas-calientes", tags=["🗺️ Análisis Geográfico"])
async def zonas_calientes(
    limite: int = Query(10, ge=1, le=50, description="Número de zonas a retornar"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Identifica las zonas geográficas más problemáticas"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df
    
    # Análisis por municipio
    municipios = df.groupby(['clave_municipio', 'nom_mun', 'nom_ent']).agg({
        '': 'count',
        'pob_total': 'max',
        'lat_decimal': 'mean',
        'lon_decimal': 'mean',
        'causa_def_cat': lambda x: x.value_counts().head(3).to_dict()
    }).reset_index()
    
    municipios.columns = ['clave_municipio', 'nombre_municipio', 'entidad', 'total_casos', 'poblacion', 'latitud', 'longitud', 'causas_principales']
    
    # Calcular tasa por 100k
    municipios['tasa_por_100k'] = (municipios['total_casos'] / municipios['poblacion'] * 100000).round(2)
    
    # Calcular índice de violencia (combinando varios factores)
    municipios['indice_violencia'] = (
        municipios['tasa_por_100k'] * 0.4 +  # 40% peso a tasa
        (municipios['total_casos'] / municipios['total_casos'].max() * 100) * 0.6  # 60% peso a volumen absoluto
    ).round(2)
    
    # Ordenar por índice de violencia
    zonas_calientes = municipios.nlargest(limite, 'indice_violencia')
    
    return zonas_calientes.to_dict('records')

# ================================
# ENDPOINTS TEMPORALES
# ================================

@app.get("/temporal/tendencias", tags=["📅 Análisis Temporal"])
async def analisis_tendencias(
    periodo: str = Query("mensual", regex="^(mensual|diario|semanal)$", description="Período de análisis"),
    entidad: Optional[str] = Query(None, description="Filtrar por entidad"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Análisis de tendencias temporales"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df.copy()
    
    # Aplicar filtro de entidad si se especifica
    if entidad:
        df = df[df['clave_entidad'] == entidad]
    
    if len(df) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron datos para los filtros especificados")
    
    if periodo == "mensual":
        # Análisis mensual
        casos_por_mes = df.groupby('mes_ocurr').agg({
            '': 'count',
            'causa_def_cat': lambda x: x.value_counts().head(3).to_dict(),
            'lugar_ocur_cat': lambda x: x.value_counts().head(3).to_dict()
        }).reset_index()
        
        casos_por_mes.columns = ['mes', 'total_casos', 'causas_principales', 'lugares_principales']
        
        # Calcular tendencia
        if len(casos_por_mes) > 1:
            casos_ordenados = casos_por_mes.sort_values('mes')
            casos_ordenados['variacion'] = casos_ordenados['total_casos'].pct_change() * 100
            tendencia_general = casos_ordenados['variacion'].mean()
        else:
            tendencia_general = 0
        
        # Mes más violento
        mes_mas_violento = casos_por_mes.loc[casos_por_mes['total_casos'].idxmax()]
        
        resultado = {
            "periodo": "Mensual",
            "datos": casos_por_mes.to_dict('records'),
            "tendencia_general": f"{tendencia_general:+.1f}%",
            "mes_mas_violento": {
                "mes": int(mes_mas_violento['mes']),
                "casos": int(mes_mas_violento['total_casos'])
            },
            "variabilidad": {
                "meses_con_datos": len(casos_por_mes),
                "promedio_mensual": round(casos_por_mes['total_casos'].mean(), 1),
                "desviacion_estandar": round(casos_por_mes['total_casos'].std(), 1)
            }
        }
    
    elif periodo == "diario":
        # Análisis diario
        casos_por_dia = df.groupby('fecha_ocurr').agg({
            '': 'count'
        }).reset_index()
        casos_por_dia.columns = ['fecha', 'total_casos']
        casos_por_dia['fecha'] = casos_por_dia['fecha'].dt.strftime('%Y-%m-%d')
        
        # Día más violento
        dia_mas_violento = casos_por_dia.loc[casos_por_dia['total_casos'].idxmax()]
        
        resultado = {
            "periodo": "Diario",
            "datos": casos_por_dia.to_dict('records'),
            "dia_mas_violento": {
                "fecha": dia_mas_violento['fecha'],
                "casos": int(dia_mas_violento['total_casos'])
            },
            "estadisticas": {
                "dias_con_datos": len(casos_por_dia),
                "promedio_diario": round(casos_por_dia['total_casos'].mean(), 1),
                "maximo_diario": int(casos_por_dia['total_casos'].max()),
                "minimo_diario": int(casos_por_dia['total_casos'].min())
            }
        }
    
    else:  # semanal
        # Análisis semanal
        casos_por_semana = df.groupby('semana_año').agg({
            '': 'count'
        }).reset_index()
        casos_por_semana.columns = ['semana', 'total_casos']
        
        # Calcular fechas de inicio de cada semana
        casos_por_semana['fecha_inicio'] = pd.to_datetime('2024-01-01') + pd.to_timedelta((casos_por_semana['semana'] - 1) * 7, unit='D')
        casos_por_semana['fecha_inicio'] = casos_por_semana['fecha_inicio'].dt.strftime('%Y-%m-%d')
        
        resultado = {
            "periodo": "Semanal",
            "datos": casos_por_semana.to_dict('records'),
            "estadisticas": {
                "semanas_con_datos": len(casos_por_semana),
                "promedio_semanal": round(casos_por_semana['total_casos'].mean(), 1),
                "maximo_semanal": int(casos_por_semana['total_casos'].max())
            }
        }
    
    # Agregar contexto
    resultado["contexto"] = {
        "total_casos_analizados": len(df),
        "entidad": df['nom_ent'].iloc[0] if entidad else "Nacional",
        "rango_fechas": {
            "inicio": df['fecha_ocurr'].min().strftime('%Y-%m-%d'),
            "fin": df['fecha_ocurr'].max().strftime('%Y-%m-%d')
        }
    }
    
    return resultado

@app.get("/temporal/patrones", tags=["📅 Análisis Temporal"])
async def patrones_temporales(
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Análisis de patrones temporales específicos"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df
    
    # Patrones por día de la semana
    patrones_dia = df['dia_semana'].value_counts().to_dict()
    
    # Patrones por mes
    meses_nombres = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    patrones_mes = {}
    for mes_num, mes_nombre in meses_nombres.items():
        casos_mes = len(df[df['mes_ocurr'] == mes_num])
        if casos_mes > 0:
            patrones_mes[mes_nombre] = casos_mes
    
    # Análisis de estacionalidad
    trimestres = {
        'Q1': len(df[df['mes_ocurr'].isin([1, 2, 3])]),
        'Q2': len(df[df['mes_ocurr'].isin([4, 5, 6])]),
        'Q3': len(df[df['mes_ocurr'].isin([7, 8, 9])]),
        'Q4': len(df[df['mes_ocurr'].isin([10, 11, 12])])
    }
    
    # Detectar tendencias
    analisis_trimestral = []
    for trimestre, casos in trimestres.items():
        analisis_trimestral.append({
            "trimestre": trimestre,
            "casos": casos,
            "porcentaje": round(casos / len(df) * 100, 1)
        })
    
    # Días más y menos violentos
    dias_ordenados = df['dia_semana'].value_counts()
    dia_mas_violento = dias_ordenados.index[0]
    dia_menos_violento = dias_ordenados.index[-1]
    
    return {
        "patrones_semanales": {
            "por_dia_semana": patrones_dia,
            "dia_mas_violento": dia_mas_violento,
            "dia_menos_violento": dia_menos_violento,
            "variabilidad_semanal": round(dias_ordenados.std(), 2)
        },
        "patrones_mensuales": {
            "por_mes": patrones_mes,
            "mes_mas_violento": max(patrones_mes, key=patrones_mes.get),
            "mes_menos_violento": min(patrones_mes, key=patrones_mes.get)
        },
        "estacionalidad": {
            "por_trimestre": analisis_trimestral,
            "trimestre_mas_violento": max(trimestres, key=trimestres.get),
            "trimestre_menos_violento": min(trimestres, key=trimestres.get)
        },
        "insights": [
            f"El {dia_mas_violento} es el día con más homicidios registrados",
            f"El {dia_menos_violento} es el día con menos homicidios registrados",
            f"El trimestre {max(trimestres, key=trimestres.get)} concentra más casos"
        ]
    }

# ================================
# ENDPOINTS DE ÍNDICES DE SEGURIDAD
# ================================

@app.get("/indices/violencia", tags=["🔒 Índices de Seguridad"])
async def indices_violencia(
    tipo: str = Query("entidad", regex="^(entidad|municipio)$", description="Tipo de análisis"),
    limite: int = Query(10, ge=1, le=50, description="Número de resultados"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Calcula índices de violencia por región"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df
    
    if tipo == "entidad":
        # Análisis por entidad
        indices = df.groupby(['clave_entidad', 'nom_ent']).agg({
            '': 'count',  # Total casos
            'pob_total': 'max',
            'sexo_cat': lambda x: x.value_counts().to_dict(),
            'causa_def_cat': lambda x: x.value_counts().head(3).to_dict(),
            'lugar_ocur_cat': lambda x: x.value_counts().head(3).to_dict()
        }).reset_index()
        
        indices.columns = ['clave', 'nombre', 'total_casos', 'poblacion', 'distribucion_sexo', 'causas_principales', 'lugares_principales']
        
    else:
        # Análisis por municipio
        indices = df.groupby(['clave_municipio', 'nom_mun', 'nom_ent']).agg({
            '': 'count',
            'pob_total': 'max',
            'sexo_cat': lambda x: x.value_counts().to_dict(),
            'causa_def_cat': lambda x: x.value_counts().head(3).to_dict(),
            'lugar_ocur_cat': lambda x: x.value_counts().head(3).to_dict()
        }).reset_index()
        
        indices.columns = ['clave', 'nombre', 'entidad', 'total_casos', 'poblacion', 'distribucion_sexo', 'causas_principales', 'lugares_principales']
    
    # Calcular métricas de violencia
    indices['tasa_por_100k'] = (indices['total_casos'] / indices['poblacion'] * 100000).round(2)
    indices['indice_violencia'] = (
        indices['tasa_por_100k'] * 0.6 +  # 60% peso a tasa demográfica
        (indices['total_casos'] / indices['total_casos'].max() * 100) * 0.4  # 40% peso a volumen absoluto
    ).round(2)
    
    # Calcular percentil nacional
    indices['percentil_nacional'] = indices['indice_violencia'].rank(pct=True).round(2) * 100
    
    # Clasificar riesgo
    def clasificar_riesgo(indice):
        if indice >= 80:
            return "🔴 CRÍTICO"
        elif indice >= 60:
            return "🟠 ALTO"
        elif indice >= 40:
            return "🟡 MEDIO"
        elif indice >= 20:
            return "🟢 BAJO"
        else:
            return "✅ MUY BAJO"
    
    indices['categoria_riesgo'] = indices['indice_violencia'].apply(clasificar_riesgo)
    
    # Ordenar por índice de violencia
    indices = indices.sort_values('indice_violencia', ascending=False)
    
    # Tomar top resultados
    indices_top = indices.head(limite)
    
    # Convertir a registros
    resultado = indices_top.to_dict('records')
    
    return {
        "tipo_analisis": tipo,
        "metodologia": {
            "indice_violencia": "0.6 * tasa_por_100k + 0.4 * volumen_relativo",
            "percentil": "Posición relativa respecto al total nacional",
            "clasificacion": "Basada en percentiles del índice de violencia"
        },
        "resumen": {
            "total_regiones_analizadas": len(indices),
            "promedio_nacional": round(indices['indice_violencia'].mean(), 2),
            "mediana_nacional": round(indices['indice_violencia'].median(), 2)
        },
        "top_regiones": resultado
    }

@app.get("/indices/tendencias-seguridad", tags=["🔒 Índices de Seguridad"])
async def tendencias_seguridad(
    entidad: Optional[str] = Query(None, description="Filtrar por entidad"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Análisis de tendencias en seguridad"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df.copy()
    
    # Aplicar filtro
    if entidad:
        df = df[df['clave_entidad'] == entidad]
    
    if len(df) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron datos para los filtros especificados")
    
    # Análisis mensual de seguridad
    seguridad_mensual = df.groupby('mes_ocurr').agg({
        '': 'count',
        'causa_def_cat': lambda x: (x == 'Arma de Fuego').sum()  # Casos con arma de fuego
    }).reset_index()
    
    seguridad_mensual.columns = ['mes', 'total_casos', 'casos_arma_fuego']
    
    # Calcular métricas de seguridad
    seguridad_mensual['tasa_seguridad'] = (1 - (seguridad_mensual['total_casos'] / seguridad_mensual['total_casos'].max())) * 100
    seguridad_mensual['porcentaje_armas'] = (seguridad_mensual['casos_arma_fuego'] / seguridad_mensual['total_casos'] * 100).round(1)
    
    # Identificar tendencias
    if len(seguridad_mensual) > 1:
        tendencia_general = "🔻 Mejorando" if seguridad_mensual['total_casos'].iloc[-1] < seguridad_mensual['total_casos'].iloc[0] else "🔺 Empeorando"
    else:
        tendencia_general = "➡️ Estable"
    
    # Meses críticos (por encima del promedio)
    promedio_mensual = seguridad_mensual['total_casos'].mean()
    meses_criticos = seguridad_mensual[seguridad_mensual['total_casos'] > promedio_mensual]['mes'].tolist()
    
    return {
        "contexto": {
            "entidad": df['nom_ent'].iloc[0] if entidad else "Nacional",
            "periodo_analizado": "2024",
            "total_casos": len(df)
        },
        "tendencias": {
            "direccion_general": tendencia_general,
            "meses_criticos": meses_criticos,
            "promedio_mensual": round(promedio_mensual, 1),
            "variacion_total": round(((seguridad_mensual['total_casos'].iloc[-1] - seguridad_mensual['total_casos'].iloc[0]) / seguridad_mensual['total_casos'].iloc[0] * 100), 1) if len(seguridad_mensual) > 1 else 0
        },
        "datos_mensuales": seguridad_mensual.to_dict('records'),
        "factores_riesgo": {
            "porcentaje_armas_promedio": round(seguridad_mensual['porcentaje_armas'].mean(), 1),
            "mes_mayor_riesgo": int(seguridad_mensual.loc[seguridad_mensual['total_casos'].idxmax(), 'mes']),
            "mes_menor_riesgo": int(seguridad_mensual.loc[seguridad_mensual['total_casos'].idxmin(), 'mes'])
        }
    }

# ================================
# ENDPOINTS COMPARATIVOS
# ================================

@app.get("/comparativo/entidades", tags=["⚖️ Análisis Comparativo"])
async def comparar_entidades(
    entidades: str = Query(..., description="Lista de entidades separadas por comas"),
    metrica: str = Query("tasa", regex="^(tasa|total|indice)$", description="Métrica de comparación"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Compara estadísticas entre entidades específicas"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    # Parsear entidades
    lista_entidades = entidades.split(',')
    
    df = data.df[data.df['clave_entidad'].isin(lista_entidades)]
    
    if len(df) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron datos para las entidades especificadas")
    
    # Estadísticas por entidad
    comparacion = df.groupby(['clave_entidad', 'nom_ent']).agg({
        '': 'count',
        'pob_total': 'max',
        'sexo_cat': lambda x: x.value_counts().to_dict(),
        'edad_cat': lambda x: x.value_counts().to_dict(),
        'causa_def_cat': lambda x: x.value_counts().head(3).to_dict()
    }).reset_index()
    
    comparacion.columns = ['clave', 'nombre', 'total_casos', 'poblacion', 'distribucion_sexo', 'distribucion_edad', 'causas_principales']
    
    # Calcular métricas
    comparacion['tasa_por_100k'] = (comparacion['total_casos'] / comparacion['poblacion'] * 100000).round(2)
    comparacion['indice_violencia'] = (
        comparacion['tasa_por_100k'] * 0.6 + 
        (comparacion['total_casos'] / comparacion['total_casos'].max() * 100) * 0.4
    ).round(2)
    
    # Seleccionar métrica de comparación
    if metrica == "total":
        comparacion = comparacion.sort_values('total_casos', ascending=False)
        valor_comparacion = 'total_casos'
    elif metrica == "indice":
        comparacion = comparacion.sort_values('indice_violencia', ascending=False)
        valor_comparacion = 'indice_violencia'
    else:
        comparacion = comparacion.sort_values('tasa_por_100k', ascending=False)
        valor_comparacion = 'tasa_por_100k'
    
    # Calcular rankings
    comparacion['ranking'] = range(1, len(comparacion) + 1)
    
    # Análisis comparativo
    maximo = comparacion[valor_comparacion].max()
    minimo = comparacion[valor_comparacion].min()
    promedio = comparacion[valor_comparacion].mean()
    
    # Agregar contexto de cada entidad
    for idx, row in comparacion.iterrows():
        comparacion.at[idx, 'contexto'] = {
            "porcentaje_del_total": round(row['total_casos'] / df.shape[0] * 100, 1),
            "vs_promedio": round((row[valor_comparacion] / promedio - 1) * 100, 1),
            "factor_vs_maximo": round(row[valor_comparacion] / maximo, 2) if maximo > 0 else 0
        }
    
    return {
        "metrica_comparacion": metrica,
        "entidades_analizadas": len(lista_entidades),
        "estadisticas_generales": {
            "maximo": round(maximo, 2),
            "minimo": round(minimo, 2),
            "promedio": round(promedio, 2),
            "rango": round(maximo - minimo, 2)
        },
        "ranking": comparacion[['ranking', 'clave', 'nombre', valor_comparacion, 'total_casos']].to_dict('records'),
        "detalle_completo": comparacion.to_dict('records')
    }

@app.get("/comparativo/tendencias-regionales", tags=["⚖️ Análisis Comparativo"])
async def tendencias_regionales(
    region_norte: str = Query("02", description="Clave de entidad del norte"),
    region_sur: str = Query("01", description="Clave de entidad del sur"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Compara tendencias entre dos regiones"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df
    
    # Obtener datos de ambas regiones
    norte = df[df['clave_entidad'] == region_norte]
    sur = df[df['clave_entidad'] == region_sur]
    
    if len(norte) == 0 or len(sur) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron datos para una o ambas regiones especificadas")
    
    # Análisis mensual de cada región
    norte_mensual = norte.groupby('mes_ocurr').size()
    sur_mensual = sur.groupby('mes_ocurr').size()
    
    # CrearDataFrame comparativo
    comparativo_mensual = pd.DataFrame({
        'mes': range(1, 13),
        'norte': [norte_mensual.get(i, 0) for i in range(1, 13)],
        'sur': [sur_mensual.get(i, 0) for i in range(1, 13)]
    })
    
    comparativo_mensual['diferencia'] = comparativo_mensual['norte'] - comparativo_mensual['sur']
    comparativo_mensual['ratio'] = (comparativo_mensual['norte'] / comparativo_mensual['sur']).round(2)
    
    # Estadísticas generales
    stats_norte = {
        'total_casos': len(norte),
        'tasa_por_100k': round(len(norte) / norte['pob_total'].max() * 100000, 2),
        'mes_pico': norte['mes_ocurr'].mode().iloc[0] if len(norte['mes_ocurr'].mode()) > 0 else None
    }
    
    stats_sur = {
        'total_casos': len(sur),
        'tasa_por_100k': round(len(sur) / sur['pob_total'].max() * 100000, 2),
        'mes_pico': sur['mes_ocurr'].mode().iloc[0] if len(sur['mes_ocurr'].mode()) > 0 else None
    }
    
    return {
        "regiones_comparadas": {
            "norte": {
                "clave": region_norte,
                "nombre": norte['nom_ent'].iloc[0],
                "estadisticas": stats_norte
            },
            "sur": {
                "clave": region_sur,
                "nombre": sur['nom_ent'].iloc[0],
                "estadisticas": stats_sur
            }
        },
        "analisis_mensual": comparativo_mensual.to_dict('records'),
        "insights": {
            "region_mas_violenta": norte['nom_ent'].iloc[0] if len(norte) > len(sur) else sur['nom_ent'].iloc[0],
            "diferencia_total": abs(len(norte) - len(sur)),
            "meses_norte_superior": len(comparativo_mensual[comparativo_mensual['norte'] > comparativo_mensual['sur']]),
            "meses_sur_superior": len(comparativo_mensual[comparativo_mensual['sur'] > comparativo_mensual['norte']])
        }
    }

# ================================
# ENDPOINTS PREDICTIVOS
# ================================

@app.get("/predictivo/tendencias", tags=["🔮 Análisis Predictivo"])
async def predicciones_tendencias(
    horizonte: int = Query(3, ge=1, le=12, description="Meses hacia adelante para predecir"),
    entidad: Optional[str] = Query(None, description="Filtrar por entidad"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Predicciones básicas de tendencias"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df.copy()
    
    if entidad:
        df = df[df['clave_entidad'] == entidad]
    
    if len(df) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron datos para los filtros especificados")
    
    # Análisis de tendencias mensuales
    casos_mensuales = df.groupby('mes_ocurr').size().reindex(range(1, 13), fill_value=0)
    
    # Modelo simple de tendencia lineal
    meses_con_datos = casos_mensuales[casos_mensuales > 0]
    if len(meses_con_datos) < 2:
        raise HTTPException(status_code=400, detail="Datos insuficientes para predicción")
    
    # Calcular tendencia
    x = np.arange(len(casos_mensuales))
    y = casos_mensuales.values
    
    # Regresión lineal simple
    slope, intercept = np.polyfit(x, y, 1)
    
    # Generar predicciones
    predicciones = []
    for i in range(1, horizonte + 1):
        mes_futuro = 12 + i
        valor_predicho = max(0, slope * (mes_futuro - 1) + intercept)
        predicciones.append({
            "mes": mes_futuro,
            "casos_predichos": round(valor_predicho),
            "intervalo_confianza": {
                "inferior": round(valor_predicho * 0.7),
                "superior": round(valor_predicho * 1.3)
            }
        })
    
    # Análisis de estacionalidad
    estacionalidad = {}
    for mes in range(1, 13):
        casos_mes = casos_mensuales[mes]
        if casos_mes > 0:
            estacionalidad[mes] = casos_mes
    
    # Identificar patrón estacional
    meses_ordenados = sorted(estacionalidad.items(), key=lambda x: x[1], reverse=True)
    mes_mas_violento = meses_ordenados[0][0] if meses_ordenados else None
    mes_menos_violento = meses_ordenados[-1][0] if meses_ordenados else None
    
    return {
        "modelo": "Regresión Lineal Simple",
        "parametros": {
            "pendiente": round(slope, 4),
            "intercepto": round(intercept, 2),
            "r_cuadrado": round(np.corrcoef(x, y)[0, 1] ** 2, 3) if len(x) > 1 else 0
        },
        "contexto": {
            "entidad": df['nom_ent'].iloc[0] if entidad else "Nacional",
            "datos_historicos": casos_mensuales.to_dict(),
            "mes_mas_violento_historico": mes_mas_violento,
            "mes_menos_violento_historico": mes_menos_violento
        },
        "predicciones": predicciones,
        "recomendaciones": [
            "Las predicciones se basan en tendencias históricas y deben interpretarse con cautela",
            "Considerar factores externos no incluidos en el modelo",
            "Actualizar predicciones mensualmente con nuevos datos"
        ]
    }

@app.get("/predictivo/escenarios", tags=["🔮 Análisis Predictivo"])
async def escenarios_futuros(
    entidad: Optional[str] = Query(None, description="Filtrar por entidad"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Genera escenarios futuros basados en diferentes supuestos"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df.copy()
    
    if entidad:
        df = df[df['clave_entidad'] == entidad]
    
    if len(df) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron datos para los filtros especificados")
    
    # Calcular estadísticas base
    total_casos = len(df)
    promedio_mensual = total_casos / 12
    
    # Escenarios
    escenarios = {
        "optimista": {
            "descripcion": "Reducción del 20% respecto a la tendencia actual",
            "casos_anuales_estimados": round(promedio_mensual * 12 * 0.8),
            "tasa_reduccion": "20%"
        },
        "realista": {
            "descripcion": "Mantenimiento de la tendencia actual",
            "casos_anuales_estimados": round(promedio_mensual * 12),
            "tasa_reduccion": "0%"
        },
        "pesimista": {
            "descripcion": "Incremento del 30% respecto a la tendencia actual",
            "casos_anuales_estimados": round(promedio_mensual * 12 * 1.3),
            "tasa_incremento": "30%"
        }
    }
    
    # Análisis de factores de riesgo
    factores_riesgo = df.groupby('causa_def_cat').size().sort_values(ascending=False)
    
    # Identificar principales factores
    factores_principales = []
    for causa, casos in factores_riesgo.head(5).items():
        factores_principales.append({
            "factor": causa,
            "casos": int(casos),
            "porcentaje": round(casos / total_casos * 100, 1)
        })
    
    return {
        "contexto": {
            "entidad": df['nom_ent'].iloc[0] if entidad else "Nacional",
            "casos_actuales": total_casos,
            "promedio_mensual": round(promedio_mensual, 1)
        },
        "escenarios": escenarios,
        "factores_riesgo_principales": factores_principales,
        "recomendaciones_estrategicas": [
            "Focalizar esfuerzos en las causas más frecuentes",
            "Monitorear mensualmente los indicadores",
            "Implementar medidas preventivas basadas en los patrones identificados"
        ]
    }

# ================================
# ENDPOINTS DE EXPORTACIÓN
# ================================

@app.get("/exportar/datos", tags=["📤 Exportación"])
async def exportar_datos(
    formato: str = Query("json", regex="^(json|csv)$", description="Formato de exportación"),
    filtros: Optional[str] = Query(None, description="Filtros en formato JSON"),
    entidad: Optional[str] = Query(None, description="Filtrar por entidad"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Exporta datos con filtros personalizados"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df.copy()
    
    # Aplicar filtros
    if entidad:
        df = df[df['clave_entidad'] == entidad]
    
    if filtros:
        try:
            filtros_dict = json.loads(filtros)
            # Aplicar filtros dinámicamente (implementación básica)
            for campo, valores in filtros_dict.items():
                if campo in df.columns and isinstance(valores, list):
                    df = df[df[campo].isin(valores)]
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Formato de filtros inválido")
    
    # Seleccionar columnas principales
    columnas_export = [
        'fecha_ocurr', 'nom_ent', 'nom_mun', 'nom_loc', 'sexo_cat', 
        'edad_cat', 'edad_anos', 'causa_def_cat', 'lugar_ocur_cat', 
        'area_ur', 'lat_decimal', 'lon_decimal'
    ]
    
    df_export = df[columnas_export].copy()
    
    if formato == "csv":
        # Generar CSV en memoria
        csv_data = df_export.to_csv(index=False)
        return JSONResponse(
            content={"message": "CSV generado exitosamente", "data": csv_data},
            media_type="application/json"
        )
    else:
        # JSON
        return {
            "metadata": {
                "total_registros": len(df_export),
                "columnas_incluidas": columnas_export,
                "filtros_aplicados": filtros or "ninguno",
                "fecha_exportacion": datetime.now().isoformat()
            },
            "datos": df_export.to_dict('records')
        }

@app.get("/exportar/reporte", tags=["📤 Exportación"])
async def generar_reporte(
    tipo: str = Query("completo", regex="^(completo|ejecutivo|tecnico)$", description="Tipo de reporte"),
    entidad: Optional[str] = Query(None, description="Filtrar por entidad"),
    data: HomicidiosDataProcessor = Depends(get_data)
):
    """Genera reportes ejecutivos o técnicos"""
    if data.df is None:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")
    
    df = data.df.copy()
    
    if entidad:
        df = df[df['clave_entidad'] == entidad]
    
    if tipo == "ejecutivo":
        # Reporte ejecutivo - solo métricas clave
        total_casos = len(df)
        entidades_afectadas = df['clave_entidad'].nunique()
        tasa_promedio = (total_casos / df['pob_total'].max() * 100000) if df['pob_total'].max() > 0 else 0
        
        return {
            "tipo_reporte": "Ejecutivo",
            "resumen_ejecutivo": {
                "situacion_general": "🔴 Crítica" if tasa_promedio > 50 else "🟡 Moderada" if tasa_promedio > 20 else "🟢 Controlada",
                "total_casos": total_casos,
                "entidades_afectadas": entidades_afectadas,
                "tasa_nacional_aproximada": round(tasa_promedio, 2),
                "recomendacion_principal": "Implementar medidas de seguridad inmediatas" if tasa_promedio > 50 else "Mantener vigilancia y prevención"
            }
        }
    
    elif tipo == "tecnico":
        # Reporte técnico - análisis detallado
        return {
            "tipo_reporte": "Técnico",
            "analisis_detallado": {
                "distribucion_estadistica": {
                    "media_edad": round(df['edad_anos'].mean(), 1) if df['edad_anos'].notna().any() else None,
                    "mediana_edad": round(df['edad_anos'].median(), 1) if df['edad_anos'].notna().any() else None,
                    "desviacion_estandar_edad": round(df['edad_anos'].std(), 1) if df['edad_anos'].notna().any() else None
                },
                "correlaciones": {
                    "edad_vs_sexo": df.groupby('sexo_cat')['edad_anos'].mean().to_dict() if df['edad_anos'].notna().any() else {},
                    "area_vs_causa": pd.crosstab(df['area_ur'], df['causa_def_cat']).to_dict()
                }
            }
        }
    
    else:
        # Reporte completo
        return {
            "tipo_reporte": "Completo",
            "contenido": {
                "estadisticas_generales": await estadisticas_generales(data),
                "analisis_demografico": await perfil_demografico(entidad=entidad, data=data),
                "indices_violencia": await indices_violencia(data=data),
                "tendencias_temporales": await analisis_tendencias(data=data)
            }
        }

# ================================
# ENDPOINTS DE MANUAL Y AYUDA
# ================================

@app.get("/manual", tags=["📚 Manual de Usuario"])
async def manual_usuario():
    """Manual completo de usuario para la API"""
    return {
        "titulo": "📚 Manual de Usuario - API de Análisis de Homicidios México 2024",
        "version": "1.0.0",
        "fecha_actualizacion": "2024-12-15",
        
        "introduccion": {
            "proposito": "Esta API proporciona acceso completo a los datos de homicidios de México 2024 con análisis avanzados para diferentes tipos de usuarios.",
            "audiencia_objetivo": [
                "Analistas de Seguridad Pública",
                "Investigadores Académicos", 
                "Empresas de Seguros",
                "Funcionarios de Gobierno",
                "Medios de Comunicación",
                "Organizaciones de Derechos Humanos"
            ]
        },
        
        "primeros_pasos": {
            "instalacion": "pip install fastapi pandas numpy uvicorn",
            "ejecucion": "uvicorn app:app --host 0.0.0.0 --port 8000 --reload",
            "documentacion_interactiva": "http://localhost:8000/docs",
            "primer_endpoint": "http://localhost:8000/estadisticas/general"
        },
        
        "endpoints_principales": {
            "estadisticas_generales": {
                "url": "/estadisticas/general",
                "descripcion": "Obtiene estadísticas generales del dataset",
                "uso": "curl http://localhost:8000/estadisticas/general",
                "parametros": "Ninguno",
                "respuesta": "Estadísticas básicas, distribuciones y casos recientes"
            },
            
            "analisis_demografico": {
                "url": "/demografico/perfil",
                "descripcion": "Análisis demográfico detallado por región",
                "uso": "curl http://localhost:8000/demografico/perfil?entidad=01",
                "parametros": "entidad (opcional), municipio (opcional)",
                "respuesta": "Perfiles por sexo, edad, etnia y estadísticas de edad"
            },
            
            "indices_violencia": {
                "url": "/indices/violencia",
                "descripcion": "Calcula índices de violencia por región",
                "uso": "curl http://localhost:8000/indices/violencia?tipo=entidad&limite=5",
                "parametros": "tipo (entidad|municipio), limite (1-50)",
                "respuesta": "Rankings de violencia con índices y percentiles"
            },
            
            "tendencias_temporales": {
                "url": "/temporal/tendencias",
                "descripcion": "Análisis de tendencias por período",
                "uso": "curl http://localhost:8000/temporal/tendencias?periodo=mensual",
                "parametros": "periodo (mensual|diario|semanal), entidad (opcional)",
                "respuesta": "Series temporales con análisis de tendencias"
            },
            
            "mapa_calor": {
                "url": "/geografico/mapa-calor",
                "descripcion": "Datos para mapas de calor geográfico",
                "uso": "curl http://localhost:8000/geografico/mapa-calor?tipo=entidad&metrica=tasa",
                "parametros": "tipo (entidad|municipio), metrica (tasa|total|casos_por_sexo)",
                "respuesta": "Coordenadas y valores para visualización geográfica"
            }
        },
        
        "ejemplos_practicos": {
            "analista_seguridad": {
                "objetivo": "Identificar zonas de alto riesgo",
                "pasos": [
                    "1. GET /indices/violencia?tipo=municipio&limite=20",
                    "2. GET /geografico/zonas-calientes?limite=15", 
                    "3. GET /temporal/patrones"
                ],
                "interpretacion": "Los municipios con mayor índice de violencia requieren atención prioritaria"
            },
            
            "investigador_academico": {
                "objetivo": "Estudiar patrones demográficos",
                "pasos": [
                    "1. GET /demografico/perfil",
                    "2. GET /comparativo/entidades?entidades=01,02,03&metrica=tasa",
                    "3. GET /temporal/tendencias?periodo=mensual"
                ],
                "interpretacion": "Comparar patrones entre entidades federativas para investigación social"
            },
            
            "empresa_seguros": {
                "objetivo": "Evaluar riesgos por región",
                "pasos": [
                    "1. GET /indices/violencia?tipo=entidad",
                    "2. GET /geografico/mapa-calor?tipo=entidad&metrica=tasa",
                    "3. GET /exportar/reporte?tipo=ejecutivo"
                ],
                "interpretacion": "Usar índices para calcular primas de seguros diferenciadas por región"
            }
        },
        
        "parametros_comunes": {
            "entidades": "Claves de entidades federativas (01=Aguascalientes, 02=Baja California, etc.)",
            "municipios": "Claves de municipios dentro de las entidades",
            "fechas": "Formato YYYY-MM-DD (2024-01-01 a 2024-12-31)",
            "periodos": "mensual, diario, semanal para análisis temporal",
            "metricas": "tasa (por 100k hab), total (volumen absoluto), indice (compuesto)"
        },
        
        "interpretacion_resultados": {
            "indices_violencia": {
                "escala": "0-100+ (mayor = más violento)",
                "clasificacion": {
                    "80+": "🔴 CRÍTICO - Acción inmediata requerida",
                    "60-79": "🟠 ALTO - Medidas de seguridad intensivas", 
                    "40-59": "🟡 MEDIO - Vigilancia reforzada",
                    "20-39": "🟢 BAJO - Prevención normal",
                    "0-19": "✅ MUY BAJO - Situación controlada"
                }
            },
            "tasas": "Casos por cada 100,000 habitantes (permite comparación entre regiones)",
            "percentiles": "Posición relativa respecto al total nacional (0-100)"
        },
        
        "limitaciones": {
            "datos": "Solo año 2024, algunos registros pueden tener datos faltantes",
            "precision": "Predicciones son estimativas basadas en tendencias históricas",
            "actualizacion": "Datos no se actualizan en tiempo real",
            "interpretacion": "Los índices son herramientas de apoyo, no diagnósticos definitivos"
        },
        
        "casos_uso_comerciales": {
            "seguros": "Cálculo de primas diferenciadas, evaluación de riesgos",
            "inmobiliaria": "Análisis de plusvalía y riesgos por ubicación",
            "turismo": "Recomendaciones de seguridad por destino",
            "gobierno": "Asignación de recursos y políticas públicas",
            "academia": "Investigación en criminología y sociología"
        },
        
        "soporte": {
            "documentacion_completa": "http://localhost:8000/docs",
            "formato_openapi": "http://localhost:8000/openapi.json",
            "contacto_tecnico": "api-support@datasciencemexico.com",
            "licencias": "Licencias comerciales disponibles"
        }
    }

# ================================
# EVENTOS DE INICIO Y CONFIGURACIÓN
# ================================

@app.on_event("startup")
async def startup_event():
    """Eventos al iniciar la aplicación"""
    print("🚀 Iniciando API de Análisis de Homicidios México 2024...")
    
    # Cargar datos
    if processor.cargar_datos():
        print("✅ Datos cargados exitosamente")
        
        # Estadísticas básicas
        if processor.df is not None:
            print(f"📊 Total de registros: {len(processor.df):,}")
            print(f"🗺️ Entidades federativas: {processor.df['clave_entidad'].nunique()}")
            print(f"🏘️ Municipios: {processor.df['clave_municipio'].nunique()}")
            print(f"📅 Período: {processor.df['fecha_ocurr'].min()} a {processor.df['fecha_ocurr'].max()}")
            
        print("🌐 Documentación disponible en:")
        print("   - Swagger UI: http://localhost:8000/docs")
        print("   - ReDoc: http://localhost:8000/redoc")
        print("   - Manual: http://localhost:8000/manual")
        
    else:
        print("❌ Error cargando datos. Verificar archivo CSV.")

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos al cerrar la aplicación"""
    print("🔄 Cerrando API de Análisis de Homicidios...")

# ================================
# MANEJO DE ERRORES GLOBAL
# ================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejador personalizado de excepciones HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "tipo": "HTTPException",
                "codigo": exc.status_code,
                "mensaje": exc.detail,
                "timestamp": datetime.now().isoformat(),
                "endpoint": str(request.url)
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Manejador general de excepciones"""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "tipo": "InternalServerError", 
                "codigo": 500,
                "mensaje": "Error interno del servidor",
                "timestamp": datetime.now().isoformat(),
                "endpoint": str(request.url)
            }
        }
    )

# ================================
# EJECUCIÓN DIRECTA
# ================================

if __name__ == "__main__":
    import uvicorn
    
    print("🩸 API de Análisis de Homicidios México 2024")
    print("=" * 50)
    print("📋 Para usar esta API:")
    print("1. Instalar dependencias: pip install fastapi pandas numpy uvicorn")
    print("2. Ejecutar: uvicorn app:app --host 0.0.0.0 --port 8000 --reload")
    print("3. Abrir navegador en: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)