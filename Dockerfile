FROM python:3.11.2

WORKDIR /app

COPY ["backend", "/app/backend"]
COPY ["django-env", "/app/django-env"]
COPY ["users", "/app/users"]
COPY ["docker-entrypoint.sh", "manage.py", "requirements.txt", "/app/"]

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && apt-get install netcat -y

EXPOSE 8000