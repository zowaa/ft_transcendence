from rest_framework import serializers
from .models import CustomUser

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'display_name', 'date_joined', 'last_login', 'avatar', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_42_user', 'double_auth']
