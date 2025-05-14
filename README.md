# FitTrack Application

A fitness tracking application with Django backend and React frontend.

## Features

- User authentication (signup and login)
- MongoDB database integration
- Secure password storage
- RESTful API endpoints

## Prerequisites

- Python 3.8+
- Node.js and npm
- Docker and Docker Compose (for MongoDB)

## Setup Instructions

### 1. Start MongoDB

The application uses MongoDB as its database. You can start MongoDB using Docker:

```bash
# Start MongoDB container
docker-compose up -d
```

This will start MongoDB on localhost:27017.

### 2. Set up the Django Backend

```bash
# Navigate to the backend directory
cd backend

# Install dependencies
pip install django djangorestframework django-cors-headers djongo pymongo

# Run the server script (this will check MongoDB, run migrations, and start the server)
./run_server.sh
```

The Django backend will start running on http://localhost:8000.

### 3. Set up the React Frontend

```bash
# Navigate to the frontend directory
cd fitrack

# Install dependencies
npm install

# Start the development server
npm start
```

The React frontend will start running on http://localhost:3000.

## API Endpoints

### Authentication

- **Register**: `POST /api/register/`
  - Request body: `{ "name": "User Name", "email": "user@example.com", "password": "password123" }`
  - Response: `{ "success": true, "message": "User registered successfully" }`

- **Login**: `POST /api/login/`
  - Request body: `{ "email": "user@example.com", "password": "password123" }`
  - Response: `{ "success": true, "user": { "id": "...", "name": "User Name", "email": "user@example.com", "created_at": "...", "updated_at": "..." } }`

## Security Notes

- Passwords are securely hashed using Django's password hashing system
- Only authenticated users can access the application
- MongoDB connection is secured and only accessible from the application

## Troubleshooting

If you encounter issues with MongoDB connection:

1. Make sure Docker is running
2. Check if the MongoDB container is running: `docker ps`
3. If needed, restart the MongoDB container: `docker-compose restart mongodb`
4. Verify the connection string in `backend/fittrack_backend/settings.py` is correct
