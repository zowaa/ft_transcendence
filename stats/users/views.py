from .models import CustomUser, Game, Tournement
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
import jwt
from rest_framework import exceptions
from .jwt import token_generation, get_user_id
from .decorators import token_required
from django.utils.decorators import method_decorator
from .serializers import  GameStateSerializer , TournementStateSerializer
from django.db.models import Q

class GameStatsView(APIView):
    @method_decorator(token_required)
    def get(self, request):
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)
            query = Q(player1user=user)
            games_data = []
            data_g= Game.objects.filter(query)
            for d in data_g:
                game_data = GameStateSerializer(d).data
                games_data.append(game_data)
                    
            response_data = {
                "success": True,
                "gamesdata": games_data 
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False,"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class TournementStatsView(APIView):
    @method_decorator(token_required)
    def get(self, request):
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)
            query = Q(player1user=user)
            games_data = []
            data_t = Tournement.objects.filter(query)
            for t in data_t:
                t_data = TournementStateSerializer(t).data
                games_data.append(t_data)
                    
            response_data = {
                "success": True,
                "gamesdata": games_data 
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False,"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    