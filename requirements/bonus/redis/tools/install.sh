#!/bin/sh

apt-get update -y && apt-get upgrade -y

apt-get install redis-server -y
