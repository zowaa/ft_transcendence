FROM node:10-alpine

RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

WORKDIR /home/node/app

COPY . .

USER root

RUN ./config.sh

RUN chown -R node:node .

USER node

EXPOSE 443