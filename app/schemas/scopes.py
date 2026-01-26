from pydantic import BaseModel
from typing import List, Optional


class ScopeCreate(BaseModel):
    name: str
    claims: Optional[List[str]] = None

class ScopeResponse(BaseModel):
    id: int
    name: str
    claims: Optional[List[str]] = None

    class Config:
        from_attributes = True
