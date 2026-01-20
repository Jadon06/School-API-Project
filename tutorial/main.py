from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv(find_dotenv()) # loads the environment variable without having to define a path(shortcut)
password = os.environ.get("MONGODB_PWD") # Locates the environment variable names 'MONGO_DB_PWD' and stores it in password

connection_string = f"mongodb+srv://jadonay:{password}@tutorial.uaj6tuy.mongodb.net/?appName=tutorial"

client = MongoClient(connection_string)

dbs = client.list_database_names()
test_db = client.test
collections = test_db.list_collection_names()
# print(collections)


""" MongoDB querying """
def insert_test_doc():
    collection = test_db.test
    test_document = {
        "name" : "Jadon Au-Yeung",
        "type" : "test"
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(inserted_id)

""" creates a database called production and a collection called person_collection """
production = client.production # by trying to access a database that doesn't exist, mongodb automatically makes one for us
person_collection = production.person_collection

def create_documents():
    first_names = ["james", "jacob", "bill", "derek"]
    last_names = ["dally", "chang", "brewell", "chan"]
    ages = [10,20,30,40]
    
    docs = []
    for first_name, last_name, age in zip(first_names, last_names, ages):
        doc = {"first name":first_name, "last name": last_name, "age": age}
        docs.append(doc)
    person_collection.insert_many(docs)


printer = pprint.PrettyPrinter()
def find_all_people():
    people = person_collection.find() # returns a cursor object which cannot be directly accessed but can be accessed by converting into list or iterating over it
    for person in people:
        printer.pprint(person) # prints the person in a better format

def find_someone():
    target = person_collection.find_one({"first name" : "james"})
    printer.pprint(target)

def count_all_people():
    count = person_collection.count_documents(filter={}) # pass a dicitonary into filter to find specific elements
    return count

def get_person_via_id(person_id):
    _id = ObjectId(person_id) # must convert string of ids to 'ObjectId' otherwise MongoDB won't recognize the entry
    person = person_collection.find_one({"_id": _id})
    return person

def get_age_range(min_age, max_age):
    query = {"$and": [                   # use $and when you want to choose different things to filter through
            {"age" : {"$gte" : min_age}},# gte = greater than or equal to
            {"age" : {"$lte" : max_age}} # lte = less than or equal to
            ]}
    people = person_collection.find(query).sort("age")
    for person in people:
        printer.pprint(person)

def project_columns():
    columns = {"_id": 0, "first name": 1, "last name": 1} # by passing 0 as the value, it shows MongoDB we don't want the key or in this case '_id' to show in our documents
    people = person_collection.find({}, columns) # will find only the columns specified
    for person in people:
        printer.pprint(person)


""" updating and replace documents """

def update_person_by_id(person_id):
    _id = ObjectId(person_id)

    # all_updates = {
    #     "$set" : {"new_field" : True}, # sets a new field for a value of our choice if field already exists, using '$set' would override the field with our new parameters
    #     "$inc" : {"age": 1}, # increments selected column by chosen amount
    #     "$rename" : {"first name" : "first", "last name" : "last"} # renames all selected fields
    #     }

    # person_collection.update_one({"_id" : _id}, all_updates)

    person_collection.update_one({"_id" : _id}, {"$unset" : {"new_field" : ""}}) # deletes the chosen field

def replace_one(person_id):
    _id = ObjectId(person_id)

    new_doc = {"first name" : "new first name",
               "last name" : "new last name",
               "age" : 100}

    person_collection.replace_one({"_id" : _id}, new_doc)


""" deleting documents """