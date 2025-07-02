"""Configuration settings for GeoEntry Edge API."""

import os

class Config:
    """Base configuration class."""
    
    # Supabase configuration
    SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://njrccrvfsnmvnbwvlvey.supabase.co')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5qcmNjcnZmc25tdm5id3ZsdmV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcxNTQ4NjEsImV4cCI6MjA2MjczMDg2MX0.BsxMyKpmDqcxgMVkJeLNT0JAKj5epWTJnUOZx6auPmU')
    
    # Flask configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

def get_config():
    """Get configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig()
    return DevelopmentConfig()
