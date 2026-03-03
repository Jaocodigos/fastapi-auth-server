from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.models.user import User
from app.schemas.users import UserCreate, UserResponse
from app.schemas.default import DeletedResponse
from app.services.security.crypt import hash_content
from app.handlers.errors.user import UserNotFound, UserAlreadyExists
from app.services.resources.client import get_client
from app.handlers.errors.client import ClientNotFound


def get_all_users(db: Session, client_name: str):

    client = get_client(db, client_name)

    if not client:
        raise ClientNotFound()

    users = db.scalars(
        select(User).where(User.client_id == client.id).order_by(User.id)
    ).all()

    response = dict(
        users=list(
            UserResponse(id=x.id, username=x.username)
            for x in users)
    )

    return response

def get_user(db: Session, client_id: str, username=None, user_id=None, return_none=True) -> User | None:
    
    user_filters = [
        User.client_id == client_id,
    ]

    if username:
        user_filters.append(User.username == username)

    if user_id:
        user_filters.append(User.id == user_id)
    
    user = db.execute(select(User).where(*user_filters)
                      ).scalar_one_or_none()

    if not user:

        if return_none:
            return None

        raise UserNotFound()

    return user


def create_user(db: Session, data: UserCreate, client_name: str):

    client = get_client(db, client_name)

    exists = get_user(db, client.client_id, username=data.username)

    if exists:
        raise UserAlreadyExists(data.username)

    user = User(
        username=data.username,
        password_hash=hash_content(data.password),
        client_id=client.client_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def erase_user(db: Session, username: str, client_name: str):

    client = get_client(db, client_name)

    if not client:
        raise ClientNotFound()

    user = get_user(db, client.client_id, username=username)

    if not user:
        raise UserNotFound()

    db.delete(user)
    db.commit()

    return DeletedResponse
