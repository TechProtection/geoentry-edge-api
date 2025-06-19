"""Flask application entry point for GeoEntry Edge API."""

from flask import Flask
from devices.interfaces.services import device_api
from locations.interfaces.services import location_api
from proximity_events.interfaces.services import proximity_event_api
from shared.infrastructure.database import init_db
from config import get_config

# Get configuration
config = get_config()

app = Flask(__name__)
app.register_blueprint(device_api)
app.register_blueprint(location_api)
app.register_blueprint(proximity_event_api)

@app.before_request
def initialize():
    """Initialize database on first request."""
    init_db()

@app.route('/')
def health_check():
    """Health check endpoint for Render."""
    return {"status": "healthy", "service": "GeoEntry Edge API"}, 200

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)