from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class CreateMessage(BaseModel):
    sender_id: str
    room_id: str
    content: str


class UpdateMessage(BaseModel):
    content: str | None = None
