"""Peewee models for Locations context."""
from peewee import Model, CharField, FloatField, DateTimeField
from shared.infrastructure.database import db


class Location(Model):
    """Location database model."""
    location_id = CharField(primary_key=True)
    name = CharField()
    latitude = FloatField()
    longitude = FloatField()
    radius = FloatField()
    profile_id = CharField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'locations'