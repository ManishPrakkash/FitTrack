"""
URL patterns for the challenges app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet
from .leaderboard import LeaderboardView

router = DefaultRouter()
router.register(r'', ChallengeViewSet, basename='challenge')

urlpatterns = [
    path('', include(router.urls)),
    path('leaderboard/<int:challenge_id>/', LeaderboardView.as_view(), name='leaderboard'),
]
