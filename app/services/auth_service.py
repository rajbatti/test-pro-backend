from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from google.oauth2 import id_token
from google.auth.transport import requests

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, GOOGLE_CLIENT_ID
from app.db import users_collection
from app.models import UserModel


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

async def get_user_by_email(email: str) -> Optional[UserModel]:
    user_doc = await users_collection.find_one({"email": email})
    if user_doc:
        return UserModel(**user_doc)
    return None

async def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        return idinfo
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Google credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_doc = await users_collection.find_one({"email": email})
    if user_doc is None:
        raise credentials_exception
    return UserModel(**user_doc)

# async def get_current_active_user(current_user: UserInDB):
#     if current_user.disabled: # Assuming a 'disabled' field in UserModel
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
#     return current_user

# async def get_current_admin_user(current_user: UserInDB):
#     if current_user.role != "admin":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin user")
#     return current_user