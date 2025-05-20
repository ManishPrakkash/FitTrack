@echo off
echo Starting FitTrack backend server...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run server
python manage.py runserver

pause
