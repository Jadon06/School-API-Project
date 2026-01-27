from fastapi import APIRouter, HTTPException, status, Depends
from bson.objectid import ObjectId
from .. import documents, pydantic_schemas
from typing import List
from beanie.odm.operators.update.general import Set
from beanie.odm.operators.update.array import AddToSet
import beanie

router = APIRouter(
    prefix="/prof",
    tags=["professors"]
)

@router.post("/", response_model=pydantic_schemas.professor_response)
async def create_professor(professor: pydantic_schemas.professor_create):
    prof = await documents.professors.find_one(documents.professors.email == professor.email)
    if prof:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                    detail=f"Professor with email:{professor.email} already exists!")
    new_prof = documents.professors(**professor.dict())
    saved_prof = await new_prof.insert()
    return saved_prof

@router.get("/{id}", response_model=pydantic_schemas.professor_response)
async def get_professor(id: str):
    prof = await documents.professors.find_one(documents.professors.id == ObjectId(id))
    if not prof:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"professor with id:{id} does not exist!")
    return prof

def serialize_prof_id(prof):
    prof.id = str(prof.id)
    return prof

@router.get("/", response_model=List[pydantic_schemas.professor_response])
async def get_all_professors(skip: int = 0, limit: int = 10):
    professors = await documents.professors.find().skip(skip).limit(limit).to_list(length=limit)
    professors = [serialize_prof_id(prof) for prof in professors]
    return professors