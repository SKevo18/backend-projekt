from db import get_db
from db.orm import User
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from utils.jwt_utils import verify_access_token
from utils.turnstile import validate_turnstile

from controllers.authentication_controller import OAUTH2_SCHEME, UserRole


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


def validate_turnstile_token(
    request: Request,
    turnstile_token: str,
) -> None:
    client_ip = request.client.host if request.client else None
    turnstile_result = validate_turnstile(turnstile_token, client_ip)

    if not turnstile_result.success:
        error_details = (
            ", ".join(turnstile_result.error_codes)
            if turnstile_result.error_codes
            else "Unknown error"
        )
        raise HTTPException(
            status_code=400, detail=f"CAPTCHA verification failed: {error_details}"
        )
