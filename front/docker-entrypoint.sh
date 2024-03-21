#!/bin/sh

npm init -y

npm install express

npm install morgan

chown -R node:node /home/node/app/certs

node server.js