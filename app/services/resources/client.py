from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.models import OAuthClient, Scopes, GrantType
from app.schemas.clients import ClientCreate, ClientResponse
from app.handlers.errors import ClientNotFound, ScopeNotFound, ClientError
from app.services.security.crypt import generate_secret


def get_all_clients(db: Session):

    clients = db.execute(select(OAuthClient)).scalars().all()
    if not clients:
        return {"clients": []}

    payload = dict(
        clients=list(
            ClientResponse(
                client_id=x.client_id,
                client_secret=None,
                redirect_uri=x.redirect_uri,
                scopes=x.allowed_scopes,
                response_type=x.response_type,
                client_type=x.client_type,
                token_exp=x.token_exp
            ).model_dump(exclude_none=True)
            for x in clients)
    )

    return payload

def create_client(db: Session, data: ClientCreate):

    client_id = generate_secret(24)

    client = OAuthClient(
        client_id=client_id,
        redirect_uri=str(data.redirect_uri),
        response_type=data.response_type,
        client_type=data.client_type,
        token_exp=data.token_exp,
    )

    for x in data.grant_types:

        grant = db.execute(select(GrantType).filter_by(name=x)).scalar_one_or_none()
        if grant is None:
            raise ClientError("Invalid grant type")

        client.grant_types.append(grant)

    for x in data.scopes:

        scope = db.execute(select(Scopes).filter_by(scope_name=x)).scalar_one_or_none()
        if scope is None:
            raise ScopeNotFound()

        client.scopes.append(scope)


    # Public clients can have a secret, even they don't use?
    secret = client.generate_secret()

    db.add(client)
    db.commit()

    return ClientResponse(
        client_id=client_id,
        client_secret=secret,
        redirect_uri=client.redirect_uri,
        scopes=client.allowed_scopes,
        token_exp=client.token_exp,
        client_type=client.client_type,
        response_type=client.response_type
    )

def erase_client(db: Session, client_id: str):

    client = db.execute(select(OAuthClient).filter_by(client_id=client_id)).scalar_one_or_none()
    if not client:
        raise ClientNotFound()

    db.delete(client)
    db.commit()


