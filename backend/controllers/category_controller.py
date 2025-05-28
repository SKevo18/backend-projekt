from datetime import datetime
from typing import List

from db import get_db
from db.orm import Category
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from controllers.dependencies import get_admin_user

CATEGORY_CONTROLLER = APIRouter(prefix="/category")


class CategoryCreate(BaseModel):
    title: str = Field(max_length=45)


class CategoryOut(CategoryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


@CATEGORY_CONTROLLER.post("/", response_model=CategoryOut)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    _=Depends(get_admin_user),
):
    category = Category(title=data.title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@CATEGORY_CONTROLLER.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_admin_user),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted"}


@CATEGORY_CONTROLLER.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    data: CategoryCreate,
    db: Session = Depends(get_db),
    _=Depends(get_admin_user),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.title = data.title
    db.commit()
    db.refresh(category)
    return category


@CATEGORY_CONTROLLER.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
