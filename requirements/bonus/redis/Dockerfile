FROM debian:12

WORKDIR /redis

COPY conf/config.sh .

COPY tools/install.sh .

RUN chmod u+x config.sh install.sh

RUN ./install.sh

EXPOSE 6379

CMD ["./config.sh"]
