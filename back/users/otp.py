import pyotp
from base64 import b32encode

def generate_secret(user_id: int) -> str:
    """Generates a base32-encoded secret for the user based on their ID."""
    user_id_encoded = str(user_id).encode("utf-8")
    return b32encode(user_id_encoded).decode('utf-8')

def generate_qrcode(user_id: int, issuer_name: str = "transcending") -> str:
    """Generates a provisioning URI for a QR code."""
    secret = generate_secret(user_id)
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=f"user{user_id}", issuer_name=issuer_name)

def verify_code(user_id: int, code: str) -> bool:
    """Verifies the provided 2FA code against the user's TOTP secret."""
    secret = generate_secret(user_id)
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
