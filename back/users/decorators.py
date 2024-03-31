from functools import wraps
from django.http import JsonResponse
import jwt
from .jwt import token_decode

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header:
                parts = auth_header.split()
                if len(parts) == 2 and parts[0].lower() == "bearer":
                    token = parts[1]
                else:
                    return JsonResponse({'detail': 'Authorization header must be Bearer token.'}, status=HTTP_401_UNAUTHORIZED)
        
        if not token:
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=HTTP_401_UNAUTHORIZED)

        try:
            payload = token_decode(token)
            request.user_payload = payload

            if payload.get('user', {}).get('double_auth') == True:
                return JsonResponse({'detail': 'Double authentication required.'}, status=HTTP_401_UNAUTHORIZED)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'detail': 'Expired token.'}, status=HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return JsonResponse({'detail': 'Invalid token.'}, status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse({'detail': 'An error occurred.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        return view_func(request, *args, **kwargs)

    return _wrapped_view
