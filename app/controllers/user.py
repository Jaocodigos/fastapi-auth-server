from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated


from app.db.session import get_db
from app.schemas.users import UserCreate, UserResponse
from app.services.user import create_user, get_all_users, erase_user

router = APIRouter(prefix="/api", tags=["Users"])


@router.get("/users")
def get_users(db: Session = Depends(get_db)):

    return get_all_users(db)

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(payload: Annotated[UserCreate, Query()], db: Session = Depends(get_db)):

    user = create_user(db, payload)

    return user

@router.delete("/users/{user_id}", status_code=200)
def delete_users(id: int, db: Session = Depends(get_db)):

    return erase_user(db=db, user_id=id)

