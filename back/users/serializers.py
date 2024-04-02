from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    display_name = serializers.CharField(max_length=100, required=False)
    avatar = serializers.URLField(required=False)
    is_42_user = serializers.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'display_name', 'avatar', 'is_42_user']

class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = CustomUser.objects.filter(username=username).first()

        if user:
            if user.check_password(password):
                user.status = "online"
                user.save()
                return user
            else:
                raise serializers.ValidationError({"password": ["Incorrect password."]})
        else:
            raise serializers.ValidationError({"username": ["User does not exist."]})