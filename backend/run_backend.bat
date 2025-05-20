@echo off
echo Setting up and running FitTrack backend with MongoDB Atlas...

REM Create virtual environment if it doesn't exist
if not exist venv_compatible (
    echo Creating virtual environment...
    python -m venv venv_compatible
)

REM Activate virtual environment
echo Activating virtual environment...
call venv_compatible\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements_compatible.txt

REM Make migrations
echo Creating database migrations...
python manage.py makemigrations authentication
python manage.py makemigrations challenges
python manage.py makemigrations activities

REM Apply migrations
echo Applying migrations...
python manage.py migrate

REM Start the server
echo Starting server...
python manage.py runserver

pause
