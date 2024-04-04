from rest_framework import serializers
from .models import Game, Tournement

class RegisterTournementSerializer(serializers.ModelSerializer):
    player1 = serializers.CharField(max_length=150)
    player2 = serializers.CharField(max_length=150)
    player3 = serializers.CharField(max_length=150)
    player4 = serializers.CharField(max_length=150)
    
    class Meta:
        model = Tournement
        fields = ['player1', 'player2', 'player3', 'player4']
    def validate(self, data):
        player1 = data.get('player1')
        player2 = data.get('player2')
        player3 = data.get('player3')
        player4 = data.get('player4')

        if player1 == '' or player2 == '' or player3 == '' or player4 == '':
            raise serializers.ValidationError("No name should be empty !")
        if len({player1, player2, player3, player4}) == 4:
            return {"player1": player1,
                    "player2": player2,
                    "player3": player3,
                    "player4": player4}
        else :
            raise serializers.ValidationError("No matches in names please") 

class FinishTournementSerializer(serializers.Serializer):
    winner = serializers.CharField(max_length=150)
    Tournementid = serializers.CharField(max_length=64)


class RegisterGameSerializer(serializers.ModelSerializer):
    player2 = serializers.CharField(max_length=150)
    class Meta:
        model = Game
        fields = ['player2']


class FinishGameSerializer(serializers.Serializer):
    winner = serializers.CharField(max_length=150)
    gameid = serializers.CharField(max_length=64)

