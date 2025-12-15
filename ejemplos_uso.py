#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplos de Uso - API de Análisis de Homicidios México 2024
==========================================================

Este archivo contiene ejemplos prácticos de cómo usar la API desde Python
para diferentes casos de uso comerciales y de investigación.

Casos de Uso Incluidos:
- Analista de Seguridad Pública
- Investigador Académico  
- Empresa de Seguros
- Funcionario de Gobierno
- Periodista de Datos

Autor: DataScience Mexico
Fecha: 2024
"""

import requests
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración base de la API
API_BASE_URL = "http://localhost:8000"

class HomicidiosAPIClient:
    """Cliente Python para interactuar con la API de Homicidios"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        
    def obtener_estadisticas_generales(self):
        """Obtiene estadísticas generales del dataset"""
        response = requests.get(f"{self.base_url}/estadisticas/general")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def obtener_analisis_demografico(self, entidad: str = None):
        """Obtiene análisis demográfico"""
        params = {}
        if entidad:
            params['entidad'] = entidad
        
        response = requests.get(f"{self.base_url}/demografico/perfil", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def obtener_indices_violencia(self, tipo: str = "entidad", limite: int = 10):
        """Obtiene índices de violencia"""
        params = {'tipo': tipo, 'limite': limite}
        response = requests.get(f"{self.base_url}/indices/violencia", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def obtener_mapa_calor(self, tipo: str = "entidad", metrica: str = "tasa"):
        """Obtiene datos para mapa de calor geográfico"""
        params = {'tipo': tipo, 'metrica': metrica}
        response = requests.get(f"{self.base_url}/geografico/mapa-calor", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def obtener_tendencias_temporales(self, periodo: str = "mensual", entidad: str = None):
        """Obtiene análisis de tendencias temporales"""
        params = {'periodo': periodo}
        if entidad:
            params['entidad'] = entidad
        
        response = requests.get(f"{self.base_url}/temporal/tendencias", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def comparar_entidades(self, entidades: list, metrica: str = "tasa"):
        """Compara estadísticas entre entidades"""
        params = {'entidades': ','.join(entidades), 'metrica': metrica}
        response = requests.get(f"{self.base_url}/comparativo/entidades", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def exportar_datos(self, formato: str = "json", entidad: str = None):
        """Exporta datos en formato especificado"""
        params = {'formato': formato}
        if entidad:
            params['entidad'] = entidad
        
        response = requests.get(f"{self.base_url}/exportar/datos", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None


def ejemplo_analista_seguridad():
    """
    CASO DE USO: Analista de Seguridad Pública
    Objetivo: Identificar zonas de alto riesgo y patrones de violencia
    """
    print("🔍 EJEMPLO: Analista de Seguridad Pública")
    print("=" * 50)
    
    client = HomicidiosAPIClient()
    
    # 1. Obtener entidades más violentas
    print("1. 📊 Identificando entidades más violentas...")
    indices_entidades = client.obtener_indices_violencia(tipo="entidad", limite=10)
    if indices_entidades:
        print("Top 5 entidades más violentas:")
        for i, entidad in enumerate(indices_entidades['top_regiones'][:5], 1):
            print(f"   {i}. {entidad['nombre']}: Índice {entidad['indice_violencia']} ({entidad['categoria_riesgo']})")
    
    # 2. Analizar municipios críticos
    print("\n2. 🏘️ Analizando municipios críticos...")
    indices_municipios = client.obtener_indices_violencia(tipo="municipio", limite=15)
    if indices_municipios:
        municipios_criticos = [m for m in indices_municipios['top_regiones'] if 'CRÍTICO' in m['categoria_riesgo']]
        print(f"Municipios en situación crítica: {len(municipios_criticos)}")
        for municipio in municipios_criticos[:3]:
            print(f"   - {municipio['nombre']}, {municipio['entidad']}: {municipio['total_casos']} casos")
    
    # 3. Analizar tendencias temporales
    print("\n3. 📅 Analizando tendencias temporales...")
    tendencias = client.obtener_tendencias_temporales(periodo="mensual")
    if tendencias:
        print(f"   - Tendencia general: {tendencias.get('tendencia_general', 'N/A')}")
        if 'mes_mas_violento' in tendencias:
            mes = tendencias['mes_mas_violento']['mes']
            casos = tendencias['mes_mas_violento']['casos']
            print(f"   - Mes más violento: {mes} ({casos} casos)")
    
    # 4. Generar reporte ejecutivo
    print("\n4. 📋 Generando reporte ejecutivo...")
    reporte = client.exportar_datos(formato="json", entidad="02")  # Baja California como ejemplo
    if reporte:
        print(f"   - Datos exportados: {len(reporte.get('datos', []))} registros")
    
    print("\n✅ Análisis completado. Recomendaciones:")
    print("   - Focalizar recursos en municipios con índice > 80")
    print("   - Implementar medidas preventivas en meses de mayor incidencia")
    print("   - Monitorear mensualmente los indicadores de violencia")


def ejemplo_investigador_academico():
    """
    CASO DE USO: Investigador Académico
    Objetivo: Estudiar patrones demográficos y sociales
    """
    print("\n\n🎓 EJEMPLO: Investigador Académico")
    print("=" * 50)
    
    client = HomicidiosAPIClient()
    
    # 1. Análisis demográfico general
    print("1. 👥 Análisis demográfico general...")
    demo_general = client.obtener_analisis_demografico()
    if demo_general:
        analisis_sexo = demo_general.get('analisis_sexo', {})
        print("   Distribución por sexo:")
        for sexo, datos in analisis_sexo.items():
            if sexo != 'No especificado':
                print(f"     - {sexo}: {datos['total_casos']} casos ({datos['porcentaje']}%)")
    
    # 2. Comparación entre entidades
    print("\n2. ⚖️ Comparación entre entidades (Aguascalientes vs Baja California)...")
    comparacion = client.comparar_entidades(["01", "02"], metrica="tasa")
    if comparacion:
        ranking = comparacion.get('ranking', [])
        print("   Ranking por tasa de homicidios:")
        for item in ranking:
            print(f"     - {item['nombre']}: {item['tasa_por_100k']} por 100k hab")
    
    # 3. Análisis temporal para patrones estacionales
    print("\n3. 📊 Patrones estacionales...")
    tendencias = client.obtener_tendencias_temporales(periodo="mensual")
    if tendencias:
        datos_mensuales = tendencias.get('datos', [])
        if datos_mensuales:
            # Crear gráfico simple
            meses = [d['mes'] for d in datos_mensuales]
            casos = [d['total_casos'] for d in datos_mensuales]
            
            print("   Distribución mensual:")
            meses_nombres = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun',
                           7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'}
            for mes, caso in zip(meses, casos):
                if caso > 0:
                    print(f"     - {meses_nombres.get(mes, mes)}: {caso} casos")
    
    # 4. Datos para análisis estadístico avanzado
    print("\n4. 📈 Preparando datos para análisis estadístico...")
    datos_export = client.exportar_datos(formato="json")
    if datos_export:
        metadata = datos_export.get('metadata', {})
        print(f"   - Total registros disponibles: {metadata.get('total_registros', 'N/A')}")
        print(f"   - Columnas: {len(metadata.get('columnas_incluidas', []))}")
    
    print("\n✅ Investigación completada. Datos preparados para:")
    print("   - Análisis estadístico avanzado")
    print("   - Modelado predictivo")
    print("   - Publicación académica")


def ejemplo_empresa_seguros():
    """
    CASO DE USO: Empresa de Seguros
    Objetivo: Evaluar riesgos para cálculo de primas
    """
    print("\n\n🏢 EJEMPLO: Empresa de Seguros")
    print("=" * 50)
    
    client = HomicidiosAPIClient()
    
    # 1. Análisis de riesgo por entidad
    print("1. 🗺️ Evaluación de riesgo por entidad...")
    mapa_calor = client.obtener_mapa_calor(tipo="entidad", metrica="tasa")
    if mapa_calor:
        datos = mapa_calor.get('datos', [])
        print("   Clasificación de riesgo para cálculo de primas:")
        
        # Clasificar entidades por riesgo
        alto_riesgo = [d for d in datos if d['valor'] > 50]
        medio_riesgo = [d for d in datos if 20 <= d['valor'] <= 50]
        bajo_riesgo = [d for d in datos if d['valor'] < 20]
        
        print(f"     🔴 Alto Riesgo (>50/100k): {len(alto_riesgo)} entidades")
        print(f"     🟡 Medio Riesgo (20-50/100k): {len(medio_riesgo)} entidades") 
        print(f"     🟢 Bajo Riesgo (<20/100k): {len(bajo_riesgo)} entidades")
        
        if alto_riesgo:
            print("     Entidades de alto riesgo:")
            for entidad in alto_riesgo[:3]:
                print(f"       - {entidad['nombre']}: {entidad['valor']} por 100k hab")
    
    # 2. Factores de riesgo específicos
    print("\n2. ⚠️ Análisis de factores de riesgo...")
    stats_generales = client.obtener_estadisticas_generales()
    if stats_generales:
        distribuciones = stats_generales.get('distribuciones', {})
        
        # Causas más frecuentes (impacto en seguros)
        causas = distribuciones.get('por_causa', {})
        print("   Causas principales de homicidio:")
        for causa, casos in list(causas.items())[:5]:
            print(f"     - {causa}: {casos} casos")
    
    # 3. Datos para modelado de riesgo
    print("\n3. 📊 Datos para modelado de riesgo...")
    indices_municipios = client.obtener_indices_violencia(tipo="municipio", limite=50)
    if indices_municipios:
        datos_modelo = indices_municipios.get('top_regiones', [])
        print(f"   - {len(datos_modelo)} municipios analizados para modelado")
        print("   - Variables disponibles: índice, tasa, total de casos, población")
    
    # 4. Recomendaciones para productos de seguros
    print("\n4. 💡 Recomendaciones para productos de seguros:")
    print("   - Implementar primas diferenciadas por entidad federativa")
    print("   - Excluir o incrementar primas en municipios de alto riesgo")
    print("   - Ofrecer descuentos en zonas de bajo riesgo")
    print("   - Desarrollar productos específicos para áreas críticas")
    
    print("\n✅ Análisis de riesgo completado.")
    print("   Datos listos para actuar en:")
    print("   - Cálculo de primas")
    print("   - Evaluación de cobertura")
    print("   - Desarrollo de productos")


def ejemplo_funcionario_gobierno():
    """
    CASO DE USO: Funcionario de Gobierno
    Objetivo: Información para toma de decisiones de política pública
    """
    print("\n\n🏛️ EJEMPLO: Funcionario de Gobierno")
    print("=" * 50)
    
    client = HomicidiosAPIClient()
    
    # 1. Reporte ejecutivo para toma de decisiones
    print("1. 📋 Generando reporte ejecutivo...")
    
    # Obtener panorama nacional
    stats_nacional = client.obtener_estadisticas_generales()
    if stats_nacional:
        resumen = stats_nacional.get('resumen', {})
        print(f"   - Total de homicidios: {resumen.get('total_casos', 'N/A'):,}")
        print(f"   - Entidades afectadas: {resumen.get('entidades_afectadas', 'N/A')}")
        print(f"   - Municipios afectados: {resumen.get('municipios_afectados', 'N/A')}")
    
    # 2. Identificar prioridades de seguridad
    print("\n2. 🎯 Identificando prioridades de seguridad...")
    indices = client.obtener_indices_violencia(tipo="entidad", limite=5)
    if indices:
        top_5 = indices.get('top_regiones', [])
        print("   Entidades que requieren atención prioritaria:")
        for i, entidad in enumerate(top_5, 1):
            riesgo = entidad.get('categoria_riesgo', 'N/A')
            print(f"     {i}. {entidad['nombre']}: {riesgo}")
    
    # 3. Análisis de tendencias para planificación
    print("\n3. 📈 Análisis de tendencias para planificación presupuestal...")
    tendencias = client.obtener_tendencias_temporales(periodo="mensual")
    if tendencias:
        variabilidad = tendencias.get('variabilidad', {})
        print(f"   - Promedio mensual: {variabilidad.get('promedio_mensual', 'N/A')} casos")
        print(f"   - Variabilidad: {variabilidad.get('desviacion_estandar', 'N/A')}")
        
        mes_critico = tendencias.get('mes_mas_violento', {})
        if mes_critico:
            print(f"   - Mes crítico: {mes_critico.get('mes', 'N/A')} ({mes_critico.get('casos', 'N/A')} casos)")
    
    # 4. Comparación regional para estrategias diferenciadas
    print("\n4. 🗺️ Comparación regional...")
    comparacion = client.comparar_entidades(["01", "02"], metrica="indice")
    if comparacion:
        stats = comparacion.get('estadisticas_generales', {})
        print(f"   - Rango de índices: {stats.get('minimo', 'N/A')} - {stats.get('maximo', 'N/A')}")
        print(f"   - Promedio nacional: {stats.get('promedio', 'N/A')}")
    
    print("\n5. 📊 Recomendaciones de política pública:")
    print("   - Asignar recursos adicionales a entidades de alto riesgo")
    print("   - Implementar programas preventivos en meses críticos")
    print("   - Desarrollar estrategias diferenciadas por región")
    print("   - Establecer monitoreo continuo de indicadores")
    
    print("\n✅ Análisis para política pública completado.")
    print("   Información disponible para:")
    print("   - Asignación presupuestal")
    print("   - Estrategias de seguridad")
    print("   - Programas preventivos")


def ejemplo_periodista_datos():
    """
    CASO DE USO: Periodista de Datos
    Objetivo: Obtener datos para reportajes y análisis periodísticos
    """
    print("\n\n📺 EJEMPLO: Periodista de Datos")
    print("=" * 50)
    
    client = HomicidiosAPIClient()
    
    # 1. Obtener datos para reportaje
    print("1. 📰 Obteniendo datos para reportaje...")
    
    stats = client.obtener_estadisticas_generales()
    if stats:
        casos_recientes = stats.get('casos_recientes', [])
        print("   Casos más recientes para contextualizar:")
        for caso in casos_recientes[:3]:
            fecha = caso.get('fecha_ocurr', 'N/A')
            lugar = f"{caso.get('nom_mun', 'N/A')}, {caso.get('nom_ent', 'N/A')}"
            print(f"     - {fecha}: {lugar}")
    
    # 2. Identificar historias interesantes
    print("\n2. 🔍 Identificando historias potenciales...")
    
    # Comparar entidades para encontrar contrastes
    comparacion = client.comparar_entidades(["01", "02"], metrica="tasa")
    if comparacion:
        ranking = comparacion.get('ranking', [])
        if len(ranking) >= 2:
            entidad1 = ranking[0]
            entidad2 = ranking[1]
            
            print("   Historia potencial: Contraste entre entidades")
            print(f"     - {entidad1['nombre']}: {entidad1['tasa_por_100k']} por 100k hab")
            print(f"     - {entidad2['nombre']}: {entidad2['tasa_por_100k']} por 100k hab")
            diferencia = abs(entidad1['tasa_por_100k'] - entidad2['tasa_por_100k'])
            print(f"     - Diferencia: {diferencia:.1f} por 100k hab")
    
    # 3. Datos para visualizaciones
    print("\n3. 📊 Datos para visualizaciones...")
    
    # Mapa de calor para gráfico geográfico
    mapa = client.obtener_mapa_calor(tipo="entidad", metrica="tasa")
    if mapa:
        datos_geograficos = mapa.get('datos', [])
        print(f"   - {len(datos_geograficos)} entidades para mapa de calor")
        
        # Top y bottom para gráficos de barras
        datos_ordenados = sorted(datos_geograficos, key=lambda x: x['valor'], reverse=True)
        print("   Top 3 entidades más violentas:")
        for entidad in datos_ordenados[:3]:
            print(f"     - {entidad['nombre']}: {entidad['valor']} por 100k hab")
        
        print("   Top 3 entidades más seguras:")
        for entidad in datos_ordenados[-3:]:
            print(f"     - {entidad['nombre']}: {entidad['valor']} por 100k hab")
    
    # 4. Exportar datos para análisis independiente
    print("\n4. 📁 Exportando datos para análisis independiente...")
    datos_export = client.exportar_datos(formato="json")
    if datos_export:
        metadata = datos_export.get('metadata', {})
        print(f"   - Total registros: {metadata.get('total_registros', 'N/A'):,}")
        print(f"   - Columnas disponibles: {len(metadata.get('columnas_incluidas', []))}")
        
        # Guardar en archivo para análisis posterior
        with open('datos_homicidios_periodismo.json', 'w', encoding='utf-8') as f:
            json.dump(datos_export, f, ensure_ascii=False, indent=2)
        print("   - Datos guardados en: datos_homicidios_periodismo.json")
    
    print("\n5. 📝 Ideas para artículos:")
    print("   - 'Los estados con mayor violencia en México: un análisis por datos'")
    print("   - 'Patrones geográficos de la violencia en 2024'")
    print("   - '¿Qué nos dicen los datos sobre la violencia en México?'")
    
    print("\n✅ Datos periodísticos preparados.")
    print("   Material disponible para:")
    print("   - Artículos informativos")
    print("   - Análisis de tendencias")
    print("   - Comparaciones regionales")


def ejemplo_visualizacion_datos():
    """
    Ejemplo de cómo crear visualizaciones con los datos de la API
    """
    print("\n\n📊 EJEMPLO: Visualización de Datos")
    print("=" * 50)
    
    client = HomicidiosAPIClient()
    
    # Obtener datos para visualización
    print("1. 📈 Obteniendo datos para visualización...")
    
    # Datos por entidad
    mapa_entidades = client.obtener_mapa_calor(tipo="entidad", metrica="tasa")
    if mapa_entidades:
        datos = mapa_entidades.get('datos', [])
        
        # Crear DataFrame para visualización
        df_viz = pd.DataFrame(datos)
        
        if not df_viz.empty:
            print(f"   - Datos preparados: {len(df_viz)} entidades")
            
            # Ejemplo de gráfico (comentado para evitar errores si no hay matplotlib)
            print("   - Ejemplo de visualización (requiere matplotlib):")
            print("     plt.bar(df_viz['nombre'][:10], df_viz['valor'][:10])")
            print("     plt.title('Top 10 Entidades por Tasa de Homicidios')")
            print("     plt.xticks(rotation=45)")
            print("     plt.show()")
    
    print("\n✅ Datos preparados para visualización.")


def main():
    """Función principal que ejecuta todos los ejemplos"""
    print("🩸 EJEMPLOS DE USO - API DE ANÁLISIS DE HOMICIDIOS MÉXICO 2024")
    print("=" * 70)
    print("Este script demuestra diferentes casos de uso comerciales y académicos")
    print("de la API de Homicidios México 2024.")
    print("=" * 70)
    
    # Verificar que la API esté corriendo
    try:
        client = HomicidiosAPIClient()
        test_response = client.obtener_estadisticas_generales()
        if not test_response:
            print("❌ ERROR: La API no está corriendo en", API_BASE_URL)
            print("💡 Para iniciar la API, ejecuta: uvicorn app:app --reload")
            return
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar con la API en", API_BASE_URL)
        print("💡 Para iniciar la API, ejecuta: uvicorn app:app --reload")
        return
    
    # Ejecutar ejemplos
    try:
        ejemplo_analista_seguridad()
        ejemplo_investigador_academico()
        ejemplo_empresa_seguros()
        ejemplo_funcionario_gobierno()
        ejemplo_periodista_datos()
        ejemplo_visualizacion_datos()
        
        print("\n\n🎉 TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("=" * 70)
        print("💡 Para más información, consulta:")
        print("   - README.md: Guía completa de instalación y uso")
        print("   - Manual API: http://localhost:8000/manual")
        print("   - Documentación: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error ejecutando ejemplos: {str(e)}")
        print("💡 Verificar que la API esté corriendo y accesible")


if __name__ == "__main__":
    main()