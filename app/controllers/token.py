from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.session import get_db
from app.services.token import create_access_token
from app.services.oauth import validate_code
from app.schemas.token import TokenExchange
from app.handlers.errors.oauth import OAuthError

router = APIRouter(prefix="/api", tags=["Oauth 2.0"])


@router.post("/token")
def token(data: Annotated[TokenExchange, Body()], db: Session = Depends(get_db)):

    try:
        response = validate_code(db=db, data=data)
    except OAuthError as e:
        raise HTTPException(status_code=e.code, detail=str(e.error))


    # Issue token
    access_token = create_access_token(
        subject=response.user_id,
        scopes=response.allowed_scopes,
        audience=response.redirect_uri
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 900,
    }
