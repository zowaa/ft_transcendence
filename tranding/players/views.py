from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserLoginForm, UserCreationForm
from django.http import JsonResponse
from django.utils import timezone
from .helpers import token_generation, token_decode
from django.contrib.auth.hashers import make_password
from .models import User
from functools import wraps
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.refresh_from_db()
            user.username = form.cleaned_data.get('username')
            user.display_name = form.cleaned_data.get('username')
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            user = authenticate(username=user.username, password=user.password)
            # login(request)
            return JsonResponse({
                "success": True,
                #"message": "Account created successfully!",
                #"redirect": True,
                #"redirect_url": "login",
            })
        else:
            return JsonResponse({
                "success": False,
                #"message": "Invalid form",
                "errors": form.errors,
            })
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')  # Redirect to a home page or dashboard
#     else:
#         form = UserLoginForm()
#     return render(request, 'login.html', {'form': form})

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            username=username, password=password)
        
        refresh = RefeshToken.for_user(user)

        return JsonResponse(
            {
               'refresh':str(refresh),
               'access':str(refresh.access_token) 
            }
        )

def login(request):
    message = "User not logged in"
    if request.user.is_authenticated:
        return JsonResponse({
            "success": True,
            "message": "User already logged in",
            # "redirect": True,
            # "redirect_url": "profile",
            "context": {},
        })

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login(request, user)
            return JsonResponse({
                "success": True,
                "message": "Login successful",
                # "redirect": True,
                # "redirect_url": "index",
                "context": {},
                "logged_in": True,
            })
        else:
            message = "Username or password is incorrect"
            return JsonResponse({
                "success": False,
                "message": message,
                # "redirect": False,
                # "redirect_url": "",
                "context": {},
                "logged_in": request.user.is_authenticated,
            })

def logout(request):
	user = User.objects.get(username=getUser(request))
	user.status = "offline"
	user.save()
	return JsonResponse({
		"success": True,
		"message": "Logged out successfully",
		# "redirect": True,
		# "redirect_url": "login",
		"context": {},
		"logged_in": request.user.is_authenticated,
	})

def index(request):
    return render(request, 'index.html')

def getUser(request):
    # Get the JWT from the request headers
    jwt = request.headers.get("Authorization")

    if jwt:
        # Decode the JWT to extract the payload
        payload = token_decode(jwt)

        # Extract user information from the payload
        userData = json.loads(payload['user'])[0]['fields']

        # Check if user data exists and if the JWT is not expired
        if userData and payload['exp'] > datetime.timestamp(datetime.utcnow()):
            try:
                # Try to retrieve the user from the database using the username from the JWT
                user_ex = User.objects.get(username=userData['username'])
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

def jwt_user(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated via JWT
        user = getUser(request)
        
        if user is not None:
            # User is authenticated, proceed to the view function
            return view_func(request, *args, **kwargs)
        else:
            # User is not authenticated, return a JSON response indicating invalid JWT
            return JsonResponse({
                "success": False,
                # "message": "Invalid JWT",
                # "redirect": True,
                # "redirect_url": "login",
                "context": {},
            })
    
    return wrapped_view


def authentication(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # If authenticated, return JSON response indicating user is already logged in
        return JsonResponse({
            "success": True,
            "message": "User already logged in",
            # "redirect": True,
            # "redirect_url": reverse("index"),  # Redirect to index page
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
    
def userProfile(request):
    if request.method == "GET":
        user = getUser(request)
        if user:
            userData = {
                "display_name": user.display_name,
                "avatar_base64": user.avatar_base64,
            }
            return JsonResponse({
                "success": True,
                "message": "",
                "redirect": False,
                "redirect_url": "",
                "context": {"user": userData},
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "User not found",
                "redirect": False,
                "redirect_url": "",
                "context": {},
            })
    elif request.method == "POST":
        user = getUser(request)
        if user:
            display_name = request.POST.get("display_name")
            avatar_base64 = request.POST.get("avatar_base64")
            if display_name:
                user.display_name = display_name
            if avatar_base64:
                user.avatar_base64 = avatar_base64
            user.save()
            return JsonResponse({
                "success": True,
                "message": "Profile updated successfully",
                "redirect": False,
                "redirect_url": "",
                "context": {},
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "User not found",
                "redirect": False,
                "redirect_url": "",
                "context": {},
            })