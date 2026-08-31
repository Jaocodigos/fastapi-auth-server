from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.models.default import Default


class Scopes(Default, Base):
    __tablename__ = "scopes"

    scope_name: Mapped[str] = mapped_column(String(100))

    claims: Mapped[list["Claims"]] = relationship(
        secondary="scope_claims",
        backref="scope"
    )

    clients: Mapped[list["OAuthClient"]] = relationship(
        secondary="client_scopes",
        back_populates="scopes"
    )