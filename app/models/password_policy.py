from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.default import Default

class PasswordPolicy(Default, Base):

    __tablename__ = "password_policies"

    min_length: Mapped[int] = mapped_column(Integer, default=8)
    max_length: Mapped[int] = mapped_column(Integer, default=128)
    require_uppercase: Mapped[bool] = mapped_column(Boolean, default=False)
    require_lowercase: Mapped[bool] = mapped_column(Boolean, default=False)
    require_digits: Mapped[bool] = mapped_column(Boolean, default=False)
    require_special: Mapped[bool] = mapped_column(Boolean, default=False)

    client: Mapped["OAuthClient"] = relationship(back_populates="password_policy")

    client_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("clients.client_id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

