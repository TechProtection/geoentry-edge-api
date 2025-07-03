"""Domain services for Devices context."""
from typing import Optional
from devices.domain.entities import Device


class DeviceService:
    """Service for device operations."""

    @staticmethod
    def validate_device_data(device_id: str, name: str, device_type: str, profile_id: str) -> bool:
        """Validate device data before creation."""
        if not device_id or not device_id.strip():
            return False
        if not name or not name.strip():
            return False
        if not device_type or not device_type.strip():
            return False
        if not profile_id or not profile_id.strip():
            return False
        return True