from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize FastAPI app

app = FastAPI()

# MongoDB connection setup using environment variables
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not all([MONGO_URL, DB_NAME, COLLECTION_NAME]):
    raise Exception("Missing environment variables. Please check your .env file.")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Utility function to convert MongoDB ObjectId to string
def object_id_to_str(obj_id):
    return str(obj_id) if ObjectId.is_valid(obj_id) else obj_id

# Utility function to validate ObjectId
def validate_object_id(obj_id: str) -> ObjectId:
    try:
        return ObjectId(obj_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

# Pydantic models for validation

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str = Field(..., min_length=3)  # Name must be at least 3 characters
    age: int = Field(..., gt=0)           # Age must be greater than 0
    address: Address

    # Validate that name is non-empty
    @field_validator('name')
    def name_must_be_non_empty(cls, v):
        if not v:
            raise ValueError('Name cannot be empty')
        return v

    # Validate that age is positive
    @field_validator('age')
    def age_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Age must be a positive integer')
        return v

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)  # Optional name update, at least 3 characters
    age: Optional[int] = Field(None, gt=0)           # Optional age update, must be greater than 0
    address: Optional[Address] = None  # Optional address update

class StudentList(BaseModel):
    name: str
    age: int

class StudentListResponse(BaseModel):
    data: List[StudentList]
class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    address: Address

    class Config:
        orm_mode = True  # To allow response model to be compatible with MongoDB data

# Routes

@app.post("/students/", status_code=201)
async def create_student(student: Student):
    # Insert student into the database
    student_dict = student.dict()
    result = collection.insert_one(student_dict)
    return {"id":str(result.inserted_id)}

@app.get("/students/", response_model=StudentListResponse)
async def get_all_students(country: str = None, age: int = None):
    # Query for students with filters
    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}

    students = list(collection.find(query,{"name":1, "age": 1, "_id": 0}))
    result = [{"name": student["name"], "age": student["age"]} for student in students]
    return {"data":students}

@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    obj_id = validate_object_id(student_id)
    student = collection.find_one({"_id": obj_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student["id"] = object_id_to_str(student["_id"])
    del student["_id"]
    return student

@app.patch("/students/{student_id}", status_code=204)
async def update_student(student_id: str, updated_data: StudentUpdate):
    obj_id = validate_object_id(student_id)
    update_dict = updated_data.dict(exclude_unset=True)  # Only update provided fields
    result = collection.find_one_and_update(
        {"_id": obj_id},
        {"$set": update_dict}
    )
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return None

@app.delete("/students/{student_id}", status_code=200)
async def delete_student(student_id: str):
    obj_id = validate_object_id(student_id)
    result = collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}
