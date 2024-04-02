from django.urls import path
from .views import FriendsView

urlpatterns = [
    path('friends/', FriendsView.as_view(), name='friends'),
]