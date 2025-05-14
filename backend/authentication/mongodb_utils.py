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
    Get user by email
    """
    return users_collection.find_one({'email': email})

def authenticate_user(email, password):
    """
    Authenticate user with email and password
    """
    print(f"Authenticating user with email: {email}")
    user = get_user_by_email(email)

    if not user:
        print(f"No user found with email: {email}")
        return None

    print(f"User found: {user.get('name')}")

    # Check password
    stored_password = user.get('password', '')
    if not stored_password:
        print("User has no password stored")
        return None

    password_match = check_password(password, stored_password)
    print(f"Password match: {password_match}")

    if password_match:
        # Return user without password
        user_data = {k: v for k, v in user.items() if k != 'password' and k != '_id'}
        print(f"Authentication successful for: {user_data.get('name')}")
        return user_data

    print("Password does not match")
    return None
