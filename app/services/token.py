
from datetime import datetime, timedelta
from jose import jwt

from app.core.config import settings

def create_access_token(subject: str, scopes: list[str], audience: str) -> str:

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "iss": settings.ISSUER,
        "aud": audience,
        "scopes": scopes,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

