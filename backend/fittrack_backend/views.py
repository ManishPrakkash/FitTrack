"""
Views for the fittrack_backend project.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    Root view for the FitTrack API.
    This view provides information about available API endpoints.
    """
    api_info = {
        'name': 'FitTrack API',
        'version': '1.0.0',
        'description': 'API for the FitTrack fitness tracking application',
        'endpoints': {
            'authentication': {
                'register': '/api/register/',
                'login': '/api/login/',
                'validate_token': '/api/validate-token/',
                'profile': '/api/profile/',
            },
            'mongodb_authentication': {
                'register': '/api/mongodb/register/',
                'login': '/api/mongodb/login/',
                'validate_token': '/api/mongodb/validate-token/',
            },
            'challenges': {
                'list': '/api/challenges/',
                'leaderboard': '/api/challenges/leaderboard/<challenge_id>/',
            },
            'activities': {
                'list': '/api/activities/',
            },
            'admin': '/admin/',
        }
    }
    return Response(api_info)
