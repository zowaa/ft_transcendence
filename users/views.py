from django.shortcuts import render
from .models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegisterUserSerializer, LoginUserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
import requests
from rest_framework.views import APIView
from django.shortcuts import redirect
import logging
import pyotp
from rest_framework import generics

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# class OAuth42APIView(APIView):
def OAuth42APIView(request):
    github_authorization_url = 'https://api.intra.42.fr/oauth/authorize'
    client_id = 'u-s4t2ud-2ceb8913100edae2ae13c981a77f7f85af527523e4a15f078054e9223d696488'
    redirect_uri = 'https://upgraded-dollop-q65pjww6654c67pp-8000.app.github.dev/auth42_callback&response_type=code' #to change after with localhost
    # scope = 'login:displayname'  # adjust scope as per your requirements
    return redirect(f'{github_authorization_url}?client_id={client_id}&redirect_uri={redirect_uri}')

# class OAuth42CallbackAPIView(APIView):
@api_view(['GET'])
def getOAuth42CallbackAPIView(request):
    code = request.GET.get('code')
    client_id = 'u-s4t2ud-2ceb8913100edae2ae13c981a77f7f85af527523e4a15f078054e9223d696488'
    client_secret = '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'
    redirect_uri = 'https://upgraded-dollop-q65pjww6654c67pp-8000.app.github.dev/auth42_callback'
    token_url = 'https://api.intra.42.fr/oauth/token'
    response = requests.post(token_url, data={
        "grant_type": "authorization_code",
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
    })
    # logging.debug(response.json())
    # access_token = response.json()['access_token']
    # if access_token:
    #     user_data = fetch_42_user(access_token)
    #     # print(user_data);
    #     if user_data:
    #         response_data = process_user_data(user_data)
    #         # Log the user in or perform any other actions as needed
    #         return Response(response_data)
    # return Response("Failed to fetch user data", status=status.HTTP_400_BAD_REQUEST)

    try:
        access_token = response.json().get('access_token')
        if access_token:
            user_data = fetch_42_user(access_token)
            if user_data:
                response_data = process_user_data(user_data)
                # Log the user in or perform any other actions as needed
                return Response(response_data)
    except KeyError:
        # Handle missing 'access_token' key in the JSON response
        return Response("Failed to find access token in response", status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Handle other exceptions
        return Response(f"An error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("Failed to fetch user data", status=status.HTTP_400_BAD_REQUEST)

def fetch_42_user(access_token):
    user_url = 'https://api.intra.42.fr/v2/me'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(user_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def process_user_data(user_data):
    username = user_data['login']
    display_name = user_data['displayname']
    if username:
        # Authenticate user with Django's authentication system
        user = authenticate(request, username=username)
        if user is not None:
            # If user exists, log in the user
            user_login(request, user)
            user.status = "online"
            user.save()
            data = {
                "success": True,
                "message": "Login completed",
                "logged_in": request.user.is_authenticated,
            }
            return data
        else:
            # If user does not exist, create a new user
            user = CustomUser.objects.create_user(username=username, display_name=display_name, from_42=True)
            user_login(request, user)
            user.status = "online"
            user.save()
            data = {
                "success": True,
                "message": "New user created and logged in",
                "logged_in": request.user.is_authenticated,
            }
            return data
    else:
        # If username is not found in response, return error
        data = {
            "success": False,
            "message": "Username not found in response",
        }
        return data


@api_view(['GET'])
def register_user_oauth2(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # If authenticated, return JSON response indicating user is already logged in
        data = {    
            "success": True,
            "message": "User already logged in",
            "logged_in": request.user.is_authenticated,
        }
        return Response(data)

    # If the request method is GET, continue with authentication process
    if request.method == "GET":
        # Get the authorization code from the query parameters
        code = request.GET.get("code")

        if code:
            # If authorization code is present, exchange it for an access token
            data = {
                "grant_type": "authorization_code",
                "client_id": os.environ.get(settings.SCHOOL_OAUTH2_CLIENT_ID),
                "client_secret": os.environ.get(settings.SCHOOL_OAUTH2_CLIENT_SECRET),
                "code": code,
                "redirect_uri": request.build_absolute_uri(reverse("register_user_oauth2")),  # Build absolute URI for callback
            }

            # Make a POST request to exchange code for access token
            auth_response = requests.post("https://api.intra.42.fr/oauth/token", data=data)
            auth_response_data = auth_response.json()

            if "access_token" in auth_response_data:
                # If access token received, fetch user information
                access_token = auth_response_data["access_token"]
                user_response = requests.get("https://api.intra.42.fr/v2/me", headers={"Authorization": f"Bearer {access_token}"})
                user_response_data = user_response.json()

                # Extract username and display name from user response
                username = user_response_data.get("login")
                display_name = user_response_data.get("displayname")

                if username:
                    # Authenticate user with Django's authentication system
                    user = authenticate(request, username=username)

                    if user is not None:
                        # If user exists, log in the user
                        user_login(request, user)
                        user.status = "online"
                        user.save()
                        data = {
                            "success": True,
                            "message": "Login completed",
                            "logged_in": request.user.is_authenticated,
                        }
                        return Response(data)
                    else:
                        # If user does not exist, create a new user
                        user = User.objects.create_user(username=username, display_name=display_name, from_42=True)
                        user_login(request, user)
                        user.status = "online"
                        user.save()
                        data = {
                            "success": True,
                            "message": "New user created and logged in",
                            "logged_in": request.user.is_authenticated,
                        }
                        return Response(data)
                else:
                    # If username is not found in response, return error
                    data = {
                        "success": False,
                        "message": "Username not found in response",
                    }
                    return Response(data)
            else:
                # If access token is not received, return error
                data = {
                    "success": False,
                    "message": "Access token not received",
                }
                return Response(data)
        else:
            # If authorization code is not present, return error
            data = {
                "success": False,
                "message": "Authorization code not found",
            }
            return Response(data)
    else:
        # If request method is not GET, return error
        data = {
            "success": False,
            "message": "Invalid method",
        }
        return Response(data)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            user.access_token = str(refresh.access_token)
            return Response({
                'message': 'Login successful.',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
def send_request(request, username):
    try:
        receiver = CustomUser.objects.get(username=username)
        request = Request(sender=request.user, receiver=receiver)
        request.save()
        return JsonResponse({"message": "Request sent successfully"})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

@permission_classes([IsAuthenticated])
def accept_request(request, requestID):
    try:
        request = Request.objects.get(id=requestID)
        # request.status = "accepted"
        # request.save()
        request.sender.friends.add(request.receiver)
        request.receiver.friends.add(request.sender)
        request.delete()
        return JsonResponse({"message": "Request accepted successfully"})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Request not found"}, status=404)

@permission_classes([IsAuthenticated])
def reject_request(request, requestID):
    try:
        request = Request.objects.get(id=requestID)
        request.delete()
        return JsonResponse({"message": "Request rejected successfully"})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Request not found"}, status=404)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_friends(request):
    user = request.user
    friends = user.friends.all()
    serializer = ProfileSerializer(friends, many=True)
    return Response(serializer.data)

###################################################
#                        2fa                      #        
###################################################

class disable2fa(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        data = request.data
        user_id = data.get('user_id', None)

        user = CustomUser.objects.filter(id=user_id).first()
        if user == None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"}, status=status.HTTP_404_NOT_FOUND)

        user.otp_enabled = False
        user.otp_verified = False
        user.otp_base32 = None
        user.otp_auth_url = None
        user.save()
        serializer = self.serializer_class(user)

        return Response({'otp_disabled': True, 'user': serializer.data})

class generateOtp(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        data = request.data
        user_id = data.get('user_id', None)
        email = data.get('email', None)

        user = CustomUser.objects.filter(id=user_id).first()
        if user == None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"}, status=status.HTTP_404_NOT_FOUND)

        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=email.lower(), issuer_name="codevoweb.com")

        user.otp_auth_url = otp_auth_url
        user.otp_base32 = otp_base32
        user.save()

        return Response({'base32': otp_base32, "otpauth_url": otp_auth_url})

class verifyOtp(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        message = "Token is invalid or user doesn't exist"
        data = request.data
        user_id = data.get('user_id', None)
        otp_token = data.get('token', None)
        user = CustomUser.objects.filter(id=user_id).first()
        if user == None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"}, status=status.HTTP_404_NOT_FOUND)

        totp = pyotp.TOTP(user.otp_base32)
        if not totp.verify(otp_token):
            return Response({"status": "fail", "message": message}, status=status.HTTP_400_BAD_REQUEST)
        user.otp_enabled = True
        user.otp_verified = True
        user.save()
        serializer = self.serializer_class(user)

        return Response({'otp_verified': True, "user": serializer.data})

class validateOtp(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        message = "Token is invalid or user doesn't exist"
        data = request.data
        user_id = data.get('user_id', None)
        otp_token = data.get('token', None)
        user = CustomUser.objects.filter(id=user_id).first()
        if user == None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.otp_verified:
            return Response({"status": "fail", "message": "OTP must be verified first"}, status=status.HTTP_404_NOT_FOUND)

        totp = pyotp.TOTP(user.otp_base32)
        if not totp.verify(otp_token, valid_window=1):
            return Response({"status": "fail", "message": message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'otp_valid': True})
