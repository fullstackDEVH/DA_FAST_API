from pydantic import BaseModel, EmailStr
from ..helpers.constant import UserRole


class UserSchema(BaseModel):
    id: str
    username: str
    phonenumber: str | None
    password: str
    avatar: str | None
    email: EmailStr | None
    verification_code: str | None
    verified: bool

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchema(BaseModel):
    email: EmailStr
    phonenumber: str
    username: str
    password: str
    system_role: str = "RENTER"
    address: str | None = None


class UserUpdateSchema(BaseModel):
    address: str | None = None
    phonenumber: str | None = None
    username: str | None = None
    password: str | None = None
    system_role: str | None = "RENTER"


class userResponseSchema(BaseModel):
    email: EmailStr | None
    password: str

    class Config:
        from_attributes = True
