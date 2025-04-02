from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from db.orm import User
from utils.mail import send_email
from db import get_db
import uuid

EMAIL_ROUTER = APIRouter(prefix="/auth")

#temporarily
def generate_reset_token(user_id: int) -> str:
    return str(uuid.uuid4())

from pydantic import BaseModel, EmailStr

class EmailResetRequest(BaseModel):
    email: EmailStr

@EMAIL_ROUTER.post("/password_reset")
def password_reset(req: EmailResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = generate_reset_token(user.id)
    reset_link = f"https://reset-password.sk/reset-password?token={reset_token}"

    message = f"Click here to reset your password: {reset_link}"
    send_email(req.email, "Password Reset", message)

    return {"message": "Password reset email sent"}

