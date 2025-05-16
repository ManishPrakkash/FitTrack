# FitTrack Backend

This is the Django backend for the FitTrack application, which provides authentication and API endpoints for the frontend.

## Features

- User authentication (signup, login, token validation)
- MongoDB Atlas integration
- RESTful API endpoints
- JWT-based authentication
- Secure password storage with bcrypt

## Prerequisites

- Python 3.12+
- MongoDB Atlas account (or local MongoDB instance)

## Note on Dependencies

This project uses Django 4.1.13 (not the latest version) due to compatibility requirements with the djongo package, which requires sqlparse==0.2.4.

## Note on Database Migrations and djongo Compatibility

Due to compatibility issues between Django's migration system and djongo, we use a custom database initialization approach:

1. We initialize the MongoDB collections directly using the `init_db.py` script
2. We provide a direct MongoDB user creation script (`create_user.py`)
3. We avoid running Django's built-in migrations which can cause errors with djongo

Additionally, we patch the djongo package to fix connection handling issues:

1. The `patch_djongo.py` script modifies the djongo base.py file to fix a compatibility issue
2. This patch is automatically applied during installation
3. If you encounter `NotImplementedError: Database objects do not implement truth value testing or bool()`, run `python patch_djongo.py` to apply the patch

## MongoDB Configuration

By default, the application is configured to use a local MongoDB instance running in Docker. The docker-compose.yml file in the root directory is set up to run MongoDB.

If you want to use MongoDB Atlas instead, set the `USE_MONGODB_ATLAS` environment variable to `True` in the `.env` file.

## Setup Instructions

### Option 1: Using the installation scripts (Recommended)

#### Windows
```bash
install_dependencies.bat
```

#### macOS/Linux
```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### Option 2: Manual installation

#### 1. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### 2. Install dependencies

```bash
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
```

### 3. Configure environment variables

Create a `.env` file in the backend directory with the following variables:

```
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# MongoDB settings
MONGODB_URI=your-mongodb-connection-string
MONGODB_NAME=fittrack_db

# JWT settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME_DAYS=1
```

### 4. Run the setup script

```bash
# Windows
python setup.py

# macOS/Linux
python setup.py
```

### 5. Initialize the database

```bash
python init_db.py
```

### 6. Create a user

```bash
# Use the direct MongoDB user creation script (recommended)
python create_user.py

# Or use the Django management command (if djongo patch is applied)
python manage.py createuser
python manage.py createuser --admin
```

### 6. Start the development server

```bash
# Windows
run_server.bat

# macOS/Linux
./run_server.sh
```

The server will start at http://localhost:8000.

## API Endpoints

### Authentication

- **Register**: `POST /api/register/`
  - Request body: `{ "name": "User Name", "email": "user@example.com", "password": "password123" }`
  - Response: `{ "success": true, "message": "User registered successfully" }`

- **Login**: `POST /api/login/`
  - Request body: `{ "email": "user@example.com", "password": "password123" }`
  - Response: `{ "success": true, "token": "jwt-token", "user": { "id": "1", "name": "User Name", "email": "user@example.com" } }`

- **Validate Token**: `GET /api/validate-token/`
  - Headers: `Authorization: Bearer jwt-token`
  - Response: `{ "success": true, "message": "Token is valid", "user": { "id": "1", "name": "User Name", "email": "user@example.com" } }`

### Users

- **Get Current User**: `GET /api/users/me/`
  - Headers: `Authorization: Bearer jwt-token`
  - Response: `{ "id": "1", "name": "User Name", "email": "user@example.com", "date_joined": "2023-01-01T00:00:00Z" }`
