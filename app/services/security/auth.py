import base64
from fastapi import Header, HTTPException, status, Depends

from app.core.config import settings
from app.schemas.clients import BaseClient
from app.handlers.errors.default import UnauthorizedError, ForbiddenError


def admin_auth(admin_token: str = Header(...)):
    if not admin_token or admin_token != settings.ADMIN_TOKEN:
        raise ForbiddenError("Forbidden access.")


def token_authentication(admin_token: str = Header(...)):
    if not admin_token or admin_token != settings.ADMIN_TOKEN:
        raise UnauthorizedError("Unauthorized access.")


def token_or_admin_authentication(admin_token: str = Header(default=None), token: str = Header(default=None)):
    if admin_token:
        admin_auth(admin_token)
    elif token:
        token_authentication(token)
    else:
        raise UnauthorizedError("Unauthorized access.")


def decode_basic_auth(authorization = Header(None)) -> BaseClient:

    if not authorization:
        return BaseClient()

    if not authorization.startswith("Basic "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_client",
            headers={"WWW-Authenticate": "Basic"},
        )

    encoded = authorization[6:].strip()

    try:
        decoded_bytes = base64.b64decode(encoded, validate=True)
        decoded = decoded_bytes.decode("utf-8")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_client",
            headers={"WWW-Authenticate": "Basic"},
        )

    if ":" not in decoded:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_client",
            headers={"WWW-Authenticate": "Basic"},
        )

    client_id, client_secret = decoded.split(":", 1)

    if not client_id or not client_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_client",
            headers={"WWW-Authenticate": "Basic"},
        )

    return BaseClient(client_id=client_id, client_secret=client_secret)

