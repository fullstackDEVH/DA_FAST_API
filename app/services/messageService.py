from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.message import CreateMessage, UpdateMessage

from ..database import Message
from enum import Enum
import uuid


class MessageService:
    def __init__(self, db: Session):
        self.db = db

    async def create_message(self, message_data: CreateMessage):
        tag_create = Message(id=str(uuid.uuid4()), **message_data.model_dump())
        self.db.add(tag_create)
        self.db.commit()
        self.db.refresh(tag_create)
        return tag_create

    async def get_message_by_id(self, message_id: str):
        return self.db.query(Message).filter(Message.id == message_id).first()

    async def update_message(self, message_id: str, message_data: UpdateMessage):
        db_message = await self.get_message_by_id(message_id)

        if not db_message:
            raise HTTPException(status_code=404, detail="message not found")

        for key, value in message_data.model_dump(exclude_unset=True).items():
            setattr(db_message, key, value)
        self.db.commit()
        self.db.refresh(db_message)

        return db_message

    async def delete_message(self, message_id: str):
        db_message = self.db.query(Message).filter(Message.id == message_id).first()
        if db_message:
            self.db.delete(db_message)
            self.db.commit()
        return db_message
