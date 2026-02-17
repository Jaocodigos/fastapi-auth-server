from typing import List

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.services.security.crypt import generate_secret, hash_content
from app.models.default import Default

class OAuthClient(Default, Base):
    __tablename__ = "clients"

    client_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    client_secret: Mapped[str] = mapped_column(String(100), unique=True, nullable=True) # May depend on client_type

    redirect_uri: Mapped[str] = mapped_column(String(500))

    client_type: Mapped[str] = mapped_column(String(20)) # Public or Confidential

    response_type: Mapped[str] = mapped_column(String(100))

    # All in minutes
    token_exp: Mapped[int] = mapped_column(Integer)
    refresh_token_exp: Mapped[int] = mapped_column(Integer, default=30)
    code_exp: Mapped[int] = mapped_column(Integer)

    scopes: Mapped[list["Scopes"]] = relationship(
        secondary="client_scopes",
        back_populates="clients"
    )

    grant_types: Mapped[list["GrantType"]] = relationship(
        secondary="client_grant_types",
        lazy="selectin"
    )

    @property
    def allowed_scopes(self) -> List[str]:
        return [x.scope_name for x in self.scopes]

    def generate_secret(self) -> str:

        client_secret = generate_secret(32)
        hash_secret = hash_content(client_secret)
        self.client_secret = hash_secret

        return hash_secret

    def validate_secret(self, secret: str) -> bool:
        return secret == self.client_secret

    def is_confidential(self) -> bool:
        return self.client_type == "confidential"

    def validate_grant_type(self, grant_type: str) -> bool:
        return any(x.name == grant_type for x in self.grant_types)

    def validate_response_type(self, response_type: str) -> bool:
        return response_type == self.response_type

    def validate_redirect_uri(self, redirect_uri: str) -> bool:
        return redirect_uri == self.redirect_uri

