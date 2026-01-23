from fastapi import APIRouter, HTTPException, status, Depends
from bson.objectid import ObjectId
from .. import pydantic_schemas, models
from typing import List
from beanie.odm.operators.update.general import Set
from beanie.odm.operators.update.array import AddToSet


router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

@router.put("/{id}")
async def choose_courses(id: str, courses: List[pydantic_schemas.course_schema]):
    student = await models.students.find_one(models.students.id == ObjectId(id))
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"student with id:{id} does not exist")
    add_courses = await models.students.find_one(models.students.id == ObjectId(id)).update(Set({"courses" : courses}))
    return {"status" : "courses have been added!"}
