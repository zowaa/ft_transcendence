from django.urls import path
from . import views
from .views import LoginView
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
	path("", views.index, name="index"),
	path('players/login/', views.login, name='login'),
    path('players/register/', views.register, name='register'),
    path("players/logout/", views.logout, name="logout"),
	path("players/authentication/", views.authentication, name="authentication"),
    # path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path("players/userProfile/", views.userProfile, name="userProfile"),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
     path('players/login', LoginView.as_view(), name ='login')
]
