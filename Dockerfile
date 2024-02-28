FROM python:3.11.2

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=backend.settings

# CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]`