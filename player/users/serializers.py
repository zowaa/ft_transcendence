from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, allow_blank=True, required=False)
    display_name = serializers.CharField(max_length=150, allow_blank=True, required=False)
    double_auth = serializers.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'display_name', 'double_auth']

    def update(self, instance, validated_data):
        # Conditional updates for each field
        if 'display_name' in validated_data:
            instance.display_name = validated_data['display_name']
        if 'username' in validated_data:
            instance.username = validated_data['username']
        if 'double_auth' in validated_data:
            instance.double_auth = validated_data['double_auth']
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'display_name', 'date_joined', 'last_login', 'avatar', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_42_user', 'double_auth']
