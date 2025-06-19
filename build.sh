#!/usr/bin/env bash
# Build script for Render deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python -c "from shared.infrastructure.database import init_db; init_db()"

echo "Build completed successfully!"
