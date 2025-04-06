import typing as t
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import uuid


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[int] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(
        String(length=15), nullable=False, index=True
    )
    last_name: Mapped[str] = mapped_column(
        String(length=15), nullable=False, index=True
    )
    user_email: Mapped[str] = mapped_column(
        String(length=40), nullable=False, index=True
    )
    user_password: Mapped[str] = mapped_column(String(length=80), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(45), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    pages: Mapped[list["Page"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    html_content: Mapped[t.Text] = mapped_column(Text(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    edited_at: Mapped[datetime] = mapped_column(onupdate=datetime.now, nullable=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    category: Mapped["Category"] = relationship(back_populates="pages")

class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(length=50), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(String(length=255), nullable=False)

class PasswordReset(Base):
    __tablename__ = "password_resets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    used: Mapped[bool] = mapped_column(default=False)
    edited_at: Mapped[datetime] = mapped_column(onupdate=datetime.now, nullable=True)