import requests
import json

# Base URL for the API
base_url = "http://localhost:8000/api"

def test_login_case_insensitive():
    """Test user login with case-insensitive email"""
    url = f"{base_url}/login/"
    
    # Original email is "Manish@gmail.com" (capital M)
    # Let's try with lowercase "manish@gmail.com"
    login_data = {
        "email": "manish@gmail.com",  # lowercase 'm'
        "password": "password123"
    }
    
    # Send POST request to login endpoint
    response = requests.post(url, json=login_data)
    
    # Print response
    print("Login Response Status:", response.status_code)
    print("Login Response Body:", response.json())
    
    return response.status_code == 200

if __name__ == "__main__":
    print("Testing Case-Insensitive Login...")
    print("-" * 50)
    
    # Test login
    login_success = test_login_case_insensitive()
    
    if login_success:
        print("Login test passed! Case-insensitive email lookup is working.")
    else:
        print("Login test failed! Case-insensitive email lookup is not working.")
