from typing import List
from datetime import datetime
from db import get_db
from db.orm import Page, Category
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

PAGE_CRUD_ROUTER = APIRouter(prefix="/page")
CATEGORY_ROUTER = APIRouter(prefix="/category")

class CategoryCreate(BaseModel):
    title: str


class CategoryOut(CategoryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PageBase(BaseModel):
    category_id: int
    title: str
    html_content: str

class PageCreate(PageBase):
    pass


class PageUpdate(PageBase):
    pass


class PageOut(PageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


@CATEGORY_ROUTER.post("/", response_model=CategoryOut)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(title=data.title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@CATEGORY_ROUTER.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

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

    db_page.html_content = page.html_content
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

@PAGE_CRUD_ROUTER.get("/", response_model=List[PageOut])
def read_all_pages(db: Session = Depends(get_db)):
    return db.query(Page).all()
