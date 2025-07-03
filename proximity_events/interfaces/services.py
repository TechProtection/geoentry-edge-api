"""Interface services for Proximity Events context."""
from flask import Blueprint, request, jsonify
from datetime import datetime
from proximity_events.application.services import ProximityEventApplicationService
from devices.interfaces.services import authenticate_device

proximity_event_api = Blueprint("proximity_event_api", __name__)
event_service = ProximityEventApplicationService()


@proximity_event_api.route("/api/v1/proximity-events", methods=["POST"])
def create_proximity_event():
    """Create a new proximity event.
    ---
    tags:
      - Proximity Events
    parameters:
      - name: X-Device-ID
        in: header
        type: string
        required: true
        description: ID único del dispositivo IoT
        example: "smart-band-001"
      - name: event_data
        in: body
        required: true
        description: Datos del evento de proximidad
        schema:
          type: object
          required:
            - device_id
            - home_location_id
            - home_location_name
            - type
            - distance
            - latitude
            - longitude
          properties:
            device_id:
              type: string
              example: "device_001"
            home_location_id:
              type: string
              example: "location_001"
            home_location_name:
              type: string
              example: "Casa"
            type:
              type: string
              example: "ENTER"
            distance:
              type: number
              example: 50.5
            latitude:
              type: number
              example: -12.12345
            longitude:
              type: number
              example: -77.54321
            user_id:
              type: string
              example: "user_123"
    responses:
      201:
        description: Proximity event created successfully
      400:
        description: Invalid request data
      401:
        description: Device ID faltante
      404:
        description: Device not found
    """
    try:
        device_id = request.headers.get("X-Device-ID")
        if not device_id:
            return jsonify({"error": "Missing X-Device-ID header"}), 401

        # Verificar que el dispositivo existe
        if not authenticate_device(device_id):
            return jsonify({"error": "Device not found"}), 404

        data = request.get_json()
        event = event_service.create_proximity_event(
            device_id=data['device_id'],
            home_location_id=data['home_location_id'],
            home_location_name=data['home_location_name'],
            event_type=data['type'],
            distance=data['distance'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            user_id=data.get('user_id')
        )
        return jsonify(event.to_dict()), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@proximity_event_api.route("/api/v1/proximity-events/<event_id>", methods=["GET"])
def get_proximity_event(event_id):
    """Get proximity event by ID.
    ---
    tags:
      - Proximity Events
    parameters:
      - in: path
        name: event_id
        required: true
        type: string
    responses:
      200:
        description: Proximity event found
      404:
        description: Proximity event not found
    """
    try:
        event = event_service.get_event_by_id(event_id)
        if not event:
            return jsonify({"error": "Proximity event not found"}), 404
        return jsonify(event.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@proximity_event_api.route("/api/v1/proximity-events/device/<device_id>", methods=["GET"])
def get_events_by_device(device_id):
    """Get proximity events by device ID.
    ---
    tags:
      - Proximity Events
    parameters:
      - in: path
        name: device_id
        required: true
        type: string
      - in: query
        name: limit
        type: integer
        default: 100
    responses:
      200:
        description: Proximity events found
    """
    try:
        limit = int(request.args.get('limit', 100))
        events = event_service.get_events_by_device(device_id, limit)
        return jsonify([event.to_dict() for event in events]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@proximity_event_api.route("/api/v1/proximity-events/user/<user_id>", methods=["GET"])
def get_events_by_user(user_id):
    """Get proximity events by user ID.
    ---
    tags:
      - Proximity Events
    parameters:
      - in: path
        name: user_id
        required: true
        type: string
      - in: query
        name: limit
        type: integer
        default: 100
    responses:
      200:
        description: Proximity events found
    """
    try:
        limit = int(request.args.get('limit', 100))
        events = event_service.get_events_by_user(user_id, limit)
        return jsonify([event.to_dict() for event in events]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@proximity_event_api.route("/api/v1/proximity-events/location/<location_id>", methods=["GET"])
def get_events_by_location(location_id):
    """Get proximity events by location ID.
    ---
    tags:
      - Proximity Events
    parameters:
      - in: path
        name: location_id
        required: true
        type: string
      - in: query
        name: limit
        type: integer
        default: 100
    responses:
      200:
        description: Proximity events found
    """
    try:
        limit = int(request.args.get('limit', 100))
        events = event_service.get_events_by_location(location_id, limit)
        return jsonify([event.to_dict() for event in events]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@proximity_event_api.route("/api/v1/proximity-events/device/<device_id>/pending", methods=["GET"])
def get_pending_events(device_id):
    """Obtener eventos pendientes para un dispositivo específico.
    ---
    tags:
      - Proximity Events
    parameters:
      - name: device_id
        in: path
        type: string
        required: true
        description: ID del dispositivo
      - name: X-Device-ID
        in: header
        type: string 
        required: true
        description: ID de autenticación del dispositivo
    responses:
      200:
        description: Eventos pendientes encontrados
      204:
        description: No hay eventos pendientes
      401:
        description: Autenticación requerida
      404:
        description: Dispositivo no encontrado
    """
    try:
        # Verificar autenticación
        auth_device_id = request.headers.get("X-Device-ID")
        if not auth_device_id or auth_device_id != device_id:
            return jsonify({"error": "Invalid device authentication"}), 401
        
        # Obtener eventos pendientes (simulado - en una implementación real usarías la base de datos)
        # Por ahora retornamos 204 (no content) para indicar que no hay eventos pendientes
        return "", 204
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@proximity_event_api.route("/api/v1/proximity-events/<event_id>/confirm", methods=["PATCH"])
def confirm_event(event_id):
    """Confirmar que un evento fue procesado por el dispositivo.
    ---
    tags:
      - Proximity Events
    parameters:
      - name: event_id
        in: path
        type: string
        required: true
        description: ID del evento a confirmar
      - name: X-Device-ID
        in: header
        type: string
        required: true
        description: ID del dispositivo
      - in: body
        name: confirmation_data
        schema:
          type: object
          properties:
            event_id:
              type: string
            device_status:
              type: string
            action_taken:
              type: string
            timestamp:
              type: number
    responses:
      200:
        description: Evento confirmado exitosamente
      404:
        description: Evento no encontrado
      401:
        description: Autenticación requerida
    """
    try:
        data = request.get_json()
        device_id = request.headers.get("X-Device-ID")
        
        if not device_id:
            return jsonify({"error": "X-Device-ID header required"}), 401
        
        # Aquí se actualizaría el evento en la base de datos
        # Por ahora solo retornamos confirmación
        
        return jsonify({
            "event_id": event_id,
            "device_id": device_id,
            "status": "confirmed",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@proximity_event_api.route("/api/v1/proximity-events/<event_id>", methods=["DELETE"])
def delete_proximity_event(event_id):
    """Delete a proximity event.
    ---
    tags:
      - Proximity Events
    parameters:
      - in: path
        name: event_id
        required: true
        type: string
    responses:
      200:
        description: Proximity event deleted successfully
      404:
        description: Proximity event not found
    """
    try:
        if event_service.delete_event(event_id):
            return jsonify({"message": "Proximity event deleted successfully"}), 200
        else:
            return jsonify({"error": "Proximity event not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
