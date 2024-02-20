#!/bin/sh

mkdir -p $WP_PATH

curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar

chmod u+x wp-cli.phar

mv wp-cli.phar /usr/local/bin/wp

wp cli update

sed -i 's#listen = /run/php/php8.2-fpm.sock#listen = 9000#' /etc/php/8.2/fpm/pool.d/www.conf

sleep 10

FILE="/var/www/html/wp-config.php"

if [ ! -f "$FILE" ]; then
	wp core download --path=$WP_PATH --allow-root

	wp core config --dbname=$MYSQL_DB_NAME --dbuser=$MYSQL_USER --dbpass=$MYSQL_PASSWORD --dbhost=$MYSQL_DB_HOST --path=$WP_PATH --allow-root

	sed -i "s/define( 'DB_COLLATE', '' );/define( 'DB_COLLATE', '' );define('WP_REDIS_HOST', 'redis');define('WP_REDIS_PORT', 6379);/" /var/www/html/wp-config.php

	wp core install --url=https://$DOMAIN_NAME --title='inception' --admin_user=$WP_ADMIN --admin_password=$WP_ADMIN_PASSWORD --admin_email=$WP_ADMIN_EMAIL --skip-email --path=$WP_PATH --allow-root

	wp user create $WP_USER $WP_USER_EMAIL --role='author' --user_pass=$WP_USER_PASSWORD --path=$WP_PATH --allow-root

	wp plugin install redis-cache --activate  --path=$WP_PATH --allow-root

	wp plugin update --path=$WP_PATH --all --allow-root

	wp redis enable --path=$WP_PATH --allow-root
	
	chown -R www-data:www-data /var/www/html/*
else
	echo "Success : Getting files from volume..."
fi

exec /usr/sbin/php-fpm8.2 -F
