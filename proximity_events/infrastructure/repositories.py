"""Repositories for Proximity Events context."""
import requests
from proximity_events.domain.entities import ProximityEvent
from proximity_events.infrastructure.models import ProximityEvent as ProximityEventModel

BACKEND_URL = "http://localhost:3000/api"

class ProximityEventRepository:
    """Repository for proximity event operations."""

    @staticmethod
    def save_event(event: ProximityEvent) -> ProximityEvent:
        """Save event with fallback if backend is unavailable."""
        # Save to local cache
        ProximityEventModel.create(
            event_id=event.event_id,
            device_id=event.device_id,
            location_id=event.location_id,
            event_type=event.event_type,
            distance=event.distance,
            latitude=event.latitude,
            longitude=event.longitude,
            created_at=event.created_at
        )

        # Try to sync with backend (fail silently)
        try:
            event_data = {
                "device_id": event.device_id,
                "location_id": event.location_id,
                "type": event.event_type,
                "latitude": event.latitude,
                "longitude": event.longitude,
                "distance": event.distance
            }
            requests.post(
                f"{BACKEND_URL}/proximity-events",
                json=event_data,
                timeout=2
            )
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass

        return event