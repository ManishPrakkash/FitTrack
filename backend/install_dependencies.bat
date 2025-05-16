@echo off
REM Script to install dependencies for the FitTrack backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install pymongo==4.6.1
pip install sqlparse==0.2.4
pip install python-dotenv==1.0.0
pip install PyJWT==2.8.0
pip install bcrypt==4.1.2
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1
pip install Django==4.1.13
pip install djongo==1.3.6

echo Patching djongo for compatibility...
python patch_djongo.py

echo Starting MongoDB container...
cd ..
docker-compose up -d
cd backend

echo Testing MongoDB connection...
python test_mongodb.py

if %ERRORLEVEL% neq 0 (
    echo Failed to connect to MongoDB. Please check your connection string and network.
    echo Please make sure Docker is running and try again.
    exit /b 1
)

echo Initializing database...
python init_db.py

echo Dependencies installed successfully!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the Django server, run:
echo   python manage.py runserver
