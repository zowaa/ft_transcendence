FROM debian:12

WORKDIR /adminer

COPY ./tools/install.sh .

COPY ./conf/config.sh .

RUN chmod u+x config.sh install.sh

RUN /bin/sh ./install.sh

EXPOSE 8080

CMD ["./config.sh"]
