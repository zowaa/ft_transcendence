from .models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
import jwt
from rest_framework import exceptions
from .jwt import token_generation, get_user_id
from .decorators import token_required
from django.utils.decorators import method_decorator

class StatsView(APIView):
    @method_decorator(token_required)
    