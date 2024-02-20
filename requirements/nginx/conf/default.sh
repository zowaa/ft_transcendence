#!/bin/sh

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $FILE_KEY -out $FILE_CRT -subj "/C=MO/L=BG/O=1337/CN=$DOMAIN_NAME"

echo "server {
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name www.$DOMAIN_NAME $DOMAIN_NAME;

    ssl_certificate $FILE_CRT;
    ssl_certificate_key $FILE_KEY;
    ssl_protocols TLSv1.3;

    index index.php;
    root /var/www/html;

    location ~ \.php$ {
	include snippets/fastcgi-php.conf;
	fastcgi_pass wordpress:9000;
	}
}" > /etc/nginx/sites-available/default

exec nginx -g "daemon off;"
