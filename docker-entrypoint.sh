#!/bin/sh

set -e
set -x

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn
