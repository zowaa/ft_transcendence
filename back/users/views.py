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

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # add jwt
            response_data = {
                "success": True,
                "message": "User registered successfully",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OAuth42RedirectView(APIView):
    def get(self, request, *args, **kwargs):
        authorization_url = 'https://api.intra.42.fr/oauth/authorize'
        client_id = settings.OAUTH42_CLIENT_ID
        redirect_uri = settings.OAUTH42_REDIRECT_URI  # Ensure this is set in your settings
        scope = 'public'  # Adjust scope as per your requirements
        auth_url = f'{authorization_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}'
        return redirect(auth_url)

class OAuth42CallbackView(APIView):
    def get(self, request, *args, **kwargs):
        code = request.query_params.get('code')
        token_url = 'https://api.intra.42.fr/oauth/token'
        payload = {
            "grant_type": "authorization_code",
            'client_id': settings.OAUTH42_CLIENT_ID,
            'client_secret': settings.OAUTH42_CLIENT_SECRET,
            'code': code,
            'redirect_uri': 'https://localhost:8000/auth42_callback',
        }

        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status()  # This will raise an exception for HTTP errors
            access_token = response.json().get('access_token')
            if not access_token:
                raise ValueError("Missing access token in response")
            
            user_data = self.fetch_42_user(access_token)
            if not user_data:
                raise ValueError("Failed to fetch user data")

            response = self.process_user_data(user_data)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                return Response({"statusCode": 401, "message": "Double authentification required."})
            else :
                user.status = "online"
                user.save()
                # Generate JWT tokens for the user
                access_token = token_generation(user)
                response = Response({"success": True,}, status=status.HTTP_200_OK)
                # Set the JWT as a cookie in the response
                response.set_cookie("jwt", value=access_token, httponly=True, secure=True)
                return response
        else:
            serializer = UserSerializer(data={'username': username, 'display_name': display_name, 'is_42_user' : True, 'avatar' : avatar_url})
            if serializer.is_valid():
                # If the data is valid, create the user
                user = serializer.save()
                user.status = "online"
                user.save()
                # Generate JWT tokens for the user
                access_token = token_generation(user)
                response = Response({"success": True,}, status=status.HTTP_200_OK)
                # Set the JWT as a cookie in the response
                response.set_cookie("jwt", value=access_token, httponly=True, secure=True)
                return response

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            access_token = token_generation(user)            
            # Prepare the response data
            response_data = {
                'message': 'Login successful.',
                'access': access_token,
                'infos': serializer.data,
            }
            
            # Create a Response object
            response = Response(response_data, status=status.HTTP_200_OK)

            # Set the JWT as a cookie in the response
            response.set_cookie("jwt", access_token, httponly=True, secure=True)
            
            return response
        
        # If the serializer is not valid
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class LogoutUserView(APIView):
    @method_decorator(token_required)
    def post(self, request):
        # request.user.status = "offline";
        # request.user.save()
        response = Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        response.delete_cookie('jwt')
        return response

###################################################
#                     profile                     #        
###################################################

class Profile(APIView):
    @method_decorator(token_required)
    def get(self, request):
        try:
            username = request.query_params.get('username')
            if username:
                user = CustomUser.objects.filter(username=username).first()
                if not user:
                    return Response({"status": 404, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                serializer = ProfileSerializer(user)
                return Response({"status": 200, "user": serializer.data}, status=status.HTTP_200_OK)
            
            user = CustomUser.objects.filter(id=request.user_payload['user']['id']).first()
            serializer = ProfileSerializer(user)
            return Response({"status": 200, "player": serializer.data}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"status": 404, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                return Response({"status": 400, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"status": 404, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PlayerAvatarUpload(APIView):
    @method_decorator(token_required)
    def post(self, request):
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)
            
            file = request.FILES['avatar']
            user.avatar.save(file.name, file, save=True)
            
            return Response({
                "status": 200,
                "message": "Avatar updated successfully",
                # "avatar_url": request.build_absolute_uri(user.avatar.url)
                "avatar_url": request.build_absolute_uri(settings.MEDIA_URL + str(user.avatar))
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
        get_type = request.query_params.get('target', 'friends')  # Default to listing friends

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

###################################################
#                        2fa                      #        
###################################################

class QRCodeTwoFactorView(APIView):
    @method_decorator(token_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        qr_code_uri = generate_qrcode(user.id, issuer_name="transcending")

        img = qrcode.make(qr_code_uri)
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response

class TwoFactorVerifyView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get("code")
        jwt = request.COOKIES.get("jwt")

        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)

            if verify_code(user_id, code):
                if not user.double_auth:
                    user.double_auth = True
                    user.save()
                    return Response({"statusCode": 200, "message": "2FA setup successfully."})
                
                # regenerate JWT token if needed
                access_token = token_generation(user)
                user.status = "online"
                user.save()
                response = Response({"statusCode": 200, "message": "2FA verified successfully."})
                response.set_cookie("jwt", value=access_token, httponly=True, secure=True)
                return response
            else:
                return Response({"statusCode": 401, "message": "Incorrect 2FA code."})
        except jwt.ExpiredSignatureError:
            return Response({"statusCode": 401, "error": "Expired token"})
        except (jwt.InvalidTokenError, CustomUser.DoesNotExist):
            return Response({"statusCode": 401, "error": "Invalid token or player not found"})