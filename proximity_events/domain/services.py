"""Domain services for Proximity Events context."""
from datetime import datetime
from typing import Optional
from .entities import ProximityEvent


class ProximityEventService:
    """Service for proximity events."""

    @staticmethod
    def validate_event_data(device_id: str, home_location_id: str, home_location_name: str,
                           event_type: str, distance: float, latitude: float, longitude: float) -> bool:
        """Validate proximity event data."""
        if not device_id or not device_id.strip():
            return False
        if not home_location_id or not home_location_id.strip():
            return False
        if not home_location_name or not home_location_name.strip():
            return False
        if not event_type or event_type not in ['ENTER', 'EXIT', 'STAY']:
            return False
        if distance < 0:
            return False
        if latitude < -90 or latitude > 90:
            return False
        if longitude < -180 or longitude > 180:
            return False
        return True

    @staticmethod
    def determine_event_type(current_distance: float, radius: float, 
                           previous_distance: Optional[float] = None) -> str:
        """Determine the type of proximity event based on distances."""
        is_inside = current_distance <= radius
        
        if previous_distance is None:
            return "ENTER" if is_inside else "EXIT"
        
        was_inside = previous_distance <= radius
        
        if not was_inside and is_inside:
            return "ENTER"
        elif was_inside and not is_inside:
            return "EXIT"
        else:
            return "STAY"