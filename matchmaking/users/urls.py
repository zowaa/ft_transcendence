from django.urls import path
from . import views

urlpatterns = [
    path('tournement/register/', views.RegistreTournement.as_view(), name='start_tournement'),
    path('tournement/finish/', views.FinishTournement.as_view(), name='finish_tournement'),
    path('game/register/', views.RegistreGame.as_view(), name='start_game'),
    path('game/finish/', views.FinishGame.as_view(), name='finish_game'),
]