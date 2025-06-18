"""Application services for Locations context."""
from locations.domain.services import LocationService
from locations.infrastructure.repositories import LocationRepository


class LocationApplicationService:
    """Application service for location operations."""

    def __init__(self):
        self.repository = LocationRepository()
        self.location_service = LocationService()

    def check_proximity(self, device_lat: float, device_lon: float, profile_id: str) -> dict:
        """Check proximity to all locations of a profile."""
        locations = self.repository.get_locations_by_profile(profile_id)
        results = []

        for location in locations:
            distance = self.location_service.calculate_distance(
                location.latitude,
                location.longitude,
                device_lat,
                device_lon
            )
            within_radius = distance <= location.radius
            event_type = "ENTER" if within_radius else "EXIT"

            results.append({
                "location_id": location.location_id,
                "location_name": location.name,
                "distance": distance,
                "within_radius": within_radius,
                "event_type": event_type
            })

        return results