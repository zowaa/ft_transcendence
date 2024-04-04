import pyotp
from base64 import b32encode
from django.conf import settings
from .models import CustomUser

def get_or_create_user_secret(user_id: int) -> str:
    user = CustomUser.objects.get(id=user_id)
    if not user.totp_secret:
        user.totp_secret = pyotp.random_base32()
        user.save(update_fields=['totp_secret'])
    return user.totp_secret

def generate_qrcode(user_id: int, issuer_name: str = "transcending") -> str:
    secret = get_or_create_user_secret(user_id)
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=f"user{user_id}@{issuer_name}", issuer_name=issuer_name)

def verify_code(user_id: int, code: str) -> bool:
    secret = get_or_create_user_secret(user_id)
    totp = pyotp.TOTP(secret)
    return totp.verify(code)