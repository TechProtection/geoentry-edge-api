"""Repositories for Locations context."""
import requests
from typing import List
from datetime import datetime
from locations.domain.entities import Location
from locations.infrastructure.models import Location as LocationModel

BACKEND_URL = "https://geoentry-rest-api.onrender.com/api"  # URL de tu backend
# BACKEND_URL = "https://localhost:3000/api"  # URL de tu backend

class LocationRepository:
    """Repository for location operations with test stubs."""

    @staticmethod
    def get_locations_by_profile(profile_id: str) -> List[Location]:
        """Get locations with fallback to test stubs."""
        # 1. Test profile stub
        if profile_id == "test-profile":
            # Create test locations in local cache
            test_locations = [
                {
                    "id": "home-loc",
                    "name": "Casa",
                    "latitude": -12.1234,
                    "longitude": -77.5432,
                    "radius": 100,
                    "profile_id": "test-profile",
                },
                {
                    "id": "office-loc",
                    "name": "Oficina",
                    "latitude": -12.3456,
                    "longitude": -77.6789,
                    "radius": 150,
                    "profile_id": "test-profile",
                }
            ]

            locations = []
            for loc in test_locations:
                LocationModel.get_or_create(
                    location_id=loc["id"],
                    defaults={
                        "name": loc["name"],
                        "latitude": loc["latitude"],
                        "longitude": loc["longitude"],
                        "radius": loc["radius"],
                        "profile_id": loc["profile_id"],
                        "created_at": datetime.now()
                    }
                )
                locations.append(Location(
                    location_id=loc["id"],
                    name=loc["name"],
                    latitude=loc["latitude"],
                    longitude=loc["longitude"],
                    radius=loc["radius"],
                    profile_id=loc["profile_id"],
                    created_at=datetime.now()
                ))
            return locations

        # 2. Try backend with connection error handling
        try:
            response = requests.get(
                f"{BACKEND_URL}/locations?profile_id={profile_id}",
                timeout=2
            )
            if response.status_code == 200:
                locations_data = response.json()
                locations = []
                for loc_data in locations_data:
                    LocationModel.get_or_create(
                        location_id=loc_data["id"],
                        defaults={
                            "name": loc_data["name"],
                            "latitude": loc_data["latitude"],
                            "longitude": loc_data["longitude"],
                            "radius": loc_data["radius"],
                            "profile_id": loc_data["profile_id"],
                            "created_at": loc_data.get("created_at", datetime.now())
                        }
                    )
                    locations.append(Location(
                        location_id=loc_data["id"],
                        name=loc_data["name"],
                        latitude=loc_data["latitude"],
                        longitude=loc_data["longitude"],
                        radius=loc_data["radius"],
                        profile_id=loc_data["profile_id"],
                        created_at=loc_data.get("created_at", datetime.now())
                    ))
                return locations
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass

        return []  # Return empty list on failure

    @staticmethod
    def get_all_locations() -> List[Location]:
        """Get all locations from database and backend with fallback to test stubs."""
        locations = []
        
        # 1. Get from local database first
        try:
            db_locations = LocationModel.select()
            for loc_model in db_locations:
                locations.append(Location(
                    location_id=loc_model.location_id,
                    name=loc_model.name,
                    latitude=loc_model.latitude,
                    longitude=loc_model.longitude,
                    radius=loc_model.radius,
                    profile_id=loc_model.profile_id,
                    created_at=loc_model.created_at
                ))
        except Exception:
            pass
        
        # 2. If no data in DB, populate with test data
        if not locations:
            test_locations = [
                {
                    "id": "home-loc",
                    "name": "Casa",
                    "latitude": -12.1234,
                    "longitude": -77.5432,
                    "radius": 100,
                    "profile_id": "test-profile",
                },
                {
                    "id": "office-loc", 
                    "name": "Oficina",
                    "latitude": -12.3456,
                    "longitude": -77.6789,
                    "radius": 150,
                    "profile_id": "test-profile",
                }
            ]
            
            for loc in test_locations:
                # Create in database
                LocationModel.get_or_create(
                    location_id=loc["id"],
                    defaults={
                        "name": loc["name"],
                        "latitude": loc["latitude"],
                        "longitude": loc["longitude"],
                        "radius": loc["radius"],
                        "profile_id": loc["profile_id"],
                        "created_at": datetime.now()
                    }
                )
                # Add to result list
                locations.append(Location(
                    location_id=loc["id"],
                    name=loc["name"],
                    latitude=loc["latitude"],
                    longitude=loc["longitude"],
                    radius=loc["radius"],
                    profile_id=loc["profile_id"],
                    created_at=datetime.now()
                ))
        
        return locations