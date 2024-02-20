FROM debian:12

WORKDIR /grafana

COPY conf/defaults.ini .

COPY conf/config.sh .

COPY tools/install.sh .

RUN chmod u+x config.sh install.sh

RUN ./install.sh

EXPOSE 3000

CMD ["./config.sh"]
