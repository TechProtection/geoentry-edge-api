"""Database initialization for GeoEntry Edge API with Supabase."""
from shared.supabase.client import get_supabase_client

def init_db() -> bool:
    """Initialize connection to Supabase."""
    # With Supabase, tables are already created via migrations
    # This function now just ensures we can connect
    client = get_supabase_client()
    
    # Test connection by making a simple query
    try:
        response = client.table('profiles').select('id').limit(1).execute()
        print("✅ Supabase connection successful")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False