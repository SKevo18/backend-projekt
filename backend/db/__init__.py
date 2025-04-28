import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()


class Database:
    def __init__(self):
        try:
            url = os.environ["DATABASE_URL"]
        except KeyError:
            raise RuntimeError("DATABASE_URL not found in .env file!")
        self.engine = create_engine(url)

    def get_session(self):
        return Session(self.engine)


DB = Database()


def get_db():
    db_instance = Database()
    session = db_instance.get_session()

    try:
        yield session
    finally:
        session.close()
