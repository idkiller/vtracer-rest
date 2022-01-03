#!/bin/sh

PORT=${SERVICE_PORT:-5959}

echo "Lightwarp Service Boot"
echo "SSL_CERTIFICATE : $SSL_CERTIFICATE"
echo "SSL_PRIVATEKEY : $SSL_PRIVATEKEY"

if [ -n "$SSL_CERTIFICATE" ] && [ -n "$SSL_PRIVATEKEY" ]; then
    echo "Run with Https"
    gunicorn --bind 0.0.0.0:$PORT -t 600 -w 4 --certfile $SSL_CERTIFICATE --keyfile $SSL_PRIVATEKEY service:application
else
echo "Run with Http"
    gunicorn --bind 0.0.0.0:$PORT -t 600 -w 4 service:application
fi