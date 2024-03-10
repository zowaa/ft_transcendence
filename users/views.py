from .models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegisterUserSerializer, LoginUserSerializer, ProfileSerializer
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
import pyotp
from rest_framework import generics

def GenerateToken(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            'redirect_uri': 'https://upgraded-dollop-q65pjww6654c67pp-8000.app.github.dev/auth42_callback',
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

            response_data = self.process_user_data(user_data)
            return Response(response_data, status=status.HTTP_200_OK)
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
        user = CustomUser.objects.filter(username=username, is_42_user=True).first()
        if user:
            user.status = "online"
            user.save()
            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response_data = {
                "success": True,
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            # Set the JWT as a cookie in the response
            response.set_cookie(
                'jwt',
                access_token,
                httponly=True,
                secure=False,  # Should be True in production
                samesite='Lax',  # Helps with CSRF protection
            )
            return response
        else:
            serializer = UserSerializer(data={'username': username, 'display_name': display_name, 'is_42_user' : True})
            if serializer.is_valid():
                # If the data is valid, create the user
                user = serializer.save()
                user.status = "online"
                user.save()
                # Generate JWT tokens for the user
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response_data = {
                    "success": True,
                }
                response = Response(response_data, status=status.HTTP_200_OK)
                # Set the JWT as a cookie in the response
                response.set_cookie(
                    'jwt',
                    access_token,
                    httponly=True,
                    secure=False,  # Should be True in production
                    samesite='Lax',  # Helps with CSRF protection
                )
                return response

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # Prepare the response data
            response_data = {
                'message': 'Login successful.',
                'refresh': str(refresh),
                'access': access_token,  # It's already a string, no need to convert again
            }
            
            # Create a Response object
            response = Response(response_data, status=status.HTTP_200_OK)
            
            # Set the JWT as a cookie in the response
            response.set_cookie(
                'jwt',
                access_token,
                httponly=True,
                secure=False,  # Should be True in production
                samesite='Lax',  # Helps with CSRF protection
            )
            
            return response
        
        # If the serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)

class GetProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        jwt = request.COOKIES['jwt']
        payload = jwt.decode(jwt, 'kmoutaou', None, verify=True)
        print(payload)
        serializer = ProfileSerializer(user, many=False)
        return Response(serializer.data)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###################################################
#                     friends                     #        
###################################################

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
