from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models import PyObjectId, QuestionModel # Import QuestionModel if it's used directly in TestCreate/Update

class QuestionCreate(BaseModel):
    question: str
    options: List[str]
    correct_option: str

class QuestionUpdate(BaseModel):
    question: str | None = None
    options: List[str] | None = None
    correct_option: str | None = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None

class User(BaseModel):
    id: PyObjectId = Field(alias="_id")
    username: str
    email: str
    role: str
    created_at: datetime
    phone: Optional[str] = None
    disabled: bool = False
    hashed_password: str # Store hashed password

    class Config:
        json_encoders = {PyObjectId: str}
        allow_population_by_field_name = True

class TestCreate(BaseModel):
    name: str
    questions: List[PyObjectId] # List of Question IDs
    time_limit_minutes: int
    is_practice: bool = False

class TestUpdate(BaseModel):
    name: Optional[str] = None
    questions: Optional[List[PyObjectId]] = None
    time_limit_minutes: Optional[int] = None
    is_practice: Optional[bool] = None

class TestInDB(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    questions: List[PyObjectId]
    time_limit_minutes: int
    is_practice: bool
    created_at: datetime

    class Config:
        json_encoders = {PyObjectId: str}
        allow_population_by_field_name = True

class ResultCreate(BaseModel):
    user_id: PyObjectId
    test_id: PyObjectId
    answers: List[str]

class ResultUpdate(BaseModel):
    end_time: Optional[datetime] = None
    answers: Optional[List[str]] = None
    completed: Optional[bool] = None

class ResultInDB(BaseModel):
    id: PyObjectId = Field(alias="_id")
    user_id: PyObjectId
    test_id: PyObjectId
    start_time: datetime
    end_time: Optional[datetime] = None
    answers: List[str]
    completed: bool

    class Config:
        json_encoders = {PyObjectId: str}
        allow_population_by_field_name = True
