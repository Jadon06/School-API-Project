from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, BeforeValidator, Field, ConfigDict
from typing import Optional, Annotated, List, Literal, Dict
from functools import partial
from datetime import datetime, timezone
from . import pydantic_schemas

PyObjectId = Annotated[str, BeforeValidator(str)]

class students(Document):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[int] = None
    GPA: Optional[float] = 0.0
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    class Settings:
        name="students"

class professors(Document):
    first_name: str 
    last_name: str
    email: EmailStr
    phone_number: Optional[int] = None
    department: Literal["ENGINEERING", "HEALTH", "LAW", "SCIENCE", "EDUCATION"]
    
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    class Settings:
        name="professors"

class courses(Document):
    course_name: str
    course_code: str
    class_size: int
    professor: Dict