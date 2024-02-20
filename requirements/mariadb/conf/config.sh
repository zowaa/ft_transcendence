#!/bin/sh

service mariadb start

mysql -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DB_NAME;CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';GRANT ALL PRIVILEGES ON $MYSQL_DB_NAME.* to '$MYSQL_USER'@'%';FLUSH PRIVILEGES"

sed -i "s/bind-address            = 127.0.0.1/bind-address	= 0.0.0.0/1" /etc/mysql/mariadb.conf.d/50-server.cnf

service mariadb stop

exec /usr/bin/mysqld_safe
