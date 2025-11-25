"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin  
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from games.views import GameViewSet
from players.views import PlayerViewSet
from scores.views import ScoreViewSet
from leaderboard.views import LeaderboardViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'scores', ScoreViewSet, basename='score')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
