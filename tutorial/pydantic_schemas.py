from pydantic import BaseModel, EmailStr, BeforeValidator, Field, ConfigDict
from typing import Optional, Annotated
from bson.objectid import ObjectId
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import List

PyObjectId = Annotated[str, BeforeValidator(str)]

class course_add(BaseModel):
    course_code: str
    course_name: str
    time_added: Optional[datetime] = datetime.now(timezone.utc)

class course_create(BaseModel):
    course_code: str
    course_name: str
    professor: str
    class_size: int

class course_response(course_create):
    pass

class student(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[int] = None
    courses: Optional[List[course_add]] = None

class student_response(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[int] = None
    courses: Optional[List[course_add]] = None
    id: PyObjectId = Field(alias="_id") 
    created_at: datetime = datetime.now(timezone.utc)

    model_config = {
        "populate_by_name": True   # ← REQUIRED so FastAPI can output "id" instead of "_id"
    }

class professor(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[int] = None
    education: Optional[str] = "Unlisted"

class professor_response(BaseModel):
    id: PyObjectId = Field(alias="_id")
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[int] = None
    education: Optional[str] = "Unlisted"

    model_config = {
        "populate_by_name": True   # ← REQUIRED so FastAPI can output "id" instead of "_id"
    }
