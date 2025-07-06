"""Application services for Sensors context."""
from typing import List, Optional
from sensors.domain.entities import Sensor
from sensors.domain.services import SensorService
from sensors.infrastructure.supabase_repository import SensorSupabaseRepository


class SensorApplicationService:
    """Application service for sensor management."""

    def __init__(self):
        self.repository = SensorSupabaseRepository()
        self.sensor_service = SensorService()

    def get_sensor(self, sensor_id: str) -> Optional[Sensor]:
        """Get sensor by ID."""
        return self.repository.get_by_id(sensor_id)
    
    def get_sensors_by_user(self, user_id: str) -> List[Sensor]:
        """Get all sensors for a user."""
        if not user_id or not user_id.strip():
            raise ValueError("User ID is required")
        
        return self.repository.get_by_user_id(user_id)
    
    def get_active_sensors_by_user(self, user_id: str) -> List[Sensor]:
        """Get all active sensors for a user."""
        if not user_id or not user_id.strip():
            raise ValueError("User ID is required")
        
        return self.repository.get_active_sensors_by_user(user_id)
    
    def get_sensors_by_type(self, user_id: str, sensor_type: str) -> List[Sensor]:
        """Get sensors by type for a user."""
        if not user_id or not user_id.strip():
            raise ValueError("User ID is required")
        
        if not self.sensor_service.validate_sensor_type(sensor_type):
            raise ValueError(f"Invalid sensor type: {sensor_type}")
        
        return self.repository.get_sensors_by_type(user_id, sensor_type)
    
    def update_sensor_status(self, sensor_id: str, is_active: bool) -> Sensor:
        """Update sensor status (activate/deactivate)."""
        if not sensor_id or not sensor_id.strip():
            raise ValueError("Sensor ID is required")
        
        # Verify sensor exists
        existing_sensor = self.repository.get_by_id(sensor_id)
        if not existing_sensor:
            raise ValueError(f"Sensor with ID {sensor_id} not found")
        
        # Update status
        updated_sensor = self.repository.update_status(sensor_id, is_active)
        if not updated_sensor:
            raise Exception("Failed to update sensor status")
        
        return updated_sensor
    
    def get_sensor_statistics(self, user_id: str) -> dict:
        """Get sensor statistics for a user."""
        if not user_id or not user_id.strip():
            raise ValueError("User ID is required")
        
        sensors = self.repository.get_by_user_id(user_id)
        
        total_sensors = len(sensors)
        active_sensors = self.sensor_service.count_active_sensors(sensors)
        inactive_sensors = total_sensors - active_sensors
        
        grouped_by_type = self.sensor_service.group_sensors_by_type(sensors)
        
        return {
            'total_sensors': total_sensors,
            'active_sensors': active_sensors,
            'inactive_sensors': inactive_sensors,
            'sensors_by_type': {
                sensor_type: len(type_sensors) 
                for sensor_type, type_sensors in grouped_by_type.items()
            }
        }
