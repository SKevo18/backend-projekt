import uuid

import os
from db import get_db
from db.orm import User, Setting, PasswordReset
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from utils.mail import send_email, get_setting
from datetime import datetime

EMAIL_ROUTER = APIRouter(prefix="/email")
# TODO: použiť adminov mail:
TEST_EMAIL = os.getenv("test_email_recipient")
FRONTEND_URL = os.getenv("FRONTEND_URL")


class EmailResetRequest(BaseModel):
    email: EmailStr


class SaveSMTPRequest(BaseModel):
    smtp_host: str
    smtp_port: int
    email_sender: str
    email_password: str

class PasswordUpdateRequest(BaseModel):
    token: str
    new_password: str

@EMAIL_ROUTER.post("/password_update")
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


@EMAIL_ROUTER.post("/password_reset")
def password_reset(req: EmailResetRequest, db: Session = Depends(get_db)):
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


@EMAIL_ROUTER.post("/save_smtp")
def save_smtp(req: SaveSMTPRequest, db: Session = Depends(get_db)):
    data = req.model_dump()

    insert_values = [{"key": k, "value": str(v)} for k, v in data.items()]
    stmt = insert(Setting).values(insert_values)
    update_stmt = stmt.on_duplicate_key_update(value=stmt.inserted.value)

    db.execute(update_stmt)
    db.commit()

    return {"message": "SMTP settings saved"}

@EMAIL_ROUTER.post("/send_test_email")
def send_test_email():
    if TEST_EMAIL is None:
        raise HTTPException(status_code=500, detail="SMTP settings are not set")

    try:
        send_email(TEST_EMAIL, "Test Email", "This is a test email.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Test mail sent successfully"}

@EMAIL_ROUTER.get("/settings")
def get_smtp_settings():
    return {
        "smtp_host": get_setting("smtp_host"),
        "smtp_port": get_setting("smtp_port"),
        "email_sender": get_setting("email_sender"),
        "email_password": get_setting("email_password"),
    }
