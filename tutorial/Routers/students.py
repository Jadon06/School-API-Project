from fastapi import APIRouter, HTTPException, status, Depends
from bson.objectid import ObjectId
from .. import pydantic_schemas 
from typing import List


router = APIRouter(
    prefix="/students",
    tags=["students"]
)

def serialize_student_id(student):
    student.id = str(student.id)
    return student

@router.get("/", response_model=List[pydantic_schemas.student_response])
async def get_students(skip: int = 0, limit: int = 10):
    students = await pydantic_schemas.students.find().skip(skip).limit(limit).to_list(length=limit)
    students = [serialize_student_id(student) for student in students]
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="collection does not exist")
    return students

@router.get("/{id}", response_model=pydantic_schemas.student_response)
async def get_one_student(id: str):
    id = ObjectId(id)
    student = await pydantic_schemas.students.find_one({"_id" : id})
    print(pydantic_schemas.student_response(**student.dict()))
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"student with {id} does not exist")
    return student

@router.post("/", response_model=pydantic_schemas.student_response)
async def create_student(student: pydantic_schemas.student):
    new_student = pydantic_schemas.students(**student.dict())
    student_exists = await pydantic_schemas.students.find_one({"email" : new_student.email})
    if student_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"Student with {new_student.email} already exists!!")
    saved_student = await new_student.insert() # must insert a document into the collection to create it
    return saved_student

@router.put("/{id}")
async def update_user(id: str):
    student = pydantic_schemas.students.find_one({"_id" : ObjectId(id)})
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student does not exist!")
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(id: str):
    student = await pydantic_schemas.students.find_one({"_id" : ObjectId(id)})
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student does not exist!")
    await pydantic_schemas.students.delete(student)
