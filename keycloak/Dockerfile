FROM jboss/keycloak:latest

COPY custom-entrypoint.sh /opt/jboss/tools/custom-entrypoint.sh
# RUN chmod 777 /opt/jboss/tools/custom-entrypoint.sh
ENTRYPOINT [ "/opt/jboss/tools/custom-entrypoint.sh" ]