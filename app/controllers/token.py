from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.session import get_db
from services.resources.token import issue_token, validate_and_issue_refresh_token, issue_refresh_token
from services.resources.oauth import validate_code_and_return_user, validate_client
from app.schemas.token import TokenExchange, TokenResponse

router = APIRouter(prefix="/api", tags=["Oauth 2.0"])

@router.post("/token", response_model=TokenResponse, response_model_exclude_none=True)
def token_endpoint(data: Annotated[TokenExchange, Body()],
          db: Session = Depends(get_db),
          client = Depends(validate_client)) -> TokenResponse:

    refresh_token = None

    if data.grant_type == "refresh_token":

        refresh_token, user = validate_and_issue_refresh_token(
            db=db,
            refresh_token=data.refresh_token,
            refresh_token_exp=client.refresh_token_exp
        )

    else:

        user = validate_code_and_return_user(data, db)

        if client.validate_grant_type("refresh_token"):

            refresh_token, _ = issue_refresh_token(
                db=db,
                user_id=user,
                client_id=client.client_id,
                refresh_token_exp=client.refresh_token_exp
            )

    # Issue token
    token = issue_token(
        subject=str(user),
        scopes=client.allowed_scopes,
        audience=client.redirect_uri,
        client_exp=client.token_exp,
        refresh_token=refresh_token
    )

    return token