from tutorial import documents, database, pydantic_schemas
from fastapi import status, HTTPException
import pytest
from tutorial import pydantic_schemas

def test_create_professor(client):
    data = {
        "first_name" : "Pamela",
        "last_name" : "Landy",
        "email" : "pamLandy@my.yorku.ca",
        "phone_number" : 5550009101,
        "department" : "ENGINEERING"
    }
    res = client.post("/prof/", json=data)

    schema_check = pydantic_schemas.professor_response(**res.json())
    assert res.status_code == 200

def test_create_professor_already_exists(client, test_professor_already_exists):
    res = client.post("/prof/", json=test_professor_already_exists)
    assert res.status_code == 403

def test_get_professor(client, test_professor_already_exists, test_professor_id):
    res = client.get(f"/prof/{test_professor_id}")
    schema_check = pydantic_schemas.professor_response(**res.json())
    assert res.status_code == 200