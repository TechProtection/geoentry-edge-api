"""Interface services for Locations context."""
from flask import Blueprint, request, jsonify
from locations.application.services import LocationApplicationService
from devices.interfaces.services import authenticate_device
from devices.application.services import DeviceApplicationService

location_api = Blueprint("location_api", __name__)
location_service = LocationApplicationService()
device_service = DeviceApplicationService()


@location_api.route("/api/v1/locations", methods=["POST"])
def create_location():
    """Create a new location.
    ---
    tags:
      - Locations
    parameters:
      - in: body
        name: location_data
        required: true
        schema:
          type: object
          required:
            - location_id
            - name
            - latitude
            - longitude
            - radius
            - profile_id
          properties:
            location_id:
              type: string
              example: "home-001"
            name:
              type: string
              example: "Casa"
            latitude:
              type: number
              example: -12.1234
            longitude:
              type: number
              example: -77.5432
            radius:
              type: number
              example: 100.0
            profile_id:
              type: string
              example: "user_123"
            address:
              type: string
              example: "Av. Principal 123"
    responses:
      201:
        description: Location created successfully
      400:
        description: Invalid request data
      409:
        description: Location already exists
    """
    try:
        data = request.get_json()
        location = location_service.create_location(
            location_id=data['location_id'],
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            radius=data['radius'],
            profile_id=data['profile_id'],
            address=data.get('address', '')
        )
        return jsonify(location.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@location_api.route("/api/v1/locations/<location_id>", methods=["GET"])
def get_location(location_id):
    """Get location by ID.
    ---
    tags:
      - Locations
    parameters:
      - in: path
        name: location_id
        required: true
        type: string
    responses:
      200:
        description: Location found
      404:
        description: Location not found
    """
    try:
        location = location_service.get_location(location_id)
        if not location:
            return jsonify({"error": "Location not found"}), 404
        return jsonify(location.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@location_api.route("/api/v1/locations/profile/<profile_id>", methods=["GET"])
def get_locations_by_profile(profile_id):
    """Get locations by profile ID.
    ---
    tags:
      - Locations
    parameters:
      - in: path
        name: profile_id
        required: true
        type: string
    responses:
      200:
        description: Locations found
    """
    try:
        locations = location_service.get_locations_by_profile(profile_id)
        return jsonify([location.to_dict() for location in locations]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@location_api.route("/api/v1/locations/proximity-check", methods=["POST"])
def proximity_check():
    """Verificar proximidad a todas las ubicaciones configuradas para el dispositivo.
    ---
    tags:
      - Locations
    parameters:
      - name: X-Device-ID
        in: header
        type: string
        required: true
        description: ID único del dispositivo IoT
        example: "smart-band-001"
      - name: position
        in: body
        required: true
        description: Coordenadas actuales del dispositivo
        schema:
          type: object
          required:
            - latitude
            - longitude
            - profile_id
          properties:
            latitude:
              type: number
              format: float
              description: Latitud en grados decimales
              example: -12.12345
            longitude:
              type: number
              format: float
              description: Longitud en grados decimales
              example: -77.54321
            profile_id:
              type: string
              description: ID del perfil del usuario
              example: "user_123"
    responses:
      200:
        description: Verificación de proximidad exitosa
      400:
        description: Datos inválidos o faltantes
      401:
        description: Device ID faltante
      404:
        description: Dispositivo no encontrado
      500:
        description: Error interno del servidor
    """
    try:
        device_id = request.headers.get("X-Device-ID")
        if not device_id:
            return jsonify({"error": "Missing X-Device-ID header"}), 401

        # Verificar que el dispositivo existe
        if not authenticate_device(device_id):
            return jsonify({"error": "Device not found"}), 404

        data = request.get_json()
        latitude = data["latitude"]
        longitude = data["longitude"]
        profile_id = data["profile_id"]

        # Realizar verificación de proximidad
        results = location_service.check_proximity(latitude, longitude, profile_id)

        return jsonify({
            "device_id": device_id,
            "current_position": {"latitude": latitude, "longitude": longitude},
            "proximity_results": results
        }), 200

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@location_api.route("/api/v1/locations/<location_id>", methods=["PATCH"])
def update_location(location_id):
    """Update location information.
    ---
    tags:
      - Locations
    parameters:
      - in: path
        name: location_id
        required: true
        type: string
      - in: body
        name: location_data
        schema:
          type: object
          properties:
            name:
              type: string
            latitude:
              type: number
            longitude:
              type: number
            radius:
              type: number
            address:
              type: string
            is_active:
              type: boolean
    responses:
      200:
        description: Location updated successfully
      404:
        description: Location not found
    """
    try:
        data = request.get_json()
        location = location_service.update_location(
            location_id=location_id,
            name=data.get('name'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            radius=data.get('radius'),
            address=data.get('address'),
            is_active=data.get('is_active')
        )
        return jsonify(location.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@location_api.route("/api/v1/locations/<location_id>", methods=["DELETE"])
def delete_location(location_id):
    """Delete a location.
    ---
    tags:
      - Locations
    parameters:
      - in: path
        name: location_id
        required: true
        type: string
    responses:
      200:
        description: Location deleted successfully
      404:
        description: Location not found
    """
    try:
        if location_service.delete_location(location_id):
            return jsonify({"message": "Location deleted successfully"}), 200
        else:
            return jsonify({"error": "Location not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500