"""Location repository with Supabase implementation."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from shared.supabase.client import get_supabase_client
from locations.domain.entities import Location


class LocationSupabaseRepository:
    """Location repository using Supabase."""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.table_name = 'locations'
    
    def create(self, location: Location) -> Location:
        """Create a new location."""
        location_data = {
            'id': location.location_id,
            'name': location.name,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'radius': location.radius,
            'profile_id': location.profile_id,
            'address': location.address,
            'is_active': location.is_active,
            'created_at': location.created_at.isoformat() if location.created_at else datetime.utcnow().isoformat()
        }
        
        response = self.client.table(self.table_name).insert(location_data).execute()
        
        if response.data:
            created_location = response.data[0]
            return Location(
                location_id=created_location['id'],
                name=created_location['name'],
                latitude=created_location['latitude'],
                longitude=created_location['longitude'],
                radius=created_location['radius'],
                profile_id=created_location['profile_id'],
                address=created_location['address'],
                is_active=created_location['is_active'],
                created_at=datetime.fromisoformat(created_location['created_at'].replace('Z', '+00:00')) if created_location['created_at'] else None
            )
        
        raise Exception("Failed to create location")
    
    def get_by_id(self, location_id: str) -> Optional[Location]:
        """Get location by ID."""
        response = self.client.table(self.table_name).select('*').eq('id', location_id).execute()
        
        if response.data:
            location_data = response.data[0]
            return Location(
                location_id=location_data['id'],
                name=location_data['name'],
                latitude=location_data['latitude'],
                longitude=location_data['longitude'],
                radius=location_data['radius'],
                profile_id=location_data['profile_id'],
                address=location_data['address'],
                is_active=location_data['is_active'],
                created_at=datetime.fromisoformat(location_data['created_at'].replace('Z', '+00:00')) if location_data['created_at'] else None
            )
        
        return None
    
    def get_by_profile_id(self, profile_id: str) -> List[Location]:
        """Get all locations for a profile."""
        response = self.client.table(self.table_name).select('*').eq('profile_id', profile_id).execute()
        
        locations = []
        for location_data in response.data:
            locations.append(Location(
                location_id=location_data['id'],
                name=location_data['name'],
                latitude=location_data['latitude'],
                longitude=location_data['longitude'],
                radius=location_data['radius'],
                profile_id=location_data['profile_id'],
                address=location_data['address'],
                is_active=location_data['is_active'],
                created_at=datetime.fromisoformat(location_data['created_at'].replace('Z', '+00:00')) if location_data['created_at'] else None
            ))
        
        return locations
    
    def get_active_locations(self, profile_id: str) -> List[Location]:
        """Get all active locations for a profile."""
        response = self.client.table(self.table_name).select('*').eq('profile_id', profile_id).eq('is_active', True).execute()
        
        locations = []
        for location_data in response.data:
            locations.append(Location(
                location_id=location_data['id'],
                name=location_data['name'],
                latitude=location_data['latitude'],
                longitude=location_data['longitude'],
                radius=location_data['radius'],
                profile_id=location_data['profile_id'],
                address=location_data['address'],
                is_active=location_data['is_active'],
                created_at=datetime.fromisoformat(location_data['created_at'].replace('Z', '+00:00')) if location_data['created_at'] else None
            ))
        
        return locations
    
    def update(self, location: Location) -> Location:
        """Update an existing location."""
        location_data = {
            'name': location.name,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'radius': location.radius,
            'address': location.address,
            'is_active': location.is_active
        }
        
        response = self.client.table(self.table_name).update(location_data).eq('id', location.location_id).execute()
        
        if response.data:
            updated_location = response.data[0]
            return Location(
                location_id=updated_location['id'],
                name=updated_location['name'],
                latitude=updated_location['latitude'],
                longitude=updated_location['longitude'],
                radius=updated_location['radius'],
                profile_id=updated_location['profile_id'],
                address=updated_location['address'],
                is_active=updated_location['is_active'],
                created_at=datetime.fromisoformat(updated_location['created_at'].replace('Z', '+00:00')) if updated_location['created_at'] else None
            )
        
        raise Exception("Failed to update location")
    
    def delete(self, location_id: str) -> bool:
        """Delete a location."""
        response = self.client.table(self.table_name).delete().eq('id', location_id).execute()
        return len(response.data) > 0
    
    def exists(self, location_id: str) -> bool:
        """Check if location exists."""
        response = self.client.table(self.table_name).select('id').eq('id', location_id).execute()
        return len(response.data) > 0
