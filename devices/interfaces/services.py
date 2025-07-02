"""Interface services for Devices context."""
from flask import Blueprint, request, jsonify
from devices.application.services import DeviceApplicationService

device_api = Blueprint("device_api", __name__)
device_service = DeviceApplicationService()


@device_api.route('/devices', methods=['POST'])
def create_device():
    """Create a new device.
    ---
    tags:
      - Devices
    parameters:
      - in: body
        name: device_data
        required: true
        schema:
          type: object
          required:
            - device_id
            - name
            - type
            - profile_id
          properties:
            device_id:
              type: string
              example: "device_001"
            name:
              type: string
              example: "My IoT Device"
            type:
              type: string
              example: "sensor"
            profile_id:
              type: string
              example: "user_123"
    responses:
      201:
        description: Device created successfully
      400:
        description: Invalid request data
      409:
        description: Device already exists
    """
    try:
        data = request.get_json()
        device = device_service.create_device(
            device_id=data['device_id'],
            name=data['name'],
            device_type=data['type'],
            profile_id=data['profile_id']
        )
        return jsonify(device.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@device_api.route('/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    """Get device by ID.
    ---
    tags:
      - Devices
    parameters:
      - in: path
        name: device_id
        required: true
        type: string
    responses:
      200:
        description: Device found
      404:
        description: Device not found
    """
    try:
        device = device_service.get_device(device_id)
        if not device:
            return jsonify({"error": "Device not found"}), 404
        return jsonify(device.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@device_api.route('/devices/profile/<profile_id>', methods=['GET'])
def get_devices_by_profile(profile_id):
    """Get devices by profile ID.
    ---
    tags:
      - Devices
    parameters:
      - in: path
        name: profile_id
        required: true
        type: string
    responses:
      200:
        description: Devices found
    """
    try:
        devices = device_service.get_devices_by_profile(profile_id)
        return jsonify([device.to_dict() for device in devices]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@device_api.route('/devices/<device_id>', methods=['PUT'])
def update_device(device_id):
    """Update device information.
    ---
    tags:
      - Devices
    parameters:
      - in: path
        name: device_id
        required: true
        type: string
      - in: body
        name: device_data
        schema:
          type: object
          properties:
            name:
              type: string
            type:
              type: string
    responses:
      200:
        description: Device updated successfully
      404:
        description: Device not found
    """
    try:
        data = request.get_json()
        device = device_service.update_device(
            device_id=device_id,
            name=data.get('name'),
            device_type=data.get('type')
        )
        return jsonify(device.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@device_api.route('/devices/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    """Delete a device.
    ---
    tags:
      - Devices
    parameters:
      - in: path
        name: device_id
        required: true
        type: string
    responses:
      200:
        description: Device deleted successfully
      404:
        description: Device not found
    """
    try:
        if device_service.delete_device(device_id):
            return jsonify({"message": "Device deleted successfully"}), 200
        else:
            return jsonify({"error": "Device not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def authenticate_device(device_id: str) -> bool:
    """Simple device authentication check."""
    return device_service.device_exists(device_id)