from sqlalchemy.sql import select

from app.models import GrantType, Scopes
from app.db.session import SessionLocal


# This will be removed when we add a migrations logic

SUPPORTED_GRANT_TYPES = [
    "authorization_code",
    "refresh_token"
]

SUPPORTED_SCOPES = [
    "openid",
    "profile",
    "email",
    "password",
    "read",
    "write"
]

def seed_database() -> None:
    db = SessionLocal()
    try:

        # Grant types

        existing = db.scalars(select(GrantType.name)).all()

        existing = set(existing)

        for g in SUPPORTED_GRANT_TYPES:

            if g not in existing:
                db.add(GrantType(name=g))

        db.commit()

        # Scopes

        existing = db.scalars(select(Scopes.scope_name)).all()

        existing = set(existing)

        for s in SUPPORTED_SCOPES:

            if s not in existing:
                db.add(Scopes(scope_name=s))

        db.commit()

    finally:
        db.close()