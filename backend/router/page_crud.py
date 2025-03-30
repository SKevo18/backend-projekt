from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db
from db.orm import Page

PAGE_CRUD_ROUTER = APIRouter(prefix="/page")


class PageBase(BaseModel):
    category_id: int
    title: str
    html_content: str


class PageCreate(PageBase):
    pass

class PageUpdate(BaseModel):
    category_id: Optional[int] = None
    title: Optional[str] = None
    html_content: Optional[str] = None

class PageOut(PageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


@PAGE_CRUD_ROUTER.post("/", response_model=PageOut)
def create_page(page: PageCreate, db: Session = Depends(get_db)):
    db_page = Page(**page.model_dump())
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page


@PAGE_CRUD_ROUTER.get("/{page_id}", response_model=PageOut)
def read_page(page_id: int, db: Session = Depends(get_db)):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    return db_page


@PAGE_CRUD_ROUTER.put("/{page_id}", response_model=PageOut)
def update_page(page_id: int, page: PageUpdate, db: Session = Depends(get_db)):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Page not found")

    if page.title is not None:
        db_page.title = page.title
    if page.html_content is not None:
        db_page.html_content = page.html_content
    if page.category_id is not None:
        db_page.category_id = page.category_id

    db.commit()
    db.refresh(db_page)
    return db_page


@PAGE_CRUD_ROUTER.delete("/{page_id}", status_code=204)
def delete_page(page_id: int, db: Session = Depends(get_db)):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    db.delete(db_page)
    db.commit()
    return None


@PAGE_CRUD_ROUTER.get("/", response_model=list[PageOut])
def read_all_pages(db: Session = Depends(get_db)):
    return db.query(Page).all()
