from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated


from app.db.session import get_db
from app.schemas.users import UserCreate, UserResponse
from app.services.resources.user import create_user, get_all_users, erase_user
from app.services.security.auth import authenticate

router = APIRouter(prefix="/api", tags=["Users"])


@router.get("/{client_name}/users")
def get_users(
    client_name: str,
    db: Session = Depends(get_db),
    _: None = Depends(authenticate)
):

    return get_all_users(db, client_name=client_name)

@router.post("/{client_name}/users", response_model=UserResponse, status_code=201)
def register_user(
    client_name: str,
    payload: Annotated[UserCreate, Body()],
    db: Session = Depends(get_db),
    _: None = Depends(authenticate)
):

    user = create_user(db, payload, client_name=client_name)

    return user

@router.delete("/{client_name}/users/{username}", status_code=200)
def delete_users(
    client_name: str,
    username: str,
    db: Session = Depends(get_db),
    _: None = Depends(authenticate)
):

    return erase_user(db=db, username=username, client_name=client_name)

