import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

SECRET_KEY = "Elona_Mask_Pekna_Zena"  #to potom presuniem do env 

#funkcija na vytvarania tokena 
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=12)): #live time tokenu 12 hodin Pan Halvonik povedal ak je tam 24 hodin je to okej preto som dal zatial 12
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

#funkcija na overovania tokenu 
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
