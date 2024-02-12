from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def index(request):
    return render(request, 'index.html')

# def logout(request):
#     logout(request)
#     return redirect('index')
