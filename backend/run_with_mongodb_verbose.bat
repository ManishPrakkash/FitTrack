@echo off
echo Starting Django server with MongoDB settings in verbose mode...
set DJANGO_SETTINGS_MODULE=fittrack_backend.settings_mongodb
python manage.py runserver --verbosity 3
