"""Domain services for Devices context."""
from typing import Optional
from devices.domain.entities import Device


class DeviceAuthService:
    """Service for device authentication."""

    @staticmethod
    def authenticate(device: Optional[Device]) -> bool:
        """Authenticate a device."""
        return device is not None