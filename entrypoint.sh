#!/bin/sh

if [ "$POSTGRES_DB" = "umatter" ];
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 3
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata event_initial_data.json
# python manage.py runserver localhost:8000

exec "$@"