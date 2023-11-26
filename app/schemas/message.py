from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class CreateMessage(BaseModel):
    id: str
    sender_id: str
    room_id: str
    content: str


class UpdateMessage(BaseModel):
    id: str | None = None
    sender_id: str | None = None
    room_id: str | None = None
    content: str | None = None
