from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db
from db.orm import Page, Category

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
    slug: str
    created_at: datetime

    class Config:
        from_attributes = True


@PAGE_CRUD_ROUTER.post("/", response_model=PageOut)
def create_page(page: PageCreate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == page.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Neplatná kategória")

    slug = slugify(page.title)

    db_page = Page(**page.model_dump(), slug=slug)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page


@PAGE_CRUD_ROUTER.get("/{id_slug}", response_model=PageOut)
def read_page(id_slug: str, db: Session = Depends(get_db)):
    try:
        page_id = int(id_slug.split("-")[0])
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Neplatné ID v URL")

    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Stránka neexistuje")
    return db_page


@PAGE_CRUD_ROUTER.put("/{id_slug}", response_model=PageOut)
def update_page(id_slug: str, page: PageUpdate, db: Session = Depends(get_db)):
    try:
        page_id = int(id_slug.split("-")[0])
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Neplatné ID v URL")

    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Stránka neexistuje")

    if page.title is not None:
        db_page.title = page.title
        db_page.slug = slugify(page.title)
    if page.html_content is not None:
        db_page.html_content = page.html_content
    if page.category_id is not None:
        db_page.category_id = page.category_id

    db.commit()
    db.refresh(db_page)
    return db_page


@PAGE_CRUD_ROUTER.delete("/{id_slug}", status_code=204)
def delete_page(id_slug: str, db: Session = Depends(get_db)):
    try:
        page_id = int(id_slug.split("-")[0])
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Neplatné ID v URL")

    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Stránka neexistuje")

    db.delete(db_page)
    db.commit()
    return None


@PAGE_CRUD_ROUTER.get("/", response_model=list[PageOut])
def read_all_pages(db: Session = Depends(get_db)):
    return db.query(Page).all()
