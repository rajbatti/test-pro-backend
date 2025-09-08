from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

# Custom ObjectId field
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
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
