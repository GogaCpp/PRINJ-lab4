import uuid
from sqlalchemy import TIMESTAMP, UUID, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from ..database import Base


class Chat(Base):
    __tablename__ = 'chat'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    is_group: Mapped[bool] = mapped_column(nullable=False)
    creator_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
    )