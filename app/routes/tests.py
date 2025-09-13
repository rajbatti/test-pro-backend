from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Request

from app.models import TestModel, TestOrResultResponse, TestModelDTO
from app.services import test_services

router = APIRouter()

# Create test: accepts name, category_id, time_limit_minutes and a .docx file
@router.post("/tests/create", response_model=TestModel)
async def create_test(
    request: Request,
    name: str = Form(...),
    time_limit_minutes: int = Form(...),
    is_practice: bool = Form(False),
    file: UploadFile = File(...)
):
    # Call service to create test with these parameters
    user=request.state.user
    return await test_services.create_test(name, time_limit_minutes, is_practice, file, user)

@router.get("/tests",response_model=List[TestModelDTO])
async def get_tests(request:Request):
    user= request.state.user
    return await test_services.get_tests(user)

@router.get("/tests/{test_id}",response_model=TestOrResultResponse)
async def get_test(request:Request,test_id: str):
    user = request.state.user
    return await test_services.get_test_by_id(test_id,user)

@router.post("/tests/{test_id}/submit")
async def submit_test_endpoint(request:Request,test_id: str,answers:List[str]=Form(...)):
    user = request.state.user
    return await test_services.submit_test(test_id,answers,user)
