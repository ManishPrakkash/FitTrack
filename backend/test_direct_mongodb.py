"""
Test script to directly interact with MongoDB for authentication.
"""
import os
import sys
import json
import hashlib
import datetime
from pymongo import MongoClient
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack_backend.settings_mongodb')
django.setup()

from django.conf import settings

def test_direct_mongodb():
    """Test direct interaction with MongoDB for authentication."""
    print("Testing direct MongoDB interaction for authentication...")
    
    # Get MongoDB connection details from Django settings
    mongodb_uri = settings.DATABASES['default']['CLIENT']['host']
    db_name = settings.DATABASES['default']['NAME']
    
    print(f"MongoDB URI: {mongodb_uri}")
    print(f"Database name: {db_name}")
    
    try:
        # Connect to MongoDB Atlas
        client = MongoClient(mongodb_uri)
        db = client[db_name]
        
        # Create test user data
        timestamp = datetime.datetime.now().timestamp()
        test_user = {
            "name": "Test Direct User",
            "email": f"testdirect_{timestamp}@example.com",
            "username": f"testdirect_{timestamp}",
            "password": hashlib.sha256("testpassword123".encode()).hexdigest(),  # Simple hash for demo
            "date_joined": datetime.datetime.now(),
            "is_active": True
        }
        
        print(f"\nCreating test user: {test_user['email']}")
        
        # Check if auth_user collection exists, create if not
        if "auth_user" not in db.list_collection_names():
            db.create_collection("auth_user")
            print("Created auth_user collection")
        
        # Insert test user
        users_collection = db["auth_user"]
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
        
        # Check if authentication_profile collection exists, create if not
        if "authentication_profile" not in db.list_collection_names():
            db.create_collection("authentication_profile")
            print("Created authentication_profile collection")
        
        # Insert profile
        profiles_collection = db["authentication_profile"]
        profile_id = profiles_collection.insert_one(profile).inserted_id
        print(f"Inserted profile with ID: {profile_id}")
        
        # Verify user was created
        created_user = users_collection.find_one({"_id": user_id})
        print(f"\nRetrieved user: {created_user['email']}")
        
        # Simulate login
        print("\nSimulating login...")
        login_user = users_collection.find_one({
            "email": test_user["email"],
            "password": test_user["password"]
        })
        
        if login_user:
            print(f"Login successful for user: {login_user['email']}")
        else:
            print("Login failed")
            return False
        
        print("\nDirect MongoDB interaction for authentication is working correctly!")
        return True
    except Exception as e:
        print(f"Error during direct MongoDB interaction: {e}")
        return False

if __name__ == "__main__":
    success = test_direct_mongodb()
    sys.exit(0 if success else 1)
