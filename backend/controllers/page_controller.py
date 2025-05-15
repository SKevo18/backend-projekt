from datetime import datetime
from typing import Optional

from db import get_db
from db.orm import Category, Page
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from slugify import slugify
from sqlalchemy.orm import Session

PAGE_CONTROLLER = APIRouter(prefix="/page")


class PageBase(BaseModel):
    category_id: int
    title: str
    html_content: str


class PageCreate(PageBase):
    slug: Optional[str] = None


class PageUpdate(BaseModel):
    category_id: Optional[int] = None
    title: Optional[str] = None
    html_content: Optional[str] = None
    slug: Optional[str] = None


class PageOut(PageBase):
    id: int
    slug: str
    created_at: datetime

    class Config:
        from_attributes = True


@PAGE_CONTROLLER.post("/", response_model=PageOut)
def create_page(page: PageCreate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == page.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Neplatná kategória")

    slug = slugify(page.slug) if page.slug else slugify(page.title)

    if db.query(Page).filter(Page.slug == slug).first():
        raise HTTPException(status_code=400, detail="Slug už existuje")

    db_page = Page(**page.model_dump(exclude={"slug"}), slug=slug)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page


@PAGE_CONTROLLER.get("/", response_model=list[PageOut])
def list_pages(
    category_id: int = Query(),
    db: Session = Depends(get_db),
):
    if not category_id:
        raise HTTPException(status_code=400, detail="ID kategórie je povinné")

    db_page = db.query(Page).filter(Page.category_id == category_id).all()
    return db_page


@PAGE_CONTROLLER.get("/{page_id}", response_model=PageOut)
def read_page(
    page_id: int,
    db: Session = Depends(get_db),
):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Stránka neexistuje")
    return db_page


@PAGE_CONTROLLER.put("/{page_id}", response_model=PageOut)
def update_page(
    page_id: int,
    page: PageUpdate,
    db: Session = Depends(get_db),
):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Stránka neexistuje")

    if page.title is not None:
        db_page.title = page.title

    if page.slug is not None and page.slug != db_page.slug:
        if db.query(Page).filter(Page.slug == page.slug).first():
            raise HTTPException(status_code=400, detail="Slug už existuje")
        db_page.slug = slugify(page.slug)

    elif page.title is not None:
        db_page.slug = slugify(page.title)

    if page.html_content is not None:
        db_page.html_content = page.html_content
    if page.category_id is not None:
        db_page.category_id = page.category_id

    db.commit()
    db.refresh(db_page)
    return db_page


@PAGE_CONTROLLER.delete("/{page_id}", status_code=204)
def delete_page(
    page_id: int,
    db: Session = Depends(get_db),
):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Stránka neexistuje")

    db.delete(db_page)
    db.commit()
    return None


@PAGE_CONTROLLER.get("/", response_model=list[PageOut])
def read_all_pages(db: Session = Depends(get_db)):
    return db.query(Page).all()
    