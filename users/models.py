from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid

class CustomUser(AbstractBaseUser):
    id = models.CharField(max_length=200, default=uuid.uuid4,unique=True,primary_key=True)
    email = None
    username = models.CharField(null=False, max_length=100, unique=True)
    display_name = models.CharField(null=True, max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='images/', default="images/default.png")
    friends = models.ManyToManyField("CustomUser", blank=True)
    nb_wins = models.IntegerField(default=0)
    nb_losses = models.IntegerField(default=0)
    nb_plays = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default="offline")
    is_active = models.BooleanField(default = True)
    is_42_user = models.BooleanField(default=False)
    otp_enabled = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    otp_base32 = models.CharField(max_length=255, null=True)
    otp_auth_url = models.CharField(max_length=255, null=True)
    
    # REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_requests")
    status = models.CharField(max_length=100, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} - {self.status}"

class Games(models.Model):
    id = models.AutoField(primary_key=True)
    first_player = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="game_results_as_first_player")
    second_player = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="game_results_as_second_player")
    first_player_score = models.IntegerField()
    second_player_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_player.username} vs {self.second_player.username} - {self.first_player_score} - {self.second_player_score}"