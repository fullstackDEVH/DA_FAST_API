from pydantic import BaseModel


class UserBase:
    id: str | None
    username: str
    email: str
    avatar: str | None


class UserCreate:
    username: str
    email: str
    avatar: str | None
