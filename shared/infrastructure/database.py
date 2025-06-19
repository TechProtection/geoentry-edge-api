"""Database initialization for GeoEntry Edge API."""
from peewee import SqliteDatabase
from config import get_config

# Get configuration
config = get_config()

# Initialize SQLite database
db = SqliteDatabase(config.DATABASE_URL)

def init_db() -> None:
    """Initialize database and create tables."""
    db.connect()
    from devices.infrastructure.models import Device
    from locations.infrastructure.models import Location
    from proximity_events.infrastructure.models import ProximityEvent
    db.create_tables([Device, Location, ProximityEvent], safe=True)
    db.close()