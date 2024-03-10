from django.urls import path
from .views import RegisterUserView, UserLoginAPIView, LogoutUserView, GetProfileView, OAuth42RedirectView, OAuth42CallbackView, UpdateProfileView, send_request, accept_request, reject_request, disable2fa, generateOtp, verifyOtp, validateOtp 

urlpatterns = [
	path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('profile/', GetProfileView.as_view(), name='profile'),
    path('auth42/', OAuth42RedirectView.as_view(), name='oauth2_42'),
    path('auth42_callback/', OAuth42CallbackView.as_view(), name='oauth2_42_callback'),
    path('update/', UpdateProfileView.as_view(), name='update'),
    path('send_request/', send_request, name='send_request'),
    path('accept_request/', accept_request, name='accept_request'),
    path('otp/disable', disable2fa.as_view(), name='disable2fa'),
    path('otp/generate', generateOtp.as_view(), name='generate_otp'),
    path('otp/verify', verifyOtp.as_view(), name='verify_otp'),
    path('otp/validate', validateOtp.as_view(), name='validate_otp'),
]