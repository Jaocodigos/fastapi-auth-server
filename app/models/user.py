from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.models.default import Default


class User(Default, Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint("user_store_id", "username", name="uq_users_store_username"),
    )

    username: Mapped[str] = mapped_column(String(150), index=True)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_store_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("user_store.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user_store: Mapped["UserStore"] = relationship(back_populates="users")
