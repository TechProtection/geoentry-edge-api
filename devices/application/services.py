"""Application services for Devices context."""
from devices.domain.services import DeviceAuthService
from devices.infrastructure.repositories import DeviceRepository


class DeviceAuthApplicationService:
    """Application service for device authentication."""

    def __init__(self):
        self.repository = DeviceRepository()
        self.auth_service = DeviceAuthService()

    def authenticate(self, device_id: str, api_key: str) -> bool:
        """Authenticate device."""
        device = self.repository.find_by_id_and_key(device_id, api_key)
        return self.auth_service.authenticate(device)