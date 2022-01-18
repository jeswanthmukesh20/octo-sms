FROM postgres:alpine
COPY docker-postgresql-multiple-databases/create-multiple-postgresql-databases.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["postgres"]