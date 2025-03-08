import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.orm import Base


class Database:
    def __init__(self):
        url = os.getenv("DATABASE_URL")
        assert url is not None, "nastav env pre `DATABASE_URL`"

        self.engine = create_engine(url)
        self.session = Session(self.engine)

    def init_db(self):
        Base.metadata.create_all(bind=self.engine)

    def close(self):
        self.session.close()


DB = Database()
DB.init_db()
