from .models import CustomUser, Friends
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegisterUserSerializer, LoginUserSerializer, ProfileSerializer, UpdateProfileSerializer, UpdatePasswordSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
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
from .jwt import token_generation, get_user_id
from .decorators import token_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from .otp import generate_qrcode, verify_code
import qrcode
from django.http import HttpResponse
from django.http import JsonResponse
import os

###################################################
#                     profile                     #        
###################################################

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

class PlayerAvatarUpload(APIView):
    @method_decorator(token_required)
    def post(self, request):
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)

            file = request.FILES['avatar']
            # Define the path for the file
            file_path = os.path.join(settings.MEDIA_ROOT, 'avatars', file.name)
            # Save the file to the filesystem
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # Generate the URL for the saved file
            avatar_url = request.build_absolute_uri(settings.MEDIA_URL + 'avatars/' + file.name)

            # Update the user's avatar URL
            user.avatar = avatar_url
            user.save()

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
            return Response({
                "status": 500,
                "message": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class PlayerAvatarUpload(APIView):
#     @method_decorator(token_required)
#     def post(self, request):
#         try:
#             user_id = request.user_payload['user']['id']
#             user = CustomUser.objects.get(id=user_id)
            
#             file = request.FILES['avatar']
#             user.avatar.save(file.name, file, save=True)
            
#             return Response({
#                 "status": 200,
#                 "message": "Avatar updated successfully",
#                 # "avatar_url": request.build_absolute_uri(user.avatar.url)
#                 "avatar_url": request.build_absolute_uri(settings.MEDIA_URL + str(user.avatar))
#             }, status=status.HTTP_200_OK)
#         except CustomUser.DoesNotExist:
#             return Response({
#                 "status": 404,
#                 "message": "User not found",
#             }, status=status.HTTP_404_NOT_FOUND)
#         except KeyError:
#             return Response({
#                 "status": 400,
#                 "message": "No avatar file provided",
#             }, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({
#                 "status": 500,
#                 "message": str(e),
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangePasswordView(APIView):
    @method_decorator(token_required)
    def put(self, request, *args, **kwargs):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"status": "success", "message": "Password updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###################################################
#                     friends                     #        
###################################################

class Friends(APIView):
    @method_decorator(token_required)
    def get(self, request):
        user_id = request.user_payload['user']['id']
        get_type = request.query_params.get('target', 'friends')

        query = Q(sender_id=user_id) | Q(receiver_id=user_id)
        if get_type == 'invites':
            query &= Q(receiver_id=user_id, status='pending')
        elif get_type == 'requests':
            query &= Q(sender_id=user_id, status='pending')
        elif get_type == 'friends':
            query &= Q(status='accepted')
        else:
            return Response({"status": 400, "message": "Invalid request type."}, status=status.HTTP_400_BAD_REQUEST)

        friends = Friends.objects.filter(query)
        friends_data = []
        for f in friends:
            friend = friends.sender if friends.sender.id != user_id else friends.receiver
            friend_data = ProfileSerializer(friend).data
            friends_data.append(friend_data)

        return Response({"status": 200, "friendships": friends_data}, status=status.HTTP_200_OK)

    @method_decorator(token_required)
    def post(self, request):
        user_id = request.user_payload['user']['id']
        receiver_id = request.data.get('receiver_id')

        if not receiver_id:
            return Response({"status": 400, "message": "Receiver ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        if user_id == receiver_id:
            return Response({"status": 400, "message": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = CustomUser.objects.get(id=user_id)
            receiver = CustomUser.objects.get(id=receiver_id)

            # Check if there's already a friend request in any direction
            existing_friend = Friends.objects.filter(
                (Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))
            ).first()

            if existing_friend:
                if existing_friend.status == 'pending':
                    return Response({"status": 400, "message": "Friend request already sent or received."}, status=status.HTTP_400_BAD_REQUEST)
                elif existing_friend.status == 'accepted':
                    return Response({"status": 400, "message": "You are already friends."}, status=status.HTTP_400_BAD_REQUEST)
            
            # No existing friend request or friendship, so create a new request
            Friends.objects.create(sender=sender, receiver=receiver, status='pending')
            return Response({"status": 200, "message": "Friend request sent successfully."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"status": 404, "message": "Player not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(token_required)
    def put(self, request):
        # New endpoint for accepting or rejecting friend requests
        user_id = request.user_payload['user']['id']
        receiver_id = request.data.get('receiver_id')
        action = request.data.get('action')  # "accept" or "reject"

        if action not in ['accept', 'reject']:
            return Response({"status": 400, "message": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # request where the current user is the receiver (to ensure they have the right to accept/reject)
            request = Friends.objects.get(receiver_id=user_id, sender_id=receiver_id, status='pending')

            if action == 'accept':
                request.status = 'accepted'
                request.save()
                message = "Friend request accepted."
            else:  # Reject
                request.status = 'rejected'
                request.save()
                message = "Friend request rejected."
            return Response({"status": 200, "message": message}, status=status.HTTP_200_OK)
        except request.DoesNotExist:
            return Response({"status": 404, "message": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(token_required)
    def delete(self, request):
        user_id = request.user_payload['user']['id']
        receiver_id = request.data.get('receiver_id')

        if not receiver_id:
            return Response({"status": 400, "message": "Receiver ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Attempt to find a relation where the current user is either the sender or receiver
            friend = Friends.objects.filter(
                (Q(sender_id=user_id) & Q(receiver_id=receiver_id)) | 
                (Q(sender_id=receiver_id) & Q(receiver_id=user_id))
            ).first()

            if friend:
                friend.delete()
                return Response({
                    "status": 200,
                    "message": "Friendship or friend request successfully deleted."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": 404,
                    "message": "Friendship or friend request not found."
                }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)