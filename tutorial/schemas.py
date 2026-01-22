student_validator = {"$jsonSchema" : 
                  {"bsonType" : "object",
                   "required" :  ["first_name", "last_name", "email"],
                   "properties" : {
                       "first_name" : {"bsonType" : "string",
                                       "description" : "first name is required"
                                       },
                       "last_name" : {"bsonType" : "string",
                                      "description" : "last name is required"
                                      },
                        "email" : {"bsonType" : "string",
                                 "description" : "email is required and must be a string value"}
                   }}}

courses_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["student", "courses"],
        "properties": {
            "student": {"bsonType": "objectId"},
            "courses": {
                "bsonType": "array",
                "minItems": 3,
                "maxItems": 6,
                "items": {
                    "bsonType": "object",
                    "required": ["course_code", "course_name"],
                    "properties": {
                        "course_code": {"bsonType": "string"},
                        "course_name": {"bsonType": "string"}
                    }
                }
            }
        }
    }
}