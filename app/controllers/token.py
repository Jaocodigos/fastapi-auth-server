from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.session import get_db
from services.resources.token import issue_token, validate_refresh_token
from services.resources.oauth import validate_code, validate_client
from app.schemas.token import TokenExchange

router = APIRouter(prefix="/api", tags=["Oauth 2.0"])

@router.post("/token")
def token(data: Annotated[TokenExchange, Body()],
          db: Session = Depends(get_db),
          client = Depends(validate_client)):

    if data.grant_type == "refresh_token":
        user = validate_refresh_token(data.refresh_token, db)
    else:
        user = validate_code(data, db)

    # Issue token
    access_token, exp = issue_token(
        subject=user,
        scopes=client.allowed_scopes,
        audience=client.redirect_uri,
        client_exp=client.token_exp
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": exp
    }
