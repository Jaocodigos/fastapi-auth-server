from pydantic import BaseModel, model_validator
from typing_extensions import Self
from typing import Literal, List


class AuthorizeParams(BaseModel):
    response_type: Literal["code"]
    client_id: str
    redirect_uri: str
    scope: str
    state: str | None = None
    code_challenge: str
    code_challenge_method: Literal["S256"]

    @model_validator(mode="after")
    def validate_scope(self) -> Self:

        if not self.scope.strip():

            raise ValueError("invalid_scope")

        return self

class CodeResponse(BaseModel):
    user_id: str
    redirect_uri: str
    allowed_scopes: List[str]
    client_exp: int

    class Config:
        from_attributes = True