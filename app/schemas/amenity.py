from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, Form
from typing import Annotated


class AmenityCreate(BaseModel):
    name: str
    desc: str


class AmenityRead(BaseModel):
    name: str
    id: str
