from db import get_db
from db.orm import User
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from utils.jwt_utils import verify_access_token

from router.authentication import UserRole, OAUTH2_SCHEME


def get_current_user(
    token: str = Depends(OAUTH2_SCHEME),
    db: Session = Depends(get_db),
) -> User:
    payload = verify_access_token(token)
    user_email = payload.get("sub")
    user = db.query(User).filter_by(user_email=user_email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user


def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role < UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
