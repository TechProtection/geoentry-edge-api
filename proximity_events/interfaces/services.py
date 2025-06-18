"""Interface services for Proximity Events context."""
from flask import Blueprint, request, jsonify
from proximity_events.application.services import ProximityEventApplicationService
from devices.interfaces.services import authenticate_request

proximity_event_api = Blueprint("proximity_event_api", __name__)
event_service = ProximityEventApplicationService()


@proximity_event_api.route("/api/v1/proximity-events", methods=["POST"])
def handle_proximity_event():
    """Handle proximity event detection."""
    # Autenticación
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json
    try:
        # Obtener datos del dispositivo
        device_id = request.headers.get("X-Device-ID")
        latitude = data["latitude"]
        longitude = data["longitude"]

        # Aquí se integraría con el servicio de ubicaciones
        # para determinar los eventos (esto sería en una implementación completa)

        # Ejemplo: Crear evento simulado
        event = event_service.create_proximity_event(
            device_id=device_id,
            location_id="loc-123",  # Debería venir del análisis de ubicación
            event_type="ENTER",
            distance=50.0,
            latitude=latitude,
            longitude=longitude
        )

        return jsonify({
            "event_id": event.event_id,
            "status": "Event processed"
        }), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500