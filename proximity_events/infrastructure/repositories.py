"""Repositories for Proximity Events context."""
import requests
from typing import List
from proximity_events.domain.entities import ProximityEvent
from proximity_events.infrastructure.models import ProximityEvent as ProximityEventModel

BACKEND_URL = "https://geoentry-rest-api.onrender.com/api"  # URL de tu backend
# BACKEND_URL = "https://localhost:3000/api"  # URL de tu backend

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

    @staticmethod
    def get_events_by_device(device_id: str, limit: int = 50) -> List[ProximityEvent]:
        """Get proximity events for a device from local cache."""
        try:
            events_data = list(ProximityEventModel.select().where(
                ProximityEventModel.device_id == device_id
            ).order_by(ProximityEventModel.created_at.desc()).limit(limit))
            
            events = []
            for event_data in events_data:
                events.append(ProximityEvent(
                    event_id=event_data.event_id,
                    device_id=event_data.device_id,
                    location_id=event_data.location_id,
                    event_type=event_data.event_type,
                    distance=event_data.distance,
                    latitude=event_data.latitude,
                    longitude=event_data.longitude,
                    created_at=event_data.created_at
                ))
            return events
        except Exception:
            return []

    @staticmethod
    def get_event_by_id(event_id: str) -> ProximityEvent:
        """Get a specific proximity event by ID."""
        try:
            event_data = ProximityEventModel.get(ProximityEventModel.event_id == event_id)
            return ProximityEvent(
                event_id=event_data.event_id,
                device_id=event_data.device_id,
                location_id=event_data.location_id,
                event_type=event_data.event_type,
                distance=event_data.distance,
                latitude=event_data.latitude,
                longitude=event_data.longitude,
                created_at=event_data.created_at
            )
        except ProximityEventModel.DoesNotExist:
            return None

    @staticmethod
    def get_all_events(limit: int = 100) -> List[ProximityEvent]:
        """Get all proximity events from local database."""
        try:
            events_data = list(ProximityEventModel.select()
                             .order_by(ProximityEventModel.created_at.desc())
                             .limit(limit))
            
            events = []
            for event_data in events_data:
                events.append(ProximityEvent(
                    event_id=event_data.event_id,
                    device_id=event_data.device_id,
                    location_id=event_data.location_id,
                    event_type=event_data.event_type,
                    distance=event_data.distance,
                    latitude=event_data.latitude,
                    longitude=event_data.longitude,
                    created_at=event_data.created_at
                ))
            return events
        except Exception:
            return []