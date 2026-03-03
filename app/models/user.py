from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.models.default import Default


class User(Default, Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint("client_id", "username", name="uq_users_client_username"),
    )

    username: Mapped[str] = mapped_column(String(150), index=True)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    client_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("clients.client_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    client: Mapped["OAuthClient"] = relationship(back_populates="users")
