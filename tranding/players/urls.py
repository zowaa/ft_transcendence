from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
	path("", views.index, name="index"),
	path('players/login/', views.login, name='login'),
    path('players/register/', views.register, name='register'),
    path("players/logout/", views.logout, name="logout"),
	path("players/authentication/", views.authentication, name="authentication"),
    # path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path("players/userProfile/", views.userProfile, name="userProfile"),
]
