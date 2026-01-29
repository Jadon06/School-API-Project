from tutorial import documents, database, pydantic_schemas
from fastapi import status, HTTPException
import pytest
from tutorial import pydantic_schemas

"""
NOTE - All tests will be sync while using AsyncMongoMockClient, 
because all tests are store in memory, meaning they simulate a database and a 
client without one actually existing
"""
def test_create_student_already_exists(client, test_student_already_exists):
    response = client.post("/students/",json={
        "first_name" : "jadon",
        "last_name" : "Au-Yeung",
        "email" : "jadonay@my.yorku.ca",
        "phone_number" : 4168343698,
        "GPA" : 3.5})
    assert response.status_code == 409
    assert response.json().get("detail") == "Student with jadonay@my.yorku.ca already exists!!"

def test_create_student(client):
    res = client.post("/students/", json={
        "first_name" : "Jimmy",
        "last_name" : "Chang",
        "email" : "JimChang@my.yorku.ca",
        "phone_number" : 1234567890,
        "GPA" : 3.5
    })
    assert res.status_code == 201
    assert documents.students.find_one(documents.students.email == "JimChang@my.yorku.ca")

def test_get_student(client, test_student_id):
    res = client.get(f"/students/{test_student_id}")

    schema_check = pydantic_schemas.student_response(**res.json())
    assert res.status_code == 200

def test_delete_student(client, test_student_already_exists, test_student_id):
    res = client.delete(f"/students/{test_student_id}")
    assert res.status_code == 204

def test_update_student(client, test_student_already_exists, test_student_id):
    res = client.put(f"/students/{test_student_id}", json={
        "first_name" : "jadon",
        "last_name" : "Au-Yeung",
        "email" : "jadonay@my.yorku.ca",
        "phone_number" : 1234567890,
        "GPA" : 3.5}
    )
    # schema_check = pydantic_schemas.student_response(**res.json())
    # assert res.json().get("phone_number") == 1234567890
    assert res.status_code == 200