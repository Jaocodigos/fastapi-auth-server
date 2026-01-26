from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Claims(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(primary_key=True)
    claim_name: Mapped[str] = mapped_column(String(100))

    scopes: Mapped[list["Scopes"]] = relationship(secondary="scope_claims", backref="scope")