from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'display_name', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
