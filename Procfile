release: python manage.py collectstatic --noinput && python manage.py migrate --noinput
web: gunicorn --pythonpath PBL --bind 0.0.0.0:$PORT MEDISAFE_PBL.wsgi:application
