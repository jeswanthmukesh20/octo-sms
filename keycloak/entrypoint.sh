#!/bin/bash
set -e

echo "executing the custom entry point script"

FILE=/opt/jboss/keycloak/standalone/configuration/keycloak-add-user.json
if [ -f "$FILE" ]; then
    echo "keycloak-add-user.json exist, hence deleting it"
    rm $FILE
fi
echo "executing the entry point script from original image"
source  "/opt/jboss/tools/docker-entrypoint.sh"