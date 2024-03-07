FROM node:10-alpine

RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

WORKDIR /home/node/app

COPY package*.json ./

USER node

RUN npm install

COPY --chown=node:node . .
# COPY --chown=node:node Frontend/ /home/node/app/Frontend/
# COPY --chown=node:node index.html /home/node/app/index.html
# COPY --chown=node:node server.js /home/node/app/server.js

EXPOSE 8080