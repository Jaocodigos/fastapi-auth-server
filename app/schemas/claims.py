from pydantic import BaseModel


class ClaimCreate(BaseModel):
    name: str

class ClaimResponse(BaseModel):
    id: int
    name: str
