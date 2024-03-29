from django.db import models


class Tournement(models.Model):
    id = models.AutoField(primary_key=True)
    tournementid = models.CharField(max_length=64)
    player1 = models.CharField(max_length=150, default='PlayerX')
    player2 = models.CharField(max_length=150, default='PlayerX')
    player3 = models.CharField(max_length=150, default='PlayerX')
    player4 = models.CharField(max_length=150, default='PlayerX')
    winner = models.CharField(max_length=150, default='PlayerX')

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tournement players : {self.player1} - {self.player2} - {self.player3} - {self.player4} , and the winner : {self.winner}"
        