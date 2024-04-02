from .models import CustomUser, Friends
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProfileSerializer, UpdateProfileSerializer
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
        try:
            user_data = request.data
            user = CustomUser.objects.filter(id=request.user_payload['user']['id']).first()
            serializer = UpdateProfileSerializer(user, data=user_data, partial=True)  # partial=True allows for partial updates
            
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 200, "message": "User updated successfully", "user": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": 400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"status": 404, "error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response({"old_password": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password:
            return Response({"new_password": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(old_password):
            return Response({"old_password": ["Old password is incorrect."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"new_password": list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"status": "success", "message": "Password updated successfully"}, status=status.HTTP_200_OK)

###################################################
#                     friends                     #        
###################################################

class FriendsView(APIView):
    @method_decorator(token_required)
    def get(self, request):  # get friends, friend requests, or friend invites
        current_user_username = request.user_payload['user']['username']

        try:
            current_user = CustomUser.objects.get(username=current_user_username)
        except CustomUser.DoesNotExist:
            return Response({"status": 404, "message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fixed syntax error in query (missing parenthesis)
        query = Q(sender=current_user) | Q(receiver=current_user) | Q(status='accepted')

        friends = Friends.objects.filter(query)
        friends_data = []
        for f in friends:
            friend = f.sender if f.sender != current_user else f.receiver
            friend_data = ProfileSerializer(friend).data
            friends_data.append(friend_data)

        return Response({"status": 200, "friendships": friends_data}, status=status.HTTP_200_OK)

    @method_decorator(token_required)
    def post(self, request):  # send friend request
        sender_username = request.user_payload['user']['username']
        receiver_username = request.data.get('username')

        if not receiver_username:
            return Response({"status": 400, "message": "Receiver username is required."}, status=status.HTTP_400_BAD_REQUEST)
        if sender_username == receiver_username:
            return Response({"status": 400, "message": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = CustomUser.objects.get(username=sender_username)
            receiver = CustomUser.objects.get(username=receiver_username)

            # Check if there's already a friend request in any direction
            existing_friend = Friends.objects.filter(
                Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
            ).first()

            if existing_friend:
                return Response({"status": 400, "message": "Friend request already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            Friends.objects.create(sender=sender, receiver=receiver, status='pending')  # Assuming status should be 'pending' initially
            return Response({"status": 200, "message": "Friend request sent successfully."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"status": 404, "message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

