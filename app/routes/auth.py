from datetime import timedelta

from fastapi import APIRouter, Response

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db import users_collection
from app.models import UserModel
from app.services import auth_service

router = APIRouter()

@router.post("/auth/google")
async def google_auth(token: str, role:str, response: Response):
    print("Token:",token)
    idinfo = await auth_service.verify_google_token(token)
    email = idinfo["email"]
    username = idinfo.get("name", email.split("@")[0])

    user = await users_collection.find_one({"email": email})

    if user:
        # User exists, log them in
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            expires=int(access_token_expires.total_seconds()),
        )
        return {"user":UserModel(**user)}
    else:
        # New user, create an account
        new_user = {
            "username":username,
            "email": email,
            "role": role,
        }
        await users_collection.insert_one(new_user)
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": new_user["email"]}, expires_delta=access_token_expires
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            expires=int(access_token_expires.total_seconds()),
        )
        return {"user":UserModel(**new_user)}
@router.get("/auth/test")
async def test():
    return {"test":"Successfull"}

@router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}