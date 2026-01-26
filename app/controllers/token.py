from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.session import get_db
from services.resources.token import create_access_token
from services.resources.oauth import validate_code
from app.schemas.token import TokenExchange

router = APIRouter(prefix="/api", tags=["Oauth 2.0"])


@router.post("/token")
def token(data: Annotated[TokenExchange, Body()], db: Session = Depends(get_db)):

    response = validate_code(db=db, data=data)

    # Issue token
    access_token, exp = create_access_token(
        subject=response.user_id,
        scopes=response.allowed_scopes,
        audience=response.redirect_uri,
        client_exp=response.client_exp
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": exp
    }
