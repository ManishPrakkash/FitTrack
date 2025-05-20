"""
Test script to verify end-to-end authentication flow.
"""
import os
import sys
import json
import requests
import django
from pymongo import MongoClient

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack_backend.settings_mongodb')
django.setup()

from django.conf import settings

def test_end_to_end_auth():
    """Test end-to-end authentication flow."""
    print("Testing end-to-end authentication flow...")
    
    # API endpoints
    base_url = "http://127.0.0.1:8000"
    register_url = f"{base_url}/api/register/"
    login_url = f"{base_url}/api/login/"
    validate_url = f"{base_url}/api/validate-token/"
    
    # Test user data
    timestamp = django.utils.timezone.now().timestamp()
    test_user = {
        "name": "E2E Test User",
        "email": f"e2etest_{timestamp}@example.com",
        "username": f"e2etest_{timestamp}",
        "password": "testpassword123"
    }
    
    print(f"\nTest user: {test_user['email']}")
    
    # Step 1: Register user
    print("\n1. Registering user...")
    try:
        register_response = requests.post(register_url, json=test_user)
        print(f"Status code: {register_response.status_code}")
        
        try:
            print(f"Response: {register_response.json()}")
        except:
            print(f"Response text: {register_response.text}")
        
        if register_response.status_code != 201:
            print("Registration failed.")
            return False
    except Exception as e:
        print(f"Error during registration: {e}")
        return False
    
    # Step 2: Verify user in MongoDB
    print("\n2. Verifying user in MongoDB...")
    try:
        # Connect to MongoDB Atlas
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]
        
        # Check if user exists in auth_user collection
        users_collection = db["auth_user"]
        user = users_collection.find_one({"email": test_user["email"]})
        
        if user:
            print(f"User found in MongoDB: {user['email']}")
        else:
            print("User not found in MongoDB.")
            return False
        
        # Check if profile exists
        profiles_collection = db["authentication_profile"]
        profile = profiles_collection.find_one({"user_id": user["_id"]})
        
        if profile:
            print(f"Profile found in MongoDB for user: {user['email']}")
        else:
            print("Profile not found in MongoDB.")
            return False
    except Exception as e:
        print(f"Error verifying user in MongoDB: {e}")
        return False
    
    # Step 3: Login user
    print("\n3. Logging in user...")
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    
    try:
        login_response = requests.post(login_url, json=login_data)
        print(f"Status code: {login_response.status_code}")
        
        try:
            login_data = login_response.json()
            print(f"Response: {login_data}")
            
            if login_response.status_code != 200:
                print("Login failed.")
                return False
            
            token = login_data.get("token")
            if not token:
                print("Token not found in response.")
                return False
            
            print(f"Token received: {token[:10]}...")
        except:
            print(f"Response text: {login_response.text}")
            print("Login failed.")
            return False
    except Exception as e:
        print(f"Error during login: {e}")
        return False
    
    # Step 4: Validate token
    print("\n4. Validating token...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        validate_response = requests.get(validate_url, headers=headers)
        print(f"Status code: {validate_response.status_code}")
        
        try:
            print(f"Response: {validate_response.json()}")
            
            if validate_response.status_code != 200:
                print("Token validation failed.")
                return False
        except:
            print(f"Response text: {validate_response.text}")
            print("Token validation failed.")
            return False
    except Exception as e:
        print(f"Error during token validation: {e}")
        return False
    
    print("\nEnd-to-end authentication flow completed successfully!")
    return True

if __name__ == "__main__":
    success = test_end_to_end_auth()
    sys.exit(0 if success else 1)
