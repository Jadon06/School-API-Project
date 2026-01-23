from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, BeforeValidator, Field, ConfigDict
from typing import Optional, Annotated, List
from . import pydantic_schemas

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
    