from .models import CustomUser, Friends
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import requests
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.views import APIView
import jwt
from rest_framework import exceptions
from .jwt import token_generation
from .decorators import token_required
from django.utils.decorators import method_decorator
from django.db.models import Q
import os
from django.core.exceptions import ValidationError
from .serializers import ProfileSerializer

###################################################
#                     friends                     #        
###################################################

class FriendsView(APIView):
    @method_decorator(token_required)
    def get(self, request):
        current_user_username = request.user_payload['user']['username']

        try:
            current_user = CustomUser.objects.get(username=current_user_username)
        except CustomUser.DoesNotExist:
            return Response({"status": 404, "message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        query = Q(sender=current_user) | Q(receiver=current_user) | Q(status='accepted')

        friends = Friends.objects.filter(query)
        friends_data = []
        for f in friends:
            friend = f.sender if f.sender != current_user else f.receiver
            friend_data = ProfileSerializer(friend).data
            friends_data.append(friend_data)

        return Response({"status": 200, "friendships": friends_data}, status=status.HTTP_200_OK)

    @method_decorator(token_required)
    def post(self, request):
        sender_username = request.user_payload['user']['username']
        receiver_username = request.data.get('username')

        if not receiver_username:
            return Response({"status": 400, "message": "Receiver username is required."}, status=status.HTTP_400_BAD_REQUEST)
        if sender_username == receiver_username:
            return Response({"status": 400, "message": "msg1"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = CustomUser.objects.get(username=sender_username)
            receiver = CustomUser.objects.get(username=receiver_username)

            existing_friend = Friends.objects.filter(
                Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
            ).first()

            if existing_friend:
                return Response({"status": 400, "message": "msg2"}, status=status.HTTP_400_BAD_REQUEST)
            
            Friends.objects.create(sender=sender, receiver=receiver, status='pending')
            return Response({"status": 200, "message": "msg3"}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"status": 404, "message": "msg4"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)