FROM python:3.11.2

WORKDIR /app

COPY . .

RUN python3 -m venv stats_env

RUN . stats_env/bin/activate && pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && apt-get install netcat -y

EXPOSE 8004