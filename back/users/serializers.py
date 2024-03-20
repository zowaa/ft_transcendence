from rest_framework import serializers
from .models import CustomUser, Games
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(min_length=8, max_length=100, required=False, write_only=True)
    avatar = serializers.ImageField(required=False)
    is_42_user = serializers.BooleanField(required=False)
    # print("UserSerializer")
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'display_name', 'date_joined', 'last_login', 'avatar', 'friends', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_active', 'is_42_user', 'otp_enabled', 'otp_verified', 'otp_base32', 'otp_auth_url']
        extra_kwargs = {'password': {'write_only': True}}
    
class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(min_length=8, max_length=100, required=True, write_only=True)
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'display_name', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username = validated_data['username'],
            display_name = validated_data['username'],
            # avatar=validated_data['avatar']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=8, max_length=100, write_only=True)
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
                user.status = "online";
                user.save()
                return user
            else:
                raise serializers.ValidationError("Incorrect password.")
        else:
            raise serializers.ValidationError("User does not exist.")

class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, allow_blank=True, required=False)
    display_name = serializers.CharField(max_length=150, allow_blank=True, required=False)
    otp_enabled = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        # Conditional updates for each field
        if 'username' in validated_data:
            instance.username = validated_data['username']
        if 'display_name' in validated_data:
            instance.first_name = validated_data['display_name']
        if 'otp_enabled' in validated_data:
            instance.otp_enabled = validated_data['otp_enabled']
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'display_name', 'date_joined', 'last_login', 'avatar', 'friends', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_42_user', 'otp_enabled']

class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'first_player', 'second_player', 'first_player_score', 'second_player_score', 'created_at', 'updated_at']
        # read_only_fields = ['id', 'created_at', 'updated_at']