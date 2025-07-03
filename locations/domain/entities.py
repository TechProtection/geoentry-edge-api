"""Domain entities for Locations context."""
from datetime import datetime
from typing import Optional


class Location:
    """Represents a geographic location entity."""

    def __init__(self, location_id: str, name: str, latitude: float,
                 longitude: float, radius: float, profile_id: str,
                 address: str = "", is_active: bool = True, created_at: Optional[datetime] = None):
        self.location_id = location_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.profile_id = profile_id
        self.address = address
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            'location_id': self.location_id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'radius': self.radius,
            'profile_id': self.profile_id,
            'address': self.address,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }