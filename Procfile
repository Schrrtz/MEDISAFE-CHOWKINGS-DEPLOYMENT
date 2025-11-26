release: python manage.py migrate --noinput
web: python manage.py collectstatic --noinput --clear && gunicorn --pythonpath PBL --bind 0.0.0.0:$PORT MEDISAFE_PBL.wsgi:application
