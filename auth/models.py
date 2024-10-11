import uuid
from datetime import datetime

from sqlalchemy import String, UUID, DateTime, ARRAY
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.base_model import Base  # noqa


class User(Base):
    __tablename__ = 'users'  # noqa

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(), nullable=False)
