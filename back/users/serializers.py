from rest_framework import serializers
from .models import CustomUser, Games
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class CustomAuthError(Exception):
    def __init__(self, detail, status_code):
        self.detail = detail
        self.status_code = status_code

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    display_name = serializers.CharField(max_length=100, required=False)
    avatar = serializers.URLField(required=False)
    is_42_user = serializers.BooleanField(required=False)
    # print("UserSerializer")
    class Meta:
        model = CustomUser
        fields = ['username', 'display_name', 'avatar', 'is_42_user']
    
# class RegisterUserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
#     password = serializers.CharField(min_length=8, max_length=100, required=True, write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUser(
#             username = validated_data['username'],
#             display_name = validated_data['username'],
#             status = "online",
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user

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

class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'first_player', 'second_player', 'first_player_score', 'second_player_score', 'created_at', 'updated_at']