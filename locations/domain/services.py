"""Domain services for Locations context."""
from geopy.distance import great_circle


class LocationService:
    """Service for location operations."""

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in meters."""
        return great_circle((lat1, lon1), (lat2, lon2)).meters

    @staticmethod
    def is_within_radius(location, device_lat: float, device_lon: float) -> bool:
        """Check if device is within location radius."""
        distance = LocationService.calculate_distance(
            location.latitude,
            location.longitude,
            device_lat,
            device_lon
        )
        return distance <= location.radius