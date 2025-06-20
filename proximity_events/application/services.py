"""Application services for Proximity Events context."""
from typing import List
from proximity_events.domain.entities import ProximityEvent
from proximity_events.domain.services import ProximityEventService
from proximity_events.infrastructure.repositories import ProximityEventRepository


class ProximityEventApplicationService:
    """Application service for proximity events."""

    def __init__(self):
        self.repository = ProximityEventRepository()
        self.event_service = ProximityEventService()

    def get_events_by_device(self, device_id: str, limit: int = 50) -> List[ProximityEvent]:
        """Get proximity events for a device."""
        return self.repository.get_events_by_device(device_id, limit)

    def get_event_by_id(self, event_id: str) -> ProximityEvent:
        """Get a specific proximity event by ID."""
        return self.repository.get_event_by_id(event_id)

    def create_proximity_event(self, device_id: str, location_id: str,
                               event_type: str, distance: float,
                               latitude: float, longitude: float) -> ProximityEvent:
        """Create and save a proximity event."""
        event = self.event_service.create_event(
            device_id, location_id, event_type, distance, latitude, longitude)
        return self.repository.save_event(event)

    def get_all_events(self, limit: int = 100) -> List[ProximityEvent]:
        """Get all proximity events in the system."""
        return self.repository.get_all_events(limit)