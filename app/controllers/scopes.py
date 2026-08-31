from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated


from app.db.session import get_db
from app.schemas.scopes import ScopeCreate, ScopeResponse
from app.services.resources.scopes import get_scopes,create_scope, delete_scope

router = APIRouter(prefix="/api", tags=["Scopes"])


@router.get("/scopes")
def list_scopes(db: Session = Depends(get_db)):

    return get_scopes(db)

@router.post("/scopes", response_model=ScopeResponse, status_code=201)
def register_scopes(payload: Annotated[ScopeCreate, Body()], db: Session = Depends(get_db)):

    scope = create_scope(db, payload)

    return scope

@router.delete("/scopes/{scope_id}", status_code=200)
def delete_scopes(scope_id: str, db: Session = Depends(get_db)):

    return delete_scope(db=db, scope_id=scope_id)

