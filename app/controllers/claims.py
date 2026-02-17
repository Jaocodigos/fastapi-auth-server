from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated


from app.db.session import get_db
from app.schemas.claims import ClaimCreate
from app.services.resources.claims import get_claims, create_claim, delete_claim

router = APIRouter(prefix="/api", tags=["Claims"])


@router.get("/claims")
def list_claims(db: Session = Depends(get_db)):

    return get_claims(db)

@router.post("/claims", status_code=201)
def register_claims(payload: Annotated[ClaimCreate, Body()], db: Session = Depends(get_db)):

    return create_claim(db, payload)

@router.delete("/claims/{claim_id}", status_code=200)
def delete_claims(claim_id: str, db: Session = Depends(get_db)):

    return delete_claim(db=db, claim_id=claim_id)

