FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/www/html

COPY logo.png /var/www/html/logo.png

RUN mkdir -p /etc/nginx/ssl

EXPOSE 80

EXPOSE 81