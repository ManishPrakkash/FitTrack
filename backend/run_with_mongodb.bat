@echo off
echo Starting Django server with MongoDB settings...
set DJANGO_SETTINGS_MODULE=fittrack_backend.settings_mongodb
python manage.py runserver
