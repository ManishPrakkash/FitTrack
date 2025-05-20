"""
Test script to check if the root URL is working correctly.
"""
import requests
import json

def test_root_url():
    """Test the root URL of the API."""
    try:
        response = requests.get('http://127.0.0.1:8000/')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("Success! The root URL is working correctly.")
            print("\nResponse Content:")
            try:
                # Try to parse as JSON
                content = response.json()
                print(json.dumps(content, indent=2))
            except:
                # If not JSON, print as text
                print(response.text)
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_root_url()
