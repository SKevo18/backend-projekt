from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
import logging

from db import get_db
from db.orm import User
from router.jwt_utils import create_access_token, verify_access_token

logger = logging.getLogger(__name__)
AUTH_ROUTER = APIRouter(prefix="/authentication")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentication/login")


USER = 0
EDITOR = 1
ADMIN = 2


class UserModel(BaseModel):
    first_name: str
    last_name: str
    user_email: str
    user_password: str
    role: int = USER  # Default role

    @validator("user_email")
    def validate_email(cls, v):
        try:
            validate_email(v)
            return v
        except EmailNotValidError:
            raise ValueError("Invalid email format")

    @validator("user_password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginModel(BaseModel):
    user_email: str
    user_password: str


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@AUTH_ROUTER.post("/register")
def register(user: UserModel, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter_by(user_email=user.user_email).first()
        if existing_user:
            logger.warning(
                f"Registration attempt with existing email: {user.user_email}"
            )
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
        logger.info(f"New user registered: {user.user_email}")

        token = create_access_token({"sub": new_user.user_email})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@AUTH_ROUTER.post("/login")
def login(user: LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(user_email=user.user_email).first()
    if not db_user or not verify_password(user.user_password, db_user.user_password):
        logger.warning(f"Failed login attempt for {user.user_email}")
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": db_user.user_email})
    logger.info(f"User logged in: {user.user_email}")
    return {"access_token": token, "token_type": "bearer"}


@AUTH_ROUTER.get("/me")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    user_email = payload.get("sub")
    user = db.query(User).filter_by(user_email=user_email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_email": user.user_email,
        "role": user.role,
    }
