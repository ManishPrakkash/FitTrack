@echo off
echo Setting up FitTrack backend...

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Make migrations
echo Creating database migrations...
python manage.py makemigrations authentication
python manage.py makemigrations challenges
python manage.py makemigrations activities

REM Apply migrations
echo Applying migrations...
python manage.py migrate

echo Setup complete!
echo.
echo To start the server, run:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
pause
