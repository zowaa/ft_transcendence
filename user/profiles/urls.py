from django.urls import path
from .views import Friends, Profile, PlayerAvatarUpload, ChangePasswordView

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('friends/', Friends.as_view(), name='friends'),
    path('avatar/', PlayerAvatarUpload.as_view(), name='avatar'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
]