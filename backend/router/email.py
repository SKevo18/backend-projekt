from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from utils.mail import send_email

EMAIL_ROUTER = APIRouter(prefix="/email")

class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    message: str

@EMAIL_ROUTER.post("/send")
def send(email: EmailSchema):
    try:
        send_email(email.email, email.subject, email.message)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
