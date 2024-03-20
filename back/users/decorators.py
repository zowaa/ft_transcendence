import jwt
from .jwt import token_decode
from django.http import JsonResponse
from functools import wraps

# jwt decorator
def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Get the token from the cookies
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)
        
        try:
            # Attempt to decode the token. 
            # Replace 'your_secret_key' with the key used to encode your JWTs
            payload = token_decode(token)
            
            # Optionally, add the payload or user to the request if needed
            request.user_payload = payload
        except jwt.ExpiredSignatureError:
            return JsonResponse({'detail': 'Expired token.'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'detail': 'Invalid token.'}, status=401)
        
        # Proceed with the view function if the token is valid
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view