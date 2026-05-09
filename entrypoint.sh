#!/bin/bash
set -e

echo "Starting Simbin application..."

# Collect static files (with error handling)
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static files collection skipped (no static files found)"

# Start the application
echo "Starting Gunicorn server..."
exec "$@"
