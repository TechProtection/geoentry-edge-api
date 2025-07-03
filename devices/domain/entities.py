"""Domain entities for Devices context."""
from datetime import datetime
from typing import Optional


class Device:
    """Represents an IoT device entity."""

    def __init__(self, device_id: str, name: str, device_type: str, profile_id: str, created_at: Optional[datetime] = None):
        self.device_id = device_id
        self.name = name
        self.device_type = device_type
        self.profile_id = profile_id
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            'device_id': self.device_id,
            'name': self.name,
            'device_type': self.device_type,
            'profile_id': self.profile_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }