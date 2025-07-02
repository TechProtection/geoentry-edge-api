#!/usr/bin/env bash
# Build script for Render deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Testing Supabase connection..."
python -c "
from shared.infrastructure.database import init_db
if init_db():
    print('✅ Supabase connection test passed')
else:
    print('❌ Supabase connection test failed')
    exit(1)
"

echo "Build completed successfully!"
