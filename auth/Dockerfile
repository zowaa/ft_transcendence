FROM python:3.11.2

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && apt-get install netcat -y

EXPOSE 8000