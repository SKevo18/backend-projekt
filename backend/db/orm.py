import typing as t
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import LONGTEXT


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[int] = mapped_column(nullable=False)
    title_before_name: Mapped[str] = mapped_column(String(length=10), nullable=True)
    title_after_name: Mapped[str] = mapped_column(String(length=10), nullable=True)
    first_name: Mapped[str] = mapped_column(
        String(length=15), nullable=False, index=True
    )
    middle_name: Mapped[str] = mapped_column(String(length=15), nullable=True)
    last_name: Mapped[str] = mapped_column(
        String(length=15), nullable=False, index=True
    )
    user_email: Mapped[str] = mapped_column(
        String(length=40), nullable=False, index=True
    )
    user_password: Mapped[str] = mapped_column(String(length=80), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)
    edited_at: Mapped[datetime] = mapped_column(onupdate=datetime.now, nullable=True)


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
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    html_content: Mapped[t.Text] = mapped_column(LONGTEXT(), nullable=False)
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
    
class UserPagePermission(Base):
    __tablename__ = "user_page_permissions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

class UserCategoryPermission(Base):
    __tablename__ = "user_category_permissions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)