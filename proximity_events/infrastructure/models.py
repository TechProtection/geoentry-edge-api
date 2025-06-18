"""Peewee models for Proximity Events context."""
from peewee import Model, CharField, FloatField, DateTimeField
from shared.infrastructure.database import db


class ProximityEvent(Model):
    """Proximity event database model."""
    event_id = CharField(primary_key=True)
    device_id = CharField()
    location_id = CharField()
    event_type = CharField()
    distance = FloatField()
    latitude = FloatField()
    longitude = FloatField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'proximity_events'