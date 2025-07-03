"""Proximity Event repository with Supabase implementation."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from shared.supabase.client import get_supabase_client
from proximity_events.domain.entities import ProximityEvent


class ProximityEventSupabaseRepository:
    """Proximity Event repository using Supabase."""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.table_name = 'proximity_events'
    
    def create(self, event: ProximityEvent) -> ProximityEvent:
        """Create a new proximity event."""
        event_data = {
            'id': event.event_id,
            'device_id': event.device_id,
            'home_location_id': event.home_location_id,
            'home_location_name': event.home_location_name,
            'type': event.event_type,
            'distance': event.distance,
            'latitude': event.latitude,
            'longitude': event.longitude,
            'user_id': event.user_id,
            'created_at': event.created_at.isoformat() if event.created_at else datetime.utcnow().isoformat()
        }
        
        response = self.client.table(self.table_name).insert(event_data).execute()
        
        if response.data:
            created_event = response.data[0]
            return ProximityEvent(
                event_id=created_event['id'],
                device_id=created_event['device_id'],
                home_location_id=created_event['home_location_id'],
                home_location_name=created_event['home_location_name'],
                event_type=created_event['type'],
                distance=created_event['distance'],
                latitude=created_event['latitude'],
                longitude=created_event['longitude'],
                user_id=created_event['user_id'],
                created_at=datetime.fromisoformat(created_event['created_at'].replace('Z', '+00:00')) if created_event['created_at'] else None
            )
        
        raise Exception("Failed to create proximity event")
    
    def get_by_id(self, event_id: str) -> Optional[ProximityEvent]:
        """Get proximity event by ID."""
        response = self.client.table(self.table_name).select('*').eq('id', event_id).execute()
        
        if response.data:
            event_data = response.data[0]
            return ProximityEvent(
                event_id=event_data['id'],
                device_id=event_data['device_id'],
                home_location_id=event_data['home_location_id'],
                home_location_name=event_data['home_location_name'],
                event_type=event_data['type'],
                distance=event_data['distance'],
                latitude=event_data['latitude'],
                longitude=event_data['longitude'],
                user_id=event_data['user_id'],
                created_at=datetime.fromisoformat(event_data['created_at'].replace('Z', '+00:00')) if event_data['created_at'] else None
            )
        
        return None
    
    def get_by_device_id(self, device_id: str, limit: int = 100) -> List[ProximityEvent]:
        """Get proximity events by device ID."""
        response = self.client.table(self.table_name).select('*').eq('device_id', device_id).order('created_at', desc=True).limit(limit).execute()
        
        events = []
        for event_data in response.data:
            events.append(ProximityEvent(
                event_id=event_data['id'],
                device_id=event_data['device_id'],
                home_location_id=event_data['home_location_id'],
                home_location_name=event_data['home_location_name'],
                event_type=event_data['type'],
                distance=event_data['distance'],
                latitude=event_data['latitude'],
                longitude=event_data['longitude'],
                user_id=event_data['user_id'],
                created_at=datetime.fromisoformat(event_data['created_at'].replace('Z', '+00:00')) if event_data['created_at'] else None
            ))
        
        return events
    
    def get_by_user_id(self, user_id: str, limit: int = 100) -> List[ProximityEvent]:
        """Get proximity events by user ID."""
        response = self.client.table(self.table_name).select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
        
        events = []
        for event_data in response.data:
            events.append(ProximityEvent(
                event_id=event_data['id'],
                device_id=event_data['device_id'],
                home_location_id=event_data['home_location_id'],
                home_location_name=event_data['home_location_name'],
                event_type=event_data['type'],
                distance=event_data['distance'],
                latitude=event_data['latitude'],
                longitude=event_data['longitude'],
                user_id=event_data['user_id'],
                created_at=datetime.fromisoformat(event_data['created_at'].replace('Z', '+00:00')) if event_data['created_at'] else None
            ))
        
        return events
    
    def get_by_location_id(self, location_id: str, limit: int = 100) -> List[ProximityEvent]:
        """Get proximity events by location ID."""
        response = self.client.table(self.table_name).select('*').eq('home_location_id', location_id).order('created_at', desc=True).limit(limit).execute()
        
        events = []
        for event_data in response.data:
            events.append(ProximityEvent(
                event_id=event_data['id'],
                device_id=event_data['device_id'],
                home_location_id=event_data['home_location_id'],
                home_location_name=event_data['home_location_name'],
                event_type=event_data['type'],
                distance=event_data['distance'],
                latitude=event_data['latitude'],
                longitude=event_data['longitude'],
                user_id=event_data['user_id'],
                created_at=datetime.fromisoformat(event_data['created_at'].replace('Z', '+00:00')) if event_data['created_at'] else None
            ))
        
        return events
    
    def delete(self, event_id: str) -> bool:
        """Delete a proximity event."""
        response = self.client.table(self.table_name).delete().eq('id', event_id).execute()
        return len(response.data) > 0
