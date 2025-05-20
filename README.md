# FitTrack Application

A fitness tracking application with Django backend and React frontend, using MongoDB Atlas as the database.

## Features

- User authentication (signup and login)
- JWT token-based authentication
- User profile management
- MongoDB Atlas database integration
- Secure password storage
- RESTful API endpoints
- CORS configuration for cross-domain requests

## Project Structure

- `fitrack/` - React frontend
- `backend/` - Django backend with MongoDB Atlas integration

## Prerequisites

- Python 3.9+
- Node.js and npm
- MongoDB Atlas account

## Setup Instructions

### 1. Set up the Django Backend

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver
```

The Django backend will start running on http://localhost:8000.

### 2. Set up the React Frontend

```bash
# Navigate to the frontend directory
cd fitrack

# Install dependencies
npm install

# Start the development server
npm run dev
```

The React frontend will start running on http://localhost:5173.

## API Endpoints

### Authentication

- **Register**: `POST /api/register/`
  - Request body: `{ "name": "User Name", "email": "user@example.com", "password": "password123" }`
  - Response: `{ "success": true, "message": "User registered successfully" }`

- **Login**: `POST /api/login/`
  - Request body: `{ "email": "user@example.com", "password": "password123" }`
  - Response: `{ "success": true, "token": "jwt_token", "user": { "id": "1", "email": "user@example.com", "name": "User Name", "profile": {...} } }`

- **Validate Token**: `GET /api/validate-token/`
  - Headers: `Authorization: Bearer jwt_token`
  - Response: `{ "success": true, "message": "Token is valid", "user": { "id": "1", "email": "user@example.com", "name": "User Name", "profile": {...} } }`

### Profile Management

- **Get Profile**: `GET /api/profile/`
  - Headers: `Authorization: Bearer jwt_token`
  - Response: `{ "success": true, "profile": { "height": 180, "weight": 75, "age": 30, "gender": "male", "fitness_goal": "weight_loss", "activity_level": "moderately_active" } }`

- **Update Profile**: `PUT /api/profile/`
  - Headers: `Authorization: Bearer jwt_token`
  - Request body: `{ "height": 180, "weight": 75, "age": 30, "gender": "male", "fitness_goal": "weight_loss", "activity_level": "moderately_active" }`
  - Response: `{ "success": true, "message": "Profile updated successfully", "user": { "id": "1", "email": "user@example.com", "name": "User Name", "profile": {...} } }`

## Deployment

### Backend Deployment (Vercel)

1. Install the Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy the backend:
   ```bash
   cd backend
   vercel
   ```

3. Set environment variables in the Vercel dashboard:
   - `SECRET_KEY`: A secure random string
   - `DEBUG`: 'False'
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `MONGODB_USERNAME`: Your MongoDB Atlas username
   - `MONGODB_PASSWORD`: Your MongoDB Atlas password

### Frontend Deployment (Vercel)

1. Deploy the frontend:
   ```bash
   cd fitrack
   vercel
   ```

2. Set environment variables in the Vercel dashboard:
   - `REACT_APP_API_URL`: Your deployed backend URL

## Security Notes

- Passwords are securely hashed using Django's password hashing system
- JWT tokens are used for authentication
- Only authenticated users can access protected endpoints
- MongoDB Atlas connection is secured with username and password

## Troubleshooting

If you encounter issues with MongoDB Atlas connection:

1. Make sure your MongoDB Atlas cluster is running
2. Check that your IP address is in the MongoDB Atlas IP access list
3. Verify the connection string in `backend/fittrack_backend/settings.py`
4. Check that the database user has the correct permissions

## Testing

You can test the API endpoints using the provided test script:

```bash
cd backend
python test_api.py
```
