"""Domain entities for Proximity Events context."""
from datetime import datetime
from typing import Optional


class ProximityEvent:
    """Represents a proximity detection event."""

    def __init__(self, event_id: str, device_id: str, home_location_id: str,
                 home_location_name: str, event_type: str, distance: float, 
                 latitude: float, longitude: float, user_id: Optional[str] = None,
                 created_at: Optional[datetime] = None):
        self.event_id = event_id
        self.device_id = device_id
        self.home_location_id = home_location_id
        self.home_location_name = home_location_name
        self.event_type = event_type
        self.distance = distance
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            'event_id': self.event_id,
            'device_id': self.device_id,
            'home_location_id': self.home_location_id,
            'home_location_name': self.home_location_name,
            'event_type': self.event_type,
            'distance': self.distance,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }