from fastapi import APIRouter

from app.services.security.crypt import build_jwk

router = APIRouter(prefix="/api", tags=["JWKS"])

KID = ["2026-01"]

@router.get("/.well-known/jwks.json")
def jwks():

    response = dict(
        keys=list(build_jwk(kid=k) for k in KID)
    )

    return response