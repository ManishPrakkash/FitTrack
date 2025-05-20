"""
Test script for the FitTrack API endpoints.
"""
import requests
import json

# Base URL - change this to your deployed URL when testing production
BASE_URL = "http://localhost:8000/api"

def test_register():
    """Test the registration endpoint."""
    print("\n=== Testing Registration ===")
    
    # Test data
    data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    
    # Make the request
    response = requests.post(f"{BASE_URL}/register/", json=data)
    
    # Print the response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def test_login(email="testuser@example.com", password="testpassword123"):
    """Test the login endpoint."""
    print("\n=== Testing Login ===")
    
    # Test data
    data = {
        "email": email,
        "password": password
    }
    
    # Make the request
    response = requests.post(f"{BASE_URL}/login/", json=data)
    
    # Print the response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def test_validate_token(token):
    """Test the token validation endpoint."""
    print("\n=== Testing Token Validation ===")
    
    # Set headers with token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Make the request
    response = requests.get(f"{BASE_URL}/validate-token/", headers=headers)
    
    # Print the response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json()

def run_tests():
    """Run all tests."""
    # Test registration
    register_response = test_register()
    
    # Test login
    login_response = test_login()
    
    # If login successful, test token validation
    if login_response.get("success"):
        token = login_response.get("token")
        test_validate_token(token)

if __name__ == "__main__":
    run_tests()
