from pydantic import BaseModel, AnyHttpUrl, model_validator, Field
from typing import List, Self, Optional


class PasswordPolicyCreate(BaseModel):
    min_length: int = Field(default=8, ge=6, le=128)
    max_length: int = Field(default=128, ge=8, le=256)
    require_uppercase: bool = False
    require_lowercase: bool = False
    require_digits: bool = False
    require_special: bool = False

    @model_validator(mode="after")
    def validate_lengths(self) -> Self:
        if self.min_length >= self.max_length:
            raise ValueError("min_length must be less than max_length")
        return self


class ClientCreate(BaseModel):
    name: str
    redirect_uri: AnyHttpUrl
    grant_types: list[str]
    client_type: str
    scopes: List[str]
    response_type: str
    token_exp: int
    refresh_token_exp: int
    code_exp: int
    password_policy: Optional[PasswordPolicyCreate] = None


    @model_validator(mode="after")
    def validate_scope(self) -> Self:

        if self.client_type not in ["public", "confidential"]:
            raise ValueError("invalid client_type")

        if self.response_type not in ["code", "id_token", "token"]:
            raise ValueError("invalid response_type")

        if self.token_exp <= 0:
            raise ValueError("invalid token_exp")

        if self.code_exp <= 0:
            raise ValueError("invalid code_exp")

        if self.refresh_token_exp <= 0 or self.refresh_token_exp <= self.token_exp:
            raise ValueError("invalid refresh_token_exp")

        return self

class ClientResponse(BaseModel):
    name: str
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    scopes: List[str]
    response_type: str
    token_exp: int
    refresh_token_exp: int
    code_exp: int
    client_type: str


class BaseClient(BaseModel):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
