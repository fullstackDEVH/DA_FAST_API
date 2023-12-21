from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class CreateMessage(BaseModel):
    sender_id: str
    room_id: str
    content: str


class CreateMessageSocket(BaseModel):
    sender_id: str
    room_id: str
    content: str
    receiver_id: str | None = None


class UpdateMessage(BaseModel):
    content: str | None = None
