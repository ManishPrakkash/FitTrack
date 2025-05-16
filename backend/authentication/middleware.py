from django.http import HttpResponse
from django.conf import settings

class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Handle preflight OPTIONS requests
        if request.method == "OPTIONS":
            response = HttpResponse()
            
            # Get the origin from the request
            origin = request.headers.get('Origin', '')
            
            # Check if the origin is in the allowed origins
            if origin in settings.CORS_ALLOWED_ORIGINS:
                response["Access-Control-Allow-Origin"] = origin
            elif settings.CORS_ALLOW_ALL_ORIGINS:
                response["Access-Control-Allow-Origin"] = "*"
                
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Max-Age"] = "86400"  # 24 hours
            return response
            
        # For non-OPTIONS requests, proceed normally
        response = self.get_response(request)
        return response
