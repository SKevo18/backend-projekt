from datetime import datetime

from db import get_db
from db.orm import Page
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

PAGE_CRUD_ROUTER = APIRouter(prefix="/page")


class PageBase(BaseModel):
    html_content: str


class PageCreate(PageBase):
    pass


class PageUpdate(PageBase):
    pass


class PageOut(PageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


@PAGE_CRUD_ROUTER.post("/", response_model=PageOut)
def create_page(page: PageCreate, db: Session = Depends(get_db)):
    db_page = Page(html_content=page.html_content)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page
