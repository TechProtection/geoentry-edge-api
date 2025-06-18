"""Application services for Proximity Events context."""
from proximity_events.domain.services import ProximityEventService
from proximity_events.infrastructure.repositories import ProximityEventRepository


class ProximityEventApplicationService:
    """Application service for proximity events."""

    def __init__(self):
        self.repository = ProximityEventRepository()
        self.event_service = ProximityEventService()

    def create_proximity_event(self, device_id: str, location_id: str,
                               event_type: str, distance: float,
                               latitude: float, longitude: float) -> 'ProximityEvent':
        """Create and save a proximity event."""
        event = self.event_service.create_event(
            device_id, location_id, event_type, distance, latitude, longitude)
        return self.repository.save_event(event)