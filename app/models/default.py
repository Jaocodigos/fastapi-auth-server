from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from uuid_utils import uuid7


class Default:

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid7()))

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


