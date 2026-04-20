#!/usr/bin/env bash
# Render.com build script for Django Todo Orchestrator

set -e  # Exit on any error

echo "Starting Django Todo Orchestrator build process..."

# Ensure shell scripts are executable
echo "Setting script permissions..."
chmod +x build.sh start.sh

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files for production
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build process completed successfully!"