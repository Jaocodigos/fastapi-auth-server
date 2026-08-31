from datetime import datetime, UTC
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
from app.models.default import Default


class Token(Default, Base):
    __tablename__ = "access_tokens"

    token_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    issued_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    expires_at: Mapped[datetime] = mapped_column(nullable=False)

