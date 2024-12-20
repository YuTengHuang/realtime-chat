#!/bin/sh

python3 manage.py migrate --noinput 

python3 manage.py createsuperuser --noinput || echo 'Super user already created'

daphne -b 0.0.0.0 -p 8080 chatroom.asgi:application