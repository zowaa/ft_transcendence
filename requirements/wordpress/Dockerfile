FROM debian:12

WORKDIR /wordpress

COPY ./tools/install.sh .

COPY ./conf/config.sh .

RUN chmod +x ./config.sh ./install.sh

RUN /bin/sh ./install.sh

EXPOSE 9000

CMD ["./config.sh"]
