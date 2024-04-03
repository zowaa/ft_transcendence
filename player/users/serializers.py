from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'display_name', 'date_joined', 'last_login', 'avatar', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_42_user', 'double_auth']
