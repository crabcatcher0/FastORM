import jwt
from datetime import datetime, timedelta
from .secrete import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from functools import wraps
from fastapi import Depends, HTTPException, Request
from fast_project.models import User
from jwt import PyJWTError


"""
    1. access_token creation
    2. decode token
    3. get_current_user
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalid")
    


def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = token.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = User.get_data(email=email)
        if user is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return user
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

def get_email_from_token(token: str):
    try:
        token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub") 
    except PyJWTError:
        return None