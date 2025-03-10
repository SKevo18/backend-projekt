from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, index=True)
    email: Mapped[str] = mapped_column(nullable=False, index=True)
    password: Mapped[str] = mapped_column(nullable=False)

    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)
