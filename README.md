# GeoEntry Edge API

API edge para el sistema GeoEntry, diseñada para dispositivos IoT y verificación de proximidad geográfica.

## Características

- ✅ Verificación de proximidad a ubicaciones definidas
- ✅ Manejo de eventos de proximidad (ENTER/EXIT)
- ✅ Autenticación por device ID y API key
- ✅ Datos stub para testing sin backend
- ✅ Tolerancia a fallos y funcionamiento offline

## Instalación Local

### Prerrequisitos
- Python 3.8+
- pip

### Configuración
```bash
# Clonar el repositorio
git clone <your-repo-url>
cd geoentry-edge-api

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## Deploy en Render

### Configuración en Render

1. **Conectar tu repositorio de GitHub a Render**

2. **Configurar el servicio web:**
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: `Python 3`

3. **Variables de entorno (opcionales):**
   ```
   FLASK_ENV=production
   PORT=10000
   HOST=0.0.0.0
   ```

### Archivos de configuración para Render

- `Procfile`: Define el comando de inicio con gunicorn
- `build.sh`: Script de construcción que instala dependencias e inicializa la DB
- `config.py`: Configuración de entorno (desarrollo/producción)

## API Endpoints

### Health Check
```
GET /
```

### Obtener Ubicaciones
```
GET /api/v1/locations
Headers:
  X-Device-ID: smart-band-001
  X-API-Key: test-api-key-123
```

### Verificar Proximidad
```
POST /api/v1/locations/proximity-check
Headers:
  X-Device-ID: smart-band-001
  X-API-Key: test-api-key-123
  Content-Type: application/json

Body:
{
  "latitude": -12.12345,
  "longitude": -77.54321
}
```

### Obtener Eventos de Proximidad
```
GET /api/v1/proximity-events
Headers:
  X-Device-ID: smart-band-001
  X-API-Key: test-api-key-123

Query Parameters:
  limit: 50 (opcional)
```

### Obtener Evento Específico
```
GET /api/v1/proximity-events/{event_id}
Headers:
  X-Device-ID: smart-band-001
  X-API-Key: test-api-key-123
```

### Manejar Eventos de Proximidad
```
POST /api/v1/proximity-events
Headers:
  X-Device-ID: smart-band-001
  X-API-Key: test-api-key-123
  Content-Type: application/json

Body:
{
  "device_id": "smart-band-001",
  "location_id": "home-loc",
  "event_type": "ENTER",
  "latitude": -12.12345,
  "longitude": -77.54321,
  "timestamp": "2025-06-19T10:30:00Z"
}
```

## Datos de Prueba

La aplicación incluye datos stub para testing:

### Dispositivos
- **ID**: `smart-band-001`
- **API Key**: `test-api-key-123`

### Ubicaciones
- **Casa**: `home-loc` (-12.1234, -77.5432, radio: 100m)
- **Oficina**: `office-loc` (-12.5678, -77.9876, radio: 50m)

## Estructura del Proyecto

```
geoentry-edge-api/
├── app.py                 # Punto de entrada de la aplicación
├── config.py             # Configuración de entornos
├── requirements.txt      # Dependencias de Python
├── Procfile             # Configuración para deployment
├── build.sh             # Script de construcción
├── devices/             # Módulo de dispositivos
├── locations/           # Módulo de ubicaciones
├── proximity_events/    # Módulo de eventos de proximidad
└── shared/             # Infraestructura compartida
    └── infrastructure/
        └── database.py  # Configuración de base de datos
```

## Tecnologías

- **Flask**: Framework web
- **Peewee**: ORM para SQLite
- **GeoPy**: Cálculos geográficos
- **Gunicorn**: Servidor WSGI para producción
- **SQLite**: Base de datos ligera

## Licencia

[Tu licencia aquí]
