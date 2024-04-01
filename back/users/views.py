from .models import CustomUser, Friends
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, LoginUserSerializer, ProfileSerializer, UpdateProfileSerializer
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
from .jwt import token_generation, get_user_id
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
# from uploadcare import FileUpload, conf

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

# class RegisterUserView(APIView):
#     def post(self, request):
#         try:
#             serializer = RegisterUserSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 user = CustomUser.objects.get(username=serializer.validated_data['username'])
#                 access_token = token_generation(user)
#                 response_data = {
#                     "success": True,
#                     "message": "User registered successfully",
#                     "access": access_token,
#                 }
#                 return Response(response_data, status=status.HTTP_201_CREATED)
#             return Response({"success": False, "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             return Response({"success": False,"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        error = request.query_params.get('error')
        if error:
            return HttpResponseRedirect("https://localhost:443/sign_in")
            # return Response({"success": False, "error": error}, status=status.HTTP_401_UNAUTHORIZED)
        if not code:
            return HttpResponseRedirect("https://localhost:443/sign_in")
            # return Response({"success": False, "error": "Code parameter is required"}, status=status.HTTP_401_UNAUTHORIZED)
        
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
            response.raise_for_status()  # This will raise an exception for HTTP errors
            access_token = response.json().get('access_token')
            if not access_token:
                # Instead of raising ValueError, return an error response
                # return Response({"success": False, "error": "Missing access token in response"}, status=status.HTTP_401_UNAUTHORIZED)
                return HttpResponseRedirect("https://localhost:443/sign_in")
            
            user_data = self.fetch_42_user(access_token)

            if not user_data:
                # Instead of raising ValueError, return an error response
                # return Response({"success": False, "error": "Failed to fetch user data"}, status=status.HTTP_400_BAD_REQUEST)
                return HttpResponseRedirect("https://localhost:443/sign_in")

            return self.process_user_data(user_data)
        except Exception as e:
            # This catch block will handle exceptions and ensure a response is returned
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return Response({"error": "Unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                # return Response({"success": False, "message": "Double authentification required."}, status=status.HTTP_401_UNAUTHORIZED)
            else :
                user.status = "online"
                user.save()
                # Generate JWT tokens for the user
                access_token = token_generation(user)
                response = HttpResponseRedirect("https://localhost:443/profile?success=true")
                response.set_cookie("jwt", value=access_token)
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
                # response = Response({"success": True, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
                response = HttpResponseRedirect("https://localhost:443/profile?success=true")
                response.set_cookie("jwt", value=access_token)
                return response
            # return Response({"success": False, "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
            return HttpResponseRedirect("https://localhost:443/sign_in")

# class UserLoginAPIView(APIView):
#     def post(self, request):
#         serializer = LoginUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             access_token = token_generation(user)            
#             # Prepare the response data
#             response_data = {
#                 "success": True,
#                 'message': 'Login successful.',
#                 'access': access_token,
#             }
        
#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             return Response({"success": False, "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            access_token = token_generation(user)            
            # Prepare the response data
            response_data = {
                "success": True,
                'message': 'Login successful.',
                'access': access_token,
            }
            
            # Create a Response object
            response = Response(response_data, status=status.HTTP_200_OK)
            return response
        
        # If the serializer is not valid
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

# ###################################################
# #                     profile                     #        
# ###################################################

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

class PlayerAvatarUpload(APIView): # CDN UploadCare to be tested after installing the package (gotta check w/ yassine)
    @method_decorator(token_required)
    def post(self, request):
        conf.pub_key = settings.UPLOADCARE['pub_key']
        conf.secret = settings.UPLOADCARE['secret']
        
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)

            file = request.FILES['avatar']

            # uc_file = FileUpload.upload(file)

            # avatar_url = uc_file.cdn_url

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

    # @method_decorator(token_required)
    # def put(self, request): # accept or reject friend request
    #     current_user_username = request.user_payload['user']['username']
    #     sender_username = request.data.get('sender_username')  # Username of the request sender
    #     action = request.data.get('action')  # "accept" or "reject"

    #     if action not in ['accept', 'reject']:
    #         return Response({"status": 400, "message": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         current_user = CustomUser.objects.get(username=current_user_username)
    #         sender = CustomUser.objects.get(username=sender_username)

    #         request_obj = Friends.objects.get(receiver=current_user, sender=sender, status='pending')

    #         if action == 'accept':
    #             request_obj.status = 'accepted'
    #         else:  # Reject
    #             request_obj.status = 'rejected'
    #         request_obj.save()

    #         message = "Friend request accepted." if action == 'accept' else "Friend request rejected."
    #         return Response({"status": 200, "message": message}, status=status.HTTP_200_OK)
    #     except CustomUser.DoesNotExist:
    #         return Response({"status": 404, "message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    #     except Friends.DoesNotExist:
    #         return Response({"status": 404, "message": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @method_decorator(token_required)
    # def delete(self, request): # delete friend or friend request
    #     current_user_username = request.user_payload['user']['username']
    #     receiver_username = request.data.get('username')

    #     if not other_username:
    #         return Response({"status": 400, "message": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         current_user = CustomUser.objects.get(username=current_user_username)
    #         other_user = CustomUser.objects.get(username=other_username)

    #         friend = Friends.objects.filter(
    #             (Q(sender=current_user, receiver=other_user) | Q(sender=other_user, receiver=current_user))
    #         ).first()

    #         if friend:
    #             friend.delete()
    #             return Response({
    #                 "status": 200,
    #                 "message": "Friendship or friend request successfully deleted."
    #             }, status=status.HTTP_200_OK)
    #         else:
    #             return Response({
    #                 "status": 404,
    #                 "message": "Friendship or friend request not found."
    #             }, status=status.HTTP_404_NOT_FOUND)
    #     except CustomUser.DoesNotExist:
    #         return Response({"status": 404, "message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        # jwt = request.jwt

        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)

            if verify_code(user_id, code):
                if not user.double_auth:
                    user.double_auth = True
                    user.save()
                    return Response({"statusCode": 200, "message": "2FA setup successfully."})
                
                # access_token = token_generation(user)
                # user.status = "online"
                # user.save()
                response = Response({"statusCode": 200, "message": "2FA verified successfully."})
                # response.set_cookie("jwt", value=access_token, httponly=True, secure=True)
                return response
            else:
                return Response({"statusCode": 401, "message": "Incorrect 2FA code."})
        # except jwt.ExpiredSignatureError:
        #     return Response({"statusCode": 401, "error": "Expired token"})
        # except (jwt.InvalidTokenError, CustomUser.DoesNotExist):
        #     return Response({"statusCode": 401, "error": "Invalid token or player not found"})
        except Exception as e:
            return Response({"statusCode": 500, "error": str(e)})