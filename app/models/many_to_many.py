from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class ScopesAndClaims(Base):
    __tablename__ = "scope_claims"

    scope_id: Mapped[int] = mapped_column(
        ForeignKey("scopes.id"), primary_key=True
    )
    claim_id: Mapped[int] = mapped_column(
        ForeignKey("claims.id"), primary_key=True
    )


class ClientScope(Base):
    __tablename__ = "client_scopes"

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), primary_key=True
    )
    scope_id: Mapped[int] = mapped_column(
        ForeignKey("scopes.id"), primary_key=True
    )


class ClientGrantType(Base):
    __tablename__ = "client_grant_types"

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"),
        primary_key=True
    )

    grant_type_id: Mapped[int] = mapped_column(
        ForeignKey("grant_types.id"),
        primary_key=True
    )