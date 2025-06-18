"""Interface services for Devices context."""
from flask import Blueprint, request, jsonify
from devices.application.services import DeviceAuthApplicationService

device_api = Blueprint("device_api", __name__)
auth_service = DeviceAuthApplicationService()


def authenticate_request():
    """Authenticate incoming request."""
    device_id = request.headers.get("X-Device-ID")
    api_key = request.headers.get("X-API-Key")

    if not device_id or not api_key:
        return jsonify({"error": "Missing authentication headers"}), 401

    if not auth_service.authenticate(device_id, api_key):
        return jsonify({"error": "Invalid device credentials"}), 403

    return None