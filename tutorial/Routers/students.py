from fastapi import APIRouter, HTTPException, status, Depends
from bson.objectid import ObjectId
from .. import pydantic_schemas, models
from typing import List
from beanie.odm.operators.update.general import Set
from beanie.odm.operators.update.array import AddToSet

router = APIRouter(
    prefix="/students",
    tags=["students"]
)

def serialize_student_id(student):
    student.id = str(student.id)
    return student

@router.get("/", response_model=List[pydantic_schemas.student_response])
async def get_students(skip: int = 0, limit: int = 10):
    students = await models.students.find().skip(skip).limit(limit).to_list(length=limit)
    students = [serialize_student_id(student) for student in students]
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="collection does not exist")
    return students

@router.get("/{id}", response_model=pydantic_schemas.student_response)
async def get_one_student(id: str):
    id = ObjectId(id)
    student = await models.students.find_one({"_id" : id})
    print(pydantic_schemas.student_response(**student.dict()))
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"student with {id} does not exist")
    return student

@router.post("/", response_model=pydantic_schemas.student_response)
async def create_student(student: pydantic_schemas.student):
    print(student)
    new_student = models.students(**student.dict())
    student_exists = await models.students.find_one({"email" : new_student.email})
    if student_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"Student with {new_student.email} already exists!!")
    
    saved_student = await new_student.insert() # must insert a document into the collection to create it
    return saved_student

@router.put("/{id}", response_model=pydantic_schemas.student_response)
async def update_user(id: str, student_info: pydantic_schemas.student):
    student = models.students.find_one({"_id" : ObjectId(id)})
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student does not exist!")
    updates = {models.students.email : student_info.email,
               models.students.phone_number : student_info.phone_number,
                  models.students.first_name : student_info.first_name, 
                  models.students.last_name : student_info.last_name}
    
    await models.students.find_one(models.students.id == ObjectId(id)).update(Set(updates))
    return {"status" : "student info updated"}
    
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(id: str):
    student = await models.students.find_one({"_id" : ObjectId(id)})
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student does not exist!")
    await models.students.delete(student)

