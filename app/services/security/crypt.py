import secrets
import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from passlib.context import CryptContext
import bcrypt

from app.schemas.jwks import JWKResponse
from app.core.config import settings

# Hashing

crypt_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_content(data: str) -> str:
    return crypt_context.hash(data)


def verify_hash(data: str, hashed: str) -> bool:
    return crypt_context.verify(data, hashed)


def generate_secret(secret_length: int) -> str:
    return secrets.token_urlsafe(secret_length)


# JWKS


def int_to_base64url(value: int) -> str:
    byte_length = (value.bit_length() + 7) // 8
    value_bytes = value.to_bytes(byte_length, "big")
    return base64.urlsafe_b64encode(value_bytes).rstrip(b"=").decode("utf-8")


def load_public_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )

def load_private_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            backend=default_backend(),
            password=None
        )

PRIVATE_KEY = load_private_key(settings.PRIVATE_KEY_PATH)
PUBLIC_KEY = load_public_key(settings.PUBLIC_KEY_PATH)


def build_jwk(kid: str) -> JWKResponse:

    numbers = PUBLIC_KEY.public_numbers()

    jwk_response = JWKResponse(
        kty="RSA",
        kid=kid,
        use="sig",
        alg="RS256",
        n= int_to_base64url(numbers.n),
        e= int_to_base64url(numbers.e)
    )

    return jwk_response