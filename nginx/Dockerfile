FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY  ./ssl/certificate.crt /etc/ssl
COPY ./ssl/private.key /etc/ssl
COPY ./default.conf /etc/nginx/conf.d/default.conf