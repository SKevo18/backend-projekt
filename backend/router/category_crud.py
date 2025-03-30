from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db
from db.orm import Category

CATEGORY_ROUTER = APIRouter(prefix="/category")


class CategoryCreate(BaseModel):
    title: str


class CategoryOut(CategoryCreate):
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
