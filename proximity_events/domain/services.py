"""Domain services for Proximity Events context."""
from datetime import datetime, timezone
from .entities import ProximityEvent  # Importación corregida


class ProximityEventService:
    """Service for proximity events."""

    @staticmethod
    def create_event(device_id: str, location_id: str, event_type: str,
                     distance: float, latitude: float, longitude: float) -> ProximityEvent:
        """Create a new proximity event."""
        return ProximityEvent(
            event_id=None,
            device_id=device_id,
            location_id=location_id,
            event_type=event_type,
            distance=distance,
            latitude=latitude,
            longitude=longitude,
            created_at=datetime.now(timezone.utc)
        )