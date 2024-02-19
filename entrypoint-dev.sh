#!/bin/sh

if [ "$POSTGRES_DB" = "umatter" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 3
    done

    echo "PostgreSQL started"
fi

if [ "$NLP_POSTGRES_DB" = "umatter_test_db" ]; then
    echo "Waiting for NLP postgres..."

    while ! nc -z $NLP_POSTGRES_HOST $NLP_POSTGRES_PORT; do
      sleep 3
    done

    echo "NLP PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate --database=app_db
python manage.py migrate --database=nlp_db
python manage.py createsuperuser --noinput \
	--email $DJANGO_SUPERUSER_EMAIL
python manage.py collectstatic
python manage.py loaddata --database=app_db event_initial_data.json
python manage.py loaddata --database=nlp_db nlp_initial_data.json
gunicorn -b web:8000 -w 4 --threads 4 --timeout 60 --log-level 'info' umatter.wsgi:application
