from pydantic import BaseModel, AnyHttpUrl
from typing import List

class ClientCreate(BaseModel):
    redirect_uri: AnyHttpUrl
    allowed_scopes: List[str]

class ClientResponse(BaseModel):
    client_id: str
    redirect_uri: AnyHttpUrl
    allowed_scopes: str


