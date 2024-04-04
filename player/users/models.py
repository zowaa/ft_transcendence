from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid

class CustomUser(AbstractBaseUser):
    STATUS_CHOICES = (
        ('offline', 'Offline'),
        ('online', 'Online'),
        ('playing', 'Playing'),
    )
    id = models.CharField(max_length=200, default=uuid.uuid4,unique=True,primary_key=True)
    email = None
    username = models.CharField(null=False, max_length=150, unique=True)
    display_name = models.CharField(null=True, max_length=150, unique=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    avatar = models.URLField(max_length=255, null=False, blank=False, default="Frontend/Assets/default.png")
    nb_wins = models.IntegerField(default=0)
    nb_losses = models.IntegerField(default=0)
    nb_plays = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="offline")
    is_active = models.BooleanField(default = True)
    is_42_user = models.BooleanField(default=False)
    double_auth = models.BooleanField(default=False)
    totp_secret = models.CharField(max_length=100, null=True, blank=True)

    # REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Friends(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.user.username} to {self.receiver.user.username} - {self.get_status_display()}"

class Tournement(models.Model):
    id = models.AutoField(primary_key=True)
    tournementid = models.CharField(max_length=64)
    is_player1 = models.BooleanField(default = False)
    # player1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='main_player')
    player1 = models.CharField(max_length=150, default='')
    player2 = models.CharField(max_length=150, default='')
    player3 = models.CharField(max_length=150, default='')
    player4 = models.CharField(max_length=150, default='')
    winner = models.CharField(max_length=150, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tournement id : {self.tournementid}    , players : {self.player1} - {self.player2} - {self.player3} - {self.player4} , and the winner : {self.winner}"

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    gameid = models.CharField(max_length=64)
    is_player1 = models.BooleanField(default = False)
    # player1user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='main_player')
    player1 = models.CharField(max_length=150, default='')
    player2 =  models.CharField(max_length=150, default='')
    winner = models.CharField(max_length=150, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game id : {self.gameid}    , players : {self.player1} - {self.player2}   , and the winner : {self.winner}"