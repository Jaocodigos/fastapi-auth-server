import hashlib
import base64

from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, Body
from fastapi.security import HTTPBasic

from app.models.authorization_code import AuthorizationCode
from app.models.client import OAuthClient
from app.schemas.authorize import AuthorizeParams
from app.schemas.token import TokenExchange
from app.schemas.clients import BaseClient
from app.handlers.errors.default import OauthError
from app.services.security.crypt import generate_secret
from app.services.security.auth import decode_basic_auth
from app.db.session import get_db

security = HTTPBasic()

def verify_pkce(code_verifier: str, code_challenge: str) -> bool:

    digest = hashlib.sha256(code_verifier.encode()).digest()
    calculated_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()

    return calculated_challenge == code_challenge


def generate_code(user_id: str, data: AuthorizeParams, db: Session) -> str:

    # 1. client
    client = db.execute(select(OAuthClient).filter_by(client_id=data.client_id)).scalar_one_or_none()

    if not client:
        raise OauthError("invalid_client")

    # 2. redirect_uri
    if data.redirect_uri != client.redirect_uri:
        raise OauthError("invalid_redirect_uri")

    # 3. scopes
    requested_scopes = set(data.scope.split()) if data.scope else set()
    allowed_scopes = set(client.allowed_scopes)

    if not requested_scopes.issubset(allowed_scopes):
        raise OauthError("invalid_scope")

    # TODO: ALSO VALIDATE -> response type, client type

    # 4. Generate code
    code = generate_secret(32)

    auth_code = AuthorizationCode(
        code=code,
        client_id=data.client_id,
        user_id=user_id,
        code_challenge=data.code_challenge,
        code_challenge_method=data.code_challenge_method,
        expires_at=datetime.utcnow() + timedelta(minutes=client.code_exp),
        used=False,
    )

    db.add(auth_code)
    db.commit()

    return code


# Must support basic and post authentications
def validate_client(data: Annotated[TokenExchange, Body],
                    credentials: BaseClient = Depends(decode_basic_auth),
                    db: Session = Depends(get_db)) -> OAuthClient:

    # confidential client
    if credentials.client_id:
        client = db.execute(select(OAuthClient).filter_by(client_id=credentials.client_id)).scalar_one_or_none()
    else:
        client = db.execute(select(OAuthClient).filter_by(client_id=data.client_id)).scalar_one_or_none()

    if not client:
        raise OauthError("invalid_client", status_code=401)

    if client.is_confidential() and not (credentials.client_secret and client.validate_secret(credentials.client_secret)):
        raise OauthError("invalid_client", status_code=401)

    if not client.validate_redirect_uri(data.redirect_uri):
        raise OauthError("invalid_redirect_uri")

    if not client.validate_grant_type(data.grant_type):
        raise OauthError("unsupported_grant_type")

    return client


def validate_code_and_return_user(data: TokenExchange, db: Session) -> int:

    auth_code = db.execute(select(AuthorizationCode).filter_by(code=data.code, client_id=data.client_id)).scalar_one_or_none()

    if not auth_code:
        raise OauthError("invalid_code")

    if auth_code.used:
        raise OauthError("invalid_code")

    if auth_code.is_expired():
        raise OauthError("expired_code")

    if not verify_pkce(data.code_verifier, auth_code.code_challenge):
        raise OauthError("invalid_grant")

    auth_code.use_code()
    db.commit()

    return auth_code.user_id
