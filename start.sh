#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting gunicorn..."
gunicorn --pythonpath PBL --bind 0.0.0.0:$PORT MEDISAFE_PBL.wsgi:application
