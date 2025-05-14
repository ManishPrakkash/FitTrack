from django.urls import path
from .views import ChallengeListView, ChallengeDetailView, UserProgressView, LeaderboardView

urlpatterns = [
    path('challenges/', ChallengeListView.as_view(), name='challenge-list'),
    path('challenges/<str:challenge_id>/', ChallengeDetailView.as_view(), name='challenge-detail'),
    path('progress/', UserProgressView.as_view(), name='user-progress-create'),
    path('progress/<str:user_id>/', UserProgressView.as_view(), name='user-progress-list'),
    path('leaderboard/<str:challenge_id>/', LeaderboardView.as_view(), name='challenge-leaderboard'),
]
