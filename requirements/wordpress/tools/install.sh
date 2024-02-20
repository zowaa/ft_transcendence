#!/bin/sh

apt-get update -y && apt-get upgrade -y

apt-get install -y curl php8.2-fpm php-mysql php8.2-redis
