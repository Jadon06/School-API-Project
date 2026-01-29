import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

from beanie import init_beanie

from tutorial import documents, database
from tutorial.Routers import students, courses, professors

from fastapi import FastAPI
from fastapi.testclient import TestClient

from contextlib import asynccontextmanager
from mongomock_motor import AsyncMongoMockClient

import os

@pytest_asyncio.fixture(scope='function') # create a testing app
async def app_test():  # pylint: disable=redefined-outer-name
    app = FastAPI()

    client = AsyncMongoMockClient()
    await init_beanie(
        database=client["testing"], document_models=[documents.students, documents.courses, documents.professors]
    )
    app.include_router(students.router)
    app.include_router(courses.router)
    app.include_router(professors.router)

    yield app

    await client.drop_database("testing")
    client.close()

@pytest_asyncio.fixture
async def client(app_test):
    with TestClient(app_test) as c:
        yield c

"""
NOTE - All tests will be sync while using AsyncMongoMockClient, 
because all tests are store in memory, meaning they simulate a database and a 
client without one actually existing
"""

@pytest.fixture(scope="function")
def test_student_already_exists(client):
    new_student = client.post("/students/",json={
        "first_name" : "jadon",
        "last_name" : "Au-Yeung",
        "email" : "jadonay@my.yorku.ca",
        "phone_number" : 4168343698,
        "GPA" : 3.5})
    return new_student.json()

@pytest_asyncio.fixture
async def test_student_id(client, test_student_already_exists):
    student = await documents.students.find_one(documents.students.email == test_student_already_exists["email"])
    id = student.id
    return id

@pytest.fixture(scope="function")
def test_professor_already_exists(client):
    new_student = client.post("/prof/",json={
        "first_name" : "Jill",
        "last_name" : "Saunders",
        "email" : "JSaunders@my.yorku.ca",
        "phone_number" : 9221334545,
        "department" : "ENGINEERING"})
    return new_student.json()

@pytest_asyncio.fixture
async def test_professor_id(client, test_professor_already_exists):
    prof = await documents.professors.find_one(documents.professors.email == test_professor_already_exists['email'])
    id = prof.id
    return id