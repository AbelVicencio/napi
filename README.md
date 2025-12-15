# 📊 API de Inteligencia Delictiva: Homicidios México 2024

Esta API REST proporciona acceso programático, analítico y eficiente a los datos de homicidios en México durante el año 2024. Diseñada para analistas de datos, desarrolladores y científicos de datos, transforma un archivo plano CSV en una base de datos consultable en tiempo real con capacidades de agregación y filtrado.

---

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.8 o superior
- El archivo de datos `Homicidios_2024_clean.csv` en el mismo directorio.

### Instalación
Instala las dependencias necesarias:

```bash
pip install fastapi uvicorn pandas
```

### Ejecución
Levanta el servidor localmente:

```bash
python app.py
```

La API estará disponible en **`http://127.0.0.1:8000`**.

---

## 📚 Documentación Interactiva
Una vez corriendo, abre tu navegador en:
- **Swagger UI (Docs Completos y Pruebas):** `http://127.0.0.1:8000/docs`
- **ReDoc (Lectura alternativa):** `http://127.0.0.1:8000/redoc`

---

## 🛠 Manual de Referencia de la API

### 1. Estado del Servicio
Verifica que la API esté operativa y los datos cargados.

- **Endpoint:** `GET /health`
- **Respuesta Ejemplo:**
  ```json
  {
    "status": "ok",
    "total_records": 32065
  }
  ```

### 2. Análisis y Resúmenes (Dashboards)
Endpoints pre-calculados para llenar tableros de control o obtener insights rápidos sin procesar todo el dataset.

#### 🇲🇽 Resumen Nacional
KPIs generales del país.
- **Endpoint:** `GET /resumen/nacional`
- **Uso:** Obtén el total de homicidios, el estado más violento y la principal causa de muerte.

#### 🏙 Ranking por Entidades
- **Endpoint:** `GET /resumen/entidades`
- **Parámetros:** `top` (opcional, default 32)
- **Ejemplo:** `/resumen/entidades?top=5` (Top 5 estados con más homicidios).

#### 📅 Análisis Temporal
Tendencias en el tiempo para detectar picos de violencia.
- **Endpoint:** `GET /resumen/temporal`
- **Parámetros:** `agrupacion` ("mensual" o "semanal")
- **Ejemplo de Respuesta:**
  ```json
  [
    {"mes_num": 1, "mes_nombre": "Ene", "total": 2450},
    {"mes_num": 2, "mes_nombre": "Feb", "total": 2300}
    ...
  ]
  ```

#### 👥 Perfil Demográfico
Distribución de las víctimas por edad y sexo.
- **Endpoint:** `GET /resumen/demografico`

### 3. Buscador Avanzado (Datos Crudos)
El "motor de consultas" de la API. Permite extraer granularmente expedientes específicos.

- **Endpoint:** `GET /datos/busqueda`
- **Parámetros de Filtro:**
    - `estado`: Nombre de la entidad (ej. "Sinaloa").
    - `municipio`: Nombre del municipio (ej. "Culiacán").
    - `sexo`: "Hombre", "Mujer", o "No especificado".
    - `causa`: Filtro parcial de texto (ej. "Fuego" para armas de fuego).
    - `fecha_inicio` / `fecha_fin`: Rango de fechas (YYYY-MM-DD).
- **Paginación:**
    - `limit`: Cantidad de resultados (max 1000).
    - `offset`: Número de registros a saltar.

### 4. Geoespacial
- **Endpoint:** `GET /geo/mapa`
- **Descripción:** Devuelve una lista ligera de coordenadas (`lat`, `lon`) optimizada para renderizar mapas de calor o clusters en librerías como Leaflet o Google Maps.

---

## 💻 Ejemplos de Uso Real

### Ejemplo 1: Python (Analista de Datos)
Obtener todos los homicidios en "Zacatecas" ocurridos en Marzo.

```python
import requests
import pandas as pd

url = "http://127.0.0.1:8000/datos/busqueda"
params = {
    "estado": "Zacatecas",
    "fecha_inicio": "2024-03-01",
    "fecha_fin": "2024-03-31",
    "limit": 1000
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"Se encontraron {data['total']} registros.")
    
    # Convertir a DataFrame para análisis local
    df = pd.DataFrame(data['data'])
    print(df.head())
else:
    print("Error:", response.text)
```

### Ejemplo 2: cURL (Terminal / Bash)
Verificar el estado de salud de la API.

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/health' \
  -H 'accept: application/json'
```

Buscar homicidios por arma de fuego ("Fuego") en mujeres:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/datos/busqueda?sexo=Mujer&causa=Fuego&limit=5' \
  -H 'accept: application/json'
```

### Ejemplo 3: JavaScript (Frontend / Web App)
Consumir el resumen nacional para un dashboard.

```javascript
async function cargarDashboard() {
    const response = await fetch('http://127.0.0.1:8000/resumen/nacional');
    const data = await response.json();
    
    console.log("Total Homicidios:", data.total_homicidios);
    console.log("Estado más crítico:", data.zona_mas_afectada.estado);
    
    // Aquí actualizarías el DOM de tu página web
    document.getElementById("total-counter").innerText = data.total_homicidios;
}

cargarDashboard();
```

---

## ⚠️ Notas Técnicas

- **Persistencia**: La API carga los datos en memoria al iniciar (`startup`). Si el archivo CSV cambia, debes reiniciar el servidor para ver los cambios.
- **Rendimiento**: Para datasets de este tamaño (~30k registros), `pandas` en memoria es extremadamente rápido. Las respuestas deberían ser menores a 100ms.
- **Seguridad**: Por defecto, CORS está habilitado para todos los orígenes (`*`) para facilitar el desarrollo. En producción, restríngelo a tus dominios.

---
**Desarrollado con ❤️ y Python por tu Asistente de IA.**
