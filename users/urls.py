from django.urls import path
from .views import register_user, user_login, user_logout, get_profile

urlpatterns = [
	path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', get_profile, name='profile'),
    path('update/', update_profile, name='update'),
    path('users/', views.UserList.as_view, name='users'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]