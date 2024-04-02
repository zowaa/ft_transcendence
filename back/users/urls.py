from django.urls import path
from .views import RegisterUserView, UserLoginAPIView, LogoutUserView, OAuth42RedirectView, OAuth42CallbackView, Friends, Profile, PlayerAvatarUpload, ChangePasswordView, QRCodeTwoFactorView, TwoFactorVerifyView#, CheckUser

urlpatterns = [
	path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('auth42/', OAuth42RedirectView.as_view(), name='oauth2_42'),
    path('auth42_callback/', OAuth42CallbackView.as_view(), name='oauth2_42_callback'),
    path('friends/', Friends.as_view(), name='friends'),
    path('avatar/', PlayerAvatarUpload.as_view(), name='avatar'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('qr_code/', QRCodeTwoFactorView.as_view(), name='qr_code'),
    path('double_factor/', TwoFactorVerifyView.as_view(), name='double_factor'),
	# path('check_user/', CheckUser.as_view(), name='check_user'),
]