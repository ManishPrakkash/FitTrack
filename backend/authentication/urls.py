"""
URL patterns for the authentication app.
"""
from django.urls import path
from .views import RegisterView, LoginView, ValidateTokenView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('validate-token/', ValidateTokenView.as_view(), name='validate-token'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
