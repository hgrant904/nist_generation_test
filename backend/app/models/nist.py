from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class NistFunction(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "nist_functions"

    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    categories: Mapped[list["NistCategory"]] = relationship(
        back_populates="function", cascade="all, delete-orphan"
    )


class NistCategory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "nist_categories"

    function_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("nist_functions.id", ondelete="CASCADE"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    function: Mapped[NistFunction] = relationship(back_populates="categories")
    subcategories: Mapped[list["NistSubcategory"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


class NistSubcategory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "nist_subcategories"

    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("nist_categories.id", ondelete="CASCADE"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[NistCategory] = relationship(back_populates="subcategories")
    questions: Mapped[list["NistQuestion"]] = relationship(
        back_populates="subcategory", cascade="all, delete-orphan"
    )


class NistQuestion(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "nist_questions"

    subcategory_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("nist_subcategories.id", ondelete="CASCADE"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    guidance: Mapped[str | None] = mapped_column(Text, default=None)
    answer_type: Mapped[str] = mapped_column(String(20), default="text", nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    subcategory: Mapped[NistSubcategory] = relationship(back_populates="questions")
