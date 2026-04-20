#!/usr/bin/env bash
# Render.com startup script for Django + FastAPI application

set -e

echo "Starting Django application on Render..."

# Set environment variables for Render deployment
export RENDER=1
export DEBUG=False

# Check if PORT is set by Render, default to 10000 if not
if [ -z "$PORT" ]; then
    export PORT=10000
fi

# Calculate FastAPI port to avoid conflicts
FASTAPI_PORT=$((PORT + 1000))
echo "Django will run on port: $PORT"
echo "FastAPI will auto-start on port: $FASTAPI_PORT"

# Start Django with proper host and port binding for Render
exec python manage.py runserver 0.0.0.0:$PORT