import requests
import json

# Base URL for the API
base_url = "http://localhost:8000/api"

def test_register():
    """Test user registration"""
    url = f"{base_url}/register/"
    
    # Test user data
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    # Send POST request to register endpoint
    response = requests.post(url, json=user_data)
    
    # Print response
    print("Register Response Status:", response.status_code)
    print("Register Response Body:", response.json())
    
    return response.status_code == 201

def test_login():
    """Test user login"""
    url = f"{base_url}/login/"
    
    # Login credentials
    login_data = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    # Send POST request to login endpoint
    response = requests.post(url, json=login_data)
    
    # Print response
    print("Login Response Status:", response.status_code)
    print("Login Response Body:", response.json())
    
    return response.status_code == 200

if __name__ == "__main__":
    print("Testing Authentication Flow...")
    print("-" * 50)
    
    # Test registration
    print("Testing Registration...")
    registration_success = test_register()
    
    if registration_success:
        print("Registration test passed!")
    else:
        print("Registration test failed!")
    
    print("-" * 50)
    
    # Test login
    print("Testing Login...")
    login_success = test_login()
    
    if login_success:
        print("Login test passed!")
    else:
        print("Login test failed!")
    
    print("-" * 50)
    
    # Overall result
    if registration_success and login_success:
        print("Authentication flow is working correctly!")
    else:
        print("Authentication flow has issues!")
