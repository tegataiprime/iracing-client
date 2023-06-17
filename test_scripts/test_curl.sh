#!/usr/bin/env bash
# Test iRacing API with curl

source ../.env

EMAILLOWER=$(echo -n "$IRACING_USERNAME" | tr [:upper:] [:lower:])
ENCODEDPW=$(echo -n $IRACING_PASSWORD$IRACING_USERNAME | openssl dgst -binary -sha256 | openssl base64)

BODY="{\"email\": \"$EMAIL\", \"password\": \"$ENCODEDPW\"}"

/usr/bin/curl -v -c cookie-jar.txt -X POST -H 'Content-Type: application/json' --data "$BODY" https://members-ng.iracing.com/auth
