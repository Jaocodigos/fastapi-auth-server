from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.session import get_db
from app.schemas.clients import ClientCreate
from app.schemas.default import DeletedResponse
from app.core.security import admin_auth
from app.services.client import get_all_clients, create_client, erase_client
from app.handlers.errors.client import ClientNotFound

router = APIRouter(prefix="/api", tags=["Clients"])


@router.get("/clients")
def get_clients(
    db: Session = Depends(get_db),
    _: None = Depends(admin_auth),
):

    clients = get_all_clients(db=db)

    return clients

@router.post("/clients")
def register_client(
    data: Annotated[ClientCreate, Query()],
    db: Session = Depends(get_db),
    _: None = Depends(admin_auth),
):

    new_client = create_client(db=db, data=data)

    return new_client

@router.delete("/clients/{client_id}")
def delete_client(
        client_id: str,
        db: Session = Depends(get_db),
        _: None = Depends(admin_auth),
):

    try:
        erase_client(db=db, client_id=client_id)
    except ClientNotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.error)

    return DeletedResponse