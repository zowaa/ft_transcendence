from django.urls import path
from .views import register_user, user_login, user_logout, get_profile, OAuth42APIView, getOAuth42CallbackAPIView,register_user_oauth2

urlpatterns = [
	path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', get_profile, name='profile'),
    path('register42', register_user_oauth2, name='register_oauth2'),
    path('auth42/', OAuth42APIView, name='oauth2_42'),
    path('auth42_callback/', getOAuth42CallbackAPIView, name='oauth2_42_callback'),
    # path('update/', update_profile, name='update'),
    # path('users/', views.UserList.as_view, name='users'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]