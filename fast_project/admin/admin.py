import jwt
from datetime import datetime, timedelta
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Request
from fast_project.models import User
from jwt import PyJWTError
from .secrete import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRETE_KEY


def create_admin_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiry})
    encode_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    return encode_jwt


def decode_admin_token(token: str):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalid.")
