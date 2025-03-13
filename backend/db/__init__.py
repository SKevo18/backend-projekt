import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.orm import Base


class Database:
    def __init__(self):
        url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

        self.engine = create_engine(url)
        self.session = Session(self.engine)

    def init_db(self):
        Base.metadata.create_all(bind=self.engine)

    def close(self):
        self.session.close()


DB = Database()
DB.init_db()


def get_db():
    db_instance = Database()
    try:
        yield db_instance.session
    finally:
        db_instance.close()
