from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class Test(Base):
    __tablename__ = "test"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str] = mapped_column(nullable=False)
