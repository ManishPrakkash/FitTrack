#!/bin/bash

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run install_dependencies.sh first."
    exit 1
fi

# Ensure MongoDB container is running
echo "Ensuring MongoDB container is running..."
cd ..
docker-compose up -d
cd backend

# Check MongoDB connection
echo "Checking MongoDB connection..."
python test_mongodb.py

if [ $? -ne 0 ]; then
    echo "Failed to connect to MongoDB. Please check your Docker installation and network."
    exit 1
fi

# Initialize database directly (bypassing Django migrations)
echo "Initializing database..."
python init_db.py

# Create superuser if needed
echo
echo "Note: You can create a superuser later with:"
echo "python manage.py createsuperuser"

# Start server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
