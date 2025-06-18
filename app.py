"""Flask application entry point for GeoEntry Edge API."""

from flask import Flask
from devices.interfaces.services import device_api
from locations.interfaces.services import location_api
from proximity_events.interfaces.services import proximity_event_api
from shared.infrastructure.database import init_db

app = Flask(__name__)
app.register_blueprint(device_api)
app.register_blueprint(location_api)
app.register_blueprint(proximity_event_api)

@app.before_request
def initialize():
    """Initialize database on first request."""
    init_db()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)