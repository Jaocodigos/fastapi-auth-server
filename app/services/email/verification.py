from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app.core.config import settings

def create_verification_token(email: str) -> str:

    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt="email-verification")

def decode_verification_token(token: str) -> str | None:

    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        return serializer.loads(token, salt="email-verification", max_age=86400)
    except (BadSignature, SignatureExpired):
        return None