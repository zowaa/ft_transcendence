from django.urls import path
from .views import RegisterUserView, UserLoginAPIView, LogoutUserView, OAuth42RedirectView, OAuth42CallbackView, QRCodeTwoFactorView, TwoFactorVerifyView

urlpatterns = [
	path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('auth42/', OAuth42RedirectView.as_view(), name='oauth2_42'),
    path('auth42_callback/', OAuth42CallbackView.as_view(), name='oauth2_42_callback'),
    path('qr_code/', QRCodeTwoFactorView.as_view(), name='qr_code'),
    path('double_factor/', TwoFactorVerifyView.as_view(), name='double_factor'),
]