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
            payload = token_decode(token)
            
            # Add the payload or user to the request if needed
            request.user_payload = payload

            if (payload['user']['double_auth'] == True):
                return JsonResponse({'detail': 'Double authentification required.'}, status=401)
        except jwt.ExpiredSignatureError:
            return Response({'detail': 'Expired token.'}, status=401)
        except jwt.InvalidTokenError:
            return Response({'detail': 'Invalid token.'}, status=401)
        except Exception as e: #500
            return Response({'detail': 'An error occured.'}, status=500)
        
        # Proceed with the view function if the token is valid
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view