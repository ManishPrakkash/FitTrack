"""
Test script to check MongoDB authentication endpoints.
"""
import os
import sys
import json
import requests
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack_backend.settings_mongodb')
django.setup()

def test_mongodb_auth_endpoints():
    """Test the MongoDB authentication endpoints."""
    base_url = "http://127.0.0.1:8000"
    
    # Test user data
    test_user = {
        "name": "MongoDB Test User",
        "email": f"mongodbtest_{django.utils.timezone.now().timestamp()}@example.com",
        "password": "testpassword123"
    }
    
    print(f"Testing MongoDB authentication endpoints with user: {test_user['email']}")
    
    # Test registration endpoint
    print("\n1. Testing MongoDB registration endpoint...")
    register_url = f"{base_url}/api/mongodb/register/"
    
    try:
        register_response = requests.post(register_url, json=test_user)
        print(f"Status code: {register_response.status_code}")
        print(f"Response: {register_response.json()}")
        
        if register_response.status_code == 201:
            print("Registration successful!")
        else:
            print("Registration failed.")
            return False
    except Exception as e:
        print(f"Error during registration: {e}")
        return False
    
    # Test login endpoint
    print("\n2. Testing MongoDB login endpoint...")
    login_url = f"{base_url}/api/mongodb/login/"
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    
    try:
        login_response = requests.post(login_url, json=login_data)
        print(f"Status code: {login_response.status_code}")
        print(f"Response: {login_response.json()}")
        
        if login_response.status_code == 200:
            print("Login successful!")
            token = login_response.json().get("token")
            user = login_response.json().get("user")
            
            if token and user:
                print(f"Received token: {token[:10]}...")
                print(f"User data: {json.dumps(user, indent=2)}")
            else:
                print("Token or user data missing in response.")
                return False
        else:
            print("Login failed.")
            return False
    except Exception as e:
        print(f"Error during login: {e}")
        return False
    
    # Test token validation endpoint
    print("\n3. Testing MongoDB token validation endpoint...")
    validate_url = f"{base_url}/api/mongodb/validate-token/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        validate_response = requests.get(validate_url, headers=headers)
        print(f"Status code: {validate_response.status_code}")
        print(f"Response: {validate_response.json()}")
        
        if validate_response.status_code == 200:
            print("Token validation successful!")
        else:
            print("Token validation failed.")
            return False
    except Exception as e:
        print(f"Error during token validation: {e}")
        return False
    
    print("\nAll MongoDB authentication endpoints are working correctly!")
    return True

if __name__ == "__main__":
    success = test_mongodb_auth_endpoints()
    sys.exit(0 if success else 1)
