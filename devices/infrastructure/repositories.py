"""Repositories for Devices context."""
from typing import Optional
from datetime import datetime
import requests
from peewee import DoesNotExist
from devices.domain.entities import Device
from devices.infrastructure.models import Device as DeviceModel

BACKEND_URL = "http://localhost:3000/api"  # URL de tu backend

class DeviceRepository:
    """Repository for device operations."""

    @staticmethod
    def find_by_id_and_key(device_id: str, api_key: str) -> Optional[Device]:
        """Find device by ID and API key with fallback to test stub."""
        # 1. Try local cache
        try:
            device = DeviceModel.get(
                (DeviceModel.device_id == device_id) &
                (DeviceModel.api_key == api_key)
            )
            return Device(
                device_id=device.device_id,
                api_key=device.api_key,
                profile_id=device.profile_id,
                created_at=device.created_at
            )
        except DoesNotExist:
            # 2. Test device stub
            if device_id == "smart-band-001" and api_key == "test-api-key-123":
                # Create test device in local cache
                DeviceModel.create(
                    device_id="smart-band-001",
                    api_key="test-api-key-123",
                    profile_id="test-profile",
                    created_at=datetime.now()
                )
                return Device(
                    device_id="smart-band-001",
                    api_key="test-api-key-123",
                    profile_id="test-profile",
                    created_at=datetime.now()
                )

            # 3. Try backend with connection error handling
            try:
                response = requests.get(
                    f"{BACKEND_URL}/devices/{device_id}",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=2  # Agregar timeout
                )
                if response.status_code == 200:
                    device_data = response.json()
                    DeviceModel.create(
                        device_id=device_id,
                        api_key=api_key,
                        profile_id=device_data.get("profile_id"),
                        created_at=device_data.get("created_at")
                    )
                    return Device(
                        device_id=device_id,
                        api_key=api_key,
                        profile_id=device_data.get("profile_id"),
                        created_at=device_data.get("created_at")
                    )
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                return None

            return None