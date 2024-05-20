#!/bin/sh

python manage.py migrate
gunicorn --workers=4 -b=0.0.0.0:8000 drfsite.wsgi:application
