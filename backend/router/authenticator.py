from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db import get_db
from db.orm import User
from sqlalchemy.orm import Session
from datetime import datetime

AUTH_ROUTER = APIRouter(prefix="/Authentication")


class UserModel(BaseModel):
    first_name: str
    last_name: str
    user_email: str
    user_password: str


@AUTH_ROUTER.post("/register")
async def register(user: UserModel, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter_by(user_email=user.user_email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            user_email=user.user_email,
            user_password=user.user_password,
            registered_at=datetime.now(),
        )
        db.add(new_user)
        db.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
