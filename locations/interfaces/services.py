"""Interface services for Locations context."""
from flask import Blueprint, request, jsonify
from locations.application.services import LocationApplicationService
from devices.interfaces.services import authenticate_request

location_api = Blueprint("location_api", __name__)
location_service = LocationApplicationService()


@location_api.route("/api/v1/locations/proximity-check", methods=["POST"])
def proximity_check():
    """Verificar proximidad a todas las ubicaciones configuradas para el dispositivo autenticado.
    ---
    tags:
      - Locations
    security:
      - DeviceAuth: []
      - ApiKeyAuth: []
    parameters:
      - name: X-Device-ID
        in: header
        type: string
        required: true
        description: ID único del dispositivo IoT
        example: "smart-band-001"
      - name: X-API-Key
        in: header
        type: string
        required: true
        description: Clave API del dispositivo
        example: "test-api-key-123"
      - name: position
        in: body
        required: true
        description: Coordenadas actuales del dispositivo
        schema:
          type: object
          required:
            - latitude
            - longitude
          properties:
            latitude:
              type: number
              format: float
              description: Latitud en grados decimales
              example: -12.12345
              minimum: -90
              maximum: 90
            longitude:
              type: number
              format: float
              description: Longitud en grados decimales
              example: -77.54321
              minimum: -180
              maximum: 180
    responses:
      200:
        description: Verificación de proximidad exitosa
        schema:
          type: object
          properties:
            device_id:
              type: string
              example: "smart-band-001"
            current_position:
              type: object
              properties:
                latitude:
                  type: number
                  example: -12.12345
                longitude:
                  type: number
                  example: -77.54321
            proximity_results:
              type: array
              items:
                type: object
                properties:
                  location_id:
                    type: string
                    example: "home-loc"
                  location_name:
                    type: string
                    example: "Casa"
                  distance:
                    type: number
                    format: float
                    example: 123.45
                    description: "Distancia en metros"
                  within_radius:
                    type: boolean
                    example: true
                  event_type:
                    type: string
                    enum: ["ENTER", "EXIT", "STAY"]
                    example: "ENTER"
      400:
        description: Datos inválidos o faltantes
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing required field: latitude"
      401:
        description: Headers de autenticación faltantes
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing authentication headers"
      403:
        description: Credenciales del dispositivo inválidas
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid device credentials"
      404:
        description: Dispositivo no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Device not found"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Internal server error"
    """
    # Autenticación
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json
    try:
        device_id = request.headers.get("X-Device-ID")
        latitude = data["latitude"]
        longitude = data["longitude"]

        # Obtener profile_id del dispositivo autenticado
        from devices.infrastructure.repositories import DeviceRepository
        device_repo = DeviceRepository()
        device = device_repo.find_by_id_and_key(device_id, request.headers.get("X-API-Key"))

        if not device:
            return jsonify({"error": "Device not found"}), 404

        # Realizar verificación de proximidad
        results = location_service.check_proximity(
            latitude, longitude, device.profile_id
        )

        return jsonify({
            "device_id": device_id,
            "current_position": {"latitude": latitude, "longitude": longitude},
            "proximity_results": results
        }), 200

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@location_api.route("/api/v1/locations", methods=["GET"])
def get_all_locations():
    """Obtener todas las ubicaciones disponibles en el sistema.
    ---
    tags:
      - Locations
    responses:
      200:
        description: Lista de todas las ubicaciones obtenida exitosamente
        schema:
          type: object
          properties:
            total_count:
              type: integer
              example: 2
              description: "Número total de ubicaciones"
            locations:
              type: array
              items:
                type: object
                properties:
                  location_id:
                    type: string
                    example: "home-loc"
                  name:
                    type: string
                    example: "Casa"
                  latitude:
                    type: number
                    format: float
                    example: -12.1234
                  longitude:
                    type: number
                    format: float
                    example: -77.5432
                  radius:
                    type: number
                    format: float
                    example: 100.0
                    description: "Radio en metros"
                  profile_id:
                    type: string
                    example: "test-profile"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Internal server error"
    """
    try:
        # Obtener todas las ubicaciones sin filtros
        locations = location_service.repository.get_all_locations()
        
        locations_data = []
        for location in locations:
            locations_data.append({
                "location_id": location.location_id,
                "name": location.name,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "radius": location.radius,
                "profile_id": location.profile_id
            })

        return jsonify({
            "total_count": len(locations_data),
            "locations": locations_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500