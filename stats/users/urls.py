from django.urls import path
from .views import GameStatsView, TournementStatsView

urlpatterns = [
    path('game/stats/', GameStatsView.as_view(), name='game stats'),
    path('tournement/stats/', TournementStatsView.as_view(), name='tournement stats'),
]