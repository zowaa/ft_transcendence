from .models import CustomUser, Game, Tournement
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
import jwt
from rest_framework import exceptions
from .jwt import token_generation
from .decorators import token_required
from django.utils.decorators import method_decorator
from .serializers import RegisterTournementSerializer, FinishTournementSerializer, FinishGameSerializer, RegisterGameSerializer
import random
import uuid
from django.utils import timezone

class RegistreTournement(APIView):
    @method_decorator(token_required)
    def post(self, request):
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)
            serializer = RegisterTournementSerializer(data=request.data)
            if serializer.is_valid():
                tournement = serializer.save()
                tournement.tournementid = uuid.uuid1()
                tournement.player1user = user
                # user.display_name = tournement.player1
                user.save()
                tournement.save()
                game2 = [0, 1, 2, 3]
                game1 = random.sample(range(4), 2)
                game2 = [x for x in game2 if x not in game1]
                response_data = {
                    "success": True,
                    "message": "Tournement registered successfully",
                    "Tournementid": tournement.tournementid,
                    "game1": game1,
                    "game2": game2,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response({"success": False, "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"success": False,"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FinishTournement(APIView):
    @method_decorator(token_required)
    def post(self, request):
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)
            serializer = FinishTournementSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                tournement = Tournement.objects.get(tournementid=data['Tournementid'])
                if tournement.winner == '' and data['winner'] in [tournement.player1, tournement.player2, tournement.player3, tournement.player4] and tournement.player1user.id == user.id:
                    tournement.finished_at = timezone.now()
                    if tournement.player1 == data['winner']:
                        tournement.is_player1 = True
                        user.nb_wins = user.nb_wins + 1
                    else :
                        user.nb_losses = user.nb_losses + 1
                    user.save()
                    tournement.winner = data['winner']
                    tournement.save()
                    response_data = {
                        "success": True,
                        "message": "Tournement finished successfully",
                        "Tournementid": tournement.tournementid,
                    }
                    return Response(response_data, status=status.HTTP_201_CREATED)
            return Response({"success": False, "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"success": False,"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class RegistreGame(APIView):
    @method_decorator(token_required)
    def post(self, request):
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)
            serializer = RegisterGameSerializer(data=request.data)
            if serializer.is_valid():
                game = serializer.save()
                game.gameid = uuid.uuid1()
                game.player1user = user
                game.player1 = user.username
                game.save()
                response_data = {
                    "success": True,
                    "message": "Game registered successfully",
                    "gameid": game.gameid,
                    "player1": game.player1
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response({"success": False, "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"success": False,"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FinishGame(APIView):
    @method_decorator(token_required)
    def post(self, request):
        try:
            user_id = request.user_payload['user']['id']
            user = CustomUser.objects.get(id=user_id)
            serializer = FinishGameSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                game = Game.objects.get(gameid=data['gameid'])
                if game.winner == '' and data['winner'] in [game.player1, game.player2] and game.player1user.id == user.id:
                    game.finished_at = timezone.now()
                    if game.player1 == data['winner'] :
                        game.is_player1 = True
                        user.nb_wins = user.nb_wins + 1
                    else :
                        user.nb_losses = user.nb_losses + 1
                    user.save()
                    game.winner = data['winner']
                    game.save()
                    response_data = {
                        "success": True,
                        "message": "Game finished successfully",
                        "gameid": game.gameid,
                    }
                    return Response(response_data, status=status.HTTP_201_CREATED)
            return Response({"success": False, "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"success": False,"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

