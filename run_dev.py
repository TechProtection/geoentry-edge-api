#!/usr/bin/env python3
"""Script para ejecutar la aplicación en modo desarrollo."""

import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == "__main__":
    print("🚀 Iniciando GeoEntry Edge API con Swagger UI...")
    print("📚 Swagger UI disponible en: http://localhost:5000/apidocs/")
    print("📄 Especificación OpenAPI en: http://localhost:5000/apispec_1.json")
    print("💚 Health check en: http://localhost:5000/")
    print("---")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
