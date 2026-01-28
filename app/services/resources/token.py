
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.security.crypt import PRIVATE_KEY

def issue_token(subject: str, scopes: list[str], audience: str, client_exp: int) -> tuple[str, float]:

    expire = datetime.utcnow() + timedelta(
        minutes=client_exp
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
        PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM,
    ), expire.timestamp()


def validate_refresh_token(token: str, db: Session) -> bool:
    # TODO: VALIDATE CLIENT_SECRET
    ...