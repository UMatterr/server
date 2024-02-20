#!/bin/sh

if [ "$POSTGRES_DB" = "umatter" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 3
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput \
	--email $DJANGO_SUPERUSER_EMAIL
python manage.py collectstatic
python manage.py loaddata event_initial_data.json
gunicorn -w 4 \
  -b web:8000 \
  --threads 4 \
  --timeout 60 \
  --log-level 'info' \
  umatter.wsgi:application
