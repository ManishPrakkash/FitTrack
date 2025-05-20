#!/bin/bash

echo "Setting up FitTrack backend..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make migrations
echo "Creating database migrations..."
python manage.py makemigrations authentication
python manage.py makemigrations challenges
python manage.py makemigrations activities

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

echo "Setup complete!"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
