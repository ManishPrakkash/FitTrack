from pymongo import MongoClient
from bson.objectid import ObjectId
import uuid
from django.contrib.auth.hashers import make_password, check_password

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['fitrack_db']
users_collection = db['users']

def create_user(name, email, password):
    """
    Create a new user in MongoDB
    """
    # Check if user with this email already exists
    if users_collection.find_one({'email': email}):
        return None

    # Create user document
    user = {
        'id': str(uuid.uuid4()),
        'name': name,
        'email': email,
        'password': make_password(password),
        'created_at': None,  # MongoDB will use current time
        'updated_at': None   # MongoDB will use current time
    }

    # Insert user into MongoDB
    result = users_collection.insert_one(user)

    if result.inserted_id:
        # Return user without password
        user.pop('password')
        return user
    return None

def get_user_by_email(email):
    """
    Get user by email (case-insensitive)
    """
    # Use regex with case-insensitive option for email lookup
    return users_collection.find_one({'email': {'$regex': f'^{email}$', '$options': 'i'}})

def authenticate_user(email, password):
    """
    Authenticate user with email and password
    """
    user = get_user_by_email(email)

    if user and check_password(password, user.get('password', '')):
        # Return user without password
        user_data = {k: v for k, v in user.items() if k != 'password' and k != '_id'}
        return user_data

    return None
