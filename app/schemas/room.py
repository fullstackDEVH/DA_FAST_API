from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class CreateRoom(BaseModel):
    name: str
    key: str
    users_id: list[str]


class UpdateRoom(BaseModel):
    name: str | None = None
    key: datetime | None = None
