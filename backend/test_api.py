"""
Script to test the API endpoints.
"""
import requests
import json

def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8000"
    
    # Test registration
    print("\nTesting registration endpoint...")
    register_url = f"{base_url}/api/register/"
    register_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    
    try:
        register_response = requests.post(register_url, json=register_data)
        print(f"Status code: {register_response.status_code}")
        print(f"Response: {register_response.json()}")
    except Exception as e:
        print(f"Error testing registration: {e}")
    
    # Test login
    print("\nTesting login endpoint...")
    login_url = f"{base_url}/api/login/"
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    
    try:
        login_response = requests.post(login_url, json=login_data)
        print(f"Status code: {login_response.status_code}")
        print(f"Response: {login_response.json()}")
        
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            
            # Test token validation
            print("\nTesting token validation endpoint...")
            validate_url = f"{base_url}/api/validate-token/"
            headers = {"Authorization": f"Bearer {token}"}
            
            try:
                validate_response = requests.get(validate_url, headers=headers)
                print(f"Status code: {validate_response.status_code}")
                print(f"Response: {validate_response.json()}")
            except Exception as e:
                print(f"Error testing token validation: {e}")
    except Exception as e:
        print(f"Error testing login: {e}")

if __name__ == "__main__":
    test_api()
