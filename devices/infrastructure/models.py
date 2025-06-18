"""Peewee models for Devices context."""
from peewee import Model, CharField, DateTimeField
from shared.infrastructure.database import db


class Device(Model):
    """Device database model."""
    device_id = CharField(primary_key=True)
    api_key = CharField()
    profile_id = CharField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'devices'