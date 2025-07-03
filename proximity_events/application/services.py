"""Application services for Proximity Events context."""
from typing import List, Optional
import uuid
from proximity_events.domain.entities import ProximityEvent
from proximity_events.infrastructure.supabase_repository import ProximityEventSupabaseRepository


class ProximityEventApplicationService:
    """Application service for proximity events."""

    def __init__(self):
        self.repository = ProximityEventSupabaseRepository()

    def create_proximity_event(self, device_id: str, home_location_id: str,
                               home_location_name: str, event_type: str, 
                               distance: float, latitude: float, longitude: float,
                               user_id: str = None) -> ProximityEvent:
        """Create and save a proximity event."""
        event_id = str(uuid.uuid4())
        
        event = ProximityEvent(
            event_id=event_id,
            device_id=device_id,
            home_location_id=home_location_id,
            home_location_name=home_location_name,
            event_type=event_type,
            distance=distance,
            latitude=latitude,
            longitude=longitude,
            user_id=user_id
        )
        
        return self.repository.create(event)
    
    def get_event_by_id(self, event_id: str) -> Optional[ProximityEvent]:
        """Get a specific proximity event by ID."""
        return self.repository.get_by_id(event_id)

    def get_events_by_device(self, device_id: str, limit: int = 100) -> List[ProximityEvent]:
        """Get proximity events for a device."""
        return self.repository.get_by_device_id(device_id, limit)
    
    def get_events_by_user(self, user_id: str, limit: int = 100) -> List[ProximityEvent]:
        """Get proximity events for a user."""
        return self.repository.get_by_user_id(user_id, limit)
    
    def get_events_by_location(self, location_id: str, limit: int = 100) -> List[ProximityEvent]:
        """Get proximity events for a location."""
        return self.repository.get_by_location_id(location_id, limit)
    
    def delete_event(self, event_id: str) -> bool:
        """Delete a proximity event."""
        return self.repository.delete(event_id)