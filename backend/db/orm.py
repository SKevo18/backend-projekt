import typing as t
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=15), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(length=15), nullable=False, index=True)
    user_email: Mapped[str] = mapped_column(String(length=40), nullable=False, index=True)
    user_password: Mapped[str] = mapped_column(String(length=80), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(45), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    pages: Mapped[t.List["Page"]] = relationship(back_populates="category", cascade="all, delete-orphan")


class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(45), nullable=False)
    html_content: Mapped[t.Text] = mapped_column(Text(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    edited_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="pages")
