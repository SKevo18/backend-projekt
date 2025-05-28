from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from slugify import slugify
from sqlalchemy.orm import Session

from controllers.dependencies import get_current_user
from controllers.authentication_controller import UserRole
from db import get_db
from db.orm import Category, Page, User, UserPagePermission, UserCategoryPermission

PAGE_CONTROLLER = APIRouter(prefix="/page")
MAX_PER_PAGE = 100


class PageBase(BaseModel):
    category_id: int
    title: str = Field(max_length=100)
    html_content: str = Field(max_length=4294967295)


class PageCreate(PageBase):
    slug: str | None = Field(max_length=100, default=None)


class PageUpdate(BaseModel):
    category_id: int | None = None
    title: str | None = Field(max_length=100, default=None)
    html_content: str | None = Field(max_length=4294967295, default=None)
    slug: str | None = Field(max_length=100, default=None)


class PageOut(PageBase):
    id: int
    slug: str
    created_at: datetime

    class Config:
        from_attributes = True


def check_can_create_page(user: User, category_id: int, db: Session):
    if user.role == UserRole.ADMIN.value:
        return True

    if user.role < UserRole.EDITOR.value:
        raise HTTPException(status_code=403, detail="Editor or admin access required")

    category_permission = (
        db.query(UserCategoryPermission)
        .filter_by(user_id=user.id, category_id=category_id)
        .first()
    )

    if not category_permission:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to create pages in this category",
        )

    return True


def check_can_edit_page(user: User, page_id: int, db: Session):
    if user.role == UserRole.ADMIN.value:
        return True

    if user.role < UserRole.EDITOR.value:
        raise HTTPException(status_code=403, detail="Editor or admin access required")

    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    page_permission = (
        db.query(UserPagePermission).filter_by(user_id=user.id, page_id=page_id).first()
    )

    if page_permission:
        return True

    category_permission = (
        db.query(UserCategoryPermission)
        .filter_by(user_id=user.id, category_id=page.category_id)
        .first()
    )

    if category_permission:
        return True

    raise HTTPException(
        status_code=403, detail="You don't have permission to edit this page"
    )


@PAGE_CONTROLLER.post("/", response_model=PageOut)
def create_page(
    page: PageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_can_create_page(current_user, page.category_id, db)

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


@PAGE_CONTROLLER.get("/", response_model=list[PageOut])
def read_pages(
    category_id: int | None = Query(None, description="Filter results by category ID"),
    page: int = Query(1, ge=1, description="Page number (must be ≥ 1)"),
    per_page: int = Query(
        10,
        ge=1,
        le=MAX_PER_PAGE,
        description=f"Number of items per page (1–{MAX_PER_PAGE})",
    ),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * per_page

    query = db.query(Page)
    if category_id is not None:
        query = query.filter(Page.category_id == category_id)

    pages = query.order_by(Page.id).offset(skip).limit(per_page).all()
    return pages


@PAGE_CONTROLLER.get("/{page_id}", response_model=PageOut)
def read_page(
    page_id: int,
    db: Session = Depends(get_db),
):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="The page does not exist")
    return db_page


@PAGE_CONTROLLER.put("/{page_id}", response_model=PageOut)
def update_page(
    page_id: int,
    page: PageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_can_edit_page(current_user, page_id, db)

    db_page = db.query(Page).filter(Page.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="The page does not exist")

    if page.category_id is not None and page.category_id != db_page.category_id:
        check_can_create_page(current_user, page.category_id, db)

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


@PAGE_CONTROLLER.delete("/{page_id}", status_code=204)
def delete_page(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_can_edit_page(current_user, page_id, db)

    db_page = db.query(Page).filter(Page.id == page_id).first()
    if db_page is None:
        raise HTTPException(status_code=404, detail="The page does not exist")

    db.delete(db_page)
    db.commit()
    return None
