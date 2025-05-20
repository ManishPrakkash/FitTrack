"""
Script to add a test user to MongoDB Atlas.
"""
import os
import sys
import django
import datetime
import hashlib
from pymongo import MongoClient
from bson import ObjectId

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack_backend.settings')
django.setup()

# MongoDB connection settings
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/?retryWrites=true&w=majority&appName=fitrack-db')
DB_NAME = 'fittrack_db'

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_test_user():
    """Add a test user to MongoDB Atlas."""
    print("Adding test user to MongoDB Atlas...")
    
    try:
        # Connect to MongoDB Atlas
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        
        # Create test user data
        timestamp = datetime.datetime.now().timestamp()
        test_user = {
            "name": "Test User",
            "email": f"testuser_{timestamp}@example.com",
            "username": f"testuser_{timestamp}",
            "password": hash_password("testpassword123"),
            "date_joined": datetime.datetime.now(),
            "is_active": True
        }
        
        print(f"\nCreating test user: {test_user['email']}")
        
        # Insert test user
        users_collection = db["users"]
        user_id = users_collection.insert_one(test_user).inserted_id
        print(f"Inserted test user with ID: {user_id}")
        
        # Create user profile
        profile = {
            "user_id": user_id,
            "name": test_user["name"],
            "height": None,
            "weight": None,
            "age": None,
            "gender": None,
            "fitness_goal": None,
            "activity_level": None
        }
        
        # Insert profile
        profiles_collection = db["profiles"]
        profile_id = profiles_collection.insert_one(profile).inserted_id
        print(f"Inserted profile with ID: {profile_id}")
        
        print(f"\nTest user created successfully: {test_user['email']}")
        print(f"Password: testpassword123")
        
        return True
    except Exception as e:
        print(f"Error adding test user: {e}")
        return False

if __name__ == "__main__":
    success = add_test_user()
    sys.exit(0 if success else 1)
