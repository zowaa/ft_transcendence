from rest_framework import authentication
from rest_framework import exceptions
import jwt
from .models import CustomUser
from django.conf import settings
from .jwt import token_decode

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the JWT token from the Authorization header
        token = request.COOKIES.get('jwt')
        print("TOKEN")
        print(token)
        jwt = request.headers.get("Authorization")
        print(jwt)
        if not token:
            return None  # No authentication attempted

        # decode and validate the token
        try:
            payload = jwt.token_decode(token)
            print(payload)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        # get user from the decoded token payload
        user = self.get_user(payload)

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, token)

    def get_user(self, payload):
        try:
            user_id = payload['user_id']
            user = CustomUser.objects.get(id=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None