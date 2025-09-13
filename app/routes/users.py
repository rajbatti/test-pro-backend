# from typing import List

# from fastapi import APIRouter, Depends, HTTPException, status
# from bson import ObjectId

# from app.services import user_service, auth_service
# from app.schemas import UserUpdate, UserInDB
# from app.models import PyObjectId

# router = APIRouter()

# @router.get("/users", response_model=List[UserInDB])
# async def get_all_users(current_user: UserInDB = Depends(auth_service.get_current_admin_user)):
#     return await user_service.get_all_users()

# @router.get("/users/{user_id}", response_model=UserInDB)
# async def get_user_by_id(user_id: PyObjectId, current_user: UserInDB = Depends(auth_service.get_current_admin_user)):
#     user = await user_service.get_user_by_id(user_id)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     return user

# @router.put("/users/{user_id}", response_model=UserInDB)
# async def update_user(user_id: PyObjectId, user_update: UserUpdate, current_user: UserInDB = Depends(auth_service.get_current_admin_user)):
#     updated_user = await user_service.update_user(user_id, user_update)
#     if not updated_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     return updated_user

# @router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(user_id: PyObjectId, current_user: UserInDB = Depends(auth_service.get_current_admin_user)):
#     if not await user_service.delete_user(user_id):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     return