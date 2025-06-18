"""Domain entities for Devices context."""
from datetime import datetime


class Device:
    """Represents an IoT device entity."""

    def __init__(self, device_id: str, api_key: str, profile_id: str, created_at: datetime):
        self.device_id = device_id
        self.api_key = api_key
        self.profile_id = profile_id
        self.created_at = created_at