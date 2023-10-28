from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, Form
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


class ApartmentCreateSchte(BaseModel):
    username: Annotated[str, Form()]
    password: Annotated[str, Form()]
    img: Annotated[UploadFile, Form()]
