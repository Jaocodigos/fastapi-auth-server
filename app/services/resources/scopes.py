from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from models import Scopes
from schemas.scopes import ScopeResponse, ScopeCreate
from schemas.default import DeletedResponse
from handlers.errors.scopes import ScopeNotFound, ScopeAlreadyExists


def get_scopes(db: Session):

    scopes = db.scalars(select(Scopes).order_by(Scopes.id)).all()

    response = dict(
        users=list(
            ScopeResponse(id=x.id, name=x.scope_name, claims=x.claims)
            for x in scopes)
    )

    return response

def create_scope(db: Session, data: ScopeCreate):

    exists = db.execute(
        select(Scopes).where(Scopes.scope_name == data.name)
    ).scalar_one_or_none()

    if exists:
        raise ScopeAlreadyExists(scope=data.name)

    scope = Scopes(
        scope_name=data.name,
    )

    if data.claims:
        # TODO: Claim association logic
        ...

    db.add(scope)
    db.commit()
    db.refresh(scope)

    return ScopeResponse(id=scope.id, name=scope.scope_name, claims=scope.claims)


def delete_scope(db: Session, scope_id: int):

    scope = db.execute(
        select(Scopes).where(Scopes.id == scope_id)
    ).scalar_one_or_none()

    if not scope:
        ScopeNotFound()

    db.delete(scope)
    db.commit()

    return DeletedResponse()