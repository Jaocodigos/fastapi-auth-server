from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class AuthorizationCode(Base):
    __tablename__ = "authorization_codes"

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(String(200), unique=True, index=True)

    client_id: Mapped[str] = mapped_column(
        String(100), ForeignKey("clients.client_id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    code_challenge: Mapped[str] = mapped_column(String(200))
    code_challenge_method: Mapped[str] = mapped_column(String(10))  # S256

    expires_at: Mapped[datetime]
    used: Mapped[bool] = mapped_column(Boolean, default=False)


    def use_code(self) -> None:
        self.used = True

    def is_expired(self) -> bool:
        return self.expires_at < datetime.utcnow()
