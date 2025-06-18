"""Domain entities for Proximity Events context."""
from datetime import datetime


class ProximityEvent:
    """Represents a proximity detection event."""

    def __init__(self, event_id: str, device_id: str, location_id: str,
                 event_type: str, distance: float, latitude: float,
                 longitude: float, created_at: datetime):
        self.event_id = event_id
        self.device_id = device_id
        self.location_id = location_id
        self.event_type = event_type
        self.distance = distance
        self.latitude = latitude
        self.longitude = longitude
        self.created_at = created_at