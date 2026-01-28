from pydantic import BaseModel, AnyHttpUrl, model_validator
from typing import List, Self, Optional

class ClientCreate(BaseModel):
    redirect_uri: AnyHttpUrl
    grant_types: list[str]
    client_type: str
    scopes: List[str]
    response_type: str
    token_exp: int

    @model_validator(mode="after")
    def validate_scope(self) -> Self:

        if self.client_type not in ["public", "confidential"]:
            raise ValueError("invalid client_type")

        if self.response_type not in ["code", "id_token", "token"]:
            raise ValueError("invalid response_type")

        if self.token_exp < 0:
            raise ValueError("invalid token_exp")


        return self

class ClientResponse(BaseModel):
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    scopes: List[str]
    response_type: str
    token_exp: int
    client_type: str


class BaseClient(BaseModel):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

