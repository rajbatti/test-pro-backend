# from typing import List, Optional

# from fastapi import HTTPException, status
# from bson import ObjectId

# from app.db import users_collection
# from app.models import UserModel, PyObjectId
# from app.schemas import UserCreate, UserUpdate, UserInDB
# from app.services.auth_service import get_password_hash

# async def get_user_by_id(user_id: PyObjectId) -> Optional[UserInDB]:
#     user = await users_collection.find_one({"_id": user_id})
#     if user:
#         return UserInDB(**user)
#     return None

# async def get_user_by_email(email: str) -> Optional[UserInDB]:
#     user = await users_collection.find_one({"email": email})
#     if user:
#         return UserInDB(**user)
#     return None

# async def get_user_by_username(username: str) -> Optional[UserInDB]:
#     user = await users_collection.find_one({"username": username})
#     if user:
#         return UserInDB(**user)
#     return None

# async def create_user(user: UserCreate) -> UserInDB:
#     existing_user = await users_collection.find_one({"email": user.email})
#     if existing_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
#     existing_username = await users_collection.find_one({"username": user.username})
#     if existing_username:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

#     hashed_password = get_password_hash(user.password)
#     user_data = user.dict()
#     user_data["hashed_password"] = hashed_password
#     user_data["role"] = "student" # Default role
    
#     new_user = UserModel(**user_data)
#     await users_collection.insert_one(new_user.dict(by_alias=True, exclude_none=True))
#     return UserInDB(**new_user.dict(by_alias=True, exclude_none=True))

# async def update_user(user_id: PyObjectId, user_update: UserUpdate) -> Optional[UserInDB]:
#     update_data = user_update.dict(exclude_unset=True)
#     if "password" in update_data:
#         update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

#     if update_data:
#         result = await users_collection.update_one(
#             {"_id": user_id}, {"$set": update_data}
#         )
#         if result.modified_count == 1:
#             updated_user = await users_collection.find_one({"_id": user_id})
#             return UserInDB(**updated_user)
#     return None

# async def delete_user(user_id: PyObjectId) -> bool:
#     result = await users_collection.delete_one({"_id": user_id})
#     return result.deleted_count == 1

# async def get_all_users() -> List[UserInDB]:
#     users = []
#     async for user in users_collection.find():
#         users.append(UserInDB(**user))
#     return users