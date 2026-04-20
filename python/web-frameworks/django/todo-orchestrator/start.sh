#!/usr/bin/env bash
# Render.com startup script for Django Todo Orchestrator

set -e

echo "Starting Django Todo Orchestrator on Render..."

# Set environment variables for Render deployment
export RENDER=1
export DEBUG=False

# Check if PORT is set by Render, default to 10000 if not
if [ -z "$PORT" ]; then
    export PORT=10000
fi

echo "Django Todo Orchestrator will run on port: $PORT"

# Verify gunicorn is installed
echo "Checking gunicorn installation..."
which gunicorn || echo "gunicorn not found in PATH"
python -m pip show gunicorn || echo "gunicorn package not found"

# Check if we can import the WSGI application
echo "Testing WSGI application import..."
python -c "from todo_orchestrator.wsgi import application; print('WSGI application import successful')"

# Run Django checks
echo "Running Django system checks..."
python manage.py check --deploy

# Start Django application with gunicorn
echo "Starting gunicorn server on 0.0.0.0:$PORT..."
exec python -m gunicorn --bind "0.0.0.0:$PORT" --workers 2 --timeout 120 --access-logfile - --error-logfile - todo_orchestrator.wsgi:application