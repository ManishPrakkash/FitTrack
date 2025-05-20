"""
Simple authentication URLs for MongoDB.
"""
from django.urls import path
from . import simple_auth_views

urlpatterns = [
    path('register/', simple_auth_views.register_user, name='simple_register'),
    path('login/', simple_auth_views.login_user, name='simple_login'),
]
