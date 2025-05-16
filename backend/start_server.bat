@echo off
REM Script to start the Django server with all necessary fixes

echo Applying pymongo fix...
python fix_djongo.py

echo Initializing database...
python init_db.py

echo Starting Django development server...
python manage.py runserver 0.0.0.0:8000
