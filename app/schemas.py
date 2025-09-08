from typing import List
from pydantic import BaseModel

class QuestionCreate(BaseModel):
    question: str
    options: List[str]
    correct_option: str

class QuestionUpdate(BaseModel):
    question: str | None = None
    options: List[str] | None = None
    correct_option: str | None = None
