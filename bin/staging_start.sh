#!/bin/sh

cd $(dirname $0)/..

python manage.py migrate
exec gunicorn pycess.wsgi --log-file -