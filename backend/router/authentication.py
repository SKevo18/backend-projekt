from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db import get_db
from db.orm import User
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext

AUTH_ROUTER = APIRouter(prefix="/authentication")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(BaseModel):
    first_name: str
    last_name: str
    user_email: str
    user_password: str
    role: int

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@AUTH_ROUTER.post("/register")
async def register(user: UserModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(user_email=user.user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.user_password)
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        user_email=user.user_email,
        user_password=hashed_password,
        role=user.role,
        registered_at=datetime.now(),
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

class LoginModel(BaseModel):
    user_email: str
    user_password: str

@AUTH_ROUTER.post("/login")
async def login(user: LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(user_email=user.user_email).first()
    if not db_user or not verify_password(user.user_password, db_user.user_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"message": "Login successful"}