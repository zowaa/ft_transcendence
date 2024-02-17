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

from datetime import datetime
from .utils import decode_jwt  # Import a function to decode JWTs
from .models import PongueUser  # Import the PongueUser model

def getUser(request):
    # Get the JWT from the request headers
    jwt = request.headers.get("Authorization")

    if jwt:
        # Decode the JWT to extract the payload
        payload = decode_jwt(jwt)

        # Extract user information from the payload
        user_data = json.loads(payload['user'])[0]['fields']

        # Check if user data exists and if the JWT is not expired
        if user_data and payload['exp'] > datetime.timestamp(datetime.utcnow()):
            try:
                # Try to retrieve the user from the database using the username from the JWT
                user_ex = User.objects.get(username=user_data['username'])
                # If user exists in the database, return it
                return user_ex
            except User.DoesNotExist:
                # If user does not exist, return None
                return None
        else:
            # If JWT is expired, return None
            return None
    else:
        # If JWT is not provided, return None
        return None

def authentication(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # If authenticated, return JSON response indicating user is already logged in
        return JsonResponse({
            "success": True,
            "message": "User already logged in",
            "redirect": True,
            "redirect_url": reverse("index"),  # Redirect to index page
            "logged_in": request.user.is_authenticated,
        })

    # If the request method is GET, continue with authentication process
    if request.method == "GET":
        # Get the authorization code from the query parameters
        code = request.GET.get("code")

        if code:
            # If authorization code is present, exchange it for an access token
            data = {
                "grant_type": "authorization_code",
                "client_id": os.environ.get("TRAN_CLIENT_ID"),
                "client_secret": os.environ.get("TRAN_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": request.build_absolute_uri(reverse("authentication")),  # Build absolute URI for callback
            }

            # Make a POST request to exchange code for access token
            auth_response = requests.post("https://api.intra.42.fr/oauth/token", data=data)
            auth_response_data = auth_response.json()

            if "access_token" in auth_response_data:
                # If access token received, fetch user information
                access_token = auth_response_data["access_token"]
                user_response = requests.get("https://api.intra.42.fr/v2/me", headers={"Authorization": f"Bearer {access_token}"})
                user_response_data = user_response.json()

                # Extract username and display name from user response
                username = user_response_data.get("login")
                display_name = user_response_data.get("displayname")

                if username:
                    # Authenticate user with Django's authentication system
                    user = authenticate(request, username=username)

                    if user is not None:
                        # If user exists, log in the user
                        login(request, user)
                        user.status = "online"
                        user.save()
                        # Redirect to index page after successful login
                        return JsonResponse({
                            "success": True,
                            "message": "Login completed",
                            "redirect": True,
                            "redirect_url": reverse("index"),  # Redirect to index page
                            "logged_in": request.user.is_authenticated,
                        })
                    else:
                        # If user does not exist, create a new user
                        user = User.objects.create_user(username=username, display_name=display_name, from_42=True)
                        login(request, user)
                        user.status = "online"
                        user.save()
                        # Redirect to index page after successful login
                        return JsonResponse({
                            "success": True,
                            "message": "New user created and logged in",
                            "redirect": True,
                            "redirect_url": reverse("index"),  # Redirect to index page
                            "logged_in": request.user.is_authenticated,
                        })
                else:
                    # If username is not found in response, return error
                    return JsonResponse({
                        "success": False,
                        "message": "Username not found in response",
                        "redirect": True,
                        "redirect_url": reverse("login"),  # Redirect to login page
                    })
            else:
                # If access token is not received, return error
                return JsonResponse({
                    "success": False,
                    "message": "Access token not received",
                    "redirect": True,
                    "redirect_url": reverse("login"),  # Redirect to login page
                })
        else:
            # If authorization code is not present, return error
            return JsonResponse({
                "success": False,
                "message": "Invalid authorization code",
                "redirect": True,
                "redirect_url": reverse("login"),  # Redirect to login page
            })
    else:
        # If request method is not GET, return error
        return JsonResponse({
            "success": False,
            "message": "Invalid method",
            "redirect": True,
            "redirect_url": reverse("login"),  # Redirect to login page
        })