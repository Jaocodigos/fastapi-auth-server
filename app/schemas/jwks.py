from pydantic import BaseModel

class JWKResponse(BaseModel):
    kty: str
    kid: str
    use: str
    alg: str
    n: str
    e: str
