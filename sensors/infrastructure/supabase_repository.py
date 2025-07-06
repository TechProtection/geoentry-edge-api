"""Sensor repository with Supabase implementation."""

from typing import List, Optional
from datetime import datetime
from shared.supabase.client import get_supabase_client
from sensors.domain.entities import Sensor, SensorType


class SensorSupabaseRepository:
    """Sensor repository using Supabase."""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.table_name = 'sensors'
    
    def get_by_id(self, sensor_id: str) -> Optional[Sensor]:
        """Get sensor by ID."""
        response = self.client.table(self.table_name).select('*').eq('id', sensor_id).execute()
        
        if response.data:
            sensor_data = response.data[0]
            return self._map_to_entity(sensor_data)
        
        return None
    
    def get_by_user_id(self, user_id: str) -> List[Sensor]:
        """Get all sensors for a user."""
        response = self.client.table(self.table_name).select('*').eq('user_id', user_id).execute()
        
        sensors = []
        if response.data:
            for sensor_data in response.data:
                sensor = self._map_to_entity(sensor_data)
                if sensor:
                    sensors.append(sensor)
        
        return sensors
    
    def update_status(self, sensor_id: str, is_active: bool) -> Optional[Sensor]:
        """Update sensor status."""
        update_data = {
            'isActive': is_active,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        response = self.client.table(self.table_name).update(update_data).eq('id', sensor_id).execute()
        
        if response.data:
            sensor_data = response.data[0]
            return self._map_to_entity(sensor_data)
        
        return None
    
    def exists(self, sensor_id: str) -> bool:
        """Check if sensor exists."""
        response = self.client.table(self.table_name).select('id').eq('id', sensor_id).execute()
        return len(response.data) > 0
    
    def get_active_sensors_by_user(self, user_id: str) -> List[Sensor]:
        """Get all active sensors for a user."""
        response = self.client.table(self.table_name).select('*').eq('user_id', user_id).eq('isActive', True).execute()
        
        sensors = []
        if response.data:
            for sensor_data in response.data:
                sensor = self._map_to_entity(sensor_data)
                if sensor:
                    sensors.append(sensor)
        
        return sensors
    
    def get_sensors_by_type(self, user_id: str, sensor_type: str) -> List[Sensor]:
        """Get sensors by type for a user."""
        response = self.client.table(self.table_name).select('*').eq('user_id', user_id).eq('sensor_type', sensor_type).execute()
        
        sensors = []
        if response.data:
            for sensor_data in response.data:
                sensor = self._map_to_entity(sensor_data)
                if sensor:
                    sensors.append(sensor)
        
        return sensors
    
    def _map_to_entity(self, sensor_data: dict) -> Optional[Sensor]:
        """Map database data to Sensor entity."""
        try:
            sensor_type = SensorType(sensor_data['sensor_type'])
            
            created_at = None
            updated_at = None
            
            if sensor_data.get('created_at'):
                created_at = datetime.fromisoformat(sensor_data['created_at'].replace('Z', '+00:00'))
            
            if sensor_data.get('updated_at'):
                updated_at = datetime.fromisoformat(sensor_data['updated_at'].replace('Z', '+00:00'))
            
            return Sensor(
                id=sensor_data['id'],
                name=sensor_data['name'],
                sensor_type=sensor_type,
                is_active=sensor_data['isActive'],
                user_id=sensor_data['user_id'],
                created_at=created_at,
                updated_at=updated_at
            )
        except (KeyError, ValueError) as e:
            print(f"Error mapping sensor data: {e}")
            return None
