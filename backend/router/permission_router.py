from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from db.orm import UserPagePermission, UserCategoryPermission, User, Page, Category
from router.dependencies import get_admin_user, get_current_user

PERMISSION_ROUTER = APIRouter(prefix="/permissions")


@PERMISSION_ROUTER.post("/")
def add_permission(
    user_id: int,
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Add permission for editor to access specific page"""
    user = db.query(User).filter(User.id == user_id, User.role == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="Editor not found")

    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    existing = (
        db.query(UserPagePermission).filter_by(user_id=user_id, page_id=page_id).first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")

    new_permission = UserPagePermission(user_id=user_id, page_id=page_id)
    db.add(new_permission)
    db.commit()
    return {"message": "Permission added"}


@PERMISSION_ROUTER.delete("/")
def remove_permission(
    user_id: int,
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Remove permission from editor for specific page"""
    permission = (
        db.query(UserPagePermission).filter_by(user_id=user_id, page_id=page_id).first()
    )
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(permission)
    db.commit()
    return {"message": "Permission removed"}


@PERMISSION_ROUTER.get("/{user_id}/pages")
def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of page IDs that user has permission to edit"""
    if current_user.role != 2 and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    permissions = db.query(UserPagePermission.page_id).filter_by(user_id=user_id).all()
    return [p.page_id for p in permissions]


@PERMISSION_ROUTER.get("/{user_id}/pages/{page_id}")
def check_user_permission(
    user_id: int,
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check if user has permission to edit specific page"""

    if current_user.role == 2:
        return {"has_permission": True}

    permission = (
        db.query(UserPagePermission).filter_by(user_id=user_id, page_id=page_id).first()
    )

    return {"has_permission": permission is not None}


@PERMISSION_ROUTER.post("/category")
def add_category_permission(
    user_id: int,
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Add permission for editor to access entire category"""
    user = db.query(User).filter(User.id == user_id, User.role == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="Editor not found")

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    existing = (
        db.query(UserCategoryPermission)
        .filter_by(user_id=user_id, category_id=category_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")

    new_permission = UserCategoryPermission(user_id=user_id, category_id=category_id)
    db.add(new_permission)
    db.commit()
    return {"message": "Category permission added"}


@PERMISSION_ROUTER.delete("/category")
def remove_category_permission(
    user_id: int,
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Remove category permission from editor"""
    permission = (
        db.query(UserCategoryPermission)
        .filter_by(user_id=user_id, category_id=category_id)
        .first()
    )
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(permission)
    db.commit()
    return {"message": "Category permission removed"}


@PERMISSION_ROUTER.get("/{user_id}/categories")
def get_user_category_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of category IDs that user has permission to edit"""
    if current_user.role != 2 and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    permissions = (
        db.query(UserCategoryPermission.category_id).filter_by(user_id=user_id).all()
    )
    return [p.category_id for p in permissions]


@PERMISSION_ROUTER.get("/{user_id}/categories/{category_id}")
def check_user_category_permission(
    user_id: int,
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check if user has permission to edit category"""
    if current_user.role == 2:
        return {"has_permission": True}

    permission = (
        db.query(UserCategoryPermission)
        .filter_by(user_id=user_id, category_id=category_id)
        .first()
    )

    return {"has_permission": permission is not None}
