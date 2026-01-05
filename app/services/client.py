import secrets

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.models.client import OAuthClient
from app.schemas.clients import ClientCreate, ClientResponse
from app.handlers.errors.client import ClientNotFound


def get_all_clients(db: Session):

    clients = db.execute(select(OAuthClient)).all()
    if not clients:
        return {"clients": []}

    payload = dict(
        clients=list(
            ClientResponse(client_id=x.client_id, redirect_uri=x.redirect_uri, allowed_scopes=x.allowed_scopes)
            for x in clients)
    )

    return payload

def create_client(db: Session, data: ClientCreate):

    client_id = secrets.token_urlsafe(24)

    client = OAuthClient(
        client_id=client_id,
        redirect_uri=str(data.redirect_uri),
        allowed_scopes=" ".join(data.allowed_scopes),
        is_public=True,
    )

    db.add(client)
    db.commit()

    return ClientResponse(
        client_id=client_id,
        redirect_uri=client.redirect_uri,
        allowed_scopes=client.allowed_scopes
    )

def erase_client(db: Session, client_id: str):

    client = db.execute(select(OAuthClient).filter_by(client_id=client_id)).first()
    if not client:
        raise ClientNotFound()

    db.delete(client)
    db.commit()


