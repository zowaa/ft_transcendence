from rest_framework import serializers
from .models import CustomUser, Games
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(min_length=8, max_length=100, write_only=True)
    avatar = serializers.ImageField(required=False)
    is_42_user = serializers.BooleanField(required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'display_name', 'date_joined', 'last_login', 'avatar', 'friends', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_active', 'is_42_user', 'access_token', 'otp_enabled', 'otp_verified', 'otp_base32', 'otp_auth_url']
        extra_kwargs = {'password': {'write_only': True}}
        # read_only_fields = ['id', 'date_joined', 'last_login']
    
    def create(self, validated_data):
        user = CustomUser(
            username = validated_data['username'],
            display_name = validated_data['username'],
            is_42_user = validated_data['is_42_user'],
        )
        user.save()
        return user
    
class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(min_length=8, max_length=100, required=True, write_only=True)
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'display_name', 'date_joined', 'last_login', 'avatar', 'friends', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_active', 'is_42_user', 'access_token', 'otp_enabled', 'otp_verified', 'otp_base32', 'otp_auth_url']
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

# class RegisterUser42Serializer(username, display_name):
#     username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
#     disoplay_name = serializers.CharField(max_length=100, required=False)
#     avatar = serializers.ImageField(required=False)
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'password', 'display_name', 'date_joined', 'last_login', 'avatar', 'friends', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_active', 'is_42_user', 'access_token', 'otp_enabled', 'otp_verified', 'otp_base32', 'otp_auth_url']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUser(
#             username = validated_data['username'],
#             display_name = validated_data['display_name'],
#             is_42_user = True,
#             # avatar=validated_data['avatar']
#         )
#         user.save()
#         return user

class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=8, max_length=100, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'display_name', 'date_joined', 'last_login', 'avatar', 'friends', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_active', 'is_42_user', 'access_token', 'otp_enabled', 'otp_verified', 'otp_base32', 'otp_auth_url']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = CustomUser.objects.filter(username=username).first()

        if user:
            if user.check_password(password):
                return user
            else:
                raise serializers.ValidationError("Incorrect password.")
        else:
            raise serializers.ValidationError("User does not exist.")
    
    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.display_name = validated_data.get('display_name', instance.display_name)
    #     instance.avatar_base64 = validated_data.get('avatar_base64', instance.avatar_base64)
    #     instance.friends = validated_data.get('friends', instance.friends)
    #     instance.nb_wins = validated_data.get('nb_wins', instance.nb_wins)
    #     instance.nb_losses = validated_data.get('nb_losses', instance.nb_losses)
    #     instance.nb_plays = validated_data.get('nb_plays', instance.nb_plays)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.is_active = validated_data.get('is_active', instance.is_active)
    #     instance.is_42_user = validated_data.get('is_42_user', instance.is_42_user)
    #     instance.save()
    #     return instance
    
    # def validate(self, data):
    #     if data.get('is_42_user') and not data.get('display_name'):
    #         raise serializers.ValidationError("display_name is required for 42 users.")
    #     return data

    # def validate(self, data):
    #     username = data.get('username')
    #     password = data.get('password')

    #     if not username or not password:
    #         raise serializers.ValidationError("Both username and password are required.")

    #     user = CustomUser.objects.filter(username=username).first()

    #     if user:
    #         if user.check_password(password):
    #             return user
    #         else:
    #             raise serializers.ValidationError("Incorrect password.")
    #     else:
    #         raise serializers.ValidationError("User does not exist.")

class UpdatePassword(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=100, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True}}
    
        def update(self, instance, validated_data):
            instance.set_password(validated_data['password'])
            instance.save()
            return instance

class UpdateUsername(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    class Meta:
        model = CustomUser
        fields = ['username']
        extra_kwargs = {'username': {'required': True, 'validators': [UniqueValidator(queryset=CustomUser.objects.all())]}}
    
        def update(self, instance, validated_data):
            instance.username = validated_data['username']
            instance.save()
            return instance

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(min_length=8, max_length=100, write_only=True)
    avatar = serializers.ImageField(required=False)
    
    class Meta:
        model = CustomUser
        fields = '__all__'

class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'first_player', 'second_player', 'first_player_score', 'second_player_score', 'created_at', 'updated_at']
        # read_only_fields = ['id', 'created_at', 'updated_at']