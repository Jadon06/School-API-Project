from dotenv import load_dotenv, find_dotenv
import os

from pymongo import AsyncMongoClient
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .pydantic_schemas import students, course_schema

load_dotenv(find_dotenv()) # loads the environment variable without having to define a path(shortcut)
password = os.environ.get("MONGODB_PWD") # Locates the environment variable names 'MONGO_DB_PWD' and stores it in password

connection_string = f"mongodb+srv://jadonay:{password}@tutorial.uaj6tuy.mongodb.net/?appName=tutorial"


# client = AsyncMongoClient(connection_string,server_api=pymongo.server_api.ServerApi(version="1", strict=True,deprecation_errors=True))
# production = client.get_database("production")

async def init_db():
    client = AsyncIOMotorClient(connection_string)
    await init_beanie(database=client.production, document_models=[students])
