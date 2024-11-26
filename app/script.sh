#!/bin/bash
sleep 10
python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:80

# python manage.py startapp films
# python manage.py startapp users
# python manage.py startapp rentals