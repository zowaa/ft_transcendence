#!/bin/bash

apt-get update -y && apt-get upgrade -y && apt-get install nginx -y

apt-get install openssl -y 

mkdir /etc/nginx/ssl
