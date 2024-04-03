from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('tournement/registre/', views.RegistreTournement.as_view(), name='start_tournement'),
    path('tournement/finish/', views.FinishTournement.as_view(), name='finish_tournement')
]