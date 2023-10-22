from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: str
    username: str
    phonenumber: str | None
    password: str
    avatar: str | None
    email: EmailStr | None
    verification_code  : str | None
    verified : bool

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


class userResponseSchema(BaseModel):
    email: EmailStr | None
    password: str

    class Config:
        from_attributes = True
