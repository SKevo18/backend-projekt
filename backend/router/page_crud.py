from datetime import datetime
from typing import Optional, List

from db import get_db
from db.orm import Category, Page, UserPagePermission, User
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from slugify import slugify
from sqlalchemy.orm import Session
from router.dependencies import get_current_user, get_admin_user

PAGE_CRUD_ROUTER = APIRouter(prefix="/page")


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
def create_page(
    page: PageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != 2:
        raise HTTPException(status_code=403, detail="Only admin can create pages")

    category = db.query(Category).filter(Category.id == page.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category")

    slug = slugify(page.slug) if page.slug else slugify(page.title)

    if db.query(Page).filter(Page.slug == slug).first():
        raise HTTPException(status_code=400, detail="Slug already exists")

    db_page = Page(**page.model_dump(exclude={"slug"}), slug=slug)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page


@PAGE_CRUD_ROUTER.get("/", response_model=List[PageOut])
def list_pages(
    category_id: int = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Page)
    if category_id:
        query = query.filter(Page.category_id == category_id)
    return query.all()


@PAGE_CRUD_ROUTER.get("/{page_id}", response_model=PageOut)
def read_page(
    page_id: int,
    db: Session = Depends(get_db),
):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    return db_page


@PAGE_CRUD_ROUTER.put("/{page_id}", response_model=PageOut)
def update_page(
    page_id: int,
    page: PageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")

    if current_user.role != 2:
        permission = (
            db.query(UserPagePermission)
            .filter_by(user_id=current_user.id, page_id=page_id)
            .first()
        )
        if not permission:
            raise HTTPException(
                status_code=403, detail="No permission to edit this page"
            )

    if page.title is not None:
        db_page.title = page.title

    if page.slug is not None and page.slug != db_page.slug:
        if db.query(Page).filter(Page.slug == page.slug).first():
            raise HTTPException(status_code=400, detail="Slug already exists")
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


@PAGE_CRUD_ROUTER.delete("/{page_id}", status_code=204)
def delete_page(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="Page not found")

    db.delete(db_page)
    db.commit()
    return None


@PAGE_CRUD_ROUTER.get("/user/{user_id}", response_model=List[PageOut])
def get_user_accessible_pages(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role != 2:
        raise HTTPException(status_code=403, detail="Access denied")

    if current_user.role == 2:
        return db.query(Page).all()

    permissions = db.query(UserPagePermission.page_id).filter_by(user_id=user_id).all()
    page_ids = [p.page_id for p in permissions]
    return db.query(Page).filter(Page.id.in_(page_ids)).all()
