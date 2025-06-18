"""Domain entities for Locations context."""
from datetime import datetime


class Location:
    """Represents a geographic location entity."""

    def __init__(self, location_id: str, name: str, latitude: float,
                 longitude: float, radius: float, profile_id: str,
                 created_at: datetime):
        self.location_id = location_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.profile_id = profile_id
        self.created_at = created_at