"""Domain entities for Sensors context."""
from datetime import datetime
from typing import Optional
from enum import Enum


class SensorType(Enum):
    """Enumeration of sensor types."""
    LED_TV = "led_tv"
    SMART_LIGHT = "smart_light"
    AIR_CONDITIONER = "air_conditioner"
    COFFEE_MAKER = "coffee_maker"


class Sensor:
    """Represents a smart home sensor entity."""

    def __init__(
        self, 
        id: str, 
        name: str, 
        sensor_type: SensorType, 
        is_active: bool, 
        user_id: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.sensor_type = sensor_type
        self.is_active = is_active
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def activate(self):
        """Activate the sensor."""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self):
        """Deactivate the sensor."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def update_status(self, is_active: bool):
        """Update sensor status."""
        self.is_active = is_active
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'sensor_type': self.sensor_type.value if isinstance(self.sensor_type, SensorType) else self.sensor_type,
            'isActive': self.is_active,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
