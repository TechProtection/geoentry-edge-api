"""Configuration settings for GeoEntry Edge API."""

import os

class Config:
    """Base configuration class."""
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'geoentry.db')
    
    # Flask configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # API configuration
    API_BASE_URL = os.environ.get('API_BASE_URL', 'https://geoentry-rest-api.onrender.com/api')
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URL = 'geoentry.db'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, we'll use SQLite but could be extended for PostgreSQL
    DATABASE_URL = os.environ.get('DATABASE_URL', '/opt/render/project/src/geoentry.db')

def get_config():
    """Get configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig()
    return DevelopmentConfig()
