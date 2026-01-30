from pydantic import BaseModel
from typing import Optional

class TokenExchange(BaseModel):
    grant_type: str
    code: str
    client_id: str
    redirect_uri: str
    code_verifier: str
    refresh_token: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None

    model_config = {
        "exclude_none": True
    }