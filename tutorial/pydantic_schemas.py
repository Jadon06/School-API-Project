from pydantic import BaseModel, EmailStr, BeforeValidator, Field, ConfigDict
from typing import Optional, Annotated
from bson.objectid import ObjectId
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from beanie import Document

PyObjectId = Annotated[str, BeforeValidator(str)]

class students(Document):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[int] = None
    GPA: Optional[float] = 0.0
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    class Settings:
        collection_name="students"

class student(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[int] = None

class student_response(student):
    pass
    id: PyObjectId
    created_at: datetime = datetime.now(timezone.utc)

class update_student(BaseModel):
    email: Optional[EmailStr]
    phone_number: Optional[int]


class course_schema(BaseModel):
    course_code: str
    course_name: str
    time_added: datetime = datetime.now(timezone.utc)