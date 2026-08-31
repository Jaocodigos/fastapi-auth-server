import base64
import hashlib
import hmac

from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.schemas.clients import BaseClient
from app.handlers.errors.default import UnauthorizedError, ForbiddenError
from app.services.resources.token import validate_access_token


security_scheme = HTTPBearer(auto_error=False)

def admin_authentication(token: HTTPAuthorizationCredentials | None = Depends(security_scheme)):

    if not token:
        raise UnauthorizedError("Unauthorized access.")

    token_hash = hashlib.sha256(token.credentials.encode("utf-8")).hexdigest()
    if not hmac.compare_digest(token_hash, settings.ADMIN_TOKEN):

        raise ForbiddenError("Forbidden access.")


def authenticate(token: HTTPAuthorizationCredentials | None = Depends(security_scheme)):

    if not token:
        raise UnauthorizedError("Unauthorized access.")

    if token.credentials.count(".") == 2:
        validate_access_token(token.credentials, ["read", "write"]) # SÓ POR ENQUANTO

    else:
        admin_authentication(token)


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

