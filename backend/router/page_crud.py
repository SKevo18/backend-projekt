from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db
from db.orm import Page, Category

PAGE_CRUD_ROUTER = APIRouter(prefix="/page")


def generate_unique_slug(db: Session, title: str) -> str:
    base_slug = slugify(title)
    slug = base_slug
    i = 1
    while db.query(Page).filter(Page.slug == slug).first():
        slug = f"{base_slug}-{i}"
        i += 1
    return slug


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


@PAGE_CRUD_ROUTER.post("/", response_model=PageOut)
def create_page(page: PageCreate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == page.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Neplatná kategória")

    slug = page.slug or generate_unique_slug(db, page.title)
    if db.query(Page).filter(Page.slug == slug).first():
        raise HTTPException(status_code=400, detail="Slug already exists")

    db_page = Page(**page.model_dump(exclude={"slug"}), slug=slug)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page


@PAGE_CRUD_ROUTER.get("/{slug}", response_model=PageOut)
def read_page(slug: str, db: Session = Depends(get_db)):
    db_page = db.query(Page).filter(Page.slug == slug).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    return db_page


@PAGE_CRUD_ROUTER.put("/{slug}", response_model=PageOut)
def update_page(slug: str, page: PageUpdate, db: Session = Depends(get_db)):
    db_page = db.query(Page).filter(Page.slug == slug).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Page not found")

    if page.title is not None:
        db_page.title = page.title
    if page.html_content is not None:
        db_page.html_content = page.html_content
    if page.category_id is not None:
        db_page.category_id = page.category_id
    if page.slug is not None and page.slug != slug:
        if db.query(Page).filter(Page.slug == page.slug).first():
            raise HTTPException(status_code=400, detail="Slug already exists")
        db_page.slug = page.slug

    db.commit()
    db.refresh(db_page)
    return db_page


@PAGE_CRUD_ROUTER.delete("/{slug}", status_code=204)
def delete_page(slug: str, db: Session = Depends(get_db)):
    db_page = db.query(Page).filter(Page.slug == slug).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    db.delete(db_page)
    db.commit()
    return None


@PAGE_CRUD_ROUTER.get("/", response_model=list[PageOut])
def read_all_pages(db: Session = Depends(get_db)):
    return db.query(Page).all()
