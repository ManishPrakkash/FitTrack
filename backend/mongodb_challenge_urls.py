"""
URL patterns for MongoDB-based challenge management.
"""
from django.urls import path
from mongodb_challenge_views import (
    MongoDBChallengeListView,
    MongoDBChallengeDetailView,
    MongoDBChallengeJoinView,
    MongoDBChallengeLeaderboardView
)

urlpatterns = [
    # Challenge CRUD operations
    path('', MongoDBChallengeListView.as_view(), name='mongodb-challenge-list'),
    path('<str:challenge_id>/', MongoDBChallengeDetailView.as_view(), name='mongodb-challenge-detail'),
    
    # Challenge actions
    path('<str:challenge_id>/join/', MongoDBChallengeJoinView.as_view(), name='mongodb-challenge-join'),
    path('<str:challenge_id>/leaderboard/', MongoDBChallengeLeaderboardView.as_view(), name='mongodb-challenge-leaderboard'),
]
