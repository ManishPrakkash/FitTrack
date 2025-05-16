@echo off
REM Run server script for Windows

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please run install_dependencies.bat first.
    exit /b 1
)

REM Ensure MongoDB container is running
echo Ensuring MongoDB container is running...
cd ..
docker-compose up -d
cd backend

REM Apply pymongo fix
echo Applying pymongo fix...
python fix_djongo.py

REM Check MongoDB connection
echo Checking MongoDB connection...
python test_mongodb.py

if %ERRORLEVEL% neq 0 (
    echo Failed to connect to MongoDB. Please check your Docker installation and network.
    exit /b 1
)

REM Initialize database directly (bypassing Django migrations)
echo Initializing database...
python init_db.py

REM Create superuser if needed
echo.
echo Note: You can create a superuser later with:
echo python manage.py createsuperuser

REM Start server
echo Starting Django development server...
python manage.py runserver 0.0.0.0:8000
