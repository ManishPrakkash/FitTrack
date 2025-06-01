"""
URL patterns for MongoDB-based activity management.
"""
from django.urls import path
from mongodb_activity_views import (
    MongoDBActivityListView,
    MongoDBActivityChallengeView,
    MongoDBActivityLogView
)

urlpatterns = [
    # Activity operations
    path('', MongoDBActivityListView.as_view(), name='mongodb-activity-list'),
    path('challenge/<str:challenge_id>/', MongoDBActivityChallengeView.as_view(), name='mongodb-activity-challenge'),
    path('log/<str:challenge_id>/', MongoDBActivityLogView.as_view(), name='mongodb-activity-log'),
]
