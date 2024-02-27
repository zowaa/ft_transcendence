from rest_framework import serializers
from .models import CustomUser, Games
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(min_length=8, max_length=100, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'display_name', 'date_joined', 'last_login', 'avatar_base64', 'friends', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_active', 'is_42_user']
        extra_kwargs = {'password': {'write_only': True}}
        # read_only_fields = ['id', 'date_joined', 'last_login']
    
class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(min_length=8, max_length=100, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'display_name', 'date_joined', 'last_login', 'avatar_base64', 'friends', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_active', 'is_42_user']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username = validated_data['username'],
            display_name = validated_data['username'],
            avatar_base64=validated_data['avatar_base64']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=8, max_length=100, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'display_name', 'date_joined', 'last_login', 'avatar_base64', 'friends', 'nb_wins', 'nb_losses', 'nb_plays', 'status', 'is_active', 'is_42_user']
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
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')
        return data
    


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
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'first_player', 'second_player', 'first_player_score', 'second_player_score', 'created_at', 'updated_at']
        # read_only_fields = ['id', 'created_at', 'updated_at']