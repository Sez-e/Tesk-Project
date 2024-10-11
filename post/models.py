import uuid
from datetime import datetime

from sqlalchemy import String, UUID, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from core.base_model import Base  # noqa


class Post(Base):
    __tablename__ = 'posts' # noqa

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(), nullable=False)
