release: python manage.py migrate --noinput
web: python manage.py collectstatic --noinput && gunicorn --pythonpath PBL MEDISAFE_PBL.wsgi:application
