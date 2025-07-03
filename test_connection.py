#!/usr/bin/env python3
"""Test script for Supabase connection."""

try:
    print("Testing Supabase connection...")
    from shared.infrastructure.database import init_db
    print("Import successful!")
    
    result = init_db()
    print(f"Connection result: {result}")
    
    if result:
        print("✅ All tests passed! The API is ready to use with Supabase.")
    else:
        print("❌ Connection failed!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
