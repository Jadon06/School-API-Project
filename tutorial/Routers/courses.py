from fastapi import APIRouter, HTTPException, status, Depends
from bson.objectid import ObjectId
from .. import documents, pydantic_schemas
from typing import List
from beanie.odm.operators.update.general import Set
from beanie.odm.operators.update.array import AddToSet


router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

@router.put("/{id}") 
async def add_courses(id: str, courses: List[pydantic_schemas.course_add]):
    student = await documents.students.find_one(documents.students.id == ObjectId(id))
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"student with id:{id} does not exist")
    add_courses = await documents.students.find_one(documents.students.id == ObjectId(id)).update(Set({"courses" : courses}))
    return {"status" : "courses have been added!"}

@router.put("/info/{course_code}", response_model=pydantic_schemas.course_response)
async def update_course_info(course_code: str, course: pydantic_schemas.course_create):
    course_found = await documents.courses.find_one(documents.courses.course_code == course_code)
    if not course_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with {course_code} exists!")
    updated_info = await documents.courses.find_one(documents.courses.course_code == course.course_code).update(Set(course.dict()))
    return course_found

@router.post("/")
async def create_course(course: pydantic_schemas.course_create):   
    course_exists = await documents.courses.find_one(documents.courses.course_code == course.course_code)
    if course_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"course with course Code:{course.course_code} already exists!")
    
    prof_exists = documents.professors.find(documents.professors.id == ObjectId(course.professor))
    if not prof_exists:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                            detail="professor does not exist!")
    new_course = documents.courses(**course.dict())
    await new_course.insert()
    return {"status": "course created successfully"}

@router.get("/{course_code}", response_model=pydantic_schemas.course_response)
async def get_a_course(course_code: str):
    course = await documents.courses.find_one(documents.courses.course_code == course_code)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course does not exist!")
    return course
    

