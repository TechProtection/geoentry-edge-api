"""Supabase client configuration for GeoEntry Edge API."""

from supabase import create_client, Client
from config import get_config

# Get configuration
config = get_config()

# Initialize Supabase client
supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def get_supabase_client() -> Client:
    """Get the Supabase client instance."""
    return supabase
