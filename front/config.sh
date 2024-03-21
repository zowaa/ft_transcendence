#!/bin/sh

npm install

apk add openssl && mkdir certs

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem -subj "/C=MO/L=BG/O=1337/CN=TR"