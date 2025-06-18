"""Interface services for Locations context."""
from flask import Blueprint, request, jsonify
from locations.application.services import LocationApplicationService
from devices.interfaces.services import authenticate_request

location_api = Blueprint("location_api", __name__)
location_service = LocationApplicationService()


@location_api.route("/api/v1/locations/proximity-check", methods=["POST"])
def proximity_check():
    """Check proximity to all locations for authenticated device."""
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