#!/bin/bash

# Apply migrations
echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

# Start the server
echo "Starting server..."
python manage.py runserver
