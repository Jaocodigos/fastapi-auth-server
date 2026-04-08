from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated


from app.db.session import get_db
from app.schemas.user_stores import UserStoreCreate, UserStoreResponse

from app.services.security.auth import authenticate

router = APIRouter(prefix="/api", tags=["User Store"])


@router.get("/{client_name}/us")
def get_user_stores(
    client_name: str,
    db: Session = Depends(get_db),
    _: None = Depends(authenticate)
):

    ...

@router.post("/{client_name}/us", response_model=UserStoreResponse, status_code=201)
def register_user_store(
    client_name: str,
    payload: Annotated[UserStoreCreate, Body()],
    db: Session = Depends(get_db),
    _: None = Depends(authenticate)
):

    ...

@router.delete("/{client_name}/us/{user_store_id}", status_code=200)
def delete_user_store(
    client_name: str,
    user_store_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(authenticate)
):

    ...

