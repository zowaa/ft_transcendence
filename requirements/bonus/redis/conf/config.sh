#!/bin/sh

echo "maxmemory 250mb
maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf

sed -i "s/bind 127.0.0.1/#bind 127.0.0.1/" /etc/redis/redis.conf

exec redis-server --protected-mode no
