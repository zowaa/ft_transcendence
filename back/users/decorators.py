from functools import wraps
from django.http import JsonResponse
import jwt
from .jwt import token_decode  # Ensure you have a utility function to decode your JWT

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Extract the token from the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            # Expecting header value as "Bearer <Token>"
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
            else:
                # Header is malformed
                return JsonResponse({'detail': 'Authorization header must be Bearer token.'}, status=401)
        else:
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)
        
        try:
            # Decode the token
            payload = token_decode(token)
            
            # Add the payload or user to the request if needed
            request.user_payload = payload

            if (payload['user']['double_auth'] == True):
                return JsonResponse({'detail': 'Double authentification required.'}, status=401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'detail': 'Expired token.'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'detail': 'Invalid token.'}, status=401)
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=500)
        
        # Proceed with the view function if the token is valid
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
