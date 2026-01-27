from pydantic import BaseModel, EmailStr, BeforeValidator, Field, ConfigDict
from functools import partial
from typing import Optional, Annotated, Literal, List
from bson.objectid import ObjectId
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

PyObjectId = Annotated[str, BeforeValidator(str)] # pass in type, followed by specified constraint

class professor_create(BaseModel):
    first_name: Annotated[str, Field(pattern=r"^[a-zA-Z-]+$")]
    last_name: Annotated[str, Field(pattern=r"^[a-zA-Z-]+$")]
    email: EmailStr
    phone_number: Optional[int] = None
    department: Literal["ENGINEERING", "HEALTH", "LAW", "SCIENCE", "EDUCATION"]

class professor_response(BaseModel):
    id: PyObjectId = Field(alias="_id")
    first_name: Annotated[str, Field(pattern=r"^[a-zA-Z-]+$")]
    last_name: Annotated[str, Field(pattern=r"^[a-zA-Z-]+$")]
    email: EmailStr
    phone_number: Optional[int] = None
    department: Literal["ENGINEERING", "HEALTH", "LAW", "SCIENCE", "EDUCATION"]

    model_config = {
        "populate_by_name": True   # ← REQUIRED so FastAPI can output "id" instead of "_id"
    }

class course_add(BaseModel):
    course_code: Annotated[str, Field(pattern=r"^[A-Z0-9]+$")]
    course_name: str
    time_added: datetime = Field(default_factory=partial(datetime.now, timezone.utc))

class course_create(BaseModel):
    course_code: Annotated[str, Field(pattern=r"^[A-Z0-9]+$")]
    course_name: str
    class_size: int
    professor: professor_response # takes a professor object

class course_response(course_create):
    pass

class student(BaseModel):
    first_name: Annotated[str, Field(pattern=r"^[a-zA-Z]+$")]
    last_name: Annotated[str, Field(pattern=r"^[a-zA-Z-]+$")]
    email: EmailStr
    phone_number: Optional[int] = None
    courses: Optional[List[course_add]] = None
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc)) # partial returns an incomplete function with the specified arguments

class student_response(BaseModel):
    first_name: Annotated[str, Field(pattern=r"^[a-zA-Z-]+$")]
    last_name: Annotated[str, Field(pattern=r"^[a-zA-Z-]+$")]
    email: EmailStr
    phone_number: Optional[int] = None
    courses: Optional[List[course_add]] = None
    id: PyObjectId = Field(alias="_id") 

    model_config = {
        "populate_by_name": True   # ← REQUIRED so FastAPI can output "id" instead of "_id"
    }