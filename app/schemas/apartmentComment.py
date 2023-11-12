from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, Form, File
from typing import Annotated


class ApartmentSchema(BaseModel):
    id: str
    username: str
    phonenumber: str | None
    password: str
    email: EmailStr | None
    user_id: str

    class Config:
        from_attributes = True


class ApartmentUpdateSchema(BaseModel):
    name: str | None = None
    desc: str | None = None
    room: str | None = None
    price_per_day: str | None = None
    num_bedrooms: str | None = None
    num_living_rooms: str | None = None
    num_bathrooms: str | None = None
    num_toilets: str | None = None


class ApartmentCommentCreateSchema(BaseModel):
    user_id: str
    apartment_id: str
    text: str

class ApartmentCommentUpdateSchema(BaseModel):
    text: str