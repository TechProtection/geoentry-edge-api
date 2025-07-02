"""Device repository with Supabase implementation."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from shared.supabase.client import get_supabase_client
from devices.domain.entities import Device


class DeviceSupabaseRepository:
    """Device repository using Supabase."""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.table_name = 'devices'
    
    def create(self, device: Device) -> Device:
        """Create a new device."""
        device_data = {
            'id': device.device_id,
            'name': device.name,
            'type': device.device_type,
            'profile_id': device.profile_id,
            'created_at': device.created_at.isoformat() if device.created_at else datetime.utcnow().isoformat()
        }
        
        response = self.client.table(self.table_name).insert(device_data).execute()
        
        if response.data:
            created_device = response.data[0]
            return Device(
                device_id=created_device['id'],
                name=created_device['name'],
                device_type=created_device['type'],
                profile_id=created_device['profile_id'],
                created_at=datetime.fromisoformat(created_device['created_at'].replace('Z', '+00:00')) if created_device['created_at'] else None
            )
        
        raise Exception("Failed to create device")
    
    def get_by_id(self, device_id: str) -> Optional[Device]:
        """Get device by ID."""
        response = self.client.table(self.table_name).select('*').eq('id', device_id).execute()
        
        if response.data:
            device_data = response.data[0]
            return Device(
                device_id=device_data['id'],
                name=device_data['name'],
                device_type=device_data['type'],
                profile_id=device_data['profile_id'],
                created_at=datetime.fromisoformat(device_data['created_at'].replace('Z', '+00:00')) if device_data['created_at'] else None
            )
        
        return None
    
    def get_by_profile_id(self, profile_id: str) -> List[Device]:
        """Get all devices for a profile."""
        response = self.client.table(self.table_name).select('*').eq('profile_id', profile_id).execute()
        
        devices = []
        for device_data in response.data:
            devices.append(Device(
                device_id=device_data['id'],
                name=device_data['name'],
                device_type=device_data['type'],
                profile_id=device_data['profile_id'],
                created_at=datetime.fromisoformat(device_data['created_at'].replace('Z', '+00:00')) if device_data['created_at'] else None
            ))
        
        return devices
    
    def update(self, device: Device) -> Device:
        """Update an existing device."""
        device_data = {
            'name': device.name,
            'type': device.device_type,
            'profile_id': device.profile_id
        }
        
        response = self.client.table(self.table_name).update(device_data).eq('id', device.device_id).execute()
        
        if response.data:
            updated_device = response.data[0]
            return Device(
                device_id=updated_device['id'],
                name=updated_device['name'],
                device_type=updated_device['type'],
                profile_id=updated_device['profile_id'],
                created_at=datetime.fromisoformat(updated_device['created_at'].replace('Z', '+00:00')) if updated_device['created_at'] else None
            )
        
        raise Exception("Failed to update device")
    
    def delete(self, device_id: str) -> bool:
        """Delete a device."""
        response = self.client.table(self.table_name).delete().eq('id', device_id).execute()
        return len(response.data) > 0
    
    def exists(self, device_id: str) -> bool:
        """Check if device exists."""
        response = self.client.table(self.table_name).select('id').eq('id', device_id).execute()
        return len(response.data) > 0
