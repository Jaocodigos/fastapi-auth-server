from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.models.user import User
from app.schemas.users import UserCreate, UserResponse
from app.schemas.default import DeletedResponse
from app.core.security import hash_password
from app.handlers.errors.user import UserNotFound, UserAlreadyExists


def get_all_users(db: Session):

    users = db.scalars(select(User).order_by(User.id)).all()

    response = dict(
        users=list(
            UserResponse(id=x.id, username=x.username)
            for x in users)
    )

    return response


def create_user(db: Session, data: UserCreate):

    exists = db.execute(
        select(User).where(User.username == data.username)
    ).scalar_one_or_none()

    if exists:
        raise UserAlreadyExists()

    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def erase_user(db: Session, user_id: int):

    user = db.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()

    if not user:
        UserNotFound()

    db.delete(user)
    db.commit()

    return DeletedResponse()