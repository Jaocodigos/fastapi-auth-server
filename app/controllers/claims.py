from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated


from app.db.session import get_db
from app.schemas.claims import ClaimCreate, ClaimResponse
from services.resources.claims import get_claims, create_claim, delete_claim

router = APIRouter(prefix="/api", tags=["Claims"])


@router.get("/claims")
def list_claims(db: Session = Depends(get_db)):

    return get_claims(db)

@router.post("/claims", response_model=ClaimResponse, status_code=201)
def register_claims(payload: Annotated[ClaimCreate, Body()], db: Session = Depends(get_db)):

    claim = create_claim(db, payload)

    return claim

@router.delete("/claims/{claims_id}", status_code=200)
def delete_claims(claim_id: int, db: Session = Depends(get_db)):

    return delete_claim(db=db, claim_id=claim_id)

