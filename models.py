from pydantic import BaseModel, Field
from typing import Optional


class Address(BaseModel):
    city: str
    country: str


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=3)  # Name must be at least 3 characters
    age: int = Field(..., gt=0)           # Age must be greater than 0
    address: Address


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)  # Optional field, can be updated
    age: Optional[int] = Field(None, gt=0)           # Optional field, must be greater than 0
    address: Optional[Address] = None  # Optional field, can be updated


class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    address: Address

    class Config:
        orm_mode = True  # To allow response model to be compatible with MongoDB data
