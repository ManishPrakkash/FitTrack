# FitTrack Backend

This is the backend for the FitTrack application, built with Django and MongoDB.

## Prerequisites

- Python 3.8+
- MongoDB running on localhost:27017

## Setup

1. Install dependencies:
```
pip install django djangorestframework django-cors-headers djongo pymongo
```

2. Make sure MongoDB is running:
```
# Start MongoDB if not already running
mongod --dbpath /path/to/data/directory
```

3. Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```

4. Start the server:
```
python manage.py runserver 0.0.0.0:8000
```

Or use the provided script:
```
./run_server.sh
```

## API Endpoints

### Authentication

- **Register**: `POST /api/register/`
  - Request body: `{ "name": "User Name", "email": "user@example.com", "password": "password123" }`
  - Response: `{ "success": true, "message": "User registered successfully" }`

- **Login**: `POST /api/login/`
  - Request body: `{ "email": "user@example.com", "password": "password123" }`
  - Response: `{ "success": true, "user": { "id": "...", "name": "User Name", "email": "user@example.com", "created_at": "...", "updated_at": "..." } }`
