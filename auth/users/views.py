from .models import CustomUser, Friends
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, LoginUserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.conf import settings
import requests
from rest_framework.views import APIView
from django.shortcuts import redirect
import pyotp
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
import jwt
from rest_framework import authentication
from rest_framework import exceptions
from .jwt import token_generation
from .decorators import token_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from .otp import generate_qrcode, verify_code
import qrcode
from django.http import HttpResponse
from django.http import JsonResponse
import os
from django.http import HttpResponseRedirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"success": False, "error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({"success": False, "error": {"username": ["A user with that username already exists."]}}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"success": False, "error": {"password": e.messages}}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser(username=username, display_name=username, status="online")
            user.set_password(password)
            user.save()
            access_token = token_generation(user)
            response_data = {
                "success": True,
                "message": "User registered successfully",
                "access": access_token,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False, "error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OAuth42RedirectView(APIView):
    def get(self, request, *args, **kwargs):
        authorization_url = 'https://api.intra.42.fr/oauth/authorize'
        client_id = settings.OAUTH42_CLIENT_ID
        redirect_uri = settings.OAUTH42_REDIRECT_URI 
        scope = 'public'  
        auth_url = f'{authorization_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}'
        return redirect(auth_url)

class OAuth42CallbackView(APIView):
    def get(self, request, *args, **kwargs):
        code = request.query_params.get('code')
        error = request.query_params.get('error')
        if error:
            return HttpResponseRedirect("https://localhost:443/sign_in")
        if not code:
            return HttpResponseRedirect("https://localhost:443/sign_in")
        
        token_url = 'https://api.intra.42.fr/oauth/token'
        payload = {
            "grant_type": "authorization_code",
            "client_id": settings.OAUTH42_CLIENT_ID,
            "client_secret": settings.OAUTH42_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.OAUTH42_REDIRECT_URI,
        }

        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status()  
            access_token = response.json().get('access_token')
            if not access_token:
                return HttpResponseRedirect("https://localhost:443/sign_in")
            
            user_data = self.fetch_42_user(access_token)

            if not user_data:
                return HttpResponseRedirect("https://localhost:443/sign_in")

            return self.process_user_data(user_data)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fetch_42_user(self, access_token):
        user_url = 'https://api.intra.42.fr/v2/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(user_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def process_user_data(self, user_data):
        username = user_data['login']
        display_name = user_data['displayname']
        avatar_url = user_data['image']['link']

        user = CustomUser.objects.filter(username=username, is_42_user=True).first()
        if user:
            if (user.double_auth == True):
                return HttpResponseRedirect("https://localhost:443/sign_in") # 2FA link
            else :
                user.status = "online"
                user.save()
                access_token = token_generation(user)
                response = HttpResponseRedirect("https://localhost:443/profile?success=true")
                response.set_cookie("jwt", value=access_token)
                return response
        else:
            serializer = UserSerializer(data={'username': username, 'display_name': display_name, 'is_42_user' : True, 'avatar' : avatar_url})
            if serializer.is_valid():
                user = serializer.save()
                user.status = "online"
                user.save()
                access_token = token_generation(user)
                response = HttpResponseRedirect("https://localhost:443/profile?success=true")
                response.set_cookie("jwt", value=access_token)
                return response
            return HttpResponseRedirect("https://localhost:443/sign_in")

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            access_token = token_generation(user)            
            response_data = {
                "success": True,
                'message': 'Login successful.',
                'access': access_token,
            }
            
            response = Response(response_data, status=status.HTTP_200_OK)
            return response
        
        return Response({"success": False, "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserView(APIView):
    @method_decorator(token_required)
    def post(self, request):
        user_id = request.user_payload['user']['id']
        user = CustomUser.objects.get(id=user_id)
        user.status = "offline"
        user.save()
        response = Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        return response

###################################################
#                        2fa                      #        
###################################################

class QRCodeTwoFactorView(APIView):
    @method_decorator(token_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user_payload['user']['id']
        qr_code_uri = generate_qrcode(user_id, issuer_name="transcending")

        img = qrcode.make(qr_code_uri)
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")

        debug_info = qr_code_uri
        response['X-Debug-Info'] = debug_info
        return response

class TwoFactorVerifyView(APIView):
    @method_decorator(token_required)
    def post(self, request, *args, **kwargs):
        code = request.data.get("code")

        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)

            if verify_code(user_id, code):
                if not user.double_auth:
                    user.double_auth = True
                    user.save()
                    return Response({"statusCode": 200, "message": "2FA setup successfully."})
                
                response = Response({"statusCode": 200, "message": "2FA verified successfully."})
                return response
            else:
                return Response({"statusCode": 401, "message": "Incorrect 2FA code."})
        except Exception as e:
            return Response({"statusCode": 500, "error": str(e)})