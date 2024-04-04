from rest_framework import serializers
from .models import Tournement, Game

class GameStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['is_player1', 'finished_at']


class TournementStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournement
        fields = ['is_player1', 'finished_at']