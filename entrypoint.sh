#!/bin/sh

python manage.py migrate
gunicorn --workers=1 -b=0.0.0.0:8080 drfsite.wsgi:application
