@echo off
echo Starting FitTrack backend server with SQLite database...

REM Set the Django settings module
set DJANGO_SETTINGS_MODULE=fittrack_backend.settings_pymongo

REM Activate virtual environment
call venv_new\Scripts\activate.bat

REM Install required packages if not already installed
pip install Django==4.2.10 djangorestframework==3.14.0 django-cors-headers==4.3.1 python-dotenv==1.0.0 PyJWT==2.8.0

REM Run migrations
python manage.py makemigrations authentication
python manage.py makemigrations challenges
python manage.py makemigrations activities
python manage.py migrate

REM Run server
python manage.py runserver

pause
