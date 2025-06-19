"""Interface services for Proximity Events context."""
from flask import Blueprint, request, jsonify
from proximity_events.application.services import ProximityEventApplicationService
from devices.interfaces.services import authenticate_request

proximity_event_api = Blueprint("proximity_event_api", __name__)
event_service = ProximityEventApplicationService()


@proximity_event_api.route("/api/v1/proximity-events", methods=["POST"])
def handle_proximity_event():
    """Registrar y procesar eventos de proximidad detectados por el dispositivo.
    ---
    tags:
      - Proximity Events
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
      - name: event_data
        in: body
        required: true
        description: Datos del evento de proximidad
        schema:
          type: object
          required:
            - latitude
            - longitude
          properties:
            latitude:
              type: number
              format: float
              description: Latitud donde ocurrió el evento
              example: -12.12345
              minimum: -90
              maximum: 90
            longitude:
              type: number
              format: float
              description: Longitud donde ocurrió el evento
              example: -77.54321
              minimum: -180
              maximum: 180
            event_type:
              type: string
              enum: ["ENTER", "EXIT", "STAY"]
              description: Tipo de evento de proximidad
              example: "ENTER"
            location_id:
              type: string
              description: ID de la ubicación relacionada (opcional)
              example: "home-loc"
            timestamp:
              type: string
              format: date-time
              description: Timestamp del evento (opcional, se usa timestamp actual si no se provee)
              example: "2025-06-19T10:30:00Z"
    responses:
      201:
        description: Evento procesado exitosamente
        schema:
          type: object
          properties:
            event_id:
              type: string
              example: "evt-123456789"
            status:
              type: string
              example: "Event processed"
            timestamp:
              type: string
              format: date-time
              example: "2025-06-19T10:30:00Z"
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