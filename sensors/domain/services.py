"""Domain services for Sensors context."""
from typing import List
from sensors.domain.entities import Sensor, SensorType


class SensorService:
    """Domain service for sensor business logic."""

    def validate_sensor_data(self, name: str, sensor_type: str, user_id: str) -> bool:
        """Validate sensor data."""
        if not name or not name.strip():
            return False
        
        if not user_id or not user_id.strip():
            return False
            
        try:
            SensorType(sensor_type)
            return True
        except ValueError:
            return False
    
    def validate_sensor_type(self, sensor_type: str) -> bool:
        """Validate if sensor type is supported."""
        try:
            SensorType(sensor_type)
            return True
        except ValueError:
            return False
    
    def get_sensor_type_display_name(self, sensor_type: SensorType) -> str:
        """Get human-readable name for sensor type."""
        type_names = {
            SensorType.LED_TV: "Smart TV",
            SensorType.SMART_LIGHT: "Luz Inteligente", 
            SensorType.AIR_CONDITIONER: "Aire Acondicionado",
            SensorType.COFFEE_MAKER: "Cafetera"
        }
        return type_names.get(sensor_type, sensor_type.value)
    
    def group_sensors_by_type(self, sensors: List[Sensor]) -> dict:
        """Group sensors by their type."""
        grouped = {}
        for sensor in sensors:
            sensor_type = sensor.sensor_type.value if isinstance(sensor.sensor_type, SensorType) else sensor.sensor_type
            if sensor_type not in grouped:
                grouped[sensor_type] = []
            grouped[sensor_type].append(sensor)
        return grouped
    
    def count_active_sensors(self, sensors: List[Sensor]) -> int:
        """Count active sensors."""
        return sum(1 for sensor in sensors if sensor.is_active)
    
    def get_sensors_by_status(self, sensors: List[Sensor], is_active: bool) -> List[Sensor]:
        """Filter sensors by status."""
        return [sensor for sensor in sensors if sensor.is_active == is_active]
