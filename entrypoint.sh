#!/bin/bash
set -e

echo "Starting Simbin application..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "Starting Gunicorn server..."
exec "$@"
