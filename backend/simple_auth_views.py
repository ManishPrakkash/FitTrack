"""
Simple authentication views for MongoDB.
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import mongodb_auth

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def register_user(request):
    """
    Register a new user in MongoDB.
    """
    # Handle OPTIONS request for CORS preflight
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
    
    # Handle POST request for registration
    try:
        print("Simple register view: Received registration request")
        
        # Parse request body
        data = json.loads(request.body)
        print("Parsed data:", data)
        
        name = data.get('name', '')
        email = data.get('email', '')
        password = data.get('password', '')
        username = data.get('username', '')
        
        print(f"Registration data: name={name}, email={email}, username={username}")
        
        # Validate data
        if not name:
            print("Validation error: Name is required")
            response = JsonResponse({
                'success': False,
                'error': {'name': ['Name is required']}
            }, status=400)
        elif not email:
            print("Validation error: Email is required")
            response = JsonResponse({
                'success': False,
                'error': {'email': ['Email is required']}
            }, status=400)
        elif not password:
            print("Validation error: Password is required")
            response = JsonResponse({
                'success': False,
                'error': {'password': ['Password is required']}
            }, status=400)
        else:
            # Register user
            print("Calling mongodb_auth.register_user")
            result = mongodb_auth.register_user(name, email, password, username)
            print("Registration result:", result)
            
            if result['success']:
                print("Registration successful")
                response = JsonResponse(result, status=201)
            else:
                print("Registration failed:", result)
                response = JsonResponse(result, status=400)
    except Exception as e:
        print(f"Registration exception: {str(e)}")
        import traceback
        traceback.print_exc()
        response = JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
    
    # Add CORS headers to response
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    return response

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def login_user(request):
    """
    Login a user in MongoDB.
    """
    # Handle OPTIONS request for CORS preflight
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
    
    # Handle POST request for login
    try:
        print("Simple login view: Received login request")
        
        # Parse request body
        data = json.loads(request.body)
        print("Parsed data:", data)
        
        email = data.get('email', '')
        password = data.get('password', '')
        
        print(f"Login data: email={email}")
        
        # Validate data
        if not email:
            print("Validation error: Email is required")
            response = JsonResponse({
                'success': False,
                'error': {'email': ['Email is required']}
            }, status=400)
        elif not password:
            print("Validation error: Password is required")
            response = JsonResponse({
                'success': False,
                'error': {'password': ['Password is required']}
            }, status=400)
        else:
            # Login user
            print("Calling mongodb_auth.login_user")
            result = mongodb_auth.login_user(email, password)
            print("Login result:", result)
            
            if result['success']:
                print("Login successful")
                response = JsonResponse(result, status=200)
            else:
                print("Login failed:", result)
                response = JsonResponse(result, status=400)
    except Exception as e:
        print(f"Login exception: {str(e)}")
        import traceback
        traceback.print_exc()
        response = JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
    
    # Add CORS headers to response
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    return response
