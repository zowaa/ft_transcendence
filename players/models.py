from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
import uuid
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
import requests
import os

class UserManager(BaseUserManager):
    def create_user(self, email, display_name, username, password=None):
        user = self.model(
            email = self.normalize_email(email),
            display_name = display_name,
            username = username,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, display_name, username, password=None):
        user = self.create_user(
            email=email,
            password=password,
            display_name = display_name,
            username = username,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.CharField(max_length=200, default=uuid.uuid4,unique=True,primary_key=True)
    email = models.EmailField(null=False, max_length=100,unique=True)
    username = models.CharField(null=False, max_length=100, unique=True)
    display_name = models.CharField(null=True, max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    avatar_base64 = models.TextField(default="", blank=True)
    friends = models.CharField(max_length=1000, default="")
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    plays = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default="offline")
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_42_user = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["display_name"]
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True