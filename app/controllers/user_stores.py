from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated


from app.db.session import get_db
from app.schemas.user_stores import UserStoreCreate, UserStoreResponse

from app.services.security.auth import authenticate
from app.services.resources.user_stores import get_user_store, create_user_store, erase_user_store

router = APIRouter(prefix="/api", tags=["User Store"])


@router.get("/us/{user_store_id}", response_model=UserStoreResponse, status_code=200)
def get_user_stores(
    user_store_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(authenticate)
):

    return get_user_store(db, user_store_id, return_none=False)


@router.post("/us", response_model=UserStoreResponse, status_code=201)
def register_user_store(
    payload: Annotated[UserStoreCreate, Body()],
    db: Session = Depends(get_db),
    _: None = Depends(authenticate)
):

    return create_user_store(db, payload)

@router.delete("/us/{user_store_id}", status_code=200)
def delete_user_store(
    user_store_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(authenticate)
):

    return erase_user_store(db, user_store_id)

