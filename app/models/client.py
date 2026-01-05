from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class OAuthClient(Base):
    __tablename__ = "oauth_clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    redirect_uri: Mapped[str] = mapped_column(String(500))

    is_public: Mapped[bool] = mapped_column(Boolean, default=True)

    allowed_scopes: Mapped[str] = mapped_column(String(500))
