#!/usr/bin/env bash
# Render.com build script for Django application

set -e  # Exit on any error

echo "Starting Django build process..."

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