from django.urls import path
from .views import register_user, user_login, user_logout, get_profile, OAuth42APIView, getOAuth42CallbackAPIView,register_user_oauth2, update_profile, send_request, accept_request, reject_request, disable2fa, generateOtp, verifyOtp, validateOtp 

urlpatterns = [
	path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', get_profile, name='profile'),
    path('register42', register_user_oauth2, name='register_oauth2'),
    path('auth42/', OAuth42APIView, name='oauth2_42'),
    path('auth42_callback/', getOAuth42CallbackAPIView, name='oauth2_42_callback'),
    path('update/', update_profile, name='update'),
    path('profile/', get_profile, name='profile'),
    path('send_request/', send_request, name='send_request'),
    path('accept_request/', accept_request, name='accept_request'),
    path('otp/disable', disable2fa.as_view(), name='disable2fa'),
    path('otp/generate', generateOtp.as_view(), name='generate_otp'),
    path('otp/verify', verifyOtp.as_view(), name='verify_otp'),
    path('otp/validate', validateOtp.as_view(), name='validate_otp'),
]