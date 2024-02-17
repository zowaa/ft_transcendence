#!/bin/sh
# Check if the DATABASE environment variable is set to "postgres"
if [ "$DATABASE" = "postgres" ]; then
    # Wait for PostgreSQL to become available
    echo "Waiting for PostgreSQL..."
    while ! nc -z $PSQL_HOST $PSQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi
#https://copyprogramming.com/howto/how-to-use-netcat-to-check-whether-postgresql-docker-container-is-up

# Perform database migrations and superuser creation
echo "Applying database migrations..."
python manage.py migrate --no-input
echo "Creating superuser..."
python manage.py createsuperuser --no-input --username $DJANGO_SUPERUSER_USERNAME --display_name $DJANGO_SUPERUSER_DISPLAY_NAME

# Start the Django development server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
