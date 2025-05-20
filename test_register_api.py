"""
Test script to register a user through the API.
"""
import requests
import json
import time

def test_register_api():
    """Test registering a user through the API."""
    print("Testing user registration through the API...")
    
    # Create test user data
    timestamp = time.time()
    test_user = {
        "name": "Test API User",
        "email": f"testapiuser_{timestamp}@example.com",
        "password": "testpassword123"
    }
    
    print(f"\nCreating test user: {test_user['email']}")
    
    try:
        # Send POST request to register endpoint
        response = requests.post(
            "http://localhost:8000/api/mongodb/register/",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_user)
        )
        
        # Print response
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("\nUser registered successfully!")
            return True
        else:
            print("\nFailed to register user.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_register_api()
