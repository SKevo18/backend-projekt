import logging
from datetime import datetime
from enum import Enum

from db import get_db
from db.orm import User
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.orm import Session
from utils.jwt_utils import create_access_token


class UserRole(Enum):
    USER = 0
    EDITOR = 1
    ADMIN = 2


AUTH_CONTROLLER = APIRouter(prefix="/authentication")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="authentication/login")
logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# circular
from controllers.dependencies import validate_turnstile_token, get_current_user  # noqa: E402


class UserBaseModel(BaseModel):
    title_before_name: str = ""
    title_after_name: str = ""

    first_name: str
    middle_name: str = ""
    last_name: str


class UserRegisterModel(UserBaseModel):
    user_email: EmailStr
    user_password: str
    turnstile_token: str

    @field_validator("user_password")
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


@AUTH_CONTROLLER.post("/register")
async def register(
    user: UserRegisterModel,
    request: Request,
    db: Session = Depends(get_db),
):
    validate_turnstile_token(request, user.turnstile_token)

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
            role=UserRole.USER.value,
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


@AUTH_CONTROLLER.post("/login")
def login(user: LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(user_email=user.user_email).first()
    if not db_user or not verify_password(user.user_password, db_user.user_password):
        logger.warning(f"Failed login attempt for {user.user_email}")
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": db_user.user_email})
    logger.info(f"User logged in: {user.user_email}")
    return {"access_token": token, "token_type": "bearer"}


@AUTH_CONTROLLER.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "title_before_name": current_user.title_before_name,
        "title_after_name": current_user.title_after_name,
        "first_name": current_user.first_name,
        "middle_name": current_user.middle_name,
        "last_name": current_user.last_name,
        "user_email": current_user.user_email,
        "role": current_user.role,
    }


@AUTH_CONTROLLER.post("/update_profile")
def update_profile(
    profile: UserBaseModel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        current_user.title_before_name = profile.title_before_name
        current_user.title_after_name = profile.title_after_name
        current_user.first_name = profile.first_name
        current_user.middle_name = profile.middle_name
        current_user.last_name = profile.last_name

        db.commit()
        logger.info(f"Profile updated for user: {current_user.user_email}")

        return {"status": "success", "message": "Profile updated successfully!"}
    except Exception as e:
        logger.error(f"Profile update failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
