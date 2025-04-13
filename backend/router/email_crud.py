import uuid

import os
from db import get_db
from db.orm import User, Setting
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from utils.mail import send_email

EMAIL_ROUTER = APIRouter(prefix="/email")
# TODO: použiť adminov mail:
TEST_EMAIL = os.getenv("test_email_recipient")


class EmailResetRequest(BaseModel):
    email: EmailStr


class SaveSMTPRequest(BaseModel):
    smtp_host: str
    smtp_port: int
    email_sender: str
    email_password: str


@EMAIL_ROUTER.post("/password_reset")
def password_reset(req: EmailResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = str(uuid.uuid4())
    reset_link = f"https://reset-password.sk/reset-password?token={reset_token}"

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
