
from sqlalchemy.sql import select
from datetime import datetime, timedelta, UTC
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.security.crypt import PRIVATE_KEY, PUBLIC_KEY, generate_secret, hash_content
from app.schemas.token import TokenResponse
from app.models.refresh_token import RefreshToken
from app.handlers.errors.default import OauthError, UnauthorizedError

def issue_token(subject: str, scopes: list[str], client_exp: int, refresh_token=None) -> TokenResponse:

    issued_at = datetime.now(UTC)
    expire = issued_at + timedelta(
        minutes=client_exp
    )

    payload = {
        "sub": subject,
        "iss": settings.ISSUER,
        "aud": settings.ISSUER,
        "scopes": scopes,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


    return TokenResponse(
        access_token=token,
        expires_in=int(expire.timestamp()),
        token_type="bearer",
        refresh_token=refresh_token
    )

def validate_access_token(token: str, required_scopes: list) -> bool :

    try:
        is_valid = jwt.decode(token, PUBLIC_KEY, algorithms=settings.JWT_ALGORITHM)

    except Exception as e:
        raise UnauthorizedError("Invalid access token.")

    if is_valid["exp"] < datetime.now(UTC):
        raise UnauthorizedError("Invalid access token.")

    if is_valid["iss"] != settings.ISSUER:
        raise UnauthorizedError("Invalid issuer.")

    # In this case, the authorization server is a resource server too.
    if is_valid["aud"] != settings.ISSUER:
        raise UnauthorizedError("Invalid audience.")

    if not all(x in is_valid["scopes"] for x in required_scopes):
        raise UnauthorizedError("Invalid scopes for this operation.")

    return True


def issue_refresh_token(db: Session, user_id: str, client_id: str, refresh_token_exp: int) -> tuple[str, str]:

    issued_at = datetime.now(UTC)
    expire = issued_at + timedelta(
        minutes=refresh_token_exp
    )

    token = generate_secret(64)

    refresh_token = RefreshToken(
        token_hash=hash_content(token),
        user_id=user_id,
        client_id=client_id,
        issued_at=issued_at,
        expires_at=expire
    )

    db.add(refresh_token)
    db.commit()

    token = f"{refresh_token.id}.{token}"

    return token, refresh_token.id

def validate_and_issue_refresh_token(db: Session, refresh_token: str, refresh_token_exp: int) -> tuple[str, str]:

    refresh_token_id = refresh_token.split(".")[0]

    refresh_token = db.execute(select(RefreshToken).filter_by(id=refresh_token_id)).scalar_one_or_none()

    if not refresh_token:
        raise OauthError("invalid_grant")

    if refresh_token.is_expired() or refresh_token.is_revoked():
        raise OauthError("invalid_grant")


    token, token_id = issue_refresh_token(
        db=db,
        user_id=refresh_token.user_id,
        client_id=refresh_token.client_id,
        refresh_token_exp=refresh_token_exp
    )

    refresh_token.rotate(token_id)

    db.commit()

    return token, refresh_token.user_id
