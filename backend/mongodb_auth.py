"""
Direct MongoDB authentication module for FitTrack.
"""
import os
import json
import hashlib
import datetime
import jwt
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/?retryWrites=true&w=majority&appName=fitrack-db')
DB_NAME = 'fittrack_db'
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-key-for-development-only')

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# Collections
users_collection = db['users']
profiles_collection = db['profiles']

class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles MongoDB ObjectId."""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against a provided password."""
    return stored_password == hash_password(provided_password)

def generate_token(user_id):
    """Generate a JWT token for the given user ID."""
    payload = {
        'id': str(user_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return token

def verify_token(token):
    """Verify a JWT token and return the user ID."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def register_user(name, email, password, username=None):
    """Register a new user."""
    # Check if user already exists
    if users_collection.find_one({'email': email}):
        return {
            'success': False,
            'message': 'Email already exists'
        }
    
    # Create username if not provided
    if not username:
        username = email.split('@')[0]
    
    # Create user document
    user = {
        'name': name,
        'email': email,
        'username': username,
        'password': hash_password(password),
        'date_joined': datetime.datetime.utcnow(),
        'is_active': True
    }
    
    # Insert user
    user_id = users_collection.insert_one(user).inserted_id
    
    # Create profile
    profile = {
        'user_id': user_id,
        'name': name,
        'height': None,
        'weight': None,
        'age': None,
        'gender': None,
        'fitness_goal': None,
        'activity_level': None
    }
    
    # Insert profile
    profiles_collection.insert_one(profile)
    
    return {
        'success': True,
        'message': 'User registered successfully'
    }

def login_user(email, password):
    """Login a user."""
    # Find user
    user = users_collection.find_one({'email': email})
    
    if not user:
        return {
            'success': False,
            'message': 'User not found'
        }
    
    # Verify password
    if not verify_password(user['password'], password):
        return {
            'success': False,
            'message': 'Invalid credentials'
        }
    
    # Generate token
    token = generate_token(user['_id'])
    
    # Get profile
    profile = profiles_collection.find_one({'user_id': user['_id']})
    
    # Prepare user data
    user_data = {
        'id': str(user['_id']),
        'name': user.get('name', ''),
        'email': user['email'],
        'username': user['username'],
        'date_joined': user['date_joined'].isoformat(),
        'profile': {
            'name': profile.get('name', '') if profile else '',
            'height': profile.get('height') if profile else None,
            'weight': profile.get('weight') if profile else None,
            'age': profile.get('age') if profile else None,
            'gender': profile.get('gender') if profile else None,
            'fitness_goal': profile.get('fitness_goal') if profile else None,
            'activity_level': profile.get('activity_level') if profile else None
        }
    }
    
    return {
        'success': True,
        'token': token,
        'user': user_data
    }

def get_user_by_token(token):
    """Get user by token."""
    user_id = verify_token(token)
    
    if not user_id:
        return None
    
    # Find user
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    
    if not user:
        return None
    
    # Get profile
    profile = profiles_collection.find_one({'user_id': user['_id']})
    
    # Prepare user data
    user_data = {
        'id': str(user['_id']),
        'name': user.get('name', ''),
        'email': user['email'],
        'username': user['username'],
        'date_joined': user['date_joined'].isoformat(),
        'profile': {
            'name': profile.get('name', '') if profile else '',
            'height': profile.get('height') if profile else None,
            'weight': profile.get('weight') if profile else None,
            'age': profile.get('age') if profile else None,
            'gender': profile.get('gender') if profile else None,
            'fitness_goal': profile.get('fitness_goal') if profile else None,
            'activity_level': profile.get('activity_level') if profile else None
        }
    }
    
    return user_data
