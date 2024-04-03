FROM python:3.11.2

WORKDIR /app

COPY . .

RUN python3 -m venv matchmaking_env 

RUN . matchmaking_env/bin/activate && pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && apt-get install netcat -y

EXPOSE 8003