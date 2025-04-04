from datetime import datetime

from db import get_db
from db.orm import User
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from router.jwt_utils import create_access_token, verify_access_token

AUTH_ROUTER = APIRouter(prefix="/authentication")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentication/login")

class UserModel(BaseModel): #user model 
    first_name: str
    last_name: str
    user_email: str
    user_password: str
    role: int

class LoginModel(BaseModel): # login model 
    user_email: str
    user_password: str

def hash_password(password: str) -> str: #chesovania hesla 
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool: #overovania chesa
    return pwd_context.verify(plain_password, hashed_password)

@AUTH_ROUTER.post("/register")
def register(user: UserModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(user_email=user.user_email).first() #overovania ci je existuje user mail 
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.user_password)
    #ak nie exsistuje tak sa vytvori novy 
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


    token = create_access_token({"sub": new_user.user_email}) #tu sa predieli user token kory sa vytvori
    return {"access_token": token, "token_type": "bearer"}

@AUTH_ROUTER.post("/login")
def login(user: LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(user_email=user.user_email).first() # tu je celkovo overovania na login ci je spravny mail alebo heslo
    if not db_user or not verify_password(user.user_password, db_user.user_password):
        raise HTTPException(status_code=400, detail="Invalid email or password") # musi sa pysat ze nepsravne mail alebo heslo, kvoli bezpecnosti nemozem dat ze je zly mail!

    token = create_access_token({"sub": db_user.user_email})# tak isto vytvorenia tokena pre usera ktory prisiel do systemu 
    return {"access_token": token, "token_type": "bearer"}

@AUTH_ROUTER.get("/me")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    user_email = payload.get("sub")
    user = db.query(User).filter_by(user_email=user_email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return jsonable_encoder(user)
