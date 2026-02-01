import pprint
from .Routers import students, courses, professors
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import init_db
import os

os.environ["TESTING"] = "1"
if os.getenv("TESTING") == "0":
    print('done')
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await init_db()
        yield

    app = FastAPI(lifespan=lifespan)

app.include_router(students.router)
app.include_router(courses.router)
app.include_router(professors.router)
print("done")
""" part 1 """

# client = MongoClient(connection_string)

# dbs = client.list_database_names()
# test_db = client.test
# collections = test_db.list_collection_names()




""" creates a database called production and a collection called person_collection """
# production = client.production # by trying to access a database that doesn't exist, mongodb automatically makes one for us
# person_collection = production.person_collection


""" MongoDB querying """
# def insert_test_doc():
#     collection = test_db.test
#     test_document = {
#         "name" : "Jadon Au-Yeung",
#         "type" : "test"
#     }
#     inserted_id = collection.insert_one(test_document).inserted_id
#     print(inserted_id)

# def create_documents():
#     first_names = ["james", "jacob", "bill", "derek"]
#     last_names = ["dally", "chang", "brewell", "chan"]
#     ages = [10,20,30,40]
    
#     docs = []
#     for first_name, last_name, age in zip(first_names, last_names, ages):
#         doc = {"first name":first_name, "last name": last_name, "age": age}
#         docs.append(doc)
#     person_collection.insert_many(docs)


# printer = pprint.PrettyPrinter()
# def find_all_people():
#     people = person_collection.find() # returns a cursor object which cannot be directly accessed but can be accessed by converting into list or iterating over it
#     for person in people:
#         printer.pprint(person) # prints the person in a better format

# def find_someone():
#     target = person_collection.find_one({"first name" : "james"})
#     printer.pprint(target)

# def count_all_people():
#     count = person_collection.count_documents(filter={}) # pass a dicitonary into filter to find specific elements
#     return count

# def get_person_via_id(person_id):
#     _id = ObjectId(person_id) # must convert string of ids to 'ObjectId' otherwise MongoDB won't recognize the entry
#     person = person_collection.find_one({"_id": _id})
#     return person

# def get_age_range(min_age, max_age):
#     query = {"$and": [                   # use $and when you want to choose different things to filter through
#             {"age" : {"$gte" : min_age}},# gte = greater than or equal to
#             {"age" : {"$lte" : max_age}} # lte = less than or equal to
#             ]}
#     people = person_collection.find(query).sort("age")
#     for person in people:
#         printer.pprint(person)

# def project_columns():
#     columns = {"_id": 0, "first name": 1, "last name": 1} # by passing 0 as the value, it shows MongoDB we don't want the key or in this case '_id' to show in our documents
#     people = person_collection.find({}, columns) # will find only the columns specified
#     for person in people:
#         printer.pprint(person)


# """ updating and replace documents """

# def update_person_by_id(person_id):
#     _id = ObjectId(person_id)

#     # all_updates = {
#     #     "$set" : {"new_field" : True}, # sets a new field for a value of our choice if field already exists, using '$set' would override the field with our new parameters
#     #     "$inc" : {"age": 1}, # increments selected column by chosen amount
#     #     "$rename" : {"first name" : "first", "last name" : "last"} # renames all selected fields
#     #     }

#     # person_collection.update_one({"_id" : _id}, all_updates)

#     person_collection.update_one({"_id" : _id}, {"$unset" : {"new_field" : ""}}) # deletes the chosen field

# def replace_one(person_id):
#     _id = ObjectId(person_id)

#     new_doc = {"first name" : "new first name",
#                "last name" : "new last name",
#                "age" : 100}

#     person_collection.replace_one({"_id" : _id}, new_doc)


# """ deleting documents """

# def delete_doc_by_id(person_id):
#     _id = ObjectId(person_id)
#     person_collection.delete_one({"_id": _id})

# """ Relationships """

# def add_address_embed(person_id):
#     _id = ObjectId(person_id)
#     address = {"street" : "100 Silverstar Blvd",
#                "city" : "Scarborough", 
#                "Province" : "Ontario"}
#     person_collection.update_one({"_id" : _id},{"$addToSet" : {'address/addresses' : address}}) # adds this address to the key addresses

# def add_address_relationship(person_id, address): # creates a new collection where the owner_id is associated with the persons id in the persons collection
#     _id = ObjectId(person_id)
#     address_collection = production.address
#     address = address.copy()
#     address['ownder_id'] = _id
#     address_collection.insert_one(address)

# add_address_relationship('696fbc0ad8306498a77fff5c', {"street" : "100 Silverstar Blvd",
#                "city" : "Scarborough", 
#                "Province" : "Ontario"})

""" part 2 """
# def create_student_collection():
#     try:
#         production.create_collection("student")
#     except Exception as e:
#         print(e)
#     production.command("collMod", "student", validator=schemas.student_validator)

# def create_courses_collection():
#     try:
#         production.create_collection("courses")
#     except Exception as e:
#         print(e)
#     production.command("collMod", "courses", validator=schemas.courses_validator)

# def create_data():
#     students = [
#         {"first_name" : "Tim",
#         "last_name" : "Tam",
#         "GPA" : 4.00},
#         {"first_name" : "Jon",
#         "last_name" : "Dingle",
#         "GPA" : 3.05},
#         {"first_name" : "Jamie",
#         "last_name" : "Oliver",
#         "GPA" : 3.81},
#         {"first_name" : "Mike",
#         "last_name" : "Owens",
#         "GPA" : 2.5}
#     ]
#     students_collection = production.student
#     student_ids = students_collection.insert_many(students).inserted_ids

#     course_selection = {
#         "student" : student_ids[0],
#         "courses" : [{"course_code" : "EECS1516",
#           "course_name" : "OOP"},
#           {"course_code" : "EECS2502",
#           "course_name" : "Data Structs & Algorithms"},
#           {"course_code" : "MATH1025",
#           "course_name" : "Linear Algebra"},
#           {"course_code" : "MATH2015N",
#           "course_name" : "Applied multivariate & vector calculus"},
#           {"course_code" : "MATH1131N",
#           "course_name" : "Statistics I"},
#           ]
#     }

#     courses_collection = production.courses
#     courses_collection.insert_one(course_selection)

# create_courses_collection()
# create_data()