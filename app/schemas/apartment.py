from pydantic import BaseModel, EmailStr, Field
from fastapi import UploadFile, Form, File
from typing import Annotated
from enum import Enum


class ApartmentType(str, Enum):
    STUDIO = "STUDIO"
    HOUSE = "HOUSE"
    CONDO = "CONDO"


class ApartmentCity(str, Enum):
    HCM = "HCM"
    ĐN = "ĐN"
    NT = "NT"
    HA = "HA"
    HUE = "HUE"
    DL = "DL"


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
    city: str | None = None
    address: str | None = None
    apartment_type: str | None = None


class ApartmentCreateSchte(BaseModel):
    name: str
    desc: str
    city: str
    price_per_day: int
    num_bedrooms: int
    num_living_rooms: int
    num_bathrooms: int
    total_people: int
    tag_ids: list[str]
    amenities: list[str]
    address: str
    user_id: str
    apartment_type: ApartmentType
