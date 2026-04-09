from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.models import UserStore
from app.schemas.user_stores import UserStoreCreate, UserStoreResponse
from app.schemas.default import DeletedResponse
from app.handlers.errors.user_stores import UserStoreAlreadyExists, UserStoreNotFound
from app.services.resources.client import get_client

SPECIAL_CHARS = "!@#$%^&*(),.?\":{}|<>"


def get_user_store(db: Session, user_store_id=None, user_store_name=None, return_none=True) -> UserStoreResponse | None:
    us_filters = []

    if user_store_id is not None:
        us_filters.append(UserStore.id == user_store_id)

    if user_store_name is not None:
        us_filters.append(UserStore.name == user_store_name)

    us = db.execute(select(UserStore).where(*us_filters)
                      ).scalar_one_or_none()

    if not us:

        if return_none:
            return None

        raise UserStoreNotFound()

    return us


def create_user_store(db: Session, data: UserStoreCreate):

    for client_id in data.clients:

        get_client(db, client_id=client_id)


    exists = get_user_store(db, user_store_name=data.name)

    if exists:
        raise UserStoreAlreadyExists(data.name)

    user = UserStore(
        name=data.name,
        type=data.type,
        clients=data.clients
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def erase_user_store(db: Session, user_store_id: str):

    us = get_user_store(db, user_store_id, return_none=False)


    db.delete(us)
    db.commit()

    return DeletedResponse