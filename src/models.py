from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Clips(Base):
    __tablename__ = "clips"

    id: Mapped[int] = mapped_column(
        Integer, nullable=True, primary_key=True, autoincrement=True
    )
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
