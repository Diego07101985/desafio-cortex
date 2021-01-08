#!/bin/sh 

echo "Starting server"
gunicorn -w 4 --bind 0.0.0.0:5000 wsgi:application;
exec "$@"