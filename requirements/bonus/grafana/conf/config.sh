#!/bin/sh

rm -rf /usr/share/grafana/conf/defaults.ini

cp defaults.ini /usr/share/grafana/conf/defaults.ini

exec grafana-server --homepath=/usr/share/grafana
