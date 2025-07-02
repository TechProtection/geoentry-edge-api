"""Application services for Devices context."""
from typing import List, Optional
from devices.domain.entities import Device
from devices.domain.services import DeviceService
from devices.infrastructure.supabase_repository import DeviceSupabaseRepository


class DeviceApplicationService:
    """Application service for device management."""

    def __init__(self):
        self.repository = DeviceSupabaseRepository()
        self.device_service = DeviceService()

    def create_device(self, device_id: str, name: str, device_type: str, profile_id: str) -> Device:
        """Create a new device."""
        if not self.device_service.validate_device_data(device_id, name, device_type, profile_id):
            raise ValueError("Invalid device data")
            
        if self.repository.exists(device_id):
            raise ValueError(f"Device with ID {device_id} already exists")
        
        device = Device(
            device_id=device_id,
            name=name,
            device_type=device_type,
            profile_id=profile_id
        )
        
        return self.repository.create(device)
    
    def get_device(self, device_id: str) -> Optional[Device]:
        """Get device by ID."""
        return self.repository.get_by_id(device_id)
    
    def get_devices_by_profile(self, profile_id: str) -> List[Device]:
        """Get all devices for a profile."""
        return self.repository.get_by_profile_id(profile_id)
    
    def update_device(self, device_id: str, name: str = None, device_type: str = None) -> Device:
        """Update device information."""
        device = self.repository.get_by_id(device_id)
        if not device:
            raise ValueError(f"Device with ID {device_id} not found")
        
        if name:
            device.name = name
        if device_type:
            device.device_type = device_type
        
        return self.repository.update(device)
    
    def delete_device(self, device_id: str) -> bool:
        """Delete a device."""
        return self.repository.delete(device_id)
    
    def device_exists(self, device_id: str) -> bool:
        """Check if device exists."""
        return self.repository.exists(device_id)