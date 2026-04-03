from fastapi import APIRouter, Request, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from typing import Annotated

from app.core.limiter import limiter

from app.db.session import get_db
from app.schemas.users import UserSelfRegister
from app.services.resources.user import self_register, verify_user_email

router = APIRouter(prefix="", tags=["Register"])


@router.post("/{client_name}/register", status_code=201)
@limiter.limit("3/minute")
async def register(
        request: Request,
        client_name: str,
        data: Annotated[UserSelfRegister, Body()],
        db: Session = Depends(get_db)
):

    await self_register(db, data, client_name)
    return {"message": "If the account was created, a verification email will be sent."}

@router.get("/{client_name}/verify")
@limiter.limit("5/minute")
async def verify_email(
        request: Request,
        client_name: str,
        token: str,
        db: Session = Depends(get_db)
):

    verify_user_email(db, token, client_name)
    return {"message": "Email verified. You can now log in."}