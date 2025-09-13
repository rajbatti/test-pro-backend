from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Any

# Custom ObjectId field
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, *args, **kwargs):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class QuestionModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    question: str
    options: List[str]
    correct_option: str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    email: str
    role: str = "student"  # Default role
    created_at: datetime = Field(default_factory=datetime.now)
    phone: Optional[str] = None
    disabled: bool = False

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class TestModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    questions: List[PyObjectId] = []  # Assuming questions will be referenced by their IDs
    time_limit_minutes: int
    is_practice: bool = False
    author: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class ResultModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    test_id: PyObjectId
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    answers: List[str] = []
    score: float = 0
    completed: bool = False
    total_questions: int=0,
    questions_attempted: int=0,
    correct_answers: int=0

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class TestPaperModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    questions: List[QuestionModel]
    time_limit_minutes: int
    is_practice: bool = False
    author: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class TestOrResultResponse(BaseModel):
    test: TestPaperModel = None
    result: Optional[ResultModel] = None

class TestModelDTO(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    questions: List[PyObjectId] = []  # Assuming questions will be referenced by their IDs
    time_limit_minutes: int
    is_practice: bool = False
    author: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    is_completed: bool = False
    score: Optional[float] = 0
    completedAt: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True