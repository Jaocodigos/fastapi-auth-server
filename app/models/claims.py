from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.models.default import Default

class Claims(Default, Base):
    __tablename__ = "claims"

    claim_name: Mapped[str] = mapped_column(String(100))

    scopes: Mapped[list["Scopes"]] = relationship(secondary="scope_claims", backref="scope")