import pyotp
from base64 import b32encode

def generate_secret(player_id: int) -> str:
    """Generates a base32-encoded secret for the player based on their ID."""
    player_id_encoded = str(player_id).encode("utf-8")
    return b32encode(player_id_encoded).decode('utf-8')

def generate_qrcode(player_id: int, issuer_name: str = "MyApp") -> str:
    """Generates a provisioning URI for a QR code."""
    secret = generate_secret(player_id)
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=f"player{player_id}", issuer_name=issuer_name)

def verify_code(player_id: int, code: str) -> bool:
    """Verifies the provided 2FA code against the player's TOTP secret."""
    secret = generate_secret(player_id)
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
