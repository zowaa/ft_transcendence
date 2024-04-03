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

from .models import Tournement
from .serializer import RegisterTournementSerializer, FinishTournementSerializer
import random
import uuid
from django.utils import timezone

class RegistreTournement(APIView):
    @method_decorator(token_required)
    def post(self, request):
        try:
            serializer = RegisterTournementSerializer(data=request.data)
            if serializer.is_valid():
                tournement = serializer.save()
                tournement.tournementid = uuid.uuid1()
                tournement.save()
                # get the tournement id and send it back
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
            serializer = FinishTournementSerializer(data=request.data)
            if serializer.is_valid():
                # process the data here before saving
                data = serializer.data
                tournement = Tournement.objects.get(tournementid=data['Tournementid'])
                if tournement.winner == '' and data['winner'] in [tournement.player1, tournement.player2, tournement.player3, tournement.player4]:
                    tournement.finished_at = timezone.now()
                    tournement.save()
                    response_data = {
                        "success": True,
                        "message": "Tournement finished successfully",
                        "Tournementid": tournement.tournementid,
                    }
                    return Response(response_data, status=status.HTTP_201_CREATED)
                # a specific response here in needed
            return Response({"success": False, "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"success": False,"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.shortcuts import render
def index(request):
    return render(request, "game.html")