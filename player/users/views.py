from .models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProfileSerializer
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import requests
from rest_framework.views import APIView
from django.shortcuts import redirect
import pyotp
from rest_framework import generics
from rest_framework.views import APIView
import jwt
from rest_framework import exceptions
from .jwt import token_generation, get_user_id
from .decorators import token_required
from django.utils.decorators import method_decorator
from django.db.models import Q
import os
import tempfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from pyuploadcare import Uploadcare

#####################################################
#                       profile                     #        
#####################################################

class Profile(APIView):
    @method_decorator(token_required)
    def get(self, request):
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)
            if not user:
                return Response({"status": 404, "error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ProfileSerializer(user)
            return Response({"status": 200, "user": serializer.data}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"status": 404, "error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(token_required)
    def put(self, request):
        user_id = request.user_payload['user']['id']
        username = request.data.get('username')
        display_name = request.data.get('display_name')
        double_auth = request.data.get('double_auth', None)

        if username is not None and CustomUser.objects.filter(username=username).exclude(id=user_id).exists():
            return Response({"success": False, "error": {"username": "This username is already taken."}}, status=status.HTTP_400_BAD_REQUEST)
        
        if display_name is not None and CustomUser.objects.filter(display_name=display_name).exclude(id=user_id).exists():
            return Response({"success": False, "error": {"display_name": "This display name is already taken."}}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(id=user_id)
            if username is not None:
                user.username = username
            if display_name is not None:
                user.display_name = display_name
            if double_auth is not None:
                user.double_auth = double_auth
            
            user.save()
            return Response({"success": True, "message": "Profile updated successfully."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"success": False, "error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e: 
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"success": False, "error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#####################################################
#         avatar upload with CDN UploadCare         #
#####################################################

class PlayerAvatarUpload(APIView): # CDN UploadCare to be tested after installing the package (gotta check w/ yassine)
    @method_decorator(token_required)
    def post(self, request):
        uploadcare = Uploadcare(public_key=settings.UPLOADCARE['pub_key'], secret_key=settings.UPLOADCARE['secret'])
        
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)

            file = request.FILES['avatar']

            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in file.chunks():
                    tmp_file.write(chunk)
                tmp_file.flush()
                
                with open(tmp_file.name, "rb") as tmp_file_for_upload:
                    ucare_file = uploadcare.upload(tmp_file_for_upload)

            avatar_url = ucare_file.cdn_url

            user.avatar = avatar_url
            user.save()

            os.remove(tmp_file.name)

            return Response({
                "status": 200,
                "message": "Avatar updated successfully",
                "avatar_url": avatar_url
            }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({
                "status": 404,
                "message": "User not found",
            }, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({
                "status": 400,
                "message": "No avatar file provided",
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if 'tmp_file.name' in locals():
                os.remove(tmp_file.name)
            return Response({
                "status": 500,
                "message": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#####################################################
#                    password                       #
#####################################################

class ChangePasswordView(APIView):
    @method_decorator(token_required)
    def put(self, request, *args, **kwargs):
        user_id = request.user_payload['user']['id']
        user = CustomUser.objects.get(id=user_id)
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password:
            return Response({"error": {"old_password": ["This field is required."]}}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password:
            return Response({"error": {"new_password": ["This field is required."]}}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(old_password):
            return Response({"error": {"old_p": ["Old password is incorrect."]}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"error": {"new_p": [e.messages]}}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"status": "success", "message": "Password updated successfully"}, status=status.HTTP_200_OK)