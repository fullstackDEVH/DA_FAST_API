from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, Form, File
from typing import Annotated


class ApartmentSchema(BaseModel):
    id: str
    class Config:
        from_attributes = True


class ApartmentCommentUpdateSchema(BaseModel):
    text: str
    rate_location: int
    rate_amenities: int
    rate_interior: int
    rate_price: int


class ApartmentCommentCreateSchema(BaseModel):
    user_id: str
    apartment_id: str
    text: str
    rate_location: int
    rate_amenities: int
    rate_interior: int
    rate_price: int
