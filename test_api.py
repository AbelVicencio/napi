#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Prueba - API de Análisis de Homicidios México 2024
===========================================================

Este script verifica que todos los componentes de la API funcionen correctamente.
Ejecuta pruebas básicas de todos los endpoints principales.

Uso: python test_api.py
"""

import requests
import json
import time
from datetime import datetime

# Configuración
API_BASE_URL = "http://localhost:8000"
TIMEOUT = 10

class APITester:
    """Clase para probar la funcionalidad de la API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.resultados = []
    
    def log_resultado(self, test_name: str, status: str, details: str = ""):
        """Registra el resultado de una prueba"""
        emoji = "✅" if status == "PASS" else "❌"
        resultado = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.resultados.append(resultado)
        print(f"{emoji} {test_name}: {status}")
        if details:
            print(f"   📝 {details}")
    
    def test_conexion(self):
        """Prueba la conexión básica con la API"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                self.log_resultado("Conexión API", "PASS", f"API activa: {data.get('mensaje', 'N/A')}")
                return True
            else:
                self.log_resultado("Conexión API", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_resultado("Conexión API", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_endpoint_estadisticas(self):
        """Prueba el endpoint de estadísticas generales"""
        try:
            response = requests.get(f"{self.base_url}/estadisticas/general", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                resumen = data.get('resumen', {})
                total = resumen.get('total_casos', 0)
                self.log_resultado("Estadísticas Generales", "PASS", f"{total} registros disponibles")
                return data
            else:
                self.log_resultado("Estadísticas Generales", "FAIL", f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_resultado("Estadísticas Generales", "FAIL", f"Error: {str(e)}")
            return None
    
    def test_endpoint_entidades(self):
        """Prueba el endpoint de entidades"""
        try:
            response = requests.get(f"{self.base_url}/entidades/lista", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                cantidad = len(data)
                self.log_resultado("Lista de Entidades", "PASS", f"{cantidad} entidades encontradas")
                return data
            else:
                self.log_resultado("Lista de Entidades", "FAIL", f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_resultado("Lista de Entidades", "FAIL", f"Error: {str(e)}")
            return None
    
    def test_endpoint_demografico(self):
        """Prueba el endpoint de análisis demográfico"""
        try:
            response = requests.get(f"{self.base_url}/demografico/perfil", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                contexto = data.get('contexto', {})
                casos = contexto.get('total_casos_analizados', 0)
                self.log_resultado("Análisis Demográfico", "PASS", f"{casos} casos analizados")
                return data
            else:
                self.log_resultado("Análisis Demográfico", "FAIL", f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_resultado("Análisis Demográfico", "FAIL", f"Error: {str(e)}")
            return None
    
    def test_endpoint_indices(self):
        """Prueba el endpoint de índices de violencia"""
        try:
            response = requests.get(f"{self.base_url}/indices/violencia?tipo=entidad&limite=5", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                regiones = len(data.get('top_regiones', []))
                self.log_resultado("Índices de Violencia", "PASS", f"{regiones} regiones analizadas")
                return data
            else:
                self.log_resultado("Índices de Violencia", "FAIL", f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_resultado("Índices de Violencia", "FAIL", f"Error: {str(e)}")
            return None
    
    def test_endpoint_geografico(self):
        """Prueba el endpoint geográfico"""
        try:
            response = requests.get(f"{self.base_url}/geografico/mapa-calor?tipo=entidad&metrica=tasa", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                datos = len(data.get('datos', []))
                self.log_resultado("Mapa de Calor Geográfico", "PASS", f"{datos} puntos geográficos")
                return data
            else:
                self.log_resultado("Mapa de Calor Geográfico", "FAIL", f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_resultado("Mapa de Calor Geográfico", "FAIL", f"Error: {str(e)}")
            return None
    
    def test_endpoint_temporal(self):
        """Prueba el endpoint temporal"""
        try:
            response = requests.get(f"{self.base_url}/temporal/tendencias?periodo=mensual", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                periodo = data.get('periodo', 'N/A')
                self.log_resultado("Tendencias Temporales", "PASS", f"Análisis {periodo}")
                return data
            else:
                self.log_resultado("Tendencias Temporales", "FAIL", f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_resultado("Tendencias Temporales", "FAIL", f"Error: {str(e)}")
            return None
    
    def test_endpoint_exportacion(self):
        """Prueba el endpoint de exportación"""
        try:
            response = requests.get(f"{self.base_url}/exportar/datos?formato=json&limite=10", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                metadata = data.get('metadata', {})
                registros = metadata.get('total_registros', 0)
                self.log_resultado("Exportación de Datos", "PASS", f"{registros} registros disponibles")
                return data
            else:
                self.log_resultado("Exportación de Datos", "FAIL", f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_resultado("Exportación de Datos", "FAIL", f"Error: {str(e)}")
            return None
    
    def test_endpoint_manual(self):
        """Prueba el endpoint del manual"""
        try:
            response = requests.get(f"{self.base_url}/manual", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                titulo = data.get('titulo', 'N/A')
                self.log_resultado("Manual de Usuario", "PASS", f"Manual disponible: {titulo}")
                return data
            else:
                self.log_resultado("Manual de Usuario", "FAIL", f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_resultado("Manual de Usuario", "FAIL", f"Error: {str(e)}")
            return None
    
    def test_parametros_opcionales(self):
        """Prueba endpoints con parámetros opcionales"""
        try:
            # Probar análisis demográfico por entidad específica
            response = requests.get(f"{self.base_url}/demografico/perfil?entidad=01", timeout=TIMEOUT)
            if response.status_code == 200:
                self.log_resultado("Parámetros Opcionales - Entidad", "PASS", "Filtro por entidad funcionando")
            else:
                self.log_resultado("Parámetros Opcionales - Entidad", "FAIL", f"Status code: {response.status_code}")
            
            # Probar comparación de entidades
            response = requests.get(f"{self.base_url}/comparativo/entidades?entidades=01,02&metrica=tasa", timeout=TIMEOUT)
            if response.status_code == 200:
                self.log_resultado("Parámetros Opcionales - Comparación", "PASS", "Comparación entre entidades funcionando")
            else:
                self.log_resultado("Parámetros Opcionales - Comparación", "FAIL", f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_resultado("Parámetros Opcionales", "FAIL", f"Error: {str(e)}")
    
    def test_manejo_errores(self):
        """Prueba el manejo de errores"""
        try:
            # Probar endpoint con parámetros inválidos
            response = requests.get(f"{self.base_url}/indices/violencia?tipo=invalid&limite=abc", timeout=TIMEOUT)
            if response.status_code in [400, 422]:  # Bad Request o Validation Error
                self.log_resultado("Manejo de Errores", "PASS", "Errores manejados correctamente")
            else:
                self.log_resultado("Manejo de Errores", "FAIL", f"Status inesperado: {response.status_code}")
        except Exception as e:
            self.log_resultado("Manejo de Errores", "FAIL", f"Error: {str(e)}")
    
    def ejecutar_todas_las_pruebas(self):
        """Ejecuta todas las pruebas disponibles"""
        print("🧪 INICIANDO PRUEBAS DE LA API")
        print("=" * 50)
        
        # Prueba de conexión
        if not self.test_conexion():
            print("\n❌ No se puede continuar: API no disponible")
            return False
        
        print("\n📋 Ejecutando pruebas de endpoints...")
        
        # Pruebas de endpoints principales
        self.test_endpoint_estadisticas()
        self.test_endpoint_entidades()
        self.test_endpoint_demografico()
        self.test_endpoint_indices()
        self.test_endpoint_geografico()
        self.test_endpoint_temporal()
        self.test_endpoint_exportacion()
        self.test_endpoint_manual()
        
        print("\n🔧 Ejecutando pruebas de parámetros y errores...")
        
        # Pruebas adicionales
        self.test_parametros_opcionales()
        self.test_manejo_errores()
        
        return True
    
    def generar_reporte(self):
        """Genera un reporte final de las pruebas"""
        print("\n📊 REPORTE DE PRUEBAS")
        print("=" * 50)
        
        total_tests = len(self.resultados)
        passed_tests = len([r for r in self.resultados if r['status'] == 'PASS'])
        failed_tests = total_tests - passed_tests
        
        print(f"✅ Pruebas exitosas: {passed_tests}/{total_tests}")
        print(f"❌ Pruebas fallidas: {failed_tests}/{total_tests}")
        
        if failed_tests > 0:
            print("\n🔍 Pruebas fallidas:")
            for resultado in self.resultados:
                if resultado['status'] == 'FAIL':
                    print(f"   - {resultado['test']}: {resultado['details']}")
        
        # Calcular tiempo total (aproximado)
        tiempo_total = len(self.resultados) * 0.1  # Estimación
        print(f"\n⏱️ Tiempo estimado de ejecución: {tiempo_total:.1f} segundos")
        
        # Guardar reporte en archivo
        with open('test_report.json', 'w', encoding='utf-8') as f:
            json.dump({
                'resumen': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%"
                },
                'detalles': self.resultados,
                'timestamp': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        
        print("📁 Reporte guardado en: test_report.json")
        
        if passed_tests == total_tests:
            print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
            print("   La API está funcionando correctamente.")
        else:
            print(f"\n⚠️ {failed_tests} pruebas fallaron.")
            print("   Revisar configuración y datos.")
        
        return passed_tests == total_tests


def main():
    """Función principal"""
    print("🩸 SCRIPT DE PRUEBA - API DE HOMICIDIOS MÉXICO 2024")
    print("=" * 60)
    print("Este script verifica que todos los componentes de la API funcionen.")
    print("=" * 60)
    
    # Verificar si la API está corriendo
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ La API no responde correctamente")
            print("💡 Asegúrate de que la API esté ejecutándose en:", API_BASE_URL)
            print("   Comando para iniciar: uvicorn app:app --reload")
            return
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar con la API")
        print("💡 Para iniciar la API, ejecuta:")
        print("   1. uvicorn app:app --reload")
        print("   2. O python app.py")
        print(f"   3. La API debería estar disponible en: {API_BASE_URL}")
        return
    
    # Ejecutar pruebas
    tester = APITester(API_BASE_URL)
    
    if tester.ejecutar_todas_las_pruebas():
        tester.generar_reporte()
    else:
        print("\n❌ No se pudieron ejecutar todas las pruebas")
    
    print("\n🔗 Enlaces útiles:")
    print(f"   - API: {API_BASE_URL}")
    print(f"   - Documentación: {API_BASE_URL}/docs")
    print(f"   - Manual: {API_BASE_URL}/manual")


if __name__ == "__main__":
    main()