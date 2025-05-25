import os
import uuid
from datetime import datetime

from db import get_db
from db.orm import PasswordReset, User
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from utils.mail import send_email

from controllers.dependencies import get_admin_user, validate_turnstile_token

EMAIL_CONTROLLER = APIRouter(prefix="/email")
FRONTEND_URL = os.getenv("FRONTEND_URL")


class EmailResetRequest(BaseModel):
    email: EmailStr
    turnstile_token: str


class PasswordUpdateRequest(BaseModel):
    token: str
    new_password: str


@EMAIL_CONTROLLER.post("/password_update")
def password_update(req: PasswordUpdateRequest, db: Session = Depends(get_db)):
    password_reset = (
        db.query(PasswordReset).filter_by(token=req.token, used=False).first()
    )

    if not password_reset:
        raise HTTPException(status_code=404, detail="Invalid or expired token")

    user = db.query(User).filter_by(id=password_reset.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    from utils.password import hash_password

    user.user_password = hash_password(req.new_password)
    password_reset.used = True
    password_reset.edited_at = datetime.now()

    db.commit()

    return {"message": "Password successfully updated"}


@EMAIL_CONTROLLER.post("/password_reset")
def password_reset(
    req: EmailResetRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    validate_turnstile_token(request, req.turnstile_token)

    user = db.query(User).filter_by(user_email=req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = str(uuid.uuid4())
    password_reset = PasswordReset(
        user_id=user.id,
        token=reset_token,
        created_at=datetime.now(),
    )
    db.add(password_reset)
    db.commit()

    reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"
    message = f"Click here to reset your password: {reset_link}"
    send_email(req.email, "Password Reset", message)

    return {"message": "Password reset email sent"}


@EMAIL_CONTROLLER.post("/send_test_email")
def send_test_email(current_user: User = Depends(get_admin_user)):
    try:
        send_email(current_user.user_email, "Test Email", "This is a test email.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f"Test mail sent successfully to {current_user.user_email}"}
