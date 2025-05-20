"""
URL patterns for direct MongoDB authentication.
"""
from django.urls import path
from mongodb_auth_views import MongoDBRegisterView, MongoDBLoginView, MongoDBValidateTokenView

urlpatterns = [
    path('register/', MongoDBRegisterView.as_view(), name='mongodb-register'),
    path('login/', MongoDBLoginView.as_view(), name='mongodb-login'),
    path('validate-token/', MongoDBValidateTokenView.as_view(), name='mongodb-validate-token'),
]
