from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from sqlalchemy import UniqueConstraint

from app.db.session import Base
from app.models.default import Default


class GrantType(Default, Base):
    __tablename__ = "grant_types"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
        default=True
    )

    clients: Mapped[list["OAuthClient"]] = relationship(
        secondary="client_grant_types",
        back_populates="grant_types"
    )

    __table_args__ = (
        UniqueConstraint("name"),
    )
