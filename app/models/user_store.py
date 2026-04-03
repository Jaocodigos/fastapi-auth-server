from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.models.default import Default


class UserStore(Default, Base):
    __tablename__ = "user_store"

    name: Mapped[str] = mapped_column(String(150), index=True)

    type: Mapped[str] = mapped_column(String(30), nullable=False)

    users: Mapped[list["User"]] = relationship(
        back_populates="user_store",
        cascade="all, delete-orphan"
    )

    clients: Mapped[list["OAuthClient"]] = relationship(
        back_populates="user_store"
    )
