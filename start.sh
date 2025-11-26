#!/bin/bash
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting gunicorn..."
exec gunicorn --pythonpath PBL --bind 0.0.0.0:$PORT MEDISAFE_PBL.wsgi:application
