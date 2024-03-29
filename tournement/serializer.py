from rest_framework import serializers
from .models import Tournement

class RegisterTournementSerializer(serializers.ModelSerializer):
    player1 = serializers.CharField(max_length=150)
    player2 = serializers.CharField(max_length=150)
    player3 = serializers.CharField(max_length=150)
    player4 = serializers.CharField(max_length=150)
    
    class Meta:
        model = Tournement
        fields = ['player1', 'player2', 'player3', 'player4']

class FinishTournementSerializer(serializers.Serializer):
    winner = serializers.CharField(max_length=150)
    Tournementid = serializers.CharField(max_length=64)
