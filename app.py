"""Flask application entry point for GeoEntry Edge API."""

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from devices.interfaces.services import device_api
from locations.interfaces.services import location_api
from proximity_events.interfaces.services import proximity_event_api
from shared.infrastructure.database import init_db
from config import get_config

# Get configuration
config = get_config()

app = Flask(__name__)
CORS(app)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "GeoEntry Edge API",
        "description": "API Edge para gestión de dispositivos IoT, ubicaciones y eventos de proximidad",
        "version": "1.0.0",
        "contact": {
            "name": "GeoEntry Team",
            "email": "support@geoentry.com"
        }
    },
    "host":"geoentry-rest-api.onrender.com/api",
    "basePath": "/",
    "securityDefinitions": {
        "DeviceAuth": {
            "type": "apiKey",
            "name": "X-Device-ID",
            "in": "header",
            "description": "ID del dispositivo IoT"
        },
        "ApiKeyAuth": {
            "type": "apiKey", 
            "name": "X-API-Key",
            "in": "header",
            "description": "Clave API del dispositivo"
        }
    },
    "security": [
        {"DeviceAuth": [], "ApiKeyAuth": []}
    ],
    "tags": [
        {
            "name": "Health",
            "description": "Endpoints de estado del servicio"
        },
        {
            "name": "Locations",
            "description": "Gestión de ubicaciones y verificación de proximidad"
        },
        {
            "name": "Proximity Events", 
            "description": "Manejo de eventos de proximidad"
        }
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

app.register_blueprint(device_api)
app.register_blueprint(location_api)
app.register_blueprint(proximity_event_api)

@app.before_request
def initialize():
    """Initialize database on first request."""
    init_db()

@app.route('/')
def health_check():
    """Health check endpoint para Render y monitoreo del servicio.
    ---
    tags:
      - Health
    responses:
      200:
        description: Servicio funcionando correctamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "healthy"
            service:
              type: string
              example: "GeoEntry Edge API"
            version:
              type: string
              example: "1.0.0"
    """
    return {
        "status": "healthy", 
        "service": "GeoEntry Edge API",
        "version": "1.0.0"
    }, 200

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)