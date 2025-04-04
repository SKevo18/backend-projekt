import uuid

from db import get_db
from db.orm import User
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from utils.mail import send_email

EMAIL_ROUTER = APIRouter(prefix="/auth")


class EmailResetRequest(BaseModel):
    email: EmailStr


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
