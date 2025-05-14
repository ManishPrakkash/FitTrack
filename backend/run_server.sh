#!/bin/bash

# Check if MongoDB is running
echo "Checking MongoDB connection..."
python test_mongodb.py
if [ $? -ne 0 ]; then
    echo "Warning: MongoDB connection failed. The application will still run, but MongoDB features will not work."
    echo "To use MongoDB, make sure it's running on localhost:27017"
fi

# Apply migrations for Django models (not MongoDB)
echo "Running migrations..."
python manage.py migrate

# Run server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
