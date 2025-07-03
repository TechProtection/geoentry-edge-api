"""Application services for Locations context."""
from typing import List, Optional
from locations.domain.entities import Location
from locations.domain.services import LocationService
from locations.infrastructure.supabase_repository import LocationSupabaseRepository


class LocationApplicationService:
    """Application service for location operations."""

    def __init__(self):
        self.repository = LocationSupabaseRepository()
        self.location_service = LocationService()

    def create_location(self, location_id: str, name: str, latitude: float, 
                       longitude: float, radius: float, profile_id: str, 
                       address: str = "") -> Location:
        """Create a new location."""
        if self.repository.exists(location_id):
            raise ValueError(f"Location with ID {location_id} already exists")
        
        location = Location(
            location_id=location_id,
            name=name,
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            profile_id=profile_id,
            address=address
        )
        
        return self.repository.create(location)
    
    def get_location(self, location_id: str) -> Optional[Location]:
        """Get location by ID."""
        return self.repository.get_by_id(location_id)
    
    def get_locations_by_profile(self, profile_id: str) -> List[Location]:
        """Get all locations for a profile."""
        return self.repository.get_by_profile_id(profile_id)
    
    def get_active_locations_by_profile(self, profile_id: str) -> List[Location]:
        """Get all active locations for a profile."""
        return self.repository.get_active_locations(profile_id)
    
    def update_location(self, location_id: str, name: str = None, latitude: float = None,
                       longitude: float = None, radius: float = None, 
                       address: str = None, is_active: bool = None) -> Location:
        """Update location information."""
        location = self.repository.get_by_id(location_id)
        if not location:
            raise ValueError(f"Location with ID {location_id} not found")
        
        if name is not None:
            location.name = name
        if latitude is not None:
            location.latitude = latitude
        if longitude is not None:
            location.longitude = longitude
        if radius is not None:
            location.radius = radius
        if address is not None:
            location.address = address
        if is_active is not None:
            location.is_active = is_active
        
        return self.repository.update(location)
    
    def delete_location(self, location_id: str) -> bool:
        """Delete a location."""
        return self.repository.delete(location_id)

    def check_proximity(self, device_lat: float, device_lon: float, profile_id: str) -> List[dict]:
        """Check proximity to all active locations of a profile."""
        locations = self.repository.get_active_locations(profile_id)
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