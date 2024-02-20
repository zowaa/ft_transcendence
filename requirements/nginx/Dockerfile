FROM debian:12

WORKDIR /nginx

COPY tools/install.sh .

COPY conf/default.sh .

RUN chmod u+x install.sh default.sh

RUN ./install.sh

EXPOSE 443

CMD ["./default.sh"]
