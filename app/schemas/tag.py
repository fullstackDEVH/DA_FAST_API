from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, Form
from typing import Annotated


class TagCreate(BaseModel):
    name: str
    desc: str


class TagRead(BaseModel):
    name: str
    id: str
