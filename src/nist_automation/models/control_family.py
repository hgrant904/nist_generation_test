"""Control Family model - represents NIST CSF categories."""

from datetime import datetime
from typing import List
from sqlalchemy import String, Text, DateTime, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base


class ControlFamily(Base):
    __tablename__ = "control_families"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    framework: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    controls: Mapped[List["Control"]] = relationship(
        "Control", back_populates="family", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ControlFamily(code='{self.code}', name='{self.name}')>"
