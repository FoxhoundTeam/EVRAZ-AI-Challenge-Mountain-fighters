FROM openresty/openresty:latest

COPY ./compose/nginx/nginx.conf /etc/openresty/nginx.conf
COPY ./compose/nginx/mf.conf /etc/nginx/conf.d/mf.conf

ENV TZ=Europe/Moscow