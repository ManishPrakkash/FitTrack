"""
URL configuration for fittrack_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from .views import api_root

urlpatterns = [
    # Root URL pattern
    path('', api_root, name='api-root'),

    # Admin and API endpoints
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/challenges/', include('challenges.urls')),
    path('api/activities/', include('activities.urls')),

    # Direct MongoDB authentication endpoints
    path('api/mongodb/', include('mongodb_auth_urls')),
]
