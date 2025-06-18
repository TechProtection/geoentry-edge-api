"""Database initialization for GeoEntry Edge API."""
from peewee import SqliteDatabase

# Initialize SQLite database
db = SqliteDatabase('geoentry.db')

def init_db() -> None:
    """Initialize database and create tables."""
    db.connect()
    from devices.infrastructure.models import Device
    from locations.infrastructure.models import Location
    from proximity_events.infrastructure.models import ProximityEvent
    db.create_tables([Device, Location, ProximityEvent], safe=True)
    db.close()