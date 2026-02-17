from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from models import Claims
from schemas.claims import ClaimCreate, ClaimResponse

from schemas.default import DeletedResponse
from handlers.errors.claims import ClaimNotFound, ClaimAlreadyExists


def get_claims(db: Session):

    claims = db.scalars(select(Claims).order_by(Claims.id)).all()

    response = dict(
        claims=list(
            ClaimResponse(id=x.id, name=x.claim_name)
            for x in claims)
    )

    return response

def create_claim(db: Session, data: ClaimCreate):

    exists = db.execute(
        select(Claims).where(Claims.claim_name == data.name)
    ).scalar_one_or_none()

    if exists:
        raise ClaimAlreadyExists(claim=data.name)

    claim = Claims(
        claim_name=data.name
    )

    db.add(claim)
    db.commit()
    db.refresh(claim)

    return claim


def delete_claim(db: Session, claim_id: str):

    claim = db.execute(
        select(Claims).where(Claims.id == claim_id)
    ).scalar_one_or_none()

    if not claim:
        ClaimNotFound()

    db.delete(claim)
    db.commit()

    return DeletedResponse()