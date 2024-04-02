#!/bin/sh

# waiting for postgres to be ready
while ! nc -z postgres 5432; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 1
done

python3 manage.py makemigrations users
python3 manage.py migrate
# python3 manage.py runserver 0.0.0.0:8000
python3 manage.py runsslserver 0.0.0.0:8001