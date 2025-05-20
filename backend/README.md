# FitTrack Backend

This is the backend for the FitTrack application, built with Django and MongoDB Atlas.

## Features

- User authentication (signup and login)
- JWT token-based authentication
- User profile management
- Fitness challenges management
- Activity tracking
- Leaderboard functionality
- MongoDB Atlas integration
- RESTful API endpoints

## Prerequisites

- Python 3.9+
- MongoDB Atlas account

## Quick Setup (Windows)

1. Run the setup script:
   ```
   setup.bat
   ```

2. Start the server:
   ```
   run_server.bat
   ```

## Quick Setup (macOS/Linux)

1. Make the scripts executable:
   ```bash
   chmod +x setup.sh run_server.sh
   ```

2. Run the setup script:
   ```bash
   ./setup.sh
   ```

3. Start the server:
   ```bash
   ./run_server.sh
   ```

## Manual Setup

1. Navigate to the backend directory
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```bash
   python manage.py makemigrations authentication
   python manage.py makemigrations challenges
   python manage.py makemigrations activities
   python manage.py migrate
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```

The server will start running on http://localhost:8000.

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

- **Get Profile**: `GET /api/profile/`
  - Headers: `Authorization: Bearer jwt_token`
  - Response: `{ "success": true, "profile": { "height": 180, "weight": 75, ... } }`

- **Update Profile**: `PUT /api/profile/`
  - Headers: `Authorization: Bearer jwt_token`
  - Request body: `{ "height": 180, "weight": 75, ... }`
  - Response: `{ "success": true, "message": "Profile updated successfully", "user": { ... } }`

### Challenges

- **List Challenges**: `GET /api/challenges/`
  - Headers: `Authorization: Bearer jwt_token`
  - Response: `{ "success": true, "data": [ { "id": 1, "name": "30-Day Walking Challenge", ... } ] }`

- **Create Challenge**: `POST /api/challenges/`
  - Headers: `Authorization: Bearer jwt_token`
  - Request body: `{ "name": "30-Day Walking Challenge", "type": "Walking", "description": "...", "goal": 100, "unit": "km" }`
  - Response: `{ "success": true, "data": { "id": 1, "name": "30-Day Walking Challenge", ... } }`

- **Join Challenge**: `POST /api/challenges/{id}/join/`
  - Headers: `Authorization: Bearer jwt_token`
  - Response: `{ "success": true, "message": "Successfully joined the challenge", "data": { ... } }`

- **Get Joined Challenges**: `GET /api/challenges/joined/`
  - Headers: `Authorization: Bearer jwt_token`
  - Response: `{ "success": true, "data": [ { "id": 1, "name": "30-Day Walking Challenge", ... } ] }`

- **Get Available Challenges**: `GET /api/challenges/available/`
  - Headers: `Authorization: Bearer jwt_token`
  - Response: `{ "success": true, "data": [ { "id": 2, "name": "Running Challenge", ... } ] }`

### Activities

- **Log Activity**: `POST /api/activities/log/`
  - Headers: `Authorization: Bearer jwt_token`
  - Request body: `{ "challenge_id": 1, "value": 5.2, "notes": "Morning walk" }`
  - Response: `{ "success": true, "message": "Activity logged successfully", "data": { ... } }`

- **Get Activities**: `GET /api/activities/`
  - Headers: `Authorization: Bearer jwt_token`
  - Response: `{ "success": true, "data": [ { "id": 1, "challenge": 1, "value": 5.2, ... } ] }`

- **Get Challenge Activities**: `GET /api/activities/challenge/?challenge_id=1`
  - Headers: `Authorization: Bearer jwt_token`
  - Response: `{ "success": true, "data": [ { "id": 1, "challenge": 1, "value": 5.2, ... } ] }`

### Leaderboard

- **Get Challenge Leaderboard**: `GET /api/challenges/leaderboard/{id}/`
  - Headers: `Authorization: Bearer jwt_token`
  - Response: `{ "success": true, "challenge": { ... }, "leaderboard": [ { "rank": 1, "user": { ... }, "score": 75.5, ... } ] }`

## Deployment

This backend is configured for deployment on Vercel. The `vercel.json` file contains the necessary configuration.

## Environment Variables

The following environment variables can be set:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to 'True' for development, 'False' for production
- `MONGODB_URI`: MongoDB Atlas connection string
- `MONGODB_USERNAME`: MongoDB Atlas username
- `MONGODB_PASSWORD`: MongoDB Atlas password
