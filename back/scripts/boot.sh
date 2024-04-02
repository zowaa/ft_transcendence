#!/bin/bash
set -e

echo "backend:boot:env:${APP_ENVIRONMENT}"

python manage.py makemigrations
python manage.py makemigrations users.Friends

python manage.py migrate
python manage.py collectstatic --noinput

if [ "$APP_ENVIRONMENT" == "Local" ]; then
  echo "backend:run:local" && python manage.py runserver 0.0.0.0:8000 --insecure
fi

if [ "$APP_ENVIRONMENT" == "Production" ]; then
  echo "backend:run:prod" && /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisor-backend.conf
fi        