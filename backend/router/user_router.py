from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from db.orm import User
from datetime import datetime
import logging
from router.dependencies import get_admin_user
from router.authentication import USER, EDITOR, ADMIN

logger = logging.getLogger(__name__)
USER_ROUTER = APIRouter(prefix="/user")


@USER_ROUTER.get("/")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_email": user.user_email,
            "role": user.role,
            "registered_at": user.registered_at,
            "edited_at": user.edited_at,
        }
        for user in users
    ]


@USER_ROUTER.patch("/{user_id}/role")
def update_user_role(
    user_id: int,
    role_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    user_to_update = db.query(User).filter_by(id=user_id).first()
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not role_data or "role" not in role_data:
        raise HTTPException(status_code=400, detail="Role is required")

    try:
        role = int(role_data["role"])
        if role not in [USER, EDITOR, ADMIN]:
            raise ValueError("Invalid role value")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    user_to_update.role = role
    user_to_update.edited_at = datetime.now()
    db.commit()

    logger.info(f"User role updated for user ID: {user_id}")
    return {"msg": "User role updated successfully"}
